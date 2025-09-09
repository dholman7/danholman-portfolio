import { CreateStudentRequest, UpdateStudentRequest, ListStudentsRequest } from '../types';

export class ValidationError extends Error {
  constructor(message: string, public field?: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

export class Validator {
  static validateEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  static validateCreateStudentRequest(data: any): CreateStudentRequest {
    const errors: string[] = [];

    if (!data.email || typeof data.email !== 'string') {
      errors.push('Email is required and must be a string');
    } else if (!this.validateEmail(data.email)) {
      errors.push('Email must be a valid email address');
    }

    if (!data.firstName || typeof data.firstName !== 'string') {
      errors.push('First name is required and must be a string');
    } else if (data.firstName.trim().length === 0) {
      errors.push('First name cannot be empty');
    }

    if (!data.lastName || typeof data.lastName !== 'string') {
      errors.push('Last name is required and must be a string');
    } else if (data.lastName.trim().length === 0) {
      errors.push('Last name cannot be empty');
    }

    if (data.programId && typeof data.programId !== 'string') {
      errors.push('Program ID must be a string');
    }

    if (data.employerId && typeof data.employerId !== 'string') {
      errors.push('Employer ID must be a string');
    }

    if (data.metadata && typeof data.metadata !== 'object') {
      errors.push('Metadata must be an object');
    }

    if (errors.length > 0) {
      throw new ValidationError(`Validation failed: ${errors.join(', ')}`);
    }

    return {
      email: data.email.trim().toLowerCase(),
      firstName: data.firstName.trim(),
      lastName: data.lastName.trim(),
      programId: data.programId?.trim(),
      employerId: data.employerId?.trim(),
      metadata: data.metadata,
    };
  }

  static validateUpdateStudentRequest(data: any): UpdateStudentRequest {
    const errors: string[] = [];

    if (data.firstName !== undefined) {
      if (typeof data.firstName !== 'string') {
        errors.push('First name must be a string');
      } else if (data.firstName.trim().length === 0) {
        errors.push('First name cannot be empty');
      }
    }

    if (data.lastName !== undefined) {
      if (typeof data.lastName !== 'string') {
        errors.push('Last name must be a string');
      } else if (data.lastName.trim().length === 0) {
        errors.push('Last name cannot be empty');
      }
    }

    if (data.programId !== undefined && typeof data.programId !== 'string') {
      errors.push('Program ID must be a string');
    }

    if (data.employerId !== undefined && typeof data.employerId !== 'string') {
      errors.push('Employer ID must be a string');
    }

    if (data.status !== undefined) {
      const validStatuses = ['PENDING', 'ACTIVE', 'INACTIVE', 'SUSPENDED', 'GRADUATED'];
      if (!validStatuses.includes(data.status)) {
        errors.push(`Status must be one of: ${validStatuses.join(', ')}`);
      }
    }

    if (data.metadata !== undefined && typeof data.metadata !== 'object') {
      errors.push('Metadata must be an object');
    }

    if (errors.length > 0) {
      throw new ValidationError(`Validation failed: ${errors.join(', ')}`);
    }

    const result: UpdateStudentRequest = {};

    if (data.firstName !== undefined) {
      result.firstName = data.firstName.trim();
    }
    if (data.lastName !== undefined) {
      result.lastName = data.lastName.trim();
    }
    if (data.programId !== undefined) {
      result.programId = data.programId.trim();
    }
    if (data.employerId !== undefined) {
      result.employerId = data.employerId.trim();
    }
    if (data.status !== undefined) {
      result.status = data.status;
    }
    if (data.metadata !== undefined) {
      result.metadata = data.metadata;
    }

    return result;
  }

  static validateListStudentsRequest(queryParams: any): ListStudentsRequest {
    const result: ListStudentsRequest = {};

    if (queryParams.limit !== undefined) {
      const limit = parseInt(queryParams.limit, 10);
      if (isNaN(limit) || limit < 1 || limit > 100) {
        throw new ValidationError('Limit must be a number between 1 and 100');
      }
      result.limit = limit;
    }

    if (queryParams.lastKey !== undefined) {
      if (typeof queryParams.lastKey !== 'string') {
        throw new ValidationError('Last key must be a string');
      }
      result.lastKey = queryParams.lastKey;
    }

    if (queryParams.status !== undefined) {
      const validStatuses = ['PENDING', 'ACTIVE', 'INACTIVE', 'SUSPENDED', 'GRADUATED'];
      if (!validStatuses.includes(queryParams.status)) {
        throw new ValidationError(`Status must be one of: ${validStatuses.join(', ')}`);
      }
      result.status = queryParams.status as any;
    }

    if (queryParams.employerId !== undefined) {
      if (typeof queryParams.employerId !== 'string') {
        throw new ValidationError('Employer ID must be a string');
      }
      result.employerId = queryParams.employerId;
    }

    if (queryParams.programId !== undefined) {
      if (typeof queryParams.programId !== 'string') {
        throw new ValidationError('Program ID must be a string');
      }
      result.programId = queryParams.programId;
    }

    return result;
  }

  static validateId(id: string): string {
    if (!id || typeof id !== 'string') {
      throw new ValidationError('ID is required and must be a string');
    }

    if (id.trim().length === 0) {
      throw new ValidationError('ID cannot be empty');
    }

    return id.trim();
  }
}
