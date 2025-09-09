import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBService } from './utils/dynamodb';
import { Validator, ValidationError } from './utils/validation';
import { ResponseBuilder } from './utils/response';
import { BatchProcessRequest, BatchProcessResponse, StudentStatus } from './types';
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';
import { SFNClient, StartExecutionCommand } from '@aws-sdk/client-sfn';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Process students request:', JSON.stringify(event, null, 2));

  try {
    // Parse and validate request body
    if (!event.body) {
      return ResponseBuilder.validationError(['Request body is required']);
    }

    let requestData;
    try {
      requestData = JSON.parse(event.body);
    } catch (error) {
      return ResponseBuilder.validationError(['Invalid JSON in request body']);
    }

    // Validate batch process request
    if (!requestData.students || !Array.isArray(requestData.students)) {
      return ResponseBuilder.validationError(['Students array is required']);
    }

    if (requestData.students.length === 0) {
      return ResponseBuilder.validationError(['At least one student is required']);
    }

    if (requestData.students.length > 100) {
      return ResponseBuilder.validationError(['Maximum 100 students allowed per batch']);
    }

    // Validate each student in the batch
    const validatedStudents = [];
    for (let i = 0; i < requestData.students.length; i++) {
      try {
        const validatedStudent = Validator.validateCreateStudentRequest(requestData.students[i]);
        validatedStudents.push(validatedStudent);
      } catch (error) {
        return ResponseBuilder.validationError([
          `Student at index ${i}: ${error instanceof Error ? error.message : 'Invalid data'}`
        ]);
      }
    }

    const batchRequest: BatchProcessRequest = {
      students: validatedStudents,
      options: requestData.options || { parallel: true, maxConcurrency: 10 },
    };

    // Initialize services
    const tableName = process.env.STUDENTS_TABLE_NAME;
    if (!tableName) {
      throw new Error('STUDENTS_TABLE_NAME environment variable is not set');
    }

    const dynamoService = new DynamoDBService(tableName);
    const sqsClient = new SQSClient({ region: process.env.AWS_REGION || 'us-west-2' });
    const sfnClient = new SFNClient({ region: process.env.AWS_REGION || 'us-west-2' });

    // Check for existing students by email
    const existingStudents = [];
    const newStudents = [];

    for (const student of batchRequest.students) {
      const existing = await dynamoService.getStudentByEmail(student.email);
      if (existing) {
        existingStudents.push(existing);
      } else {
        newStudents.push(student);
      }
    }

    // If all students already exist, return conflict
    if (existingStudents.length === batchRequest.students.length) {
      return ResponseBuilder.conflict('All students already exist');
    }

    // Generate execution ID
    const executionId = `batch_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    // Process students based on options
    let response: BatchProcessResponse;

    if (batchRequest.options?.parallel && newStudents.length > 1) {
      // Use Step Functions for parallel processing
      const stateMachineArn = process.env.STATE_MACHINE_ARN;
      if (!stateMachineArn) {
        throw new Error('STATE_MACHINE_ARN environment variable is not set');
      }

      // Start Step Functions execution
      const startExecutionCommand = new StartExecutionCommand({
        stateMachineArn,
        name: executionId,
        input: JSON.stringify({
          students: newStudents.map(student => ({
            ...student,
            type: 'single',
          })),
          executionId,
          options: batchRequest.options,
        }),
      });

      await sfnClient.send(startExecutionCommand);

      response = {
        executionId,
        status: 'STARTED',
        totalStudents: batchRequest.students.length,
        processedStudents: 0,
        failedStudents: 0,
      };
    } else {
      // Process synchronously
      const result = await dynamoService.batchCreateStudents(
        newStudents.map(student => ({
          ...student,
          status: StudentStatus.PENDING,
        }))
      );

      // Send completion message to SQS
      const completionQueueUrl = process.env.COMPLETION_QUEUE_URL;
      if (completionQueueUrl) {
        const completionMessage = {
          executionId,
          status: 'COMPLETED',
          timestamp: new Date().toISOString(),
          results: {
            successful: result.successful,
            failed: result.failed,
          },
          summary: {
            total: batchRequest.students.length,
            successful: result.successful.length,
            failed: result.failed.length,
            processingTime: 0, // Would be calculated in real implementation
          },
        };

        await sqsClient.send(new SendMessageCommand({
          QueueUrl: completionQueueUrl,
          MessageBody: JSON.stringify(completionMessage),
        }));
      }

      response = {
        executionId,
        status: 'COMPLETED',
        totalStudents: batchRequest.students.length,
        processedStudents: result.successful.length,
        failedStudents: result.failed.length,
        results: result.successful,
        errors: result.failed,
      };
    }

    console.log(`Batch processing initiated: ${executionId}`);

    return ResponseBuilder.success(response, 202, 'Student processing initiated');

  } catch (error) {
    console.error('Error processing students:', error);

    if (error instanceof ValidationError) {
      return ResponseBuilder.validationError([error.message]);
    }

    return ResponseBuilder.internalError(error as Error);
  }
};
