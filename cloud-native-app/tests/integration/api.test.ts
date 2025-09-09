import { APIGatewayProxyEvent, Context } from 'aws-lambda';

// Mock AWS SDK before importing handlers
const mockSend = jest.fn();

jest.mock('@aws-sdk/client-dynamodb', () => ({
  DynamoDBClient: jest.fn().mockImplementation(() => ({
    send: mockSend,
  })),
  DescribeTableCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'DescribeTableCommand' }
  })),
}));

jest.mock('@aws-sdk/lib-dynamodb', () => ({
  DynamoDBDocumentClient: {
    from: jest.fn().mockReturnValue({
      send: mockSend,
    }),
  },
  QueryCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'QueryCommand' }
  })),
  PutCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'PutCommand' }
  })),
  UpdateCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'UpdateCommand' }
  })),
  DeleteCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'DeleteCommand' }
  })),
  ScanCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'ScanCommand' }
  })),
}));

jest.mock('@aws-sdk/client-s3', () => ({
  S3Client: jest.fn().mockImplementation(() => ({
    send: jest.fn(),
  })),
  HeadBucketCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'HeadBucketCommand' }
  })),
}));

jest.mock('@aws-sdk/client-sqs', () => ({
  SQSClient: jest.fn().mockImplementation(() => ({
    send: jest.fn(),
  })),
  GetQueueAttributesCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'GetQueueAttributesCommand' }
  })),
}));

jest.mock('@aws-sdk/client-sfn', () => ({
  SFNClient: jest.fn().mockImplementation(() => ({
    send: jest.fn(),
  })),
  DescribeStateMachineCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'DescribeStateMachineCommand' }
  })),
  StartExecutionCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'StartExecutionCommand' }
  })),
}));

// Import handlers after mocking
import { handler as createStudentHandler } from '../../lambda/create-student';
import { handler as getStudentHandler } from '../../lambda/get-student';
import { handler as listStudentsHandler } from '../../lambda/list-students';
import { handler as updateStudentHandler } from '../../lambda/update-student';
import { handler as deleteStudentHandler } from '../../lambda/delete-student';
import { handler as processStudentsHandler } from '../../lambda/process-students';
import { handler as statusHandler } from '../../lambda/status';

