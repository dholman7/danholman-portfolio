import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
// import { DynamoDBService } from './utils/dynamodb';
import { ResponseBuilder } from './utils/response';
import { ProcessingResult, CompletionMessage } from './types';
import { SQSClient, SendMessageCommand } from '@aws-sdk/client-sqs';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Results handler request:', JSON.stringify(event, null, 2));

  try {
    // Parse the event data
    let eventData;
    try {
      eventData = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    } catch (error) {
      console.error('Error parsing event data:', error);
      return ResponseBuilder.error('Invalid event data format', 400);
    }

    const { executionId, results } = eventData;

    if (!executionId) {
      return ResponseBuilder.validationError(['Execution ID is required']);
    }

    if (!results || !Array.isArray(results)) {
      return ResponseBuilder.validationError(['Results array is required']);
    }

    // Initialize services
    const tableName = process.env.STUDENTS_TABLE_NAME;
    if (!tableName) {
      throw new Error('STUDENTS_TABLE_NAME environment variable is not set');
    }

    // const dynamoService = new DynamoDBService(tableName);
    const sqsClient = new SQSClient({ region: process.env.AWS_REGION || 'us-west-2' });

    // Process results
    const processedResults: ProcessingResult[] = [];
    let successfulCount = 0;
    let failedCount = 0;
    const totalProcessingTime = results.reduce((total, result) => total + (result.processingTime || 0), 0);

    for (const result of results) {
      const processingResult: ProcessingResult = {
        success: result.success || false,
        studentId: result.studentId,
        error: result.error,
        processingTime: result.processingTime || 0,
        timestamp: new Date().toISOString(),
      };

      processedResults.push(processingResult);

      if (processingResult.success) {
        successfulCount++;
      } else {
        failedCount++;
      }
    }

    // Create completion message
    const completionMessage: CompletionMessage = {
      executionId,
      status: failedCount === 0 ? 'COMPLETED' : 'FAILED',
      timestamp: new Date().toISOString(),
      results: processedResults,
      summary: {
        total: results.length,
        successful: successfulCount,
        failed: failedCount,
        processingTime: totalProcessingTime,
      },
    };

    // Send completion message to SQS
    const completionQueueUrl = process.env.COMPLETION_QUEUE_URL;
    if (completionQueueUrl) {
      try {
        await sqsClient.send(new SendMessageCommand({
          QueueUrl: completionQueueUrl,
          MessageBody: JSON.stringify(completionMessage),
        }));
        console.log('Completion message sent to SQS:', executionId);
      } catch (error) {
        console.error('Error sending completion message to SQS:', error);
        // Don't fail the function if SQS is unavailable
      }
    }

    // Log summary
    console.log(`Results processed for execution ${executionId}:`, {
      total: results.length,
      successful: successfulCount,
      failed: failedCount,
      processingTime: totalProcessingTime,
    });

    return ResponseBuilder.success(completionMessage, 200, 'Results processed successfully');

  } catch (error) {
    console.error('Error processing results:', error);
    return ResponseBuilder.internalError(error as Error);
  }
};
