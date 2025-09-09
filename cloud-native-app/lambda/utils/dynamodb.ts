import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, PutCommand, UpdateCommand, DeleteCommand, QueryCommand, ScanCommand } from '@aws-sdk/lib-dynamodb';
import { Student, StudentStatus } from '../types';

export class DynamoDBService {
  private client: DynamoDBDocumentClient;
  private tableName: string;

  constructor(tableName: string) {
    const dynamoClient = new DynamoDBClient({
      region: process.env.AWS_REGION || 'us-west-2',
    });
    
    this.client = DynamoDBDocumentClient.from(dynamoClient);
    this.tableName = tableName;
  }

  async createStudent(student: Omit<Student, 'id' | 'createdAt' | 'updatedAt'>): Promise<Student> {
    const now = new Date().toISOString();
    const id = this.generateId();
    
    const newStudent: Student = {
      ...student,
      id,
      createdAt: now,
      updatedAt: now,
      ttl: Math.floor(Date.now() / 1000) + (365 * 24 * 60 * 60), // 1 year TTL
    };

    try {
      await this.client.send(new PutCommand({
        TableName: this.tableName,
        Item: newStudent,
        ConditionExpression: 'attribute_not_exists(id)',
      }));

      return newStudent;
    } catch (error: any) {
      if (error.name === 'ConditionalCheckFailedException') {
        throw new Error('Student with this ID already exists');
      }
      throw error;
    }
  }

  async getStudent(id: string): Promise<Student | null> {
    try {
      // Since we have a composite key, we need to query by id and get the latest record
      const result = await this.client.send(new QueryCommand({
        TableName: this.tableName,
        KeyConditionExpression: 'id = :id',
        ExpressionAttributeValues: {
          ':id': id,
        },
        ScanIndexForward: false, // Sort by createdAt in descending order
        Limit: 1,
      }));

      return result.Items?.[0] as Student || null;
    } catch (error) {
      console.error('Error getting student:', error);
      throw error;
    }
  }

  async getStudentByEmail(email: string): Promise<Student | null> {
    try {
      const result = await this.client.send(new QueryCommand({
        TableName: this.tableName,
        IndexName: 'EmailIndex',
        KeyConditionExpression: 'email = :email',
        ExpressionAttributeValues: {
          ':email': email,
        },
        Limit: 1,
      }));

      return result.Items?.[0] as Student || null;
    } catch (error) {
      console.error('Error getting student by email:', error);
      throw error;
    }
  }

  async updateStudent(id: string, updates: Partial<Student>): Promise<Student | null> {
    const now = new Date().toISOString();
    
    // First, get the current student to get the createdAt value
    const currentStudent = await this.getStudent(id);
    if (!currentStudent) {
      return null;
    }
    
    // Build update expression dynamically
    const updateExpressions: string[] = [];
    const expressionAttributeNames: Record<string, string> = {};
    const expressionAttributeValues: Record<string, any> = {};

    Object.keys(updates).forEach((key, index) => {
      if (key !== 'id' && key !== 'createdAt' && updates[key as keyof Student] !== undefined) {
        const attrName = `#attr${index}`;
        const attrValue = `:val${index}`;
        
        updateExpressions.push(`${attrName} = ${attrValue}`);
        expressionAttributeNames[attrName] = key;
        expressionAttributeValues[attrValue] = updates[key as keyof Student];
      }
    });

    if (updateExpressions.length === 0) {
      throw new Error('No valid fields to update');
    }

    updateExpressions.push('#updatedAt = :updatedAt');
    expressionAttributeNames['#updatedAt'] = 'updatedAt';
    expressionAttributeValues[':updatedAt'] = now;

    try {
      const result = await this.client.send(new UpdateCommand({
        TableName: this.tableName,
        Key: {
          id,
          createdAt: currentStudent.createdAt,
        },
        UpdateExpression: `SET ${updateExpressions.join(', ')}`,
        ExpressionAttributeNames: expressionAttributeNames,
        ExpressionAttributeValues: expressionAttributeValues,
        ConditionExpression: 'attribute_exists(id)',
        ReturnValues: 'ALL_NEW',
      }));

      return result.Attributes as Student || null;
    } catch (error: any) {
      if (error.name === 'ConditionalCheckFailedException') {
        return null;
      }
      throw error;
    }
  }

