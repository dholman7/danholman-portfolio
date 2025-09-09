import { APIGatewayProxyResult } from 'aws-lambda';
import { ApiResponse } from '../types';

export class ResponseBuilder {
  static success<T>(data: T, statusCode: number = 200, message?: string): APIGatewayProxyResult {
    const response: ApiResponse<T> = {
      success: true,
      data,
      message,
      timestamp: new Date().toISOString(),
      requestId: this.generateRequestId(),
    };

    return {
      statusCode,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
      },
      body: JSON.stringify(response),
    };
  }

  static error(
    error: string | Error,
    statusCode: number = 500,
    message?: string
  ): APIGatewayProxyResult {
    const errorMessage = error instanceof Error ? error.message : error;
    
    const response: ApiResponse = {
      success: false,
      error: errorMessage,
      message,
      timestamp: new Date().toISOString(),
      requestId: this.generateRequestId(),
    };

    return {
      statusCode,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
      },
      body: JSON.stringify(response),
    };
  }

  static validationError(errors: string[]): APIGatewayProxyResult {
    return this.error(
      `Validation failed: ${errors.join(', ')}`,
      400,
      'Invalid request data'
    );
  }

  static notFound(resource: string): APIGatewayProxyResult {
    return this.error(
      `${resource} not found`,
      404,
      'Resource not found'
    );
  }

  static conflict(message: string): APIGatewayProxyResult {
    return this.error(
      message,
      409,
      'Resource conflict'
    );
  }

  static internalError(error: Error): APIGatewayProxyResult {
    console.error('Internal server error:', error);
    return this.error(
      'Internal server error',
      500,
      'An unexpected error occurred'
    );
  }

  static methodNotAllowed(): APIGatewayProxyResult {
    return this.error(
      'Method not allowed',
      405,
      'The requested method is not allowed for this resource'
    );
  }

  static tooManyRequests(): APIGatewayProxyResult {
    return this.error(
      'Too many requests',
      429,
      'Rate limit exceeded'
    );
  }

  private static generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
