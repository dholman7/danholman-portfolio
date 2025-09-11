import * as dotenv from 'dotenv';
import * as path from 'path';

/**
 * Load environment variables based on the STAGE environment variable
 * @param stage - The deployment stage (dev, staging, prod)
 * @returns The loaded environment variables
 */
export function loadEnvironmentConfig(stage?: string): void {
  const targetStage = stage || process.env.STAGE || 'dev';
  const envFile = path.join(__dirname, '..', '..', 'env', `.env.${targetStage}`);
  
  try {
    dotenv.config({ path: envFile });
    console.log(`Loaded environment configuration from: ${envFile}`);
  } catch (error) {
    console.warn(`Could not load environment file ${envFile}, using defaults`);
  }
}

/**
 * Get environment variable with fallback
 * @param key - Environment variable key
 * @param defaultValue - Default value if not found
 * @returns Environment variable value or default
 */
export function getEnvVar(key: string, defaultValue?: string): string | undefined {
  return process.env[key] || defaultValue;
}

/**
 * Get required environment variable
 * @param key - Environment variable key
 * @returns Environment variable value
 * @throws Error if environment variable is not set
 */
export function getRequiredEnvVar(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Required environment variable ${key} is not set`);
  }
  return value;
}

/**
 * Get environment configuration object
 * @param stage - The deployment stage (dev, staging, prod)
 * @returns Environment configuration object
 */
export function getEnvironmentConfig(stage?: string) {
  loadEnvironmentConfig(stage);
  
  return {
    stage: getEnvVar('STAGE', 'dev'),
    serviceName: getEnvVar('SERVICE_NAME', 'student-factory'),
    nodeEnv: getEnvVar('NODE_ENV', 'development'),
    awsRegion: getEnvVar('AWS_REGION', 'us-west-2'),
    awsAccountId: getEnvVar('AWS_ACCOUNT_ID', '123456789012'),
    studentsTableName: getEnvVar('STUDENTS_TABLE_NAME'),
    dataBucketName: getEnvVar('DATA_BUCKET_NAME'),
    processingQueueUrl: getEnvVar('PROCESSING_QUEUE_URL'),
    completionQueueUrl: getEnvVar('COMPLETION_QUEUE_URL'),
    stateMachineArn: getEnvVar('STATE_MACHINE_ARN'),
    apiUrl: getEnvVar('API_URL'),
    apiKey: getEnvVar('API_KEY'),
    apiStage: getEnvVar('API_STAGE'),
    lambdaTimeout: parseInt(getEnvVar('LAMBDA_TIMEOUT', '30') || '30'),
    lambdaMemorySize: parseInt(getEnvVar('LAMBDA_MEMORY_SIZE', '256') || '256'),
    lambdaLogRetentionDays: parseInt(getEnvVar('LAMBDA_LOG_RETENTION_DAYS', '30') || '30'),
    logRetentionDays: parseInt(getEnvVar('LOG_RETENTION_DAYS', '30') || '30'),
    enableXrayTracing: getEnvVar('ENABLE_XRAY_TRACING', 'true') === 'true',
    enableDetailedMonitoring: getEnvVar('ENABLE_DETAILED_MONITORING', 'true') === 'true',
    encryptionAtRest: getEnvVar('ENCRYPTION_AT_REST', 'true') === 'true',
    encryptionInTransit: getEnvVar('ENCRYPTION_IN_TRANSIT', 'true') === 'true',
    dynamodbBillingMode: getEnvVar('DYNAMODB_BILLING_MODE', 'PAY_PER_REQUEST'),
    sqsVisibilityTimeout: parseInt(getEnvVar('SQS_VISIBILITY_TIMEOUT', '900') || '900'),
    sqsMessageRetentionPeriod: parseInt(getEnvVar('SQS_MESSAGE_RETENTION_PERIOD', '1209600') || '1209600'),
    enableBatchProcessing: getEnvVar('ENABLE_BATCH_PROCESSING', 'true') === 'true',
    enableParallelProcessing: getEnvVar('ENABLE_PARALLEL_PROCESSING', 'true') === 'true',
    enableNotifications: getEnvVar('ENABLE_NOTIFICATIONS', 'true') === 'true',
    enableArchiving: getEnvVar('ENABLE_ARCHIVING', 'true') === 'true',
    maxBatchSize: parseInt(getEnvVar('MAX_BATCH_SIZE', '100') || '100'),
    maxConcurrentExecutions: parseInt(getEnvVar('MAX_CONCURRENT_EXECUTIONS', '10') || '10'),
    maxRetryAttempts: parseInt(getEnvVar('MAX_RETRY_ATTEMPTS', '3') || '3'),
    timeoutThreshold: parseInt(getEnvVar('TIMEOUT_THRESHOLD', '300') || '300'),
    externalApiTimeout: parseInt(getEnvVar('EXTERNAL_API_TIMEOUT', '5000') || '5000'),
    externalApiRetryAttempts: parseInt(getEnvVar('EXTERNAL_API_RETRY_ATTEMPTS', '3') || '3'),
  };
}

/**
 * Validate required environment variables
 * @param requiredVars - Array of required environment variable keys
 * @throws Error if any required environment variable is missing
 */
export function validateRequiredEnvVars(requiredVars: string[]): void {
  const missingVars: string[] = [];
  
  for (const varName of requiredVars) {
    if (!process.env[varName]) {
      missingVars.push(varName);
    }
  }
  
  if (missingVars.length > 0) {
    throw new Error(`Missing required environment variables: ${missingVars.join(', ')}`);
  }
}

/**
 * Check if running in production
 * @returns True if running in production
 */
export function isProduction(): boolean {
  return process.env.NODE_ENV === 'production' || process.env.STAGE === 'prod';
}

/**
 * Check if running in development
 * @returns True if running in development
 */
export function isDevelopment(): boolean {
  return process.env.NODE_ENV === 'development' || process.env.STAGE === 'dev';
}

/**
 * Check if running in staging
 * @returns True if running in staging
 */
export function isStaging(): boolean {
  return process.env.STAGE === 'staging';
}
