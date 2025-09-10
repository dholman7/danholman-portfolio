# Python Testing Standards

## Testing Principles

- Use pytest for all testing
- Write descriptive test names that explain behavior
- Use fixtures for test data and setup
- Aim for 80%+ test coverage
- Use parametrized tests for multiple test cases
- Mock external dependencies appropriately

## Test Structure

- Test files should be named `test_*.py` or `*_test.py`
- Test functions should start with `test_`
- Use descriptive test names that explain the behavior
- Group related tests in classes
- Use setup and teardown methods when appropriate

```python
def test_user_can_login_with_valid_credentials():
    """Test that user can login with valid credentials."""
    pass

def test_user_cannot_login_with_invalid_credentials():
    """Test that user cannot login with invalid credentials."""
    pass
```

## Fixtures

- Use `@pytest.fixture` for reusable test data
- Scope fixtures appropriately (function, class, module, session)
- Use parametrized fixtures for multiple test cases
- Use fixture factories for complex data creation

```python
import pytest

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(name="Test User", email="test@example.com")

@pytest.fixture(scope="module")
def database():
    """Create a test database."""
    db = create_test_database()
    yield db
    db.cleanup()
```

## Mocking

- Use `unittest.mock` for mocking external dependencies
- Mock at the boundary of your system
- Use `patch` decorators for clean mocking
- Verify mock calls when behavior matters
- Use `side_effect` for complex mock behavior

```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'status': 'success'}
    result = api_client.get_data()
    assert result['status'] == 'success'
    mock_get.assert_called_once()
```
