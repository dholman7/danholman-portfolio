"""
Example of tests that would be generated using the FastAPI testing guidance.
This demonstrates how AI assistants would create tests following the guidance patterns.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import Mock
from sample_fastapi_app import app, get_db

client = TestClient(app)

class TestUserEndpoints:
    """Test user-related endpoints following FastAPI testing guidance."""
    
    def test_get_users_returns_all_users(self):
        """Test GET /users returns all users."""
        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 3
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
        assert user["age"] == 30
    
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
        assert response.status_code == 201
        user = response.json()
        assert user["name"] == "New User"
        assert user["email"] == "new@example.com"
        assert user["age"] == 28
        assert user["id"] == 4  # Next available ID
    
    def test_create_user_with_invalid_email_returns_422(self):
        """Test POST /users returns 422 for invalid email format."""
        invalid_data = {
            "name": "Invalid User",
            "email": "invalid-email-format"
        }
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
    
    def test_update_user_with_valid_data(self):
        """Test PUT /users/{id} updates user with valid data."""
        update_data = {
            "name": "Updated Name",
            "age": 31
        }
        response = client.put("/users/1", json=update_data)
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == "Updated Name"
        assert user["age"] == 31
        assert user["email"] == "john@example.com"  # Unchanged
    
    def test_update_nonexistent_user_returns_404(self):
        """Test PUT /users/{id} returns 404 for non-existent user."""
        update_data = {"name": "Updated Name"}
        response = client.put("/users/999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    
    def test_delete_user_returns_204(self):
        """Test DELETE /users/{id} deletes user and returns 204."""
        response = client.delete("/users/3")
        assert response.status_code == 204
        
        # Verify user is deleted
        response = client.get("/users/3")
        assert response.status_code == 404
    
    def test_delete_nonexistent_user_returns_404(self):
        """Test DELETE /users/{id} returns 404 for non-existent user."""
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

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

class TestResponseModelSerialization:
    """Test response models and serialization following guidance patterns."""
    
    def test_response_model_serialization(self):
        """Test response model serialization."""
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
        assert isinstance(user["age"], int)
    
    def test_create_user_response_model(self):
        """Test create user response model."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "age": 25
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 201
        
        user = response.json()
        # Verify response model structure
        assert "id" in user
        assert user["name"] == "Test User"
        assert user["email"] == "test@example.com"
        assert user["age"] == 25

class TestErrorHandling:
    """Test error handling following guidance patterns."""
    
    def test_404_error(self):
        """Test 404 error response."""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
    
    def test_422_validation_error(self):
        """Test 422 validation error response."""
        response = client.post("/users", json={"name": ""})  # Empty name
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("string too short" in error["msg"] for error in errors)
    
    def test_invalid_json_returns_422(self):
        """Test invalid JSON returns 422."""
        response = client.post("/users", json={"invalid": "data"})
        assert response.status_code == 422

@pytest.mark.asyncio
class TestAsyncEndpoints:
    """Test async endpoints using AsyncClient following guidance patterns."""
    
    async def test_async_user_retrieval(self):
        """Test async user retrieval."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/users/1")
            assert response.status_code == 200
            user = response.json()
            assert user["id"] == 1
            assert user["name"] == "John Doe"
    
    async def test_async_user_creation(self):
        """Test async user creation."""
        user_data = {
            "name": "Async User",
            "email": "async@example.com",
            "age": 30
        }
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/users", json=user_data)
            assert response.status_code == 201
            user = response.json()
            assert user["name"] == "Async User"

class TestRootEndpoint:
    """Test root endpoint following guidance patterns."""
    
    def test_root_endpoint_returns_api_info(self):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User Management API"
        assert data["version"] == "1.0.0"

# Integration tests
class TestUserWorkflow:
    """Test complete user workflow following guidance patterns."""
    
    def test_complete_user_crud_workflow(self):
        """Test complete CRUD workflow for users."""
        # Create user
        user_data = {
            "name": "Workflow User",
            "email": "workflow@example.com",
            "age": 30
        }
        create_response = client.post("/users", json=user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        user_id = created_user["id"]
        
        # Read user
        read_response = client.get(f"/users/{user_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Workflow User"
        
        # Update user
        update_data = {"name": "Updated Workflow User"}
        update_response = client.put(f"/users/{user_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Workflow User"
        
        # Delete user
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204
        
        # Verify deletion
        verify_response = client.get(f"/users/{user_id}")
        assert verify_response.status_code == 404

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
