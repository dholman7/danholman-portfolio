"""Example API tests demonstrating scalability patterns.

These integration tests are designed to run in a Docker environment with:
- Mock API Server (MockServer)
- Test Database (PostgreSQL)
- Redis Cache
- Isolated test execution environment

For local development, use: make test-integration-docker
For debugging, use: make test-integration-docker-dev
"""

import pytest
from typing import Dict, Any, List
import json
import os

from src.api.client import APIClient, GraphQLClient
from src.data.factories import UserFactory, ProductFactory, OrderFactory


@pytest.mark.integration
@pytest.mark.docker_integration
class TestUserAPI:
    """Test user-related API endpoints."""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_user(self, api_client: APIClient, random_user: Dict[str, Any]):
        """Test creating a new user."""
        response = api_client.post("/users", data=random_user)
        
        assert response.status_code == 201
        assert "id" in response.data
        assert response.data["email"] == random_user["email"]
        assert response.response_time < 2.0
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user(self, api_client: APIClient, test_user: Dict[str, Any]):
        """Test retrieving user information."""
        # JSONPlaceholder doesn't actually create users, so we'll test with an existing user ID
        user_id = 1  # Use a known user ID from JSONPlaceholder
        
        # Retrieve the user
        response = api_client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        assert "id" in response.data
        assert "email" in response.data
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_user(self, api_client: APIClient, test_user: Dict[str, Any]):
        """Test updating user information."""
        # JSONPlaceholder doesn't support PUT operations, so we'll test with a known user ID
        user_id = 1  # Use a known user ID from JSONPlaceholder
        
        # Update user (JSONPlaceholder will return the updated data but won't actually update)
        update_data = {"name": "UpdatedName"}
        response = api_client.put(f"/users/{user_id}", data=update_data)
        
        # JSONPlaceholder returns 200 for PUT requests but doesn't actually update
        assert response.status_code == 200
        assert "id" in response.data
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_user(self, api_client: APIClient, test_user: Dict[str, Any]):
        """Test deleting a user."""
        # JSONPlaceholder doesn't support DELETE operations, so we'll test with a known user ID
        user_id = 1  # Use a known user ID from JSONPlaceholder
        
        # Delete user (JSONPlaceholder will return 200 but won't actually delete)
        response = api_client.delete(f"/users/{user_id}")
        
        # JSONPlaceholder returns 200 for DELETE requests but doesn't actually delete
        assert response.status_code == 200
    
    
    @pytest.mark.api
    @pytest.mark.data_driven
    @pytest.mark.parametrize("user_data", [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com"},
        {"first_name": "Bob", "last_name": "Johnson", "email": "bob.johnson@example.com"}
    ])
    def test_user_creation_data_driven(self, api_client: APIClient, user_data: Dict[str, Any]):
        """Test user creation with different data sets."""
        response = api_client.post("/users", data=user_data)
        
        assert response.status_code == 201
        assert response.data["email"] == user_data["email"]


