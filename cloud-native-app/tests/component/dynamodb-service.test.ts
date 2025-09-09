import { DynamoDBService } from '../../lambda/utils/dynamodb';
import { StudentStatus } from '../../lambda/types';

// Mock AWS SDK
jest.mock('@aws-sdk/client-dynamodb', () => ({
  DynamoDBClient: jest.fn().mockImplementation(() => ({
    send: jest.fn(),
  })),
}));

jest.mock('@aws-sdk/lib-dynamodb', () => ({
  DynamoDBDocumentClient: {
    from: jest.fn().mockReturnValue({
      send: jest.fn(),
    }),
  },
  PutCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'PutCommand' }
  })),
  QueryCommand: jest.fn().mockImplementation((input) => ({
    input,
    constructor: { name: 'QueryCommand' }
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

// @test-type: component
describe('DynamoDBService Component Tests', () => {
  let dynamoService: DynamoDBService;
  let mockSend: jest.Mock;

  beforeEach(() => {
    // Clear all mocks
    jest.clearAllMocks();
    
    // Get the mock function
    const { DynamoDBDocumentClient } = require('@aws-sdk/lib-dynamodb');
    mockSend = DynamoDBDocumentClient.from().send;
    
    // Create service instance
    dynamoService = new DynamoDBService('test-table');
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('createStudent', () => {
    it('should create a student successfully', async () => {
      const studentData = {
        email: 'test@example.com',
        firstName: 'John',
        lastName: 'Doe',
        programId: 'program-123',
        employerId: 'employer-456',
        status: StudentStatus.PENDING,
      };

      // Mock the DynamoDB client send method
      mockSend.mockResolvedValue({
        Attributes: {
          id: 'student-123',
          ...studentData,
          createdAt: '2023-01-01T00:00:00.000Z',
          updatedAt: '2023-01-01T00:00:00.000Z',
        },
      });

      const result = await dynamoService.createStudent(studentData);

      expect(result).toBeDefined();
      expect(result.email).toBe('test@example.com');
      expect(result.firstName).toBe('John');
      expect(result.lastName).toBe('Doe');
      expect(result.status).toBe(StudentStatus.PENDING);
    });

    it('should handle DynamoDB errors', async () => {
      const studentData = {
        email: 'test@example.com',
        firstName: 'John',
        lastName: 'Doe',
        status: StudentStatus.PENDING,
      };

      // Mock the DynamoDB client to throw an error
      mockSend.mockRejectedValue(new Error('DynamoDB error'));

      await expect(dynamoService.createStudent(studentData)).rejects.toThrow('DynamoDB error');
    });
  });

  describe('getStudentByEmail', () => {
    it('should retrieve a student by email', async () => {
      const email = 'test@example.com';
      const mockStudent = {
        id: 'student-123',
        email,
        firstName: 'John',
        lastName: 'Doe',
        status: StudentStatus.ACTIVE,
        createdAt: '2023-01-01T00:00:00.000Z',
        updatedAt: '2023-01-01T00:00:00.000Z',
      };

      mockSend.mockResolvedValue({
        Items: [mockStudent],
      });

      const result = await dynamoService.getStudentByEmail(email);

      expect(result).toEqual(mockStudent);
    });

    it('should return null if student not found', async () => {
      const email = 'nonexistent@example.com';

      mockSend.mockResolvedValue({
        Items: [],
      });

      const result = await dynamoService.getStudentByEmail(email);

      expect(result).toBeNull();
    });
  });

  describe('updateStudent', () => {
    it('should update a student successfully', async () => {
      const studentId = 'student-123';
      const updateData = {
        firstName: 'Updated',
        lastName: 'Name',
        status: StudentStatus.ACTIVE,
      };

      const mockUpdatedStudent = {
        id: studentId,
        email: 'test@example.com',
        ...updateData,
        createdAt: '2023-01-01T00:00:00.000Z',
        updatedAt: '2023-01-01T00:00:00.000Z',
      };

      // Mock the getStudent call first
      mockSend
        .mockResolvedValueOnce({
          Items: [{
            id: studentId,
            email: 'test@example.com',
            firstName: 'John',
            lastName: 'Doe',
            status: StudentStatus.PENDING,
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
          }]
        })
        .mockResolvedValueOnce({
          Attributes: mockUpdatedStudent,
        });

      const result = await dynamoService.updateStudent(studentId, updateData);

      expect(result).toEqual(mockUpdatedStudent);
    });
  });

  describe('deleteStudent', () => {
    it('should delete a student successfully', async () => {
      const studentId = 'student-123';

      // Mock the getStudent call first, then the delete call
      mockSend
        .mockResolvedValueOnce({
          Items: [{
            id: studentId,
            email: 'test@example.com',
            firstName: 'John',
            lastName: 'Doe',
            status: StudentStatus.PENDING,
            createdAt: '2023-01-01T00:00:00.000Z',
            updatedAt: '2023-01-01T00:00:00.000Z',
          }]
        })
        .mockResolvedValueOnce({});

      const result = await dynamoService.deleteStudent(studentId);

      expect(result).toBe(true);
      expect(mockSend).toHaveBeenCalledTimes(2);
    });
  });

  describe('listStudents', () => {
    it('should list students with pagination', async () => {
      const mockStudents = [
        {
          id: 'student-1',
          email: 'student1@example.com',
          firstName: 'Student',
          lastName: 'One',
          status: StudentStatus.ACTIVE,
        },
        {
          id: 'student-2',
          email: 'student2@example.com',
          firstName: 'Student',
          lastName: 'Two',
          status: StudentStatus.PENDING,
        },
      ];

      mockSend.mockResolvedValue({
        Items: mockStudents,
        Count: 2,
        LastEvaluatedKey: { id: 'student-2' },
      });

      const result = await dynamoService.listStudents({ limit: 10 });

      expect(result).toEqual({
        students: mockStudents,
        count: 2,
        lastKey: 'eyJpZCI6InN0dWRlbnQtMiJ9', // base64 encoded version of {"id":"student-2"}
        hasMore: true,
      });
    });
  });
});