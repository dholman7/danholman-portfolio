#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CloudNativeAppStack } from './cloud-native-app-stack';

const app = new cdk.App();

// Environment configuration
const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION || 'us-west-2',
};

// Stack configuration
const stage = app.node.tryGetContext('stage') || 'dev';
const serviceName = app.node.tryGetContext('serviceName') || 'student-factory';

new CloudNativeAppStack(app, `${serviceName}-${stage}`, {
  env,
  stage,
  serviceName,
  description: 'Highly scalable AWS serverless application demonstrating cloud-native development expertise',
  tags: {
    Environment: stage,
    Service: serviceName,
    Owner: 'Dan Holman',
    Project: 'Portfolio',
  },
});
