import { APIGatewayProxyEvent, Context } from 'aws-lambda';
import { handler } from '../../../lambda/create-student';
import { DynamoDBService } from '../../../lambda/utils/dynamodb';
import { StudentStatus } from '../../../lambda/types';

// Mock the DynamoDB service
jest.mock('../../../lambda/utils/dynamodb');
const MockedDynamoDBService = DynamoDBService as jest.MockedClass<typeof DynamoDBService>;

// @test-type: unit
describe('Create Student Lambda', () => {
  let mockDynamoService: jest.Mocked<DynamoDBService>;
  let mockContext: Context;

  beforeEach(() => {
    mockDynamoService = {
      createStudent: jest.fn(),
      getStudentByEmail: jest.fn(),
    } as any;

    MockedDynamoDBService.mockImplementation(() => mockDynamoService);

    mockContext = {
      callbackWaitsForEmptyEventLoop: false,
      functionName: 'create-student',
      functionVersion: '1',
      invokedFunctionArn: 'arn:aws:lambda:us-west-2:123456789012:function:create-student',
      memoryLimitInMB: '256',
      awsRequestId: 'test-request-id',
      logGroupName: '/aws/lambda/create-student',
      logStreamName: '2023/01/01/[$LATEST]test-stream',
      getRemainingTimeInMillis: () => 30000,
      done: jest.fn(),
      fail: jest.fn(),
      succeed: jest.fn(),
    };

    // Set environment variables
    process.env.STUDENTS_TABLE_NAME = 'test-students-table';
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should create a student successfully', async () => {
    const event: APIGatewayProxyEvent = {
      body: JSON.stringify({
        email: 'test@example.com',
        firstName: 'John',
        lastName: 'Doe',
        programId: 'program-123',
        employerId: 'employer-456',
      }),
      headers: {},
      multiValueHeaders: {},
      httpMethod: 'POST',
      isBase64Encoded: false,
      path: '/students',
      pathParameters: null,
      queryStringParameters: null,
      multiValueQueryStringParameters: null,
      requestContext: {} as any,
      resource: '/students',
      stageVariables: null,
    };

    const mockStudent = {
      id: 'student-123',
      email: 'test@example.com',
      firstName: 'John',
      lastName: 'Doe',
      programId: 'program-123',
      employerId: 'employer-456',
      status: StudentStatus.PENDING,
      createdAt: '2023-01-01T00:00:00.000Z',
      updatedAt: '2023-01-01T00:00:00.000Z',
    };

    mockDynamoService.getStudentByEmail.mockResolvedValue(null);
    mockDynamoService.createStudent.mockResolvedValue(mockStudent);

    const result = await handler(event, mockContext);

    expect(result.statusCode).toBe(201);
    expect(JSON.parse(result.body)).toMatchObject({
      success: true,
      data: mockStudent,
      message: 'Student created successfully',
    });

    expect(mockDynamoService.getStudentByEmail).toHaveBeenCalledWith('test@example.com');
    expect(mockDynamoService.createStudent).toHaveBeenCalledWith({
      email: 'test@example.com',
      firstName: 'John',
      lastName: 'Doe',
      programId: 'program-123',
      employerId: 'employer-456',
      status: 'PENDING',
    });
  });

  it('should return 409 if student already exists', async () => {
    const event: APIGatewayProxyEvent = {
      body: JSON.stringify({
        email: 'existing@example.com',
        firstName: 'Jane',
        lastName: 'Smith',
      }),
      headers: {},
      multiValueHeaders: {},
      httpMethod: 'POST',
      isBase64Encoded: false,
      path: '/students',
      pathParameters: null,
      queryStringParameters: null,
      multiValueQueryStringParameters: null,
      requestContext: {} as any,
      resource: '/students',
      stageVariables: null,
    };

    const existingStudent = {
      id: 'existing-student-123',
      email: 'existing@example.com',
      firstName: 'Jane',
      lastName: 'Smith',
      status: StudentStatus.ACTIVE,
      createdAt: '2023-01-01T00:00:00.000Z',
      updatedAt: '2023-01-01T00:00:00.000Z',
    };

    mockDynamoService.getStudentByEmail.mockResolvedValue(existingStudent);

    const result = await handler(event, mockContext);

    expect(result.statusCode).toBe(409);
    expect(JSON.parse(result.body)).toMatchObject({
      success: false,
      error: 'Student with this email already exists',
    });

    expect(mockDynamoService.getStudentByEmail).toHaveBeenCalledWith('existing@example.com');
    expect(mockDynamoService.createStudent).not.toHaveBeenCalled();
  });

  it('should return 400 for invalid request body', async () => {
    const event: APIGatewayProxyEvent = {
      body: JSON.stringify({
        email: 'invalid-email',
        firstName: '',
        lastName: 'Doe',
      }),
      headers: {},
      multiValueHeaders: {},
      httpMethod: 'POST',
      isBase64Encoded: false,
      path: '/students',
      pathParameters: null,
      queryStringParameters: null,
      multiValueQueryStringParameters: null,
      requestContext: {} as any,
      resource: '/students',
      stageVariables: null,
    };

    const result = await handler(event, mockContext);

    expect(result.statusCode).toBe(400);
    expect(JSON.parse(result.body)).toMatchObject({
      success: false,
      error: expect.stringContaining('Validation failed'),
    });

    expect(mockDynamoService.getStudentByEmail).not.toHaveBeenCalled();
    expect(mockDynamoService.createStudent).not.toHaveBeenCalled();
  });

  it('should return 400 for missing request body', async () => {
    const event: APIGatewayProxyEvent = {
      body: null,
      headers: {},
      multiValueHeaders: {},
      httpMethod: 'POST',
      isBase64Encoded: false,
      path: '/students',
      pathParameters: null,
      queryStringParameters: null,
      multiValueQueryStringParameters: null,
      requestContext: {} as any,
      resource: '/students',
      stageVariables: null,
    };

    const result = await handler(event, mockContext);

    expect(result.statusCode).toBe(400);
    expect(JSON.parse(result.body)).toMatchObject({
      success: false,
      error: 'Validation failed: Request body is required',
    });
  });

  it('should handle DynamoDB errors', async () => {
    const event: APIGatewayProxyEvent = {
      body: JSON.stringify({
        email: 'test@example.com',
        firstName: 'John',
        lastName: 'Doe',
      }),
      headers: {},
      multiValueHeaders: {},
      httpMethod: 'POST',
      isBase64Encoded: false,
      path: '/students',
      pathParameters: null,
      queryStringParameters: null,
      multiValueQueryStringParameters: null,
      requestContext: {} as any,
      resource: '/students',
      stageVariables: null,
    };

    mockDynamoService.getStudentByEmail.mockRejectedValue(new Error('DynamoDB error'));

    const result = await handler(event, mockContext);

    expect(result.statusCode).toBe(500);
    expect(JSON.parse(result.body)).toMatchObject({
      success: false,
      error: 'Internal server error',
    });
  });
});
