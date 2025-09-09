import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as stepfunctionsTasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ssm from 'aws-cdk-lib/aws-ssm';
import { Construct } from 'constructs';
import { LambdaConstruct } from './lambda-construct';
import { DatabaseConstruct } from './database-construct';
import { ApiConstruct } from './api-construct';
import { StepFunctionsConstruct } from './step-functions-construct';

export interface CloudNativeAppStackProps extends cdk.StackProps {
  stage: string;
  serviceName: string;
}

export class CloudNativeAppStack extends cdk.Stack {
  public readonly api: apigateway.RestApi;
  public readonly studentsTable: dynamodb.Table;
  public readonly processingQueue: sqs.Queue;
  public readonly completionQueue: sqs.Queue;
  public readonly stateMachine: stepfunctions.StateMachine;
  public readonly dataBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props: CloudNativeAppStackProps) {
    super(scope, id, props);

    const { stage, serviceName } = props;

    // Database layer
    const database = new DatabaseConstruct(this, 'Database', {
      stage,
      serviceName,
    });
    this.studentsTable = database.studentsTable;

    // S3 bucket for data storage
    this.dataBucket = new s3.Bucket(this, 'DataBucket', {
      bucketName: `${serviceName}-data-${stage}-${this.account}`,
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      lifecycleRules: [
        {
          id: 'DeleteIncompleteMultipartUploads',
          abortIncompleteMultipartUploadAfter: cdk.Duration.days(1),
        },
        {
          id: 'TransitionToIA',
          transitions: [
            {
              storageClass: s3.StorageClass.INFREQUENT_ACCESS,
              transitionAfter: cdk.Duration.days(30),
            },
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: cdk.Duration.days(90),
            },
          ],
        },
      ],
      removalPolicy: stage === 'prod' ? cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY,
    });

    // SQS queues for async processing
    this.processingQueue = new sqs.Queue(this, 'ProcessingQueue', {
      queueName: `${serviceName}-processing-${stage}`,
      visibilityTimeout: cdk.Duration.minutes(15),
      retentionPeriod: cdk.Duration.days(14),
      deadLetterQueue: {
        queue: new sqs.Queue(this, 'ProcessingDLQ', {
          queueName: `${serviceName}-processing-dlq-${stage}`,
          retentionPeriod: cdk.Duration.days(14),
        }),
        maxReceiveCount: 3,
      },
    });

    this.completionQueue = new sqs.Queue(this, 'CompletionQueue', {
      queueName: `${serviceName}-completion-${stage}`,
      visibilityTimeout: cdk.Duration.minutes(5),
      retentionPeriod: cdk.Duration.days(7),
    });

    // Lambda functions
    const lambdaConstruct = new LambdaConstruct(this, 'Lambda', {
      stage,
      serviceName,
      studentsTable: this.studentsTable,
      dataBucket: this.dataBucket,
      processingQueue: this.processingQueue,
      completionQueue: this.completionQueue,
    });

    // Step Functions workflow
    const stepFunctions = new StepFunctionsConstruct(this, 'StepFunctions', {
      stage,
      serviceName,
      studentsTable: this.studentsTable,
      processingQueue: this.processingQueue,
      completionQueue: this.completionQueue,
      createStudentFunction: lambdaConstruct.createStudentFunction,
      processStudentsFunction: lambdaConstruct.processStudentsFunction,
      resultsHandlerFunction: lambdaConstruct.resultsHandlerFunction,
    });
    this.stateMachine = stepFunctions.stateMachine;

    // API Gateway
    const api = new ApiConstruct(this, 'Api', {
      stage,
      serviceName,
      studentsTable: this.studentsTable,
      stateMachine: this.stateMachine,
      createStudentFunction: lambdaConstruct.createStudentFunction,
      getStudentFunction: lambdaConstruct.getStudentFunction,
      listStudentsFunction: lambdaConstruct.listStudentsFunction,
      updateStudentFunction: lambdaConstruct.updateStudentFunction,
      deleteStudentFunction: lambdaConstruct.deleteStudentFunction,
      processStudentsFunction: lambdaConstruct.processStudentsFunction,
      statusFunction: lambdaConstruct.statusFunction,
    });
    this.api = api.api;

    // Store important values in SSM for external access
    new ssm.StringParameter(this, 'ApiUrlParameter', {
      parameterName: `/${serviceName}/${stage}/api-url`,
      stringValue: this.api.url,
      description: 'API Gateway URL',
    });

    new ssm.StringParameter(this, 'StateMachineArnParameter', {
      parameterName: `/${serviceName}/${stage}/state-machine-arn`,
      stringValue: this.stateMachine.stateMachineArn,
      description: 'Step Functions State Machine ARN',
    });

    new ssm.StringParameter(this, 'StudentsTableNameParameter', {
      parameterName: `/${serviceName}/${stage}/students-table-name`,
      stringValue: this.studentsTable.tableName,
      description: 'DynamoDB Students Table Name',
    });

    // CloudWatch Log Groups with retention
    new logs.LogGroup(this, 'ApiLogGroup', {
      logGroupName: `/aws/apigateway/${serviceName}-${stage}`,
      retention: logs.RetentionDays.ONE_MONTH,
    });

    new logs.LogGroup(this, 'StateMachineLogGroup', {
      logGroupName: `/aws/stepfunctions/${serviceName}-${stage}`,
      retention: logs.RetentionDays.ONE_MONTH,
    });

    // Outputs
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: this.api.url,
      description: 'API Gateway URL',
      exportName: `${serviceName}-${stage}-api-url`,
    });

    new cdk.CfnOutput(this, 'StateMachineArn', {
      value: this.stateMachine.stateMachineArn,
      description: 'Step Functions State Machine ARN',
      exportName: `${serviceName}-${stage}-state-machine-arn`,
    });

    new cdk.CfnOutput(this, 'StudentsTableName', {
      value: this.studentsTable.tableName,
      description: 'DynamoDB Students Table Name',
      exportName: `${serviceName}-${stage}-students-table-name`,
    });

    new cdk.CfnOutput(this, 'DataBucketName', {
      value: this.dataBucket.bucketName,
      description: 'S3 Data Bucket Name',
      exportName: `${serviceName}-${stage}-data-bucket-name`,
    });
  }
}