// @test-type: integration
describe('API Integration Tests', () => {
  let mockContext: Context;
  let createdStudentId: string;

  beforeEach(() => {
    // Clear all mocks
    jest.clearAllMocks();
    
    mockContext = {
      callbackWaitsForEmptyEventLoop: false,
      functionName: 'test-function',
      functionVersion: '1',
      invokedFunctionArn: 'arn:aws:lambda:us-west-2:123456789012:function:test-function',
      memoryLimitInMB: '256',
      awsRequestId: 'test-request-id',
      logGroupName: '/aws/lambda/test-function',
      logStreamName: '2023/01/01/[$LATEST]test-stream',
      getRemainingTimeInMillis: () => 30000,
      done: jest.fn(),
      fail: jest.fn(),
      succeed: jest.fn(),
    };

    // Set environment variables
    process.env.STUDENTS_TABLE_NAME = 'test-students-table';
    process.env.DATA_BUCKET_NAME = 'test-data-bucket';
    process.env.PROCESSING_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue';
    process.env.COMPLETION_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/123456789012/completion-queue';
    process.env.STATE_MACHINE_ARN = 'arn:aws:states:us-west-2:123456789012:stateMachine:test-state-machine';
    process.env.STAGE = 'test';
    process.env.SERVICE_NAME = 'test-service';

    // Set up default mock responses
    mockSend.mockImplementation((command) => {
      // Mock QueryCommand for getStudentByEmail and getStudent
      if (command.constructor.name === 'QueryCommand') {
        // Check if it's querying by email (EmailIndex) or by id (main table)
        if (command.input.IndexName === 'EmailIndex') {
          return Promise.resolve({ Items: [] }); // No existing student with this email
        } else {
          // Query by id - return the student with the created ID
          return Promise.resolve({
            Items: [{
              id: createdStudentId || 'student_1234567890_abc123',
              email: 'integration@example.com',
              firstName: 'Integration',
              lastName: 'Test',
              programId: 'program-123',
              status: 'PENDING',
              createdAt: '2023-01-01T00:00:00.000Z',
              updatedAt: '2023-01-01T00:00:00.000Z',
              ttl: 1672531200
            }]
          });
        }
      }
      
      // Mock PutCommand for createStudent
      if (command.constructor.name === 'PutCommand') {
        return Promise.resolve({});
      }
      
      // Mock UpdateCommand for updateStudent
      if (command.constructor.name === 'UpdateCommand') {
        return Promise.resolve({
          Attributes: {
            id: createdStudentId || 'student_1234567890_abc123',
            email: 'integration@example.com',
            firstName: 'Updated',
            lastName: 'Name',
            programId: 'program-123',
            status: 'ACTIVE',
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
            ttl: 1672531200
          }
        });
      }
      
      // Mock DeleteCommand for deleteStudent
      if (command.constructor.name === 'DeleteCommand') {
        return Promise.resolve({});
      }
      
      // Mock ScanCommand for listStudents
      if (command.constructor.name === 'ScanCommand') {
        return Promise.resolve({
          Items: [
            {
              id: createdStudentId || 'student_1234567890_abc123',
              email: 'integration@example.com',
              firstName: 'Integration',
              lastName: 'Test',
              programId: 'program-123',
              status: 'PENDING',
              createdAt: '2023-01-01T00:00:00.000Z',
              updatedAt: '2023-01-01T00:00:00.000Z',
              ttl: 1672531200
            }
          ],
          LastEvaluatedKey: undefined
        });
      }
      
      // Mock StartExecutionCommand for processStudents
      if (command.constructor.name === 'StartExecutionCommand') {
        return Promise.resolve({
          executionArn: 'arn:aws:states:us-west-2:123456789012:execution:test-state-machine:test-execution-123',
          startDate: new Date('2023-01-01T00:00:00.000Z'),
        });
      }
      
      // Mock DescribeTableCommand for status check
      if (command.constructor.name === 'DescribeTableCommand') {
        return Promise.resolve({
          Table: {
            TableName: 'test-students-table',
            TableStatus: 'ACTIVE',
          },
        });
      }
      
      // Mock HeadBucketCommand for S3 status check
      if (command.constructor.name === 'HeadBucketCommand') {
        return Promise.resolve({});
      }
      
      // Mock GetQueueAttributesCommand for SQS status check
      if (command.constructor.name === 'GetQueueAttributesCommand') {
        return Promise.resolve({
          Attributes: {
            ApproximateNumberOfMessages: '0',
          },
        });
      }
      
      // Mock DescribeStateMachineCommand for Step Functions status check
      if (command.constructor.name === 'DescribeStateMachineCommand') {
        return Promise.resolve({
          stateMachineArn: 'arn:aws:states:us-west-2:123456789012:stateMachine:test-state-machine',
          name: 'test-state-machine',
          status: 'ACTIVE',
        });
      }
      
      // Default response
      return Promise.resolve({});
    });
  });

  describe('Student CRUD Operations', () => {
    it('should create, read, update, and delete a student', async () => {
      // Create student
      const createEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          email: 'integration@example.com',
          firstName: 'Integration',
          lastName: 'Test',
          programId: 'program-123',
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

      const createResult = await createStudentHandler(createEvent, mockContext);
      expect(createResult.statusCode).toBe(201);

      const createdStudent = JSON.parse(createResult.body).data;
      expect(createdStudent.email).toBe('integration@example.com');
      expect(createdStudent.firstName).toBe('Integration');
      expect(createdStudent.lastName).toBe('Test');
      
      // Store the created student ID for use in subsequent operations
      createdStudentId = createdStudent.id;

      // Get student
      const getEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'GET',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: createdStudent.id },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const getResult = await getStudentHandler(getEvent, mockContext);
      expect(getResult.statusCode).toBe(200);

      const retrievedStudent = JSON.parse(getResult.body).data;
      expect(retrievedStudent.id).toBe(createdStudent.id);

      // Update student
      const updateEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          firstName: 'Updated',
          lastName: 'Name',
          status: 'ACTIVE',
        }),
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'PUT',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: createdStudent.id },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const updateResult = await updateStudentHandler(updateEvent, mockContext);
      expect(updateResult.statusCode).toBe(200);

      const updatedStudent = JSON.parse(updateResult.body).data;
      expect(updatedStudent.firstName).toBe('Updated');
      expect(updatedStudent.lastName).toBe('Name');
      expect(updatedStudent.status).toBe('ACTIVE');

      // List students
      const listEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'GET',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: null,
        queryStringParameters: { limit: '10' },
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students',
        stageVariables: null,
      };

      const listResult = await listStudentsHandler(listEvent, mockContext);
      expect(listResult.statusCode).toBe(200);

      const studentsList = JSON.parse(listResult.body).data;
      expect(studentsList.students).toBeDefined();
      expect(Array.isArray(studentsList.students)).toBe(true);

      // Delete student
      const deleteEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'DELETE',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: createdStudent.id },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const deleteResult = await deleteStudentHandler(deleteEvent, mockContext);
      expect(deleteResult.statusCode).toBe(204);
    });
  });

  describe('Batch Processing', () => {
    it('should process multiple students in batch', async () => {
      const batchEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          students: [
            {
              email: 'batch1@example.com',
              firstName: 'Batch',
              lastName: 'One',
              programId: 'program-123',
            },
            {
              email: 'batch2@example.com',
              firstName: 'Batch',
              lastName: 'Two',
              programId: 'program-456',
            },
          ],
          options: {
            parallel: true,
            maxConcurrency: 5,
          },
        }),
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'POST',
        isBase64Encoded: false,
        path: '/students/batch',
        pathParameters: null,
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/batch',
        stageVariables: null,
      };

      const result = await processStudentsHandler(batchEvent, mockContext);
      expect(result.statusCode).toBe(202);

      const batchResponse = JSON.parse(result.body).data;
      expect(batchResponse.executionId).toBeDefined();
      expect(batchResponse.status).toBe('STARTED');
      expect(batchResponse.totalStudents).toBe(2);
    });
  });

  describe('Health Check', () => {
    it('should return health status', async () => {
      const healthEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'GET',
        isBase64Encoded: false,
        path: '/health',
        pathParameters: null,
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/health',
        stageVariables: null,
      };

      const result = await statusHandler(healthEvent, mockContext);
      expect(result.statusCode).toBe(200);

      const healthResponse = JSON.parse(result.body).data;
      expect(healthResponse.status).toBeDefined();
      expect(healthResponse.timestamp).toBeDefined();
      expect(healthResponse.services).toBeDefined();
      expect(healthResponse.version).toBeDefined();
      expect(healthResponse.environment).toBeDefined();
    });
  });

  describe('Error Handling', () => {
    it('should handle validation errors gracefully', async () => {
      const invalidEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          email: 'invalid-email',
          firstName: '',
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

      const result = await createStudentHandler(invalidEvent, mockContext);
      expect(result.statusCode).toBe(400);

      const errorResponse = JSON.parse(result.body);
      expect(errorResponse.success).toBe(false);
      expect(errorResponse.error).toContain('Validation failed');
    });

    it('should handle missing required fields', async () => {
      const incompleteEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          email: 'test@example.com',
          // Missing firstName and lastName
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

      const result = await createStudentHandler(incompleteEvent, mockContext);
      expect(result.statusCode).toBe(400);

      const errorResponse = JSON.parse(result.body);
      expect(errorResponse.success).toBe(false);
      expect(errorResponse.error).toContain('Validation failed');
    });
  });
});
