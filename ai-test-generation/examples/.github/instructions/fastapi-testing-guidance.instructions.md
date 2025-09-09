# FastAPI Testing Guidance - GitHub Copilot Guidance

Comprehensive guidance for testing FastAPI applications with pytest and httpx

## Supported Languages
- python


## Supported Frameworks
- fastapi
- pytest
- httpx


## Test Categories
- api
- integration
- unit


---

## Testing Guidance and Patterns


### Dependency Injection Testing

Test FastAPI dependencies and dependency overrides

```python
# Test FastAPI dependencies
from fastapi import Depends
from unittest.mock import Mock

# Override dependencies for testing
def test_with_dependency_override():
    def override_get_db():
        return Mock()
    
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    response = client.get("/protected-route")
    assert response.status_code == 200
    
    # Clean up
    app.dependency_overrides.clear()
```


**Related concepts:** dependencies, mocking, fastapi



### Request Validation Testing

Test request body validation and error responses

```python
# Test request validation
def test_invalid_request_body():
    client = TestClient(app)
    response = client.post("/users", json={"invalid": "data"})
    assert response.status_code == 422
    assert "validation error" in response.json()["detail"][0]["msg"]

def test_missing_required_fields():
    client = TestClient(app)
    response = client.post("/users", json={})
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("field required" in error["msg"] for error in errors)
```


**Related concepts:** validation, errors, pydantic



### Response Model Testing

Test response models and serialization

```python
# Test response models
def test_response_model_serialization():
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 200
    
    user = response.json()
    # Verify all expected fields are present
    assert "id" in user
    assert "name" in user
    assert "email" in user
    assert "age" in user
    
    # Verify data types
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["email"], str)
```


**Related concepts:** serialization, models, pydantic



### Error Handling Testing

Test HTTP exceptions and error responses

```python
# Test error handling
def test_404_error():
    client = TestClient(app)
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_422_validation_error():
    client = TestClient(app)
    response = client.post("/users", json={"name": ""})  # Empty name
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("string too short" in error["msg"] for error in errors)
```


**Related concepts:** errors, exceptions, http



### API Endpoint Testing

Test FastAPI endpoints with proper request/response validation

```python
# Test FastAPI endpoints
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

# Use TestClient for synchronous testing
def test_get_endpoint():
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# Use AsyncClient for async testing
@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users/1")
        assert response.status_code == 200
```


**Related concepts:** api, endpoints, fastapi




## Usage Instructions

When generating tests, please follow these guidance patterns:

1. **Structure**: Follow the test structure patterns defined above
2. **Naming**: Use descriptive test names that explain the expected behavior
3. **Coverage**: Ensure comprehensive test coverage including edge cases
4. **Maintainability**: Write tests that are easy to read, understand, and maintain
5. **Best Practices**: Follow the specific best practices for the chosen framework

## Example Prompts

- "Generate unit tests for this Python function using pytest"
- "Create integration tests for this API endpoint"
- "Write end-to-end tests for this user flow using Playwright"
- "Generate contract tests for this service using Pact"

Remember to adapt these guidance patterns to the specific context and requirements of your project.