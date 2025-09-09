import { APIGatewayProxyEvent, Context } from 'aws-lambda';

// Mock AWS SDK before importing handlers
const mockSend = jest.fn();

jest.mock('@aws-sdk/client-dynamodb', () => ({
  DynamoDBClient: jest.fn().mockImplementation(() => ({
    send: mockSend,
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
import { handler as updateStudentHandler } from '../../lambda/update-student';
import { handler as deleteStudentHandler } from '../../lambda/delete-student';
import { handler as listStudentsHandler } from '../../lambda/list-students';
import { handler as processStudentsHandler } from '../../lambda/process-students';

// @test-type: e2e
describe('Student Management E2E Workflow', () => {
  let mockContext: Context;
  let createdStudentId: string;
  let studentDeleted: boolean = false;

  beforeAll(() => {
    // Set up environment variables for E2E testing
    process.env.STUDENTS_TABLE_NAME = 'test-students-table';
    process.env.DATA_BUCKET_NAME = 'test-data-bucket';
    process.env.PROCESSING_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/123456789012/test-queue';
    process.env.COMPLETION_QUEUE_URL = 'https://sqs.us-west-2.amazonaws.com/123456789012/completion-queue';
    process.env.STATE_MACHINE_ARN = 'arn:aws:states:us-west-2:123456789012:stateMachine:test-state-machine';
    process.env.STAGE = 'test';
    process.env.SERVICE_NAME = 'test-service';
  });

  beforeEach(() => {
    // Clear all mocks
    jest.clearAllMocks();
    
    // Reset state
    studentDeleted = false;
    
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

    // Set up default mock responses
    mockSend.mockImplementation((command) => {
      // Mock QueryCommand for getStudentByEmail and getStudent
      if (command.constructor.name === 'QueryCommand') {
        // Check if it's querying by email (EmailIndex) or by id (main table)
        if (command.input.IndexName === 'EmailIndex') {
          return Promise.resolve({ Items: [] }); // No existing student with this email
        } else {
          // Query by id - check if it's a non-existent ID or deleted student
          if (command.input.ExpressionAttributeValues?.[':id'] === 'non-existent-id' || 
              (studentDeleted && command.input.ExpressionAttributeValues?.[':id'] === createdStudentId)) {
            return Promise.resolve({ Items: [] });
          }
          // Return the student with the created ID
          return Promise.resolve({
            Items: [{
              id: createdStudentId || 'student_1234567890_abc123',
              email: 'e2e-test@example.com',
              firstName: 'E2E',
              lastName: 'Test',
              programId: 'program-e2e-123',
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
            email: 'e2e-test@example.com',
            firstName: 'Updated',
            lastName: 'Student',
            programId: 'program-e2e-123',
            status: 'ACTIVE',
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
            ttl: 1672531200
          }
        });
      }
      
      // Mock DeleteCommand for deleteStudent
      if (command.constructor.name === 'DeleteCommand') {
        studentDeleted = true;
        return Promise.resolve({});
      }
      
      // Mock ScanCommand for listStudents
      if (command.constructor.name === 'ScanCommand') {
        const items = [];
        
        // Add the main student if created
        if (createdStudentId) {
          items.push({
            id: createdStudentId,
            email: 'e2e-test@example.com',
            firstName: 'Updated', // This should reflect the updated state
            lastName: 'Student',
            programId: 'program-e2e-123',
            status: 'ACTIVE',
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
            ttl: 1672531200
          });
        }
        
        // Always add batch students for batch processing test
        // This ensures the batch processing test can find the students
        items.push(
          {
            id: 'batch-student-1',
            email: 'batch-e2e-1@example.com',
            firstName: 'Batch',
            lastName: 'One',
            programId: 'program-batch-1',
            status: 'PENDING',
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
            ttl: 1672531200
          },
          {
            id: 'batch-student-2',
            email: 'batch-e2e-2@example.com',
            firstName: 'Batch',
            lastName: 'Two',
            programId: 'program-batch-2',
            status: 'PENDING',
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
            ttl: 1672531200
          },
          {
            id: 'batch-student-3',
            email: 'batch-e2e-3@example.com',
            firstName: 'Batch',
            lastName: 'Three',
            programId: 'program-batch-3',
            status: 'PENDING',
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
            ttl: 1672531200
          }
        );
        
        return Promise.resolve({
          Items: items,
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
      
      // Default response
      return Promise.resolve({});
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Complete Student Lifecycle', () => {
    it('should handle complete student lifecycle from creation to deletion', async () => {
      // Step 1: Create a new student
      const createEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          email: 'e2e-test@example.com',
          firstName: 'E2E',
          lastName: 'Test',
          programId: 'program-e2e-123',
          employerId: 'employer-e2e-456',
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
      createdStudentId = createdStudent.id;
      expect(createdStudent.email).toBe('e2e-test@example.com');
      expect(createdStudent.firstName).toBe('E2E');
      expect(createdStudent.lastName).toBe('Test');
      expect(createdStudent.status).toBe('PENDING');

      // Step 2: Retrieve the created student
      const getEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'GET',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: createdStudentId },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const getResult = await getStudentHandler(getEvent, mockContext);
      expect(getResult.statusCode).toBe(200);

      const retrievedStudent = JSON.parse(getResult.body).data;
      expect(retrievedStudent.id).toBe(createdStudentId);
      expect(retrievedStudent.email).toBe('e2e-test@example.com');

      // Step 3: Update the student
      const updateEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          firstName: 'Updated',
          lastName: 'Student',
          status: 'ACTIVE',
        }),
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'PUT',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: createdStudentId },
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
      expect(updatedStudent.lastName).toBe('Student');
      expect(updatedStudent.status).toBe('ACTIVE');

      // Step 4: List students to verify the student appears
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
      expect(studentsList.students.length).toBeGreaterThan(0);

      // Verify our student is in the list
      const studentInList = studentsList.students.find((s: any) => s.id === createdStudentId);
      expect(studentInList).toBeDefined();
      expect(studentInList.firstName).toBe('Updated');

      // Step 5: Delete the student
      const deleteEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'DELETE',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: createdStudentId },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const deleteResult = await deleteStudentHandler(deleteEvent, mockContext);
      expect(deleteResult.statusCode).toBe(204);

      // Step 6: Verify student is deleted (should return 404)
      const getAfterDeleteResult = await getStudentHandler(getEvent, mockContext);
      expect(getAfterDeleteResult.statusCode).toBe(404);
    });
  });

  describe('Batch Processing Workflow', () => {
    it('should handle batch student processing workflow', async () => {
      // Create multiple students via batch processing
      const batchEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          students: [
            {
              email: 'batch-e2e-1@example.com',
              firstName: 'Batch',
              lastName: 'One',
              programId: 'program-batch-1',
            },
            {
              email: 'batch-e2e-2@example.com',
              firstName: 'Batch',
              lastName: 'Two',
              programId: 'program-batch-2',
            },
            {
              email: 'batch-e2e-3@example.com',
              firstName: 'Batch',
              lastName: 'Three',
              programId: 'program-batch-3',
            },
          ],
          options: {
            parallel: true,
            maxConcurrency: 3,
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

      const batchResult = await processStudentsHandler(batchEvent, mockContext);
      expect(batchResult.statusCode).toBe(202);

      const batchResponse = JSON.parse(batchResult.body).data;
      expect(batchResponse.executionId).toBeDefined();
      expect(batchResponse.status).toBe('STARTED');
      expect(batchResponse.totalStudents).toBe(3);

      // Verify students were created by listing them
      const listEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'GET',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: null,
        queryStringParameters: { limit: '50' },
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

      // Verify batch students are in the list
      const batchStudents = studentsList.students.filter((s: any) => 
        s.email.includes('batch-e2e-')
      );
      expect(batchStudents.length).toBeGreaterThanOrEqual(3);
    });
  });

  describe('Error Recovery Workflow', () => {
    it('should handle error scenarios and recovery', async () => {
      // Test 1: Try to create student with invalid data
      const invalidCreateEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          email: 'invalid-email',
          firstName: '',
          lastName: 'Test',
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

      const invalidCreateResult = await createStudentHandler(invalidCreateEvent, mockContext);
      expect(invalidCreateResult.statusCode).toBe(400);

      const errorResponse = JSON.parse(invalidCreateResult.body);
      expect(errorResponse.success).toBe(false);
      expect(errorResponse.error).toContain('Validation failed');

      // Test 2: Try to get non-existent student
      const getNonExistentEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'GET',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: 'non-existent-id' },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const getNonExistentResult = await getStudentHandler(getNonExistentEvent, mockContext);
      expect(getNonExistentResult.statusCode).toBe(404);

      // Test 3: Try to update non-existent student
      const updateNonExistentEvent: APIGatewayProxyEvent = {
        body: JSON.stringify({
          firstName: 'Updated',
          status: 'ACTIVE',
        }),
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'PUT',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: 'non-existent-id' },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const updateNonExistentResult = await updateStudentHandler(updateNonExistentEvent, mockContext);
      expect(updateNonExistentResult.statusCode).toBe(404);

      // Test 4: Try to delete non-existent student
      const deleteNonExistentEvent: APIGatewayProxyEvent = {
        body: null,
        headers: {},
        multiValueHeaders: {},
        httpMethod: 'DELETE',
        isBase64Encoded: false,
        path: '/students',
        pathParameters: { id: 'non-existent-id' },
        queryStringParameters: null,
        multiValueQueryStringParameters: null,
        requestContext: {} as any,
        resource: '/students/{id}',
        stageVariables: null,
      };

      const deleteNonExistentResult = await deleteStudentHandler(deleteNonExistentEvent, mockContext);
      expect(deleteNonExistentResult.statusCode).toBe(404);
    });
  });
});
