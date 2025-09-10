# Test Types and Organization

This document describes the different types of tests in the cloud-native-app project and how they are organized.

## Test Structure

```
tests/
├── unit/           # Unit tests - test individual functions/methods in isolation
├── component/      # Component tests - test modules with mocked dependencies
├── integration/    # Integration tests - test API endpoints and external services
└── e2e/           # End-to-end tests - test complete user workflows
```

## Test Types

### Unit Tests (`tests/unit/`)

**Purpose**: Test individual functions, methods, or classes in complete isolation.

**Characteristics**:
- Fast execution (< 1ms per test)
- No external dependencies
- No I/O operations
- Pure function testing
- Mock all dependencies

**Examples**:
- Lambda function handlers with mocked AWS services
- Utility functions
- Data validation functions
- Business logic functions

**Test Markers**: `@test-type: unit`

### Component Tests (`tests/component/`)

**Purpose**: Test modules or components with their dependencies mocked.

**Characteristics**:
- Medium execution time (1-100ms per test)
- Mock external dependencies
- Test component interactions
- Verify component behavior with mocked services

**Examples**:
- DynamoDB service with mocked AWS SDK
- S3 service with mocked AWS SDK
- SQS service with mocked AWS SDK
- Step Functions service with mocked AWS SDK

**Test Markers**: `@test-type: component`

### Integration Tests (`tests/integration/`)

**Purpose**: Test integration between different parts of the system.

**Characteristics**:
- Slower execution (100ms-1s per test)
- Test real integrations between components
- May use test databases or services
- Verify API contracts and data flow

**Examples**:
- API Gateway integration with Lambda functions
- DynamoDB operations with real test database
- S3 operations with test bucket
- SQS message processing
- Step Functions execution

**Test Markers**: `@test-type: integration`

### End-to-End Tests (`tests/e2e/`)

**Purpose**: Test complete user workflows and business processes.

**Characteristics**:
- Slowest execution (1s+ per test)
- Test complete user journeys
- May use real or near-real environments
- Verify end-to-end functionality

**Examples**:
- Complete student registration workflow
- Batch processing workflow
- Error recovery scenarios
- Performance testing
- User acceptance testing

**Test Markers**: `@test-type: e2e`

## Running Tests

### All Tests
```bash
make test
# or
yarn test
```

### By Type
```bash
make test-unit        # Run unit tests
make test-component   # Run component tests
make test-integration # Run integration tests
make test-e2e         # Run E2E tests
```

### With Coverage
```bash
make test:coverage
# or
yarn test:coverage
```

## Test Configuration

### Jest Configuration
The project uses Jest for testing with the following configuration in `package.json`:

```json
{
  "jest": {
    "preset": "ts-jest",
    "testEnvironment": "node",
    "roots": ["<rootDir>/tests", "<rootDir>/lambda"],
    "testMatch": ["**/__tests__/**/*.ts", "**/?(*.)+(spec|test).ts"],
    "collectCoverageFrom": [
      "lambda/**/*.ts",
      "!lambda/**/*.d.ts",
      "!lambda/**/__tests__/**"
    ],
    "coverageDirectory": "coverage",
    "coverageReporters": ["text", "lcov", "html"]
  }
}
```

### Test Markers
Tests are marked with comments to indicate their type:
- `// @test-type: unit`
- `// @test-type: component`
- `// @test-type: integration`
- `// @test-type: e2e`

## Best Practices

### Unit Tests
- Test one thing at a time
- Use descriptive test names
- Arrange-Act-Assert pattern
- Mock all external dependencies
- Test edge cases and error conditions

### Component Tests
- Mock external services
- Test component interfaces
- Verify error handling
- Test configuration and setup

### Integration Tests
- Use test databases/services
- Clean up test data
- Test real API contracts
- Verify data persistence

### E2E Tests
- Test complete user workflows
- Use realistic test data
- Test error scenarios
- Verify business requirements

## Test Data Management

### Test Data Creation
- Use factories for consistent test data
- Create test data in `beforeEach` or `beforeAll`
- Clean up test data in `afterEach` or `afterAll`

### Test Data Isolation
- Each test should be independent
- Use unique identifiers for test data
- Avoid shared state between tests

## Continuous Integration

### Test Execution Order
1. Unit tests (fastest, run first)
2. Component tests
3. Integration tests
4. E2E tests (slowest, run last)

### Test Failures
- Unit test failures should block the build
- Component test failures should block the build
- Integration test failures should block the build
- E2E test failures may be warnings in some environments

## Monitoring and Reporting

### Test Results
- Jest provides detailed test results
- Coverage reports are generated in `coverage/` directory
- Test results are displayed in the console

### Test Metrics
- Test execution time
- Test coverage percentage
- Number of tests by type
- Test failure rates

## Troubleshooting

### Common Issues
1. **Test timeouts**: Increase timeout for slow tests
2. **Mock issues**: Ensure mocks are properly configured
3. **Environment variables**: Set required environment variables
4. **Test data conflicts**: Use unique test data identifiers

### Debugging
- Use `console.log` for debugging
- Use Jest's `--verbose` flag for detailed output
- Use `--runInBand` for sequential test execution
- Use `--detectOpenHandles` to find open handles
