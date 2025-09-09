# Cloud-Native App (Serverless)

A highly scalable AWS serverless application demonstrating cloud-native development expertise with TypeScript, CDK, and comprehensive testing.

## 🚀 Features

### Core Functionality
- **Student Management System**: Full CRUD operations for student records
- **Batch Processing**: Parallel processing of multiple students using Step Functions
- **RESTful API**: Comprehensive API Gateway with validation and rate limiting
- **Data Storage**: DynamoDB with optimized indexing and TTL support
- **File Storage**: S3 integration for data persistence and archival
- **Message Queuing**: SQS for asynchronous processing and notifications

### Technical Highlights
- **Infrastructure as Code**: AWS CDK with TypeScript for reproducible deployments
- **Type Safety**: Full TypeScript implementation with strict type checking
- **Error Handling**: Comprehensive error handling and validation
- **Monitoring**: CloudWatch integration with structured logging
- **Security**: IAM roles, encryption, and secure parameter storage
- **Scalability**: Auto-scaling Lambda functions and DynamoDB on-demand billing

### Testing & Quality
- **Unit Tests**: Comprehensive test coverage with Jest
- **Integration Tests**: End-to-end API testing
- **Type Checking**: Strict TypeScript compilation
- **Linting**: ESLint and Prettier for code quality
- **CI/CD**: GitHub Actions pipeline with automated testing and deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │────│   Lambda Layer   │────│   DynamoDB      │
│   (REST API)    │    │   (TypeScript)   │    │   (Students)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Step Functions│    │   SQS Queues     │    │   S3 Bucket     │
│   (Workflows)   │    │   (Messaging)    │    │   (Data Store)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
cloud-native-app/
├── infra/                    # CDK Infrastructure
│   ├── app.ts               # CDK App entry point
│   ├── cloud-native-app-stack.ts
│   ├── database-construct.ts
│   ├── lambda-construct.ts
│   ├── api-construct.ts
│   └── step-functions-construct.ts
├── lambda/                   # Lambda Functions
│   ├── types.ts             # TypeScript type definitions
│   ├── utils/               # Shared utilities
│   │   ├── response.ts      # API response helpers
│   │   ├── validation.ts    # Input validation
│   │   └── dynamodb.ts      # DynamoDB service layer
│   ├── create-student.ts    # Create student endpoint
│   ├── get-student.ts       # Get student endpoint
│   ├── list-students.ts     # List students endpoint
│   ├── update-student.ts    # Update student endpoint
│   ├── delete-student.ts    # Delete student endpoint
│   ├── process-students.ts  # Batch processing
│   ├── results-handler.ts   # Results processing
│   └── status.ts            # Health check
├── tests/                    # Test Suite
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── .github/workflows/       # CI/CD Pipeline
│   └── ci.yml              # GitHub Actions workflow
├── package.json             # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── cdk.json                # CDK configuration
├── Makefile                # Build automation
└── README.md               # This file
```

## 🛠️ Tech Stack

### Backend
- **AWS Lambda**: Serverless compute with Node.js 18
- **API Gateway**: RESTful API with request validation
- **DynamoDB**: NoSQL database with GSI and LSI
- **S3**: Object storage with lifecycle policies
- **SQS**: Message queuing for async processing
- **Step Functions**: Workflow orchestration
- **CloudWatch**: Logging and monitoring

### Development
- **TypeScript**: Type-safe JavaScript
- **AWS CDK**: Infrastructure as Code
- **Jest**: Testing framework
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **GitHub Actions**: CI/CD pipeline

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Yarn package manager
- AWS CLI configured
- AWS CDK installed globally
- Git

#### Installing Node.js with nvm
```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload your shell or run:
source ~/.bashrc
# or
source ~/.zshrc

# Install and use the exact Node.js version specified in .nvmrc
nvm install
nvm use
nvm alias default $(cat .nvmrc)

# Verify installation (npm comes bundled with Node.js)
node --version
npm --version
```

**Note**: 
- This project includes a `.nvmrc` file specifying Node.js version 18.19.0
- npm comes bundled with Node.js, so no separate installation is needed
- After installing nvm, you can simply run `nvm use` in the project directory to automatically use the correct Node.js version

**Troubleshooting**: If you get "command not found" errors:
```bash
# Make sure nvm is loaded in your current shell
source ~/.bashrc
# or
source ~/.zshrc

# Verify nvm is working
nvm --version

# Reinstall Node.js if needed
nvm uninstall 18.19.0
nvm install 18.19.0
nvm use 18.19.0
```

#### Installing Yarn
```bash
# Install Yarn globally via npm (after Node.js is installed)
npm install -g yarn

# Or install via Homebrew (macOS)
brew install yarn

# Or install via curl (Linux/macOS)
curl -o- -L https://yarnpkg.com/install.sh | bash

