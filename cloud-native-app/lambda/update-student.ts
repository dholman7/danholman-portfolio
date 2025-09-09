import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBService } from './utils/dynamodb';
import { Validator, ValidationError } from './utils/validation';
import { ResponseBuilder } from './utils/response';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Update student request:', JSON.stringify(event, null, 2));

  try {
    // Extract and validate student ID from path parameters
    const studentId = event.pathParameters?.id;
    if (!studentId) {
      return ResponseBuilder.validationError(['Student ID is required in path parameters']);
    }

    const validatedId = Validator.validateId(studentId);

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

    const validatedData = Validator.validateUpdateStudentRequest(requestData);

    // Check if there are any fields to update
    if (Object.keys(validatedData).length === 0) {
      return ResponseBuilder.validationError(['At least one field must be provided for update']);
    }

    // Initialize DynamoDB service
    const tableName = process.env.STUDENTS_TABLE_NAME;
    if (!tableName) {
      throw new Error('STUDENTS_TABLE_NAME environment variable is not set');
    }

    const dynamoService = new DynamoDBService(tableName);

    // Update student
    const updatedStudent = await dynamoService.updateStudent(validatedId, validatedData);
    if (!updatedStudent) {
      return ResponseBuilder.notFound('Student');
    }

    console.log('Student updated successfully:', updatedStudent.id);

    return ResponseBuilder.success(updatedStudent, 200, 'Student updated successfully');

  } catch (error) {
    console.error('Error updating student:', error);

    if (error instanceof ValidationError) {
      return ResponseBuilder.validationError([error.message]);
    }

    return ResponseBuilder.internalError(error as Error);
  }
};
