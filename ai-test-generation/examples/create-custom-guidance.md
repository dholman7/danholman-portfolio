# Creating Custom Guidance Templates

This example shows how to create a new guidance template and use it to generate tests.

## Part A: Creating a New Guidance Template

### 1. Define Your Guidance Template

Create a new guidance template for a specific testing scenario:

```python
from ai_test_generation.core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem

# Create metadata for your custom guidance
metadata = GuidanceTemplateMetadata(
    name="FastAPI Testing Guidance",
    version="1.0.0",
    description="Comprehensive guidance for testing FastAPI applications",
    languages=["python"],
    frameworks=["fastapi", "pytest", "httpx"],
    categories=["api", "integration", "unit"],
    author="Your Name",
    license="MIT"
)

# Create the guidance template
template = GuidanceTemplate(metadata=metadata)

# Add guidance items
template.add_guidance(GuidanceItem(
    name="API Endpoint Testing",
    description="Test FastAPI endpoints with proper request/response validation",
    content="""# Test FastAPI endpoints
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
        assert response.status_code == 200""",
    tags=["api", "endpoints", "fastapi"],
    priority=1
))

template.add_guidance(GuidanceItem(
    name="Dependency Injection Testing",
    description="Test FastAPI dependencies and dependency overrides",
    content="""# Test FastAPI dependencies
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
    app.dependency_overrides.clear()""",
    tags=["dependencies", "mocking", "fastapi"],
    priority=2
))

template.add_guidance(GuidanceItem(
    name="Request Validation Testing",
    description="Test request body validation and error responses",
    content="""# Test request validation
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
    assert any("field required" in error["msg"] for error in errors)""",
    tags=["validation", "errors", "pydantic"],
    priority=2
))

# Save the template to a file
template.save_to_file("fastapi-testing-guidance.yaml")
```

### 2. Generate AI Assistant Guidance

Use the CLI to generate guidance files for different AI tools:

```bash
# Generate Cursor guidance
ai-test-gen generate cursor --type custom --output .cursor/rules

# Generate GitHub Copilot guidance  
ai-test-gen generate copilot --type custom --output .github/instructions
```

Or programmatically:

```python
from ai_test_generation.renderers import CursorRenderer, CopilotRenderer

# Render for Cursor
cursor_renderer = CursorRenderer()
cursor_guidance = cursor_renderer.render(template, language="python")
with open(".cursor/rules/fastapi-testing-guidance.mdc", "w") as f:
    f.write(cursor_guidance)

# Render for GitHub Copilot
copilot_renderer = CopilotRenderer()
copilot_guidance = copilot_renderer.render(template, language="python")
with open(".github/instructions/fastapi-testing-guidance.instructions.md", "w") as f:
    f.write(copilot_guidance)
```

## Part B: Creating Tests Based on the Guidance

### 1. Example FastAPI Application

First, let's create a simple FastAPI app to test:

```python
# app.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

# Mock database
users_db = [
    User(id=1, name="John Doe", email="john@example.com", age=30),
    User(id=2, name="Jane Smith", email="jane@example.com", age=25)
]

def get_db():
    """Mock database dependency"""
    return users_db

@app.get("/users", response_model=List[User])
async def get_users(db: List[User] = Depends(get_db)):
    return db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: List[User] = Depends(get_db)):
    user = next((u for u in db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
async def create_user(user: UserCreate, db: List[User] = Depends(get_db)):
    new_id = max(u.id for u in db) + 1
    new_user = User(id=new_id, **user.dict())
    db.append(new_user)
    return new_user
```

### 2. Generate Tests Using AI Assistant

With the guidance files in place, you can now ask your AI assistant to generate tests:

#### **For Cursor:**
1. Open Cursor in your project directory
2. The guidance will be automatically loaded from `.cursor/rules/`
3. Ask Cursor: "Generate comprehensive tests for this FastAPI application following the FastAPI testing guidance"

#### **For GitHub Copilot:**
1. Place the guidance file in `.github/instructions/`
2. Start typing test code and let Copilot suggest completions
3. Copilot will follow the guidance patterns

### 3. Example Generated Tests

Based on the guidance, here's what the AI assistant might generate:

```python
# test_app.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock
from app import app, get_db

client = TestClient(app)

class TestUserEndpoints:
    """Test user-related endpoints following FastAPI testing guidance."""
    
    def test_get_users_returns_all_users(self):
        """Test GET /users returns all users."""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2
        assert users[0]["id"] == 1
        assert users[0]["name"] == "John Doe"
    
    def test_get_user_by_id_returns_specific_user(self):
        """Test GET /users/{id} returns specific user."""
        response = client.get("/users/1")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == 1
        assert user["name"] == "John Doe"
        assert user["email"] == "john@example.com"
    
    def test_get_user_by_id_returns_404_for_nonexistent_user(self):
        """Test GET /users/{id} returns 404 for non-existent user."""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    
    def test_create_user_with_valid_data(self):
        """Test POST /users creates user with valid data."""
        user_data = {
            "name": "New User",
            "email": "new@example.com",
            "age": 28
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == "New User"
        assert user["email"] == "new@example.com"
        assert user["age"] == 28
        assert user["id"] == 3  # Next available ID
    
    def test_create_user_with_invalid_data_returns_422(self):
        """Test POST /users returns 422 for invalid data."""
        invalid_data = {"invalid": "data"}
        response = client.post("/users", json=invalid_data)
        assert response.status_code == 422
        assert "validation error" in str(response.json())
    
    def test_create_user_with_missing_required_fields_returns_422(self):
        """Test POST /users returns 422 for missing required fields."""
        incomplete_data = {"name": "Incomplete User"}
        response = client.post("/users", json=incomplete_data)
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("field required" in error["msg"] for error in errors)

class TestDependencyInjection:
    """Test FastAPI dependencies following guidance patterns."""
    
    def test_with_dependency_override(self):
        """Test endpoint with dependency override."""
        # Override the database dependency
        def override_get_db():
            return [
                {"id": 1, "name": "Mock User", "email": "mock@example.com", "age": 30}
            ]
        
        app.dependency_overrides[get_db] = override_get_db
        
        try:
            response = client.get("/users")
            assert response.status_code == 200
            users = response.json()
            assert len(users) == 1
            assert users[0]["name"] == "Mock User"
        finally:
            # Clean up dependency override
            app.dependency_overrides.clear()

@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Test async endpoints using AsyncClient."""
    
    async def test_async_user_retrieval(self):
        """Test async user retrieval."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/users/1")
            assert response.status_code == 200
            user = response.json()
            assert user["id"] == 1
            assert user["name"] == "John Doe"
```

### 4. Running the Tests

```bash
# Install dependencies
pip install fastapi pytest httpx

# Run the tests
pytest test_app.py -v

# Run with coverage
pytest test_app.py --cov=app --cov-report=html
```

## Key Benefits

1. **Consistent Patterns**: All tests follow the same structure and patterns
2. **Comprehensive Coverage**: Tests cover happy path, error cases, and edge cases
3. **Maintainable**: Clear naming and organization make tests easy to understand
4. **AI-Generated**: Tests are generated following your specific guidance patterns
5. **Customizable**: You can modify the guidance template to match your team's preferences

## Next Steps

1. **Customize the guidance** to match your team's specific testing patterns
2. **Add more guidance items** for different testing scenarios
3. **Create templates for other frameworks** (Django, Flask, etc.)
4. **Integrate with CI/CD** to automatically generate and run tests
5. **Share templates** across your organization for consistency
