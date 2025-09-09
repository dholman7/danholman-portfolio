import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { ResponseBuilder } from './utils/response';
import { HealthCheckResponse } from './types';
import { DynamoDBClient, DescribeTableCommand } from '@aws-sdk/client-dynamodb';
import { S3Client, HeadBucketCommand } from '@aws-sdk/client-s3';
import { SQSClient, GetQueueAttributesCommand } from '@aws-sdk/client-sqs';
import { SFNClient, DescribeStateMachineCommand } from '@aws-sdk/client-sfn';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Status check request:', JSON.stringify(event, null, 2));

  try {
    const startTime = Date.now();
    const services: HealthCheckResponse['services'] = {
      dynamodb: 'down',
      s3: 'down',
      sqs: 'down',
      stepfunctions: 'down',
    };

    // Check DynamoDB
    try {
      const dynamoClient = new DynamoDBClient({ region: process.env.AWS_REGION || 'us-west-2' });
      const tableName = process.env.STUDENTS_TABLE_NAME;
      
      if (tableName) {
        await dynamoClient.send(new DescribeTableCommand({
          TableName: tableName,
        }));
        services.dynamodb = 'up';
      }
    } catch (error) {
      console.error('DynamoDB health check failed:', error);
    }

    // Check S3
    try {
      const s3Client = new S3Client({ region: process.env.AWS_REGION || 'us-west-2' });
      const bucketName = process.env.DATA_BUCKET_NAME;
      
      if (bucketName) {
        await s3Client.send(new HeadBucketCommand({
          Bucket: bucketName,
        }));
        services.s3 = 'up';
      }
    } catch (error) {
      console.error('S3 health check failed:', error);
    }

    // Check SQS
    try {
      const sqsClient = new SQSClient({ region: process.env.AWS_REGION || 'us-west-2' });
      const queueUrl = process.env.PROCESSING_QUEUE_URL;
      
      if (queueUrl) {
        await sqsClient.send(new GetQueueAttributesCommand({
          QueueUrl: queueUrl,
          AttributeNames: ['QueueArn'],
        }));
        services.sqs = 'up';
      }
    } catch (error) {
      console.error('SQS health check failed:', error);
    }

    // Check Step Functions
    try {
      const sfnClient = new SFNClient({ region: process.env.AWS_REGION || 'us-west-2' });
      const stateMachineArn = process.env.STATE_MACHINE_ARN;
      
      if (stateMachineArn) {
        await sfnClient.send(new DescribeStateMachineCommand({
          stateMachineArn,
        }));
        services.stepfunctions = 'up';
      }
    } catch (error) {
      console.error('Step Functions health check failed:', error);
    }

    // Determine overall health
    const allServicesUp = Object.values(services).every(status => status === 'up');
    const overallStatus = allServicesUp ? 'healthy' : 'unhealthy';

    const response: HealthCheckResponse = {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      services,
      version: process.env.SERVICE_VERSION || '1.0.0',
      environment: process.env.STAGE || 'dev',
    };

    const responseTime = Date.now() - startTime;
    console.log(`Health check completed in ${responseTime}ms:`, response);

    // Return appropriate status code based on health
    const statusCode = overallStatus === 'healthy' ? 200 : 503;

    return ResponseBuilder.success(response, statusCode, 'Health check completed');

  } catch (error) {
    console.error('Error during health check:', error);
    
    const errorResponse: HealthCheckResponse = {
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      services: {
        dynamodb: 'down',
        s3: 'down',
        sqs: 'down',
        stepfunctions: 'down',
      },
      version: process.env.SERVICE_VERSION || '1.0.0',
      environment: process.env.STAGE || 'dev',
    };

    return ResponseBuilder.success(errorResponse, 503, 'Health check failed');
  }
};
