# Test Types and Organization

This document defines the different types of tests used in the automation framework and how they are organized.

## Test Type Definitions

### Unit Tests (`tests/unit/`)
**Purpose**: Test individual functions, methods, or classes in isolation.

**Characteristics**:
- Fast execution (< 1ms per test)
- No external dependencies (databases, APIs, file systems)
- No network calls
- Test single units of code
- Use mocks for any dependencies
- High test coverage

**Examples**:
- Testing helper functions with various inputs
- Testing data validation logic
- Testing utility functions
- Testing individual class methods

**Naming Convention**: `test_<component>_unit.py`

### Component Tests (`tests/component/`)
**Purpose**: Test components with mocked external dependencies.

**Characteristics**:
- Medium execution time (< 100ms per test)
- Mock external dependencies (APIs, databases, file systems)
- Test integration between multiple units
- Verify component behavior with mocked dependencies
- Test error handling and edge cases

**Examples**:
- Testing API client with mocked HTTP responses
- Testing data factories with mocked Faker
- Testing component integration with mocked services
- Testing error handling scenarios

**Naming Convention**: `test_<component>_component.py`

### Integration Tests (`tests/integration/`)
**Purpose**: Test with real external dependencies.

**Characteristics**:
- Slower execution (100ms - 10s per test)
- Use real external services (APIs, databases, file systems)
- Test actual integration points
- Verify data flow between systems
- May require test environment setup

**Examples**:
- Testing API endpoints with real HTTP calls
- Testing database operations
- Testing third-party service integration
- Testing file system operations

**Naming Convention**: `test_<component>_integration.py`

### End-to-End Tests (`tests/e2e/`)
**Purpose**: Test complete user workflows and system behavior.

**Characteristics**:
- Longest execution time (1s - 60s per test)
- Test complete user journeys
- Simulate real user interactions
- Test system integration from user perspective
- May require full application stack

**Examples**:
- Complete user registration workflow
- Complete order placement workflow
- Complete data processing pipeline
- Complete API workflow from start to finish

**Naming Convention**: `test_<workflow>_e2e.py`

## Test Organization

```
tests/
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_helpers_unit.py
│   └── test_<component>_unit.py
├── component/               # Component tests
│   ├── __init__.py
│   ├── test_api_client_component.py
│   ├── test_factories_component.py
│   └── test_<component>_component.py
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_api_examples.py
│   └── test_<component>_integration.py
├── e2e/                     # End-to-end tests
│   ├── __init__.py
│   ├── test_user_registration_e2e.py
│   └── test_<workflow>_e2e.py
└── conftest.py             # Shared fixtures and configuration
```

## Test Execution Strategy

### Development Workflow
1. **Unit Tests**: Run on every code change (fast feedback)
2. **Component Tests**: Run on every commit (medium feedback)
3. **Integration Tests**: Run on pull requests (slower feedback)
4. **E2E Tests**: Run on deployment (comprehensive validation)

### CI/CD Pipeline
1. **Unit + Component**: Run on every push
2. **Integration**: Run on pull requests
3. **E2E**: Run on merge to main branch
4. **All Tests**: Run on release candidates

## Test Markers

Use pytest markers to categorize tests:

```python
@pytest.mark.unit          # Unit tests
@pytest.mark.component     # Component tests
@pytest.mark.integration   # Integration tests
@pytest.mark.e2e          # End-to-end tests
@pytest.mark.smoke        # Critical tests
@pytest.mark.regression   # Regression tests
@pytest.mark.performance  # Performance tests
@pytest.mark.slow         # Slow tests
```

## Running Different Test Types

```bash
# Run all tests
make test

# Run specific test types
make test-unit          # Unit tests only
make test-component     # Component tests only
make test-integration   # Integration tests only
make test-e2e          # E2E tests only

# Run by markers
pytest -m unit          # Unit tests
pytest -m component     # Component tests
pytest -m integration   # Integration tests
pytest -m e2e          # E2E tests
pytest -m smoke        # Smoke tests
pytest -m slow         # Slow tests

# Run specific test files
pytest tests/unit/test_helpers_unit.py
pytest tests/component/test_api_client_component.py
pytest tests/integration/test_api_examples.py
pytest tests/e2e/test_user_registration_e2e.py
```

## Best Practices

### Unit Tests
- Test one thing at a time
- Use descriptive test names
- Test edge cases and error conditions
- Keep tests simple and focused
- Use mocks for all dependencies

### Component Tests
- Test component integration
- Mock external dependencies
- Test error handling
- Verify component behavior
- Test with various data scenarios

### Integration Tests
- Test real external dependencies
- Use test data that won't affect production
- Clean up after tests
- Test error scenarios
- Verify data consistency

### E2E Tests
- Test complete user workflows
- Use realistic test data
- Test error scenarios
- Verify system behavior
- Keep tests independent

## Test Data Management

### Unit Tests
- Use simple, predictable test data
- No external data dependencies
- Use constants and fixtures

### Component Tests
- Use factory-generated test data
- Mock external data sources
- Use realistic but fake data

### Integration Tests
- Use test database/API
- Clean up test data
- Use realistic test scenarios
- Avoid production data

### E2E Tests
- Use complete, realistic test data
- Test with various user scenarios
- Clean up test data
- Use test environment

## Performance Considerations

### Unit Tests
- Should run in < 1ms each
- No I/O operations
- Minimal setup/teardown

### Component Tests
- Should run in < 100ms each
- Mock all I/O operations
- Minimal external dependencies

### Integration Tests
- May take 100ms - 10s each
- Real I/O operations
- May require external services

### E2E Tests
- May take 1s - 60s each
- Full system operations
- Complete user workflows
