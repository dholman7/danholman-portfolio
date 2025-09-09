# Allure Integration for Automation Framework

## Overview

This document provides specific guidance for integrating Allure reporting with the automation framework module. It covers setup, configuration, and advanced usage patterns specific to test automation.

## Quick Start

### 1. Install Dependencies

```bash
cd automation-framework
pip install -e ".[test]"
```

### 2. Generate Test Results

```bash
# Run tests with Allure results
make allure-results

# Or run specific test types
make test-unit
make test-integration
make test-e2e
```

### 3. View Reports

```bash
# Generate and serve report
make allure-serve

# Or generate static report
make allure-generate
make allure-open
```

## Configuration

### Pytest Configuration

The framework is pre-configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = [
    "--alluredir=reports/allure-results",
    # ... other options
]
```

### Allure Properties

Configuration is in `allure.properties`:

```properties
allure.results.directory=reports/allure-results
allure.environment=automation-framework
allure.link.issue.pattern=https://github.com/danholman/danholman-portfolio/issues/{}
```

## Test Organization

### Epic and Feature Structure

```python
@allure.epic("Test Automation Framework")
@allure.feature("Web UI Testing")
class TestWebUI:
    pass

@allure.epic("Test Automation Framework")
@allure.feature("API Testing")
class TestAPI:
    pass

@allure.epic("Test Automation Framework")
@allure.feature("Database Testing")
class TestDatabase:
    pass
```

### Story Organization

```python
@allure.story("User Authentication")
@allure.story("User Registration")
@allure.story("Password Management")
class TestUserManagement:
    pass
```

## Advanced Patterns

### Page Object Model Integration

```python
import allure
from src.pages.login_page import LoginPage

@allure.epic("Test Automation Framework")
@allure.feature("Web UI Testing")
class TestLoginPage:
    
    @allure.story("User Authentication")
    @allure.title("Test login with valid credentials")
    def test_valid_login(self, driver):
        """Test successful login with valid credentials."""
        login_page = LoginPage(driver)
        
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login()
            allure.attach(driver.get_screenshot_as_png(), 
                         "Login Page", allure.attachment_type.PNG)
        
        with allure.step("Enter valid credentials"):
            login_page.enter_username("testuser")
            login_page.enter_password("testpass")
            allure.attach("Username: testuser", "Credentials", allure.attachment_type.TEXT)
        
        with allure.step("Submit login form"):
            login_page.click_login_button()
        
        with allure.step("Verify successful login"):
            assert login_page.is_logged_in()
            allure.attach(driver.get_screenshot_as_png(), 
                         "Dashboard After Login", allure.attachment_type.PNG)
```

### API Testing Integration

```python
import allure
import requests
from src.api.client import APIClient

