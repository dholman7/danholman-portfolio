# Allure Reporting Documentation

## Overview

This document provides comprehensive guidance on using Allure reporting in the Dan Holman Portfolio project. Allure is a flexible, lightweight multi-language test reporting tool that provides clear visual feedback about what has been tested and what has failed.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

## Installation

### Prerequisites

- Python 3.11+ (for automation-framework)
- Python 3.13+ (for ai-rulesets)
- Node.js 18+ (for Allure commandline)

### Install Allure Dependencies

The Allure dependencies are already included in the project requirements:

```bash
# For automation-framework
cd automation-framework
pip install -e ".[test]"

# For ai-rulesets
cd ai-rulesets
pip install -e ".[dev]"
```

### Install Allure Commandline

#### Option 1: Using npm (Recommended)
```bash
npm install -g allure-commandline
```

#### Option 2: Using Docker
```bash
# No installation needed, use Docker commands directly
docker run -p 5050:5050 frankescobar/allure-docker-service:latest
```

## Configuration

### Allure Properties

Each module has its own `allure.properties` file:

- `automation-framework/allure.properties`
- `ai-rulesets/allure.properties`

These files configure:
- Report directories
- Issue tracking links
- Environment information
- Categories for test failures
- History and trend settings

### Categories Configuration

Test failures are automatically categorized using `allure-categories.json`:

- **Test Defects**: Assertion errors, timeouts
- **Product Defects**: API errors, connection issues
- **Infrastructure Issues**: WebDriver, Selenium errors
- **Environment Issues**: Configuration, setup errors
- **Performance Issues**: Slow tests, timeouts

## Basic Usage

### Generate Allure Results

```bash
# Generate results for automation-framework
cd automation-framework
make allure-results

# Generate results for ai-rulesets
cd ai-rulesets
make allure-results
```

### Generate and View Reports

```bash
# Generate HTML report
make allure-generate

# Serve report locally
make allure-serve

# Open report in browser
make allure-open
```

### Docker Usage

```bash
# Generate report using Docker
make allure-docker-generate

# Serve report using Docker
make allure-docker-serve
```

## Advanced Features

### Test Annotations

#### Epic and Feature
```python
@allure.epic("Test Automation Framework")
@allure.feature("API Testing")
class TestAPI:
    pass
```

#### Story and Title
```python
@allure.story("User Authentication")
@allure.title("Test user login with valid credentials")
def test_user_login():
    pass
```

#### Description and Severity
```python
@allure.description("This test verifies user login functionality")
@allure.severity(allure.severity_level.CRITICAL)
def test_critical_login():
    pass
```

#### Tags
```python
@allure.tag("smoke", "regression", "api")
def test_api_endpoint():
    pass
```

### Test Steps

```python
def test_with_steps():
    with allure.step("Setup test data"):
        data = {"user_id": 123}
    
    with allure.step("Execute test action"):
        result = perform_action(data)
    
    with allure.step("Verify results"):
        assert result.success
```

### Attachments

```python
# Text attachment
allure.attach("Test data", "Data", allure.attachment_type.TEXT)

# JSON attachment
allure.attach(json.dumps(data), "JSON Data", allure.attachment_type.JSON)

# HTML attachment
allure.attach("<h1>Report</h1>", "HTML", allure.attachment_type.HTML)

# Screenshot attachment
allure.attach(screenshot_data, "Screenshot", allure.attachment_type.PNG)
```

### Dynamic Titles and Descriptions

```python
def test_dynamic():
    environment = os.getenv("TEST_ENVIRONMENT", "local")
    allure.dynamic.title(f"Test in {environment} environment")
    allure.dynamic.description(f"Environment-specific test for {environment}")
```

### Links

```python
# Issue link
allure.link("https://github.com/user/repo/issues/123", "Bug Report", allure.link_type.ISSUE)

# TMS link
allure.link("https://testmanagement.com/test/456", "Test Case", allure.link_type.TMS)

# Custom link
allure.link("https://docs.example.com", "Documentation", allure.link_type.LINK)
```

