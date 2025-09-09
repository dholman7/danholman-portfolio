import { APIGatewayProxyEvent, APIGatewayProxyResult, Context } from 'aws-lambda';
import { DynamoDBService } from './utils/dynamodb';
import { Validator, ValidationError } from './utils/validation';
import { ResponseBuilder } from './utils/response';
import { StudentStatus } from './types';

export const handler = async (
  event: APIGatewayProxyEvent,
  _context: Context
): Promise<APIGatewayProxyResult> => {
  console.log('Create student request:', JSON.stringify(event, null, 2));

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

    const validatedData = Validator.validateCreateStudentRequest(requestData);

    // Initialize DynamoDB service
    const tableName = process.env.STUDENTS_TABLE_NAME;
    if (!tableName) {
      throw new Error('STUDENTS_TABLE_NAME environment variable is not set');
    }

    const dynamoService = new DynamoDBService(tableName);

    // Check if student with email already exists
    const existingStudent = await dynamoService.getStudentByEmail(validatedData.email);
    if (existingStudent) {
      return ResponseBuilder.conflict('Student with this email already exists');
    }

    // Create student
    const student = await dynamoService.createStudent({
      email: validatedData.email,
      firstName: validatedData.firstName,
      lastName: validatedData.lastName,
      programId: validatedData.programId,
      employerId: validatedData.employerId,
      status: StudentStatus.PENDING,
      metadata: validatedData.metadata,
    });

    console.log('Student created successfully:', student.id);

    return ResponseBuilder.success(student, 201, 'Student created successfully');

  } catch (error) {
    console.error('Error creating student:', error);

    if (error instanceof ValidationError) {
      return ResponseBuilder.validationError([error.message]);
    }

    return ResponseBuilder.internalError(error as Error);
  }
};
