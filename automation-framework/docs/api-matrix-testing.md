# API Matrix Testing with GitHub Actions

## Overview

This document describes the comprehensive API matrix testing solution integrated into the automation framework. The solution provides parallel execution, comprehensive reporting, and flexible test configuration for testing Students & Courses APIs using GitHub Actions matrix strategy.

## Architecture

### Components

1. **Test Matrix Configuration** (`students_courses_test_matrix.json`)
   - Defines test scenarios for different API endpoints
   - Supports filtering by API type, environment, and test scenario
   - Configurable for different HTTP methods and expected status codes

2. **GitHub Actions Workflow** (`.github/workflows/students-courses-api-matrix.yml`)
   - Parallel execution using matrix strategy
   - Dynamic test filtering based on inputs
   - Comprehensive reporting and artifact management
   - Support for multiple environments (dev, staging, prod)

3. **Python Test Suite** (`tests/api/test_students_courses_api.py`)
   - Comprehensive API tests using pytest
   - Allure integration for detailed reporting
   - Support for students, courses, and enrollments APIs
   - Configurable via environment variables

4. **Dependencies** (`requirements.txt`)
   - All necessary testing libraries
   - API testing tools (requests, httpx)
   - Reporting tools (Allure, pytest-html)
   - Performance and security testing tools

## Test Matrix Configuration

### Structure

The test matrix (`students_courses_test_matrix.json`) defines test scenarios with the following structure:

```json
{
  "api_type": "students|courses|enrollments",
  "endpoint": "/api/v1/endpoint",
  "method": "GET|POST|PUT|DELETE",
  "environment": "staging|production",
  "test_scenario": "list_students|create_student|...",
  "expected_status": 200,
  "job_name": "unique_job_identifier"
}
```

### Supported API Types

- **Students**: Student management operations
- **Courses**: Course management operations  
- **Enrollments**: Student-course enrollment operations

### Supported Test Scenarios

- **list**: List all resources
- **create**: Create new resource
- **get_by_id**: Get resource by ID
- **update**: Update existing resource
- **delete**: Delete resource
- **enroll**: Enroll student in course

## GitHub Actions Workflow

### Workflow Triggers

- **Manual Dispatch**: Run with custom parameters
- **Push**: Triggered on pushes to main/develop branches
- **Pull Request**: Triggered on PRs affecting API test files

### Workflow Features

1. **Dynamic Matrix Loading**: Loads and filters test matrix based on inputs
2. **Parallel Execution**: Runs up to 10 tests in parallel
3. **Environment Support**: Supports dev, staging, and production environments
4. **Comprehensive Reporting**: Generates HTML, JUnit XML, and Allure reports
5. **Artifact Management**: Uploads and consolidates test results
6. **PR Integration**: Comments on PRs with test results summary

### Parallel Execution Strategy

**Important Note**: This solution uses GitHub Actions matrix strategy for parallel execution, not pytest-xdist.

#### Why Not pytest-xdist?

- **GitHub Actions Limitation**: pytest-xdist does not work reliably in GitHub Actions environments
- **Matrix Strategy**: GitHub Actions matrix provides better parallelization for CI/CD
- **Resource Management**: Matrix jobs run on separate runners, providing better isolation
- **Scalability**: Matrix strategy scales better for large test suites

#### Parallel Execution Approach

1. **GitHub Actions Matrix**: Each test configuration runs in a separate job
2. **Concurrent Jobs**: Up to 10 jobs can run simultaneously (configurable)
3. **Resource Isolation**: Each job has its own runner and environment
4. **Independent Execution**: Jobs can fail independently without affecting others

#### Local Development

For local development, you can still use pytest-xdist:

```bash
# Install pytest-xdist for local parallel execution
pip install pytest-xdist

# Run tests in parallel locally
pytest tests/api/test_students_courses_api.py -n auto

# Run specific tests in parallel
pytest tests/api/test_students_courses_api.py -m "students and list" -n 4
```

### Manual Workflow Dispatch

You can manually trigger the workflow with these parameters:

- **Environment**: dev, staging, prod (default: staging)
- **API Type**: all, students, courses, enrollments (default: all)
- **Test Scenario**: all, list, create, get_by_id, update, delete, enroll (default: all)

## Test Implementation

### Test Structure

The test suite is organized using pytest classes and markers:

```python
class TestStudentsAPI:
    """Students API test class"""
    
    @allure.feature("Students API")
    @allure.story("List Students")
    @pytest.mark.api
    @pytest.mark.students
    @pytest.mark.list
    def test_list_students(self, api_client, test_data):
        """Test listing all students"""
        # Test implementation
```

### API Client

The framework includes a generic API client for testing:

```python
class APIClient:
    """Generic API client for testing"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        return self._make_request('POST', endpoint, json=data, **kwargs)
```

### Test Data Management

Test data is managed through fixtures and data classes:

```python
@dataclass
class TestData:
    """Test data for API testing"""
    student_id: str = "test_student_123"
    course_id: str = "test_course_456"
    student_payload: Dict[str, Any] = None
    course_payload: Dict[str, Any] = None
```

## Configuration

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `API_BASE_URL` | Base URL for API | `https://staging-api.university.edu` | `https://api.university.edu` |
| `API_TYPE` | Type of API to test | `students` | `courses`, `enrollments` |
| `ENDPOINT` | Specific endpoint | `/api/v1/students` | `/api/v1/courses` |
| `METHOD` | HTTP method | `GET` | `POST`, `PUT`, `DELETE` |
| `TEST_SCENARIO` | Test scenario | `list_students` | `create_student` |
| `EXPECTED_STATUS` | Expected HTTP status | `200` | `201`, `204` |
| `ENVIRONMENT` | Target environment | `staging` | `dev`, `prod` |

