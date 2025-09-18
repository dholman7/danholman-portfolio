import { APIGatewayProxyEvent, Context } from 'aws-lambda';
import { handler } from '../../../lambda/create-student';
import { DynamoDBService } from '../../../lambda/utils/dynamodb';
import { StudentStatus } from '../../../lambda/types';
import { allure } from 'allure-jest';

// Mock the DynamoDB service
jest.mock('../../../lambda/utils/dynamodb');
const MockedDynamoDBService = DynamoDBService as jest.MockedClass<typeof DynamoDBService>;

// @test-type: unit
@allure.epic('AWS Lambda Functions')
@allure.feature('Student Management')
@allure.story('Create Student')
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

  @allure.title('Create student successfully')
  @allure.description('Test successful student creation with valid data')
  @allure.severity('critical')
  @allure.tag('unit', 'lambda', 'student-creation')
  it('should create a student successfully', async () => {
    await allure.step('Step 1: Prepare valid student data', async () => {
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
      allure.attachment(JSON.stringify(event, null, 2), 'API Gateway Event', 'application/json');
      return event;
    });

    await allure.step('Step 2: Setup mock student response', async () => {
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
      allure.attachment(JSON.stringify(mockStudent, null, 2), 'Mock Student Data', 'application/json');
      return mockStudent;
    });

    await allure.step('Step 3: Configure DynamoDB mocks', async () => {
      mockDynamoService.getStudentByEmail.mockResolvedValue(null);
      mockDynamoService.createStudent.mockResolvedValue({
        id: 'student-123',
        email: 'test@example.com',
        firstName: 'John',
        lastName: 'Doe',
        programId: 'program-123',
        employerId: 'employer-456',
        status: StudentStatus.PENDING,
        createdAt: '2023-01-01T00:00:00.000Z',
        updatedAt: '2023-01-01T00:00:00.000Z',
      });
    });

    await allure.step('Step 4: Execute Lambda handler', async () => {
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

      const result = await handler(event, mockContext);
      allure.attachment(JSON.stringify(result, null, 2), 'Lambda Response', 'application/json');
      return result;
    });

    await allure.step('Step 5: Verify successful response', async () => {
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

      const result = await handler(event, mockContext);

      expect(result.statusCode).toBe(201);
      expect(JSON.parse(result.body)).toMatchObject({
        success: true,
        data: expect.objectContaining({
          email: 'test@example.com',
          firstName: 'John',
          lastName: 'Doe',
        }),
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
  });

  @allure.title('Return 409 if student already exists')
  @allure.description('Test duplicate student creation prevention')
  @allure.severity('normal')
  @allure.tag('unit', 'lambda', 'duplicate-prevention')
  it('should return 409 if student already exists', async () => {
    await allure.step('Step 1: Prepare event with existing student email', async () => {
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
      allure.attachment(JSON.stringify(event, null, 2), 'API Gateway Event', 'application/json');
      return event;
    });

    await allure.step('Step 2: Setup mock existing student response', async () => {
      const existingStudent = {
        id: 'existing-student-123',
        email: 'existing@example.com',
        firstName: 'Jane',
        lastName: 'Smith',
        status: StudentStatus.ACTIVE,
        createdAt: '2023-01-01T00:00:00.000Z',
        updatedAt: '2023-01-01T00:00:00.000Z',
      };
      allure.attachment(JSON.stringify(existingStudent, null, 2), 'Existing Student Data', 'application/json');
      mockDynamoService.getStudentByEmail.mockResolvedValue(existingStudent);
    });

    await allure.step('Step 3: Execute Lambda handler and verify 409 response', async () => {
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

      const result = await handler(event, mockContext);
      allure.attachment(JSON.stringify(result, null, 2), 'Lambda Response', 'application/json');

      expect(result.statusCode).toBe(409);
      expect(JSON.parse(result.body)).toMatchObject({
        success: false,
        error: 'Student with this email already exists',
      });

      expect(mockDynamoService.getStudentByEmail).toHaveBeenCalledWith('existing@example.com');
      expect(mockDynamoService.createStudent).not.toHaveBeenCalled();
    });
  });

  @allure.title('Return 400 for invalid request body')
  @allure.description('Test validation error handling for invalid student data')
  @allure.severity('normal')
  @allure.tag('unit', 'lambda', 'validation')
  it('should return 400 for invalid request body', async () => {
    await allure.step('Step 1: Prepare event with invalid data', async () => {
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
      allure.attachment(JSON.stringify(event, null, 2), 'Invalid API Gateway Event', 'application/json');
      return event;
    });

    await allure.step('Step 2: Execute Lambda handler and verify validation error', async () => {
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
      allure.attachment(JSON.stringify(result, null, 2), 'Validation Error Response', 'application/json');

      expect(result.statusCode).toBe(400);
      expect(JSON.parse(result.body)).toMatchObject({
        success: false,
        error: expect.stringContaining('Validation failed'),
      });

      expect(mockDynamoService.getStudentByEmail).not.toHaveBeenCalled();
      expect(mockDynamoService.createStudent).not.toHaveBeenCalled();
    });
  });

  @allure.title('Return 400 for missing request body')
  @allure.description('Test validation error handling for missing request body')
  @allure.severity('normal')
  @allure.tag('unit', 'lambda', 'validation')
  it('should return 400 for missing request body', async () => {
    await allure.step('Step 1: Prepare event with null body', async () => {
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
      allure.attachment(JSON.stringify(event, null, 2), 'Null Body API Gateway Event', 'application/json');
      return event;
    });

    await allure.step('Step 2: Execute Lambda handler and verify missing body error', async () => {
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
      allure.attachment(JSON.stringify(result, null, 2), 'Missing Body Error Response', 'application/json');

      expect(result.statusCode).toBe(400);
      expect(JSON.parse(result.body)).toMatchObject({
        success: false,
        error: 'Validation failed: Request body is required',
      });
    });
  });

  @allure.title('Handle DynamoDB errors')
  @allure.description('Test error handling when DynamoDB operations fail')
  @allure.severity('normal')
  @allure.tag('unit', 'lambda', 'error-handling')
  it('should handle DynamoDB errors', async () => {
    await allure.step('Step 1: Prepare valid event data', async () => {
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
      allure.attachment(JSON.stringify(event, null, 2), 'Valid API Gateway Event', 'application/json');
      return event;
    });

    await allure.step('Step 2: Configure DynamoDB to throw error', async () => {
      mockDynamoService.getStudentByEmail.mockRejectedValue(new Error('DynamoDB error'));
      allure.attachment('DynamoDB error configured', 'Error Setup', 'text/plain');
    });

    await allure.step('Step 3: Execute Lambda handler and verify error handling', async () => {
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

      const result = await handler(event, mockContext);
      allure.attachment(JSON.stringify(result, null, 2), 'DynamoDB Error Response', 'application/json');

      expect(result.statusCode).toBe(500);
      expect(JSON.parse(result.body)).toMatchObject({
        success: false,
        error: 'Internal server error',
      });
    });
  });
});
