import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBService } from './utils/dynamodb';
import { Validator, ValidationError } from './utils/validation';
import { ResponseBuilder } from './utils/response';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('List students request:', JSON.stringify(event, null, 2));

  try {
    // Parse and validate query parameters
    const queryParams = event.queryStringParameters || {};
    const validatedParams = Validator.validateListStudentsRequest(queryParams);

    // Initialize DynamoDB service
    const tableName = process.env.STUDENTS_TABLE_NAME;
    if (!tableName) {
      throw new Error('STUDENTS_TABLE_NAME environment variable is not set');
    }

    const dynamoService = new DynamoDBService(tableName);

    // List students
    const result = await dynamoService.listStudents(validatedParams);

    console.log(`Retrieved ${result.count} students`);

    return ResponseBuilder.success(result, 200, 'Students retrieved successfully');

  } catch (error) {
    console.error('Error listing students:', error);

    if (error instanceof ValidationError) {
      return ResponseBuilder.validationError([error.message]);
    }

    return ResponseBuilder.internalError(error as Error);
  }
};