## CI/CD Integration

### GitHub Actions

The project includes comprehensive GitHub Actions workflows:

1. **CI Workflow** (`.github/workflows/ci.yml`):
   - Generates Allure results for each module
   - Uploads results as artifacts

2. **Allure Report Workflow** (`.github/workflows/allure-report.yml`):
   - Downloads Allure results from CI
   - Generates HTML reports
   - Deploys to GitHub Pages

### Artifact Management

- Results are stored for 30 days
- Reports are automatically generated on successful builds
- GitHub Pages deployment for easy access

### Matrix Testing

The project supports matrix testing similar to the reference `plans_matrix.yaml`:

```yaml
# Example matrix configuration
strategy:
  matrix:
    module: [automation-framework, ai-test-generation]
    environment: [dev, staging, prod]
```

## Best Practices

### Test Organization

1. **Use Epic and Feature**: Organize tests by major functionality
2. **Consistent Story Naming**: Use clear, descriptive story names
3. **Meaningful Titles**: Make test titles self-explanatory
4. **Proper Severity**: Assign appropriate severity levels

### Step Management

1. **Logical Steps**: Break tests into logical, atomic steps
2. **Descriptive Names**: Use clear step descriptions
3. **Appropriate Granularity**: Don't over-segment or under-segment

### Attachments

1. **Relevant Data**: Only attach data that adds value
2. **Appropriate Types**: Use correct attachment types
3. **Size Management**: Keep attachments reasonably sized
4. **Sensitive Data**: Never attach sensitive information

### Error Handling

1. **Clear Error Messages**: Provide descriptive error messages
2. **Context Information**: Include relevant context in failures
3. **Screenshots**: Attach screenshots for UI test failures
4. **Logs**: Include relevant log information

### Performance

1. **Execution Time**: Monitor test execution times
2. **Memory Usage**: Track memory consumption
3. **Resource Cleanup**: Ensure proper cleanup in teardown
4. **Parallel Execution**: Use appropriate parallel execution

## Troubleshooting

### Common Issues

#### Allure Command Not Found
```bash
# Install Allure commandline
npm install -g allure-commandline

# Or use Docker
docker run -p 5050:5050 frankescobar/allure-docker-service:latest
```

#### Empty Reports
- Ensure tests are generating Allure results
- Check that `--alluredir` is specified in pytest configuration
- Verify Allure results directory exists and contains files

#### Missing Attachments
- Check file paths and permissions
- Ensure attachment data is valid
- Verify attachment types are correct

#### CI/CD Issues
- Check artifact upload/download permissions
- Verify workflow dependencies
- Ensure proper file paths in workflows

### Debug Commands

```bash
# Check Allure installation
allure --version

# List available commands
allure --help

# Generate report with verbose output
allure generate reports/allure-results --clean -o reports/allure-report --verbose

# Serve with debug information
allure serve reports/allure-results --debug
```

## Examples

### Basic Test Example

```python
import allure
import pytest

@allure.epic("User Management")
@allure.feature("Authentication")
class TestUserAuth:
    
    @allure.story("Login")
    @allure.title("Test successful user login")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "regression")
    def test_successful_login(self):
        """Test that users can login with valid credentials."""
        with allure.step("Enter valid credentials"):
            username = "testuser"
            password = "testpass"
            allure.attach(f"Username: {username}", "Credentials", allure.attachment_type.TEXT)
        
        with allure.step("Submit login form"):
            result = login(username, password)
            allure.attach(str(result), "Login Result", allure.attachment_type.JSON)
        
        with allure.step("Verify successful login"):
            assert result.success
            assert result.user_id is not None
```

### Advanced Test Example

