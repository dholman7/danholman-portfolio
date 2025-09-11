/**
 * Environment configuration for different deployment stages
 */

export interface EnvironmentConfig {
  name: string;
  apiUrl: string;
  debug: boolean;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
  features: {
    analytics: boolean;
    errorReporting: boolean;
    devTools: boolean;
  };
}

const environments: Record<string, EnvironmentConfig> = {
  development: {
    name: 'Development',
    apiUrl: 'http://localhost:3000/api',
    debug: true,
    logLevel: 'debug',
    features: {
      analytics: false,
      errorReporting: false,
      devTools: true,
    },
  },
  staging: {
    name: 'Staging',
    apiUrl: 'https://staging-api.example.com/api',
    debug: false,
    logLevel: 'info',
    features: {
      analytics: true,
      errorReporting: true,
      devTools: false,
    },
  },
  production: {
    name: 'Production',
    apiUrl: 'https://api.example.com/api',
    debug: false,
    logLevel: 'error',
    features: {
      analytics: true,
      errorReporting: true,
      devTools: false,
    },
  },
};

/**
 * Get the current environment configuration
 */
export function getEnvironmentConfig(): EnvironmentConfig {
  // Default to development environment
  // In a real app, this would be determined by build process or runtime environment
  const env = 'development';
  return environments[env] || environments.development;
}

/**
 * Check if we're in a specific environment
 */
export function isEnvironment(env: keyof typeof environments): boolean {
  // Default to development environment
  // In a real app, this would be determined by build process or runtime environment
  const currentEnv = 'development';
  return currentEnv === env;
}

/**
 * Get environment-specific API URL
 */
export function getApiUrl(): string {
  return getEnvironmentConfig().apiUrl;
}

/**
 * Check if debug mode is enabled
 */
export function isDebugMode(): boolean {
  return getEnvironmentConfig().debug;
}

/**
 * Get current log level
 */
export function getLogLevel(): string {
  return getEnvironmentConfig().logLevel;
}
