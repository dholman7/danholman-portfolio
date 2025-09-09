import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBService } from './utils/dynamodb';
import { Validator, ValidationError } from './utils/validation';
import { ResponseBuilder } from './utils/response';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Get student request:', JSON.stringify(event, null, 2));

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

    // Get student
    const student = await dynamoService.getStudent(validatedId);
    if (!student) {
      return ResponseBuilder.notFound('Student');
    }

    console.log('Student retrieved successfully:', student.id);

    return ResponseBuilder.success(student, 200, 'Student retrieved successfully');

  } catch (error) {
    console.error('Error getting student:', error);

    if (error instanceof ValidationError) {
      return ResponseBuilder.validationError([error.message]);
    }

    return ResponseBuilder.internalError(error as Error);
  }
};
