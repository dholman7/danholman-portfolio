import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import * as path from 'path';

export interface LambdaConstructProps {
  stage: string;
  serviceName: string;
  studentsTable: dynamodb.Table;
  dataBucket: s3.Bucket;
  processingQueue: sqs.Queue;
  completionQueue: sqs.Queue;
}

export class LambdaConstruct extends Construct {
  public readonly createStudentFunction: NodejsFunction;
  public readonly getStudentFunction: NodejsFunction;
  public readonly listStudentsFunction: NodejsFunction;
  public readonly updateStudentFunction: NodejsFunction;
  public readonly deleteStudentFunction: NodejsFunction;
  public readonly processStudentsFunction: NodejsFunction;
  public readonly resultsHandlerFunction: NodejsFunction;
  public readonly statusFunction: NodejsFunction;

  constructor(scope: Construct, id: string, props: LambdaConstructProps) {
    super(scope, id);

    const { stage, serviceName, studentsTable, dataBucket, processingQueue, completionQueue } = props;

    // Common Lambda configuration
    const commonLambdaConfig: Partial<lambda.FunctionProps> = {
      runtime: lambda.Runtime.NODEJS_20_X,
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      logRetention: logs.RetentionDays.ONE_MONTH,
      environment: {
        STAGE: stage,
        SERVICE_NAME: serviceName,
        STUDENTS_TABLE_NAME: studentsTable.tableName,
        DATA_BUCKET_NAME: dataBucket.bucketName,
        PROCESSING_QUEUE_URL: processingQueue.queueUrl,
        COMPLETION_QUEUE_URL: completionQueue.queueUrl,
        NODE_ENV: stage === 'prod' ? 'production' : 'development',
      },
    };

    // Create Student Function
    this.createStudentFunction = new NodejsFunction(this, 'CreateStudentFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-create-student-${stage}`,
      entry: path.join(__dirname, '../lambda/create-student.ts'),
      handler: 'handler',
      description: 'Creates a new student record',
      timeout: cdk.Duration.seconds(15),
    });

    // Get Student Function
    this.getStudentFunction = new NodejsFunction(this, 'GetStudentFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-get-student-${stage}`,
      entry: path.join(__dirname, '../lambda/get-student.ts'),
      handler: 'handler',
      description: 'Retrieves a student record by ID',
      timeout: cdk.Duration.seconds(10),
    });

    // List Students Function
    this.listStudentsFunction = new NodejsFunction(this, 'ListStudentsFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-list-students-${stage}`,
      entry: path.join(__dirname, '../lambda/list-students.ts'),
      handler: 'handler',
      description: 'Lists students with pagination and filtering',
      timeout: cdk.Duration.seconds(20),
      memorySize: 512,
    });

    // Update Student Function
    this.updateStudentFunction = new NodejsFunction(this, 'UpdateStudentFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-update-student-${stage}`,
      entry: path.join(__dirname, '../lambda/update-student.ts'),
      handler: 'handler',
      description: 'Updates an existing student record',
      timeout: cdk.Duration.seconds(15),
    });

    // Delete Student Function
    this.deleteStudentFunction = new NodejsFunction(this, 'DeleteStudentFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-delete-student-${stage}`,
      entry: path.join(__dirname, '../lambda/delete-student.ts'),
      handler: 'handler',
      description: 'Deletes a student record',
      timeout: cdk.Duration.seconds(10),
    });

    // Process Students Function (for batch processing)
    this.processStudentsFunction = new NodejsFunction(this, 'ProcessStudentsFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-process-students-${stage}`,
      entry: path.join(__dirname, '../lambda/process-students.ts'),
      handler: 'handler',
      description: 'Processes multiple students in parallel',
      timeout: cdk.Duration.minutes(15),
      memorySize: 1024,
    });

    // Results Handler Function
    this.resultsHandlerFunction = new NodejsFunction(this, 'ResultsHandlerFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-results-handler-${stage}`,
      entry: path.join(__dirname, '../lambda/results-handler.ts'),
      handler: 'handler',
      description: 'Handles processing results and notifications',
      timeout: cdk.Duration.minutes(5),
      memorySize: 512,
    });

    // Status Function
    this.statusFunction = new NodejsFunction(this, 'StatusFunction', {
      ...commonLambdaConfig,
      functionName: `${serviceName}-status-${stage}`,
      entry: path.join(__dirname, '../lambda/status.ts'),
      handler: 'handler',
      description: 'Provides system status and health checks',
      timeout: cdk.Duration.seconds(10),
    });

    // Grant permissions to DynamoDB
    studentsTable.grantReadWriteData(this.createStudentFunction);
    studentsTable.grantReadWriteData(this.getStudentFunction);
    studentsTable.grantReadWriteData(this.listStudentsFunction);
    studentsTable.grantReadWriteData(this.updateStudentFunction);
    studentsTable.grantReadWriteData(this.deleteStudentFunction);
    studentsTable.grantReadWriteData(this.processStudentsFunction);
    studentsTable.grantReadWriteData(this.resultsHandlerFunction);
    studentsTable.grantReadData(this.statusFunction);

    // Grant permissions to S3
    dataBucket.grantReadWrite(this.createStudentFunction);
    dataBucket.grantReadWrite(this.processStudentsFunction);
    dataBucket.grantReadWrite(this.resultsHandlerFunction);
    dataBucket.grantRead(this.getStudentFunction);
    dataBucket.grantRead(this.listStudentsFunction);
    dataBucket.grantRead(this.statusFunction);

    // Grant permissions to SQS
    processingQueue.grantSendMessages(this.createStudentFunction);
    processingQueue.grantSendMessages(this.processStudentsFunction);
    processingQueue.grantConsumeMessages(this.processStudentsFunction);
    completionQueue.grantSendMessages(this.processStudentsFunction);
    completionQueue.grantSendMessages(this.resultsHandlerFunction);
    completionQueue.grantConsumeMessages(this.resultsHandlerFunction);

    // Add custom IAM policies for Step Functions
    const stepFunctionsPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'states:StartExecution',
        'states:DescribeExecution',
        'states:StopExecution',
      ],
      resources: ['*'],
    });

    this.processStudentsFunction.addToRolePolicy(stepFunctionsPolicy);
    this.resultsHandlerFunction.addToRolePolicy(stepFunctionsPolicy);

    // Add CloudWatch Logs permissions
    const logsPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: [
        'logs:CreateLogGroup',
        'logs:CreateLogStream',
        'logs:PutLogEvents',
        'logs:DescribeLogGroups',
        'logs:DescribeLogStreams',
      ],
      resources: ['*'],
    });

    [
      this.createStudentFunction,
      this.getStudentFunction,
      this.listStudentsFunction,
      this.updateStudentFunction,
      this.deleteStudentFunction,
      this.processStudentsFunction,
      this.resultsHandlerFunction,
      this.statusFunction,
    ].forEach(func => {
      func.addToRolePolicy(logsPolicy);
    });
  }
}
