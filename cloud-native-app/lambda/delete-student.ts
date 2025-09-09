import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBService } from './utils/dynamodb';
import { Validator, ValidationError } from './utils/validation';
import { ResponseBuilder } from './utils/response';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Delete student request:', JSON.stringify(event, null, 2));

  try {
    // Extract and validate student ID from path parameters
    const studentId = event.pathParameters?.id;
    if (!studentId) {
      return ResponseBuilder.validationError(['Student ID is required in path parameters']);
    }

    const validatedId = Validator.validateId(studentId);

    // Initialize DynamoDB service
    const tableName = process.env.STUDENTS_TABLE_NAME;
    if (!tableName) {
      throw new Error('STUDENTS_TABLE_NAME environment variable is not set');
    }

    const dynamoService = new DynamoDBService(tableName);

    // Delete student
    const deleted = await dynamoService.deleteStudent(validatedId);
    if (!deleted) {
      return ResponseBuilder.notFound('Student');
    }

    console.log('Student deleted successfully:', validatedId);

    return ResponseBuilder.success(null, 204, 'Student deleted successfully');

  } catch (error) {
    console.error('Error deleting student:', error);

    if (error instanceof ValidationError) {
      return ResponseBuilder.validationError([error.message]);
    }

    return ResponseBuilder.internalError(error as Error);
  }
};
