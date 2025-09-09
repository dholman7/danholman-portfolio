import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';
import { Construct } from 'constructs';

export interface ApiConstructProps {
  stage: string;
  serviceName: string;
  studentsTable: dynamodb.Table;
  stateMachine: stepfunctions.StateMachine;
  createStudentFunction: NodejsFunction;
  getStudentFunction: NodejsFunction;
  listStudentsFunction: NodejsFunction;
  updateStudentFunction: NodejsFunction;
  deleteStudentFunction: NodejsFunction;
  processStudentsFunction: NodejsFunction;
  statusFunction: NodejsFunction;
}

export class ApiConstruct extends Construct {
  public readonly api: apigateway.RestApi;

  constructor(scope: Construct, id: string, props: ApiConstructProps) {
    super(scope, id);

    const {
      stage,
      serviceName,
      stateMachine,
      createStudentFunction,
      getStudentFunction,
      listStudentsFunction,
      updateStudentFunction,
      deleteStudentFunction,
      processStudentsFunction,
      statusFunction,
    } = props;

    // API Gateway with comprehensive configuration
    this.api = new apigateway.RestApi(this, 'Api', {
      restApiName: `${serviceName}-api-${stage}`,
      description: `REST API for ${serviceName} - ${stage} environment`,
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
          'X-Amz-Security-Token',
          'X-Amz-User-Agent',
        ],
        allowCredentials: true,
        maxAge: cdk.Duration.days(1),
      },
      deployOptions: {
        stageName: stage,
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: stage !== 'prod',
        metricsEnabled: true,
        throttlingRateLimit: 1000,
        throttlingBurstLimit: 2000,
      },
      endpointConfiguration: {
        types: [apigateway.EndpointType.REGIONAL],
      },
    });

    // API Key for rate limiting
    const apiKey = this.api.addApiKey('ApiKey', {
      apiKeyName: `${serviceName}-api-key-${stage}`,
      description: `API Key for ${serviceName} ${stage} environment`,
    });

    // Usage Plan
    const usagePlan = this.api.addUsagePlan('UsagePlan', {
      name: `${serviceName}-usage-plan-${stage}`,
      description: `Usage plan for ${serviceName} ${stage} environment`,
      throttle: {
        rateLimit: 100,
        burstLimit: 200,
      },
      quota: {
        limit: 10000,
        period: apigateway.Period.DAY,
      },
    });

    usagePlan.addApiKey(apiKey);
    usagePlan.addApiStage({
      stage: this.api.deploymentStage,
    });

    // Health Check endpoint
    const healthResource = this.api.root.addResource('health');
    healthResource.addMethod('GET', new apigateway.LambdaIntegration(statusFunction), {
      apiKeyRequired: false,
      methodResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // Students resource
    const studentsResource = this.api.root.addResource('students');

    // GET /students - List students
    studentsResource.addMethod('GET', new apigateway.LambdaIntegration(listStudentsFunction), {
      apiKeyRequired: true,
      requestParameters: {
        'method.request.querystring.limit': false,
        'method.request.querystring.lastKey': false,
        'method.request.querystring.status': false,
        'method.request.querystring.employerId': false,
        'method.request.querystring.programId': false,
      },
      methodResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '400',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // POST /students - Create student
    studentsResource.addMethod('POST', new apigateway.LambdaIntegration(createStudentFunction), {
      apiKeyRequired: true,
      requestValidator: new apigateway.RequestValidator(this, 'CreateStudentValidator', {
        restApi: this.api,
        validateRequestBody: true,
        validateRequestParameters: false,
      }),
      requestModels: {
        'application/json': new apigateway.Model(this, 'CreateStudentModel', {
          restApi: this.api,
          contentType: 'application/json',
          modelName: 'CreateStudentModel',
          schema: {
            type: apigateway.JsonSchemaType.OBJECT,
            required: ['email', 'firstName', 'lastName'],
            properties: {
              email: { type: apigateway.JsonSchemaType.STRING, format: 'email' },
              firstName: { type: apigateway.JsonSchemaType.STRING, minLength: 1 },
              lastName: { type: apigateway.JsonSchemaType.STRING, minLength: 1 },
              programId: { type: apigateway.JsonSchemaType.STRING },
              employerId: { type: apigateway.JsonSchemaType.STRING },
              metadata: { type: apigateway.JsonSchemaType.OBJECT },
            },
          },
        }),
      },
      methodResponses: [
        {
          statusCode: '201',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '400',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '409',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // POST /students/batch - Process multiple students
    const batchResource = studentsResource.addResource('batch');
    batchResource.addMethod('POST', new apigateway.LambdaIntegration(processStudentsFunction), {
      apiKeyRequired: true,
      requestValidator: new apigateway.RequestValidator(this, 'BatchStudentsValidator', {
        restApi: this.api,
        validateRequestBody: true,
        validateRequestParameters: false,
      }),
      methodResponses: [
        {
          statusCode: '202',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '400',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // Individual student resource
    const studentResource = studentsResource.addResource('{id}');

    // GET /students/{id} - Get student
    studentResource.addMethod('GET', new apigateway.LambdaIntegration(getStudentFunction), {
      apiKeyRequired: true,
      requestParameters: {
        'method.request.path.id': true,
      },
      methodResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '404',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // PUT /students/{id} - Update student
    studentResource.addMethod('PUT', new apigateway.LambdaIntegration(updateStudentFunction), {
      apiKeyRequired: true,
      requestParameters: {
        'method.request.path.id': true,
      },
      requestValidator: new apigateway.RequestValidator(this, 'UpdateStudentValidator', {
        restApi: this.api,
        validateRequestBody: true,
        validateRequestParameters: true,
      }),
      methodResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '400',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '404',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // DELETE /students/{id} - Delete student
    studentResource.addMethod('DELETE', new apigateway.LambdaIntegration(deleteStudentFunction), {
      apiKeyRequired: true,
      requestParameters: {
        'method.request.path.id': true,
      },
      methodResponses: [
        {
          statusCode: '204',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
        {
          statusCode: '404',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // Status endpoint
    const statusResource = this.api.root.addResource('status');
    statusResource.addMethod('GET', new apigateway.LambdaIntegration(statusFunction), {
      apiKeyRequired: false,
      methodResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Origin': true,
          },
        },
      ],
    });

    // Add tags
    cdk.Tags.of(this.api).add('Environment', stage);
    cdk.Tags.of(this.api).add('Service', serviceName);
    cdk.Tags.of(this.api).add('Purpose', 'API Gateway');
  }
}