```python
import allure
import pytest
import json
import time

@allure.epic("API Testing")
@allure.feature("User Endpoints")
class TestUserAPI:
    
    @allure.story("User CRUD Operations")
    @allure.title("Test complete user lifecycle")
    @allure.severity(allure.severity_level.HIGH)
    @allure.tag("api", "crud", "integration")
    def test_user_lifecycle(self, user_data):
        """Test complete user lifecycle: create, read, update, delete."""
        
        # Create user
        with allure.step("Create new user"):
            create_response = create_user(user_data)
            allure.attach(json.dumps(create_response.json(), indent=2), 
                         "Create Response", allure.attachment_type.JSON)
            assert create_response.status_code == 201
            user_id = create_response.json()["id"]
        
        # Read user
        with allure.step("Read created user"):
            read_response = get_user(user_id)
            allure.attach(json.dumps(read_response.json(), indent=2), 
                         "Read Response", allure.attachment_type.JSON)
            assert read_response.status_code == 200
            assert read_response.json()["username"] == user_data["username"]
        
        # Update user
        with allure.step("Update user information"):
            updated_data = {**user_data, "email": "updated@example.com"}
            update_response = update_user(user_id, updated_data)
            allure.attach(json.dumps(update_response.json(), indent=2), 
                         "Update Response", allure.attachment_type.JSON)
            assert update_response.status_code == 200
        
        # Delete user
        with allure.step("Delete user"):
            delete_response = delete_user(user_id)
            allure.attach(str(delete_response.status_code), 
                         "Delete Status", allure.attachment_type.TEXT)
            assert delete_response.status_code == 204
        
        # Verify deletion
        with allure.step("Verify user deletion"):
            verify_response = get_user(user_id)
            assert verify_response.status_code == 404
```

### Performance Test Example

```python
import allure
import pytest
import time
import psutil

@allure.epic("Performance Testing")
@allure.feature("API Performance")
class TestAPIPerformance:
    
    @allure.story("Response Time")
    @allure.title("Test API response time under load")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("performance", "load")
    def test_api_response_time(self):
        """Test that API responds within acceptable time limits."""
        
        with allure.step("Measure response time"):
            start_time = time.time()
            
            # Simulate API call
            response = make_api_call()
            
            end_time = time.time()
            response_time = end_time - start_time
            
            allure.attach(f"Response time: {response_time:.3f} seconds", 
                         "Performance Metrics", allure.attachment_type.TEXT)
        
        with allure.step("Measure memory usage"):
            memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            allure.attach(f"Memory usage: {memory_usage:.2f} MB", 
                         "Memory Metrics", allure.attachment_type.TEXT)
        
        with allure.step("Validate performance requirements"):
            assert response_time < 2.0  # Should respond within 2 seconds
            assert memory_usage < 100  # Should use less than 100 MB
```

## Makefile Commands

### Automation Framework

```bash
# Generate Allure results
make allure-results

# Generate HTML report
make allure-generate

# Serve report locally
make allure-serve

# Open report in browser
make allure-open

# Clean Allure reports
make allure-clean

# Generate comprehensive reports
make report-comprehensive
```

### AI Rulesets

```bash
# Generate Allure results
make allure-results

# Generate HTML report
make allure-generate

# Serve report locally
make allure-serve

# Open report in browser
make allure-open

# Clean Allure reports
make allure-clean

# Generate comprehensive reports
make report-comprehensive
```

## Integration with Existing Workflows

The Allure reporting system integrates seamlessly with the existing project structure:

- **Automation Framework**: Full integration with pytest configuration
- **AI Rulesets**: Integrated with quality checking pipeline
- **CI/CD**: Automated report generation and deployment
- **Documentation**: Comprehensive examples and best practices

## Conclusion

Allure reporting provides powerful visualization and analysis capabilities for test results. By following the guidelines in this document, you can create comprehensive, informative test reports that help identify issues quickly and provide valuable insights into test execution.

For more information, refer to:
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Allure Python Documentation](https://docs.qameta.io/allure-python/)
- [Project Examples](tests/test_allure_example.py)
