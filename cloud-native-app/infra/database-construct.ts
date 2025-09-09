import * as cdk from 'aws-cdk-lib';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { Construct } from 'constructs';

export interface DatabaseConstructProps {
  stage: string;
  serviceName: string;
}

export class DatabaseConstruct extends Construct {
  public readonly studentsTable: dynamodb.Table;

  constructor(scope: Construct, id: string, props: DatabaseConstructProps) {
    super(scope, id);

    const { stage, serviceName } = props;

    // Main students table with GSI for efficient querying
    this.studentsTable = new dynamodb.Table(this, 'StudentsTable', {
      tableName: `${serviceName}-students-${stage}`,
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      sortKey: {
        name: 'createdAt',
        type: dynamodb.AttributeType.STRING,
      },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      pointInTimeRecovery: stage === 'prod',
      encryption: dynamodb.TableEncryption.AWS_MANAGED,
      removalPolicy: stage === 'prod' ? cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY,
      timeToLiveAttribute: 'ttl',
    });

    // Global Secondary Index for querying by email
    this.studentsTable.addGlobalSecondaryIndex({
      indexName: 'EmailIndex',
      partitionKey: {
        name: 'email',
        type: dynamodb.AttributeType.STRING,
      },
      sortKey: {
        name: 'createdAt',
        type: dynamodb.AttributeType.STRING,
      },
    });

    // Global Secondary Index for querying by status
    this.studentsTable.addGlobalSecondaryIndex({
      indexName: 'StatusIndex',
      partitionKey: {
        name: 'status',
        type: dynamodb.AttributeType.STRING,
      },
      sortKey: {
        name: 'createdAt',
        type: dynamodb.AttributeType.STRING,
      },
    });

    // Global Secondary Index for querying by employer
    this.studentsTable.addGlobalSecondaryIndex({
      indexName: 'EmployerIndex',
      partitionKey: {
        name: 'employerId',
        type: dynamodb.AttributeType.STRING,
      },
      sortKey: {
        name: 'createdAt',
        type: dynamodb.AttributeType.STRING,
      },
    });

    // Local Secondary Index for querying by program
    this.studentsTable.addLocalSecondaryIndex({
      indexName: 'ProgramIndex',
      sortKey: {
        name: 'programId',
        type: dynamodb.AttributeType.STRING,
      },
    });

    // Add tags to the table
    cdk.Tags.of(this.studentsTable).add('Environment', stage);
    cdk.Tags.of(this.studentsTable).add('Service', serviceName);
    cdk.Tags.of(this.studentsTable).add('Purpose', 'Student Records');
  }
}