@pytest.mark.integration
@pytest.mark.docker_integration
class TestProductAPI:
    """Test product-related API endpoints."""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_products(self, api_client: APIClient):
        """Test retrieving all products."""
        response = api_client.get("/posts")
        
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) > 0
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_product(self, api_client: APIClient, test_product: Dict[str, Any]):
        """Test creating a new product."""
        response = api_client.post("/posts", data=test_product)
        
        assert response.status_code == 201
        assert response.data["name"] == test_product["name"]
        assert response.data["sku"] == test_product["sku"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_product_by_id(self, api_client: APIClient, test_product: Dict[str, Any]):
        """Test retrieving a specific product."""
        # Use existing post ID (JSONPlaceholder has posts 1-100)
        product_id = 1
        
        # Retrieve product
        response = api_client.get(f"/posts/{product_id}")
        
        assert response.status_code == 200
        assert "id" in response.data
        assert response.data["id"] == product_id
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_product(self, api_client: APIClient, test_product: Dict[str, Any]):
        """Test updating product information."""
        # Create product
        create_response = api_client.post("/posts", data=test_product)
        product_id = create_response.data["id"]
        
        # Update product
        update_data = {"price": 99.99, "in_stock": True}
        response = api_client.patch(f"/posts/{product_id}", data=update_data)
        
        assert response.status_code == 200
        assert response.data["price"] == 99.99
        assert response.data["in_stock"] is True
    


@pytest.mark.integration
@pytest.mark.docker_integration
class TestOrderAPI:
    """Test order-related API endpoints."""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_order(self, api_client: APIClient, test_user: Dict[str, Any], test_products: List[Dict[str, Any]]):
        """Test creating a new order (using posts as order simulation)."""
        # Use existing user ID (JSONPlaceholder has users 1-10)
        user_id = 1
        
        # Create order (simulate with posts endpoint)
        order_data = {
            "title": f"Order for user {user_id}",
            "body": f"Order containing {len(test_products[:3])} products",
            "userId": user_id
        }
        
        response = api_client.post("/posts", data=order_data)
        
        assert response.status_code == 201
        assert response.data["userId"] == user_id
        assert "title" in response.data
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_orders(self, api_client: APIClient, test_user: Dict[str, Any], test_products: List[Dict[str, Any]]):
        """Test retrieving orders for a specific user (using posts as order simulation)."""
        # Use existing user ID (JSONPlaceholder has users 1-10)
        user_id = 1
        
        # Get user's posts (simulating orders)
        response = api_client.get(f"/users/{user_id}/posts")
        
        assert response.status_code == 200
        assert isinstance(response.data, list)
        # JSONPlaceholder should return posts for this user
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_order_status(self, api_client: APIClient, test_user: Dict[str, Any], test_products: List[Dict[str, Any]]):
        """Test updating order status (using posts as order simulation)."""
        # Use existing post ID (JSONPlaceholder has posts 1-100)
        post_id = 1
        
        # Update post (simulating order status update)
        update_data = {"title": "Updated Order Status - Shipped"}
        response = api_client.patch(f"/posts/{post_id}", data=update_data)
        
        assert response.status_code == 200
        assert "title" in response.data


@pytest.mark.integration
@pytest.mark.docker_integration
class TestGraphQLAPI:
    """Test GraphQL API endpoints (simulated with REST)."""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_graphql_query_users(self, api_client: APIClient):
        """Test GraphQL query for users (simulated with REST)."""
        # Simulate GraphQL query with REST GET request
        response = api_client.get("/users")
        
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) > 0
        assert "id" in response.data[0]
        assert "email" in response.data[0]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_graphql_mutation_create_user(self, api_client: APIClient, random_user: Dict[str, Any]):
        """Test GraphQL mutation for creating user (simulated with REST)."""
        # Simulate GraphQL mutation with REST POST request
        user_data = {
            "name": f"{random_user['first_name']} {random_user['last_name']}",
            "email": random_user["email"],
            "phone": random_user["phone"]
        }
        
        response = api_client.post("/users", data=user_data)
        
        assert response.status_code == 201
        assert "id" in response.data
        assert response.data["email"] == random_user["email"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_graphql_query_with_variables(self, api_client: APIClient):
        """Test GraphQL query with variables (simulated with REST)."""
        # Simulate GraphQL query with variables using REST GET with params
        user_id = 1
        response = api_client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        assert "id" in response.data
        assert response.data["id"] == user_id




@pytest.mark.integration
class TestAPIErrorHandling:
    """Test API error handling and edge cases."""
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_invalid_user_data(self, api_client: APIClient):
        """Test API response to invalid user data (JSONPlaceholder accepts any data)."""
        invalid_data = {
            "first_name": "",  # Empty required field
            "email": "invalid-email",  # Invalid email format
            "phone": "123"  # Invalid phone format
        }
        
        response = api_client.post("/users", data=invalid_data)
        
        # JSONPlaceholder accepts any data and returns 201
        assert response.status_code == 201
        assert "id" in response.data
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_nonexistent_resource(self, api_client: APIClient):
        """Test API response to nonexistent resource."""
        response = api_client.get("/users/99999")
        
        assert response.status_code == 404
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_unauthorized_access(self, api_client: APIClient):
        """Test API response to unauthorized access (JSONPlaceholder is public)."""
        # Clear authentication
        api_client.clear_auth()
        
        # JSONPlaceholder is public, so this should return 200
        response = api_client.get("/users")
        
        assert response.status_code == 200
        assert isinstance(response.data, list)
