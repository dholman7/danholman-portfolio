#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CloudNativeAppStack } from './cloud-native-app-stack';
import { loadEnvironmentConfig, getEnvironmentConfig } from '../src/config/env';

// Load environment variables based on stage
loadEnvironmentConfig();

const app = new cdk.App();

// Get environment configuration
const config = getEnvironmentConfig();

// Environment configuration
const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT || config.awsAccountId,
  region: process.env.CDK_DEFAULT_REGION || config.awsRegion,
};

// Stack configuration - use environment variables with fallbacks
const finalStage = config.stage || 'dev';
const serviceName = config.serviceName || 'student-factory';

new CloudNativeAppStack(app, `${serviceName}-${finalStage}`, {
  env,
  stage: finalStage,
  serviceName,
  description: 'Highly scalable AWS serverless application demonstrating cloud-native development expertise',
  tags: {
    Environment: finalStage,
    Service: serviceName,
    Owner: 'Dan Holman',
    Project: 'Portfolio',
  },
});