@allure.epic("Test Automation Framework")
@allure.feature("API Testing")
class TestUserAPI:
    
    @allure.story("User CRUD Operations")
    @allure.title("Test user creation via API")
    def test_create_user(self, api_client):
        """Test user creation through API."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword"
        }
        
        with allure.step("Prepare user data"):
            allure.attach(json.dumps(user_data, indent=2), 
                         "User Data", allure.attachment_type.JSON)
        
        with allure.step("Send POST request"):
            response = api_client.create_user(user_data)
            allure.attach(f"Status Code: {response.status_code}", 
                         "Response Status", allure.attachment_type.TEXT)
            allure.attach(response.text, "Response Body", allure.attachment_type.JSON)
        
        with allure.step("Verify response"):
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["username"] == user_data["username"]
```

### Database Testing Integration

```python
import allure
from src.database.connection import DatabaseConnection

@allure.epic("Test Automation Framework")
@allure.feature("Database Testing")
class TestUserDatabase:
    
    @allure.story("Data Integrity")
    @allure.title("Test user data persistence")
    def test_user_data_persistence(self, db_connection):
        """Test that user data is properly persisted."""
        user_id = 123
        expected_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        
        with allure.step("Insert test data"):
            db_connection.insert_user(expected_data)
            allure.attach(f"Inserted user with ID: {user_id}", 
                         "Database Operation", allure.attachment_type.TEXT)
        
        with allure.step("Query user data"):
            actual_data = db_connection.get_user(user_id)
            allure.attach(json.dumps(actual_data, indent=2), 
                         "Retrieved Data", allure.attachment_type.JSON)
        
        with allure.step("Verify data integrity"):
            assert actual_data["username"] == expected_data["username"]
            assert actual_data["email"] == expected_data["email"]
```

## Error Handling and Debugging

### Screenshot on Failure

```python
import allure
import pytest
from selenium import webdriver

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshot on test failure."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Get the driver from the test
        driver = getattr(item, "driver", None)
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, "Screenshot on Failure", allure.attachment_type.PNG)
```

### Detailed Error Information

```python
import allure
import traceback

def test_with_detailed_errors():
    """Test with detailed error reporting."""
    try:
        # Test logic here
        result = perform_operation()
        assert result.success
    except Exception as e:
        with allure.step("Capture error details"):
            error_info = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            }
            allure.attach(json.dumps(error_info, indent=2), 
                         "Error Details", allure.attachment_type.JSON)
        raise
```

## Performance Monitoring

### Test Execution Time

```python
import allure
import time

def test_with_timing():
    """Test with execution time monitoring."""
    with allure.step("Measure execution time"):
        start_time = time.time()
        
        # Test logic
        result = perform_operation()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        allure.attach(f"Execution time: {execution_time:.3f} seconds", 
                     "Performance Metrics", allure.attachment_type.TEXT)
        
        # Validate performance requirements
        assert execution_time < 5.0  # Should complete within 5 seconds
```

### Memory Usage Monitoring

```python
import allure
import psutil
import os

def test_with_memory_monitoring():
    """Test with memory usage monitoring."""
    process = psutil.Process(os.getpid())
    
    with allure.step("Measure memory usage"):
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        allure.attach(f"Memory usage: {memory_mb:.2f} MB", 
                     "Memory Metrics", allure.attachment_type.TEXT)
        
        # Validate memory requirements
        assert memory_mb < 100  # Should use less than 100 MB
```

## CI/CD Integration

### GitHub Actions

The framework automatically generates Allure results in CI:

```yaml
- name: Generate Allure Results
  if: always()
  run: |
    if [ -d tests ] || ls -1 *.py >/dev/null 2>&1; then 
      pytest --alluredir=reports/allure-results || true
    fi

- name: Upload Allure Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: automation-framework-allure-results
    path: reports/allure-results/
    retention-days: 30
```

### Local Development

```bash
# Run tests with Allure results
make test

# Generate and view report
make allure-serve

# Clean up
make allure-clean
```

## Best Practices

### 1. Test Structure

- Use clear, descriptive test names
- Organize tests by epic, feature, and story
- Assign appropriate severity levels
- Use meaningful tags

### 2. Step Organization

- Break tests into logical steps
- Use descriptive step names
- Include relevant data in steps
- Keep steps atomic and focused

### 3. Attachments

- Attach screenshots for UI tests
- Include API request/response data
- Add database query results
- Provide context for failures

### 4. Error Handling

- Capture detailed error information
- Include stack traces
- Attach relevant logs
- Provide debugging context

### 5. Performance

- Monitor execution times
- Track memory usage
- Validate performance requirements
- Include performance metrics

## Troubleshooting

### Common Issues

1. **Empty Reports**: Ensure `--alluredir` is configured
2. **Missing Screenshots**: Check WebDriver integration
3. **Attachment Issues**: Verify file paths and permissions
4. **CI/CD Problems**: Check artifact upload/download

### Debug Commands

```bash
# Check Allure installation
allure --version

# Generate with verbose output
allure generate reports/allure-results --clean -o reports/allure-report --verbose

# Serve with debug information
allure serve reports/allure-results --debug
```

## Examples

See `tests/test_allure_example.py` for comprehensive examples of Allure integration with the automation framework.

## Conclusion

Allure reporting provides powerful visualization and analysis capabilities for the automation framework. By following the patterns and practices outlined in this document, you can create comprehensive, informative test reports that help identify issues quickly and provide valuable insights into test execution.