### Pytest Markers

- `@pytest.mark.api`: API tests
- `@pytest.mark.students`: Student API tests
- `@pytest.mark.courses`: Course API tests
- `@pytest.mark.enrollments`: Enrollment API tests
- `@pytest.mark.list`: List operation tests
- `@pytest.mark.create`: Create operation tests
- `@pytest.mark.get_by_id`: Get by ID operation tests
- `@pytest.mark.update`: Update operation tests
- `@pytest.mark.delete`: Delete operation tests
- `@pytest.mark.enroll`: Enrollment operation tests

## Local Testing

### Prerequisites

- Python 3.13+
- Node.js 20+ (for Allure reporting)
- All dependencies from `requirements.txt`

### Setup

1. **Install Dependencies**
   ```bash
   cd automation-framework
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export API_BASE_URL="https://your-api-base-url.com"
   export API_TYPE="students"
   export TEST_SCENARIO="list"
   export ENVIRONMENT="staging"
   ```

3. **Run Tests**
   ```bash
   # Run all API tests
   pytest tests/api/test_students_courses_api.py -v
   
   # Run specific API type
   pytest tests/api/test_students_courses_api.py -m "students" -v
   
   # Run specific test scenario
   pytest tests/api/test_students_courses_api.py -m "list" -v
   
   # Generate HTML report
   pytest tests/api/test_students_courses_api.py --html=reports/report.html --self-contained-html
   
   # Generate Allure report
   pytest tests/api/test_students_courses_api.py --allure-results-dir=allure-results
   allure serve allure-results
   ```

## Reporting

### Report Types

1. **HTML Reports**: Individual test results with detailed information
2. **JUnit XML**: Standard format for CI/CD integration
3. **Allure Reports**: Rich interactive reports with trends and analytics
4. **Consolidated Reports**: Merged results from all parallel test runs

### Report Locations

- **Individual Results**: `reports/{job_name}.html`
- **Consolidated Results**: `merged_reports/consolidated_report.html`
- **Allure Results**: `merged_reports/allure-report/`
- **Test Summary**: `merged_reports/test_summary.json`

### Allure Integration

The framework includes comprehensive Allure integration:

```python
@allure.feature("Students API")
@allure.story("List Students")
@allure.severity(allure.severity_level.CRITICAL)
def test_list_students(self, api_client, test_data):
    """Test listing all students"""
    with allure.step("GET /api/v1/students"):
        response = api_client.get('/api/v1/students')
    
    with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
        assert response.status_code == EXPECTED_STATUS
```

## Best Practices

### 1. Test Organization

- Use clear, descriptive test names
- Organize tests by API type and scenario
- Use appropriate pytest markers
- Follow the Page Object Model pattern

### 2. Data Management

- Use fixtures for test data
- Implement proper test data cleanup
- Use realistic but anonymized data
- Avoid hardcoded test data

### 3. Error Handling

- Implement proper error handling and logging
- Use descriptive error messages
- Include context in error reports
- Test error scenarios

### 4. Performance

- Monitor test execution times
- Use parallel execution where possible
- Optimize test data setup and teardown
- Implement proper timeouts

### 5. Security

- Store sensitive data in environment variables
- Use secure authentication methods
- Implement proper secret management
- Follow security best practices

## Troubleshooting

### Common Issues

1. **Test Failures**: Check API endpoints and authentication
2. **Matrix Loading**: Verify JSON syntax in test matrix
3. **Environment Variables**: Ensure all required variables are set
4. **Dependencies**: Install all required packages

### Debug Mode

Run tests with debug logging:
```bash
pytest tests/api/test_students_courses_api.py -v -s --log-cli-level=DEBUG
```

### GitHub Actions Debugging

1. Check workflow logs for matrix loading issues
2. Verify environment variables are set correctly
3. Check artifact upload/download permissions
4. Review test execution logs

## Extending the Framework

### Adding New API Types

1. Add new test class in `test_students_courses_api.py`
2. Add corresponding entries in `students_courses_test_matrix.json`
3. Update workflow filters if needed

### Adding New Test Scenarios

1. Add new test methods to appropriate test class
2. Add corresponding entries in test matrix
3. Update pytest markers if needed

### Modifying Test Data

Update the `TestData` class and fixtures in `test_students_courses_api.py` to match your API schema.

## Integration with CI/CD

### GitHub Actions Integration

The workflow integrates seamlessly with GitHub Actions:

- Automatic triggering on code changes
- Parallel execution for faster feedback
- Comprehensive artifact management
- PR integration with test results

### Artifact Management

- Individual test results are uploaded as artifacts
- Consolidated reports are generated and uploaded
- Test summaries are provided in PR comments
- Historical data is maintained for trend analysis

## Security Considerations

- API keys and sensitive data should be stored in GitHub Secrets
- Test data should be anonymized and non-sensitive
- Use environment-specific configurations
- Implement proper authentication in API client

## Performance Optimization

- Use parallel execution for faster test runs
- Implement proper caching strategies
- Optimize test data setup and teardown
- Monitor and optimize test execution times

## Conclusion

The API Matrix Testing solution provides a comprehensive, scalable approach to testing APIs using GitHub Actions matrix strategy. It offers parallel execution, comprehensive reporting, and flexible configuration, making it suitable for both small teams and enterprise environments.

The solution demonstrates best practices for:
- Test automation at scale
- CI/CD integration
- Parallel test execution
- Comprehensive reporting
- Flexible configuration management