# Verify installation
yarn --version
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd danholman-portfolio/cloud-native-app
   ```

2. **Use the correct Node.js version**
   ```bash
   # If using nvm, automatically use the version specified in .nvmrc
   nvm use
   ```

3. **Install dependencies**
   ```bash
   make install
   # or manually with yarn
   yarn install
   # or with npm (fallback)
   npm install
   ```

4. **Set up development environment**
   ```bash
   make dev-setup
   ```

### Development

1. **Run type checking**
   ```bash
   make type-check
   ```

2. **Run linting**
   ```bash
   make lint
   ```

3. **Run tests**
   ```bash
   make test
   ```

4. **Build the project**
   ```bash
   make build
   ```

### Deployment

1. **Bootstrap CDK (first time only)**
   ```bash
   cdk bootstrap
   ```

2. **Deploy to development**
   ```bash
   make deploy:stage STAGE=dev
   ```

3. **Deploy to staging**
   ```bash
   make deploy:stage STAGE=staging
   ```

4. **Deploy to production**
   ```bash
   make deploy:stage STAGE=prod
   ```

## 📚 API Documentation

### Base URL
- Development: `https://api-dev.example.com`
- Staging: `https://api-staging.example.com`
- Production: `https://api.example.com`

### Authentication
All endpoints require an API key in the `X-API-Key` header.

### Endpoints

#### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check (no auth required) |
| `GET` | `/students` | List students with pagination |
| `POST` | `/students` | Create a new student |
| `GET` | `/students/{id}` | Get student by ID |
| `PUT` | `/students/{id}` | Update student |
| `DELETE` | `/students/{id}` | Delete student |
| `POST` | `/students/batch` | Process multiple students |
| `GET` | `/status` | System status |

#### Request/Response Examples

**Create Student**
```bash
curl -X POST https://api.example.com/students \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "programId": "program-123",
    "employerId": "employer-456"
  }'
```

**List Students**
```bash
curl -X GET "https://api.example.com/students?limit=10&status=ACTIVE" \
  -H "X-API-Key: your-api-key"
```

**Batch Process Students**
```bash
curl -X POST https://api.example.com/students/batch \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "students": [
      {
        "email": "student1@example.com",
        "firstName": "Student",
        "lastName": "One"
      },
      {
        "email": "student2@example.com",
        "firstName": "Student",
        "lastName": "Two"
      }
    ],
    "options": {
      "parallel": true,
      "maxConcurrency": 10
    }
  }'
```

## 🧪 Testing

### Unit Tests
```bash
make test
```

### Integration Tests
```bash
npm run test -- --testPathPattern=integration
```

### Test Coverage
```bash
make test:coverage
```

### Test Structure
- **Unit Tests**: Test individual Lambda functions in isolation
- **Integration Tests**: Test API endpoints end-to-end
- **Mocking**: AWS services are mocked for testing

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `STAGE` | Deployment stage (dev/staging/prod) | Yes |
| `SERVICE_NAME` | Service name prefix | Yes |
| `STUDENTS_TABLE_NAME` | DynamoDB table name | Yes |
| `DATA_BUCKET_NAME` | S3 bucket name | Yes |
| `PROCESSING_QUEUE_URL` | SQS processing queue URL | Yes |
| `COMPLETION_QUEUE_URL` | SQS completion queue URL | Yes |
| `STATE_MACHINE_ARN` | Step Functions state machine ARN | Yes |

### CDK Context

The CDK app accepts the following context variables:

```bash
# Deploy to specific stage
cdk deploy --context stage=dev

# Deploy with custom service name
cdk deploy --context serviceName=my-service
```

## 📊 Monitoring

### CloudWatch Metrics
- Lambda function invocations and errors
- API Gateway request count and latency
- DynamoDB read/write capacity
- SQS queue depth and processing time

### Logging
- Structured JSON logging
- Request/response logging
- Error tracking with stack traces
- Performance metrics

### Alerts
- Lambda function errors
- API Gateway 4xx/5xx responses
- DynamoDB throttling
- SQS queue depth

## 🔒 Security

### IAM Roles
- Least privilege access
- Service-specific roles
- Cross-service permissions

### Encryption
- DynamoDB encryption at rest
- S3 server-side encryption
- Lambda environment variable encryption

### Network Security
- VPC configuration (if needed)
- Security groups
- Private subnets for sensitive resources

## 🚀 Performance

### Scalability
- Auto-scaling Lambda functions
- DynamoDB on-demand billing
- API Gateway throttling
- SQS batch processing

### Optimization
- Lambda memory optimization
- DynamoDB query optimization
- S3 lifecycle policies
- CloudFront caching (if needed)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Development Guidelines
- Follow TypeScript best practices
- Write comprehensive tests
- Update documentation
- Follow conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Dan Holman**
- Email: danxholman@gmail.com
- LinkedIn: [linkedin.com/in/danxholman](https://linkedin.com/in/danxholman)
- GitHub: [github.com/dholman7](https://github.com/dholman7)

## 🙏 Acknowledgments

- AWS CDK team for the excellent infrastructure as code framework
- TypeScript team for the powerful type system
- Jest team for the comprehensive testing framework
- All open source contributors who made this project possible
