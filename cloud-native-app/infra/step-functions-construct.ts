import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as stepfunctionsTasks from 'aws-cdk-lib/aws-stepfunctions-tasks';
import * as logs from 'aws-cdk-lib/aws-logs';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import { Construct } from 'constructs';

export interface StepFunctionsConstructProps {
  stage: string;
  serviceName: string;
  studentsTable: dynamodb.Table;
  processingQueue: sqs.Queue;
  completionQueue: sqs.Queue;
  createStudentFunction: NodejsFunction;
  processStudentsFunction: NodejsFunction;
  resultsHandlerFunction: NodejsFunction;
}

export class StepFunctionsConstruct extends Construct {
  public readonly stateMachine: stepfunctions.StateMachine;

  constructor(scope: Construct, id: string, props: StepFunctionsConstructProps) {
    super(scope, id);

    const {
      stage,
      serviceName,
      studentsTable,
      processingQueue,
      completionQueue,
      createStudentFunction,
      processStudentsFunction,
      resultsHandlerFunction,
    } = props;

    // CloudWatch Log Group for Step Functions
    const logGroup = new logs.LogGroup(this, 'StepFunctionsLogGroup', {
      logGroupName: `/aws/stepfunctions/${serviceName}-${stage}`,
      retention: logs.RetentionDays.ONE_MONTH,
    });

    // Create student task
    const createStudentTask = new stepfunctionsTasks.LambdaInvoke(this, 'CreateStudentTask', {
      lambdaFunction: createStudentFunction,
      payloadResponseOnly: true,
      retryOnServiceExceptions: true,
    });

    // Process students task
    const processStudentsTask = new stepfunctionsTasks.LambdaInvoke(this, 'ProcessStudentsTask', {
      lambdaFunction: processStudentsFunction,
      payloadResponseOnly: true,
      retryOnServiceExceptions: true,
    });

    // Send to SQS task
    const sendToQueueTask = new stepfunctionsTasks.SqsSendMessage(this, 'SendToQueueTask', {
      queue: processingQueue,
      messageBody: stepfunctions.TaskInput.fromObject({
        'executionId.$': '$$.Execution.Name',
        'timestamp.$': '$$.State.EnteredTime',
        'input.$': '$',
      }),
    });

    // Wait task for processing
    const waitTask = new stepfunctions.Wait(this, 'WaitForProcessing', {
      time: stepfunctions.WaitTime.duration(cdk.Duration.seconds(30)),
    });

    // Results handler task
    const resultsHandlerTask = new stepfunctionsTasks.LambdaInvoke(this, 'ResultsHandlerTask', {
      lambdaFunction: resultsHandlerFunction,
      payloadResponseOnly: true,
      retryOnServiceExceptions: true,
    });

    // Send completion notification task
    const sendCompletionTask = new stepfunctionsTasks.SqsSendMessage(this, 'SendCompletionTask', {
      queue: completionQueue,
      messageBody: stepfunctions.TaskInput.fromObject({
        'executionId.$': '$$.Execution.Name',
        'status': 'COMPLETED',
        'timestamp.$': '$$.State.EnteredTime',
        'results.$': '$',
      }),
    });

    // Error handling
    const errorHandler = new stepfunctions.Pass(this, 'ErrorHandler', {
      result: stepfunctions.Result.fromObject({
        error: 'Processing failed',
        status: 'FAILED',
      }),
    });

    // Success handler
    const successHandler = new stepfunctions.Pass(this, 'SuccessHandler', {
      result: stepfunctions.Result.fromObject({
        status: 'SUCCESS',
        message: 'All students processed successfully',
      }),
    });

    // Choice state for error handling
    const checkForErrors = new stepfunctions.Choice(this, 'CheckForErrors')
      .when(
        stepfunctions.Condition.booleanEquals('$.hasErrors', true),
        errorHandler
      )
      .otherwise(successHandler);

    // Parallel processing state
    const parallelProcessing = new stepfunctions.Parallel(this, 'ParallelProcessing', {
      comment: 'Process students in parallel with error handling',
    });

    // Add branches to parallel processing
    parallelProcessing.branch(createStudentTask);
    parallelProcessing.branch(processStudentsTask);
    parallelProcessing.branch(sendToQueueTask);

    // Add error handling to parallel processing
    parallelProcessing.addCatch(errorHandler, {
      errors: ['States.ALL'],
      resultPath: '$.error',
    });

    // Map state for processing multiple students
    const mapStudents = new stepfunctions.Map(this, 'MapStudents', {
      itemsPath: '$.students',
      maxConcurrency: 10,
      comment: 'Process each student individually',
    });

    // Add iterator to map state
    mapStudents.iterator(
      new stepfunctions.Choice(this, 'StudentTypeChoice')
        .when(
          stepfunctions.Condition.stringEquals('$.type', 'single'),
          createStudentTask
        )
        .when(
          stepfunctions.Condition.stringEquals('$.type', 'batch'),
          processStudentsTask
        )
        .otherwise(createStudentTask)
    );

    // Add error handling to map state
    mapStudents.addCatch(errorHandler, {
      errors: ['States.ALL'],
      resultPath: '$.error',
    });

    // Main workflow definition
    const definition = stepfunctions.Chain.start(parallelProcessing)
      .next(waitTask)
      .next(resultsHandlerTask)
      .next(sendCompletionTask)
      .next(checkForErrors);

    // State Machine
    this.stateMachine = new stepfunctions.StateMachine(this, 'StateMachine', {
      stateMachineName: `${serviceName}-workflow-${stage}`,
      definition,
      logs: {
        destination: logGroup,
        level: stepfunctions.LogLevel.ALL,
        includeExecutionData: true,
      },
      tracingEnabled: true,
      timeout: cdk.Duration.hours(1),
    });

    // Grant permissions
    studentsTable.grantReadWriteData(this.stateMachine.role);
    processingQueue.grantSendMessages(this.stateMachine.role);
    completionQueue.grantSendMessages(this.stateMachine.role);

    // Add custom policy for Step Functions
    this.stateMachine.addToRolePolicy(
      new cdk.aws_iam.PolicyStatement({
        effect: cdk.aws_iam.Effect.ALLOW,
        actions: [
          'lambda:InvokeFunction',
          'sqs:SendMessage',
          'dynamodb:GetItem',
          'dynamodb:PutItem',
          'dynamodb:UpdateItem',
          'dynamodb:DeleteItem',
          'dynamodb:Query',
          'dynamodb:Scan',
        ],
        resources: [
          studentsTable.tableArn,
          `${studentsTable.tableArn}/index/*`,
          processingQueue.queueArn,
          completionQueue.queueArn,
          createStudentFunction.functionArn,
          processStudentsFunction.functionArn,
          resultsHandlerFunction.functionArn,
        ],
      })
    );

    // Add tags
    cdk.Tags.of(this.stateMachine).add('Environment', stage);
    cdk.Tags.of(this.stateMachine).add('Service', serviceName);
    cdk.Tags.of(this.stateMachine).add('Purpose', 'Student Processing Workflow');
  }
}