  async deleteStudent(id: string): Promise<boolean> {
    try {
      // First, get the current student to get the createdAt value
      const currentStudent = await this.getStudent(id);
      if (!currentStudent) {
        return false;
      }

      await this.client.send(new DeleteCommand({
        TableName: this.tableName,
        Key: {
          id,
          createdAt: currentStudent.createdAt,
        },
        ConditionExpression: 'attribute_exists(id)',
      }));

      return true;
    } catch (error: any) {
      if (error.name === 'ConditionalCheckFailedException') {
        return false;
      }
      throw error;
    }
  }

  async listStudents(options: {
    limit?: number;
    lastKey?: string;
    status?: StudentStatus;
    employerId?: string;
    programId?: string;
  } = {}): Promise<{
    students: Student[];
    lastKey?: string;
    count: number;
    hasMore: boolean;
  }> {
    const { limit = 20, lastKey, status, employerId, programId } = options;

    try {
      let command: QueryCommand | ScanCommand;

      // Determine which index to use based on filters
      if (status) {
        command = new QueryCommand({
          TableName: this.tableName,
          IndexName: 'StatusIndex',
          KeyConditionExpression: '#status = :status',
          ExpressionAttributeNames: {
            '#status': 'status',
          },
          ExpressionAttributeValues: {
            ':status': status,
          },
          Limit: limit,
          ExclusiveStartKey: lastKey ? JSON.parse(Buffer.from(lastKey, 'base64').toString('utf8')) : undefined,
        });
      } else if (employerId) {
        command = new QueryCommand({
          TableName: this.tableName,
          IndexName: 'EmployerIndex',
          KeyConditionExpression: 'employerId = :employerId',
          ExpressionAttributeValues: {
            ':employerId': employerId,
          },
          Limit: limit,
          ExclusiveStartKey: lastKey ? JSON.parse(Buffer.from(lastKey, 'base64').toString('utf8')) : undefined,
        });
      } else {
        // Use scan for general queries
        const filterExpressions: string[] = [];
        const expressionAttributeNames: Record<string, string> = {};
        const expressionAttributeValues: Record<string, any> = {};

        if (programId) {
          filterExpressions.push('programId = :programId');
          expressionAttributeValues[':programId'] = programId;
        }

        command = new ScanCommand({
          TableName: this.tableName,
          FilterExpression: filterExpressions.length > 0 ? filterExpressions.join(' AND ') : undefined,
          ExpressionAttributeNames: Object.keys(expressionAttributeNames).length > 0 ? expressionAttributeNames : undefined,
          ExpressionAttributeValues: Object.keys(expressionAttributeValues).length > 0 ? expressionAttributeValues : undefined,
          Limit: limit,
          ExclusiveStartKey: lastKey ? JSON.parse(Buffer.from(lastKey, 'base64').toString('utf8')) : undefined,
        });
      }

      const result = await this.client.send(command);
      
      const students = (result.Items || []) as Student[];
      const hasMore = !!result.LastEvaluatedKey;
      const nextLastKey = hasMore ? Buffer.from(JSON.stringify(result.LastEvaluatedKey)).toString('base64') : undefined;

      return {
        students,
        lastKey: nextLastKey,
        count: students.length,
        hasMore,
      };
    } catch (error) {
      console.error('Error listing students:', error);
      throw error;
    }
  }

  async batchCreateStudents(students: Omit<Student, 'id' | 'createdAt' | 'updatedAt'>[]): Promise<{
    successful: Student[];
    failed: Array<{ student: any; error: string }>;
  }> {
    const successful: Student[] = [];
    const failed: Array<{ student: any; error: string }> = [];

    for (const studentData of students) {
      try {
        const student = await this.createStudent(studentData);
        successful.push(student);
      } catch (error: any) {
        failed.push({
          student: studentData,
          error: error.message,
        });
      }
    }

    return { successful, failed };
  }

  private generateId(): string {
    return `student_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
