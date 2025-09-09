export interface Student {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  programId?: string;
  employerId?: string;
  status: StudentStatus;
  createdAt: string;
  updatedAt: string;
  ttl?: number;
  metadata?: Record<string, any>;
}

export enum StudentStatus {
  PENDING = 'PENDING',
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE',
  SUSPENDED = 'SUSPENDED',
  GRADUATED = 'GRADUATED',
}

export interface CreateStudentRequest {
  email: string;
  firstName: string;
  lastName: string;
  programId?: string;
  employerId?: string;
  metadata?: Record<string, any>;
}

export interface UpdateStudentRequest {
  firstName?: string;
  lastName?: string;
  programId?: string;
  employerId?: string;
  status?: StudentStatus;
  metadata?: Record<string, any>;
}

export interface ListStudentsRequest {
  limit?: number;
  lastKey?: string;
  status?: StudentStatus;
  employerId?: string;
  programId?: string;
}

export interface ListStudentsResponse {
  students: Student[];
  lastKey?: string;
  count: number;
  hasMore: boolean;
}

export interface BatchProcessRequest {
  students: CreateStudentRequest[];
  options?: {
    parallel?: boolean;
    maxConcurrency?: number;
  };
}

export interface BatchProcessResponse {
  executionId: string;
  status: 'STARTED' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  totalStudents: number;
  processedStudents: number;
  failedStudents: number;
  results?: Student[];
  errors?: Array<{
    student: CreateStudentRequest;
    error: string;
  }>;
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp: string;
  requestId: string;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  services: {
    dynamodb: 'up' | 'down';
    s3: 'up' | 'down';
    sqs: 'up' | 'down';
    stepfunctions: 'up' | 'down';
  };
  version: string;
  environment: string;
}

export interface ProcessingResult {
  success: boolean;
  studentId?: string;
  error?: string;
  processingTime: number;
  timestamp: string;
}

export interface SQSMessage {
  executionId: string;
  timestamp: string;
  input: any;
  results?: ProcessingResult[];
}

export interface CompletionMessage {
  executionId: string;
  status: 'COMPLETED' | 'FAILED';
  timestamp: string;
  results: ProcessingResult[];
  summary: {
    total: number;
    successful: number;
    failed: number;
    processingTime: number;
  };
}
