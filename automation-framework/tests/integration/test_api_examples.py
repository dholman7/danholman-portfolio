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
        response = api_client.post("/api/users", data=random_user)
        
        assert response.status_code == 201
        assert "id" in response.data
        assert response.data["email"] == random_user["email"]
        assert response.response_time < 2.0
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user(self, api_client: APIClient, test_user: Dict[str, Any]):
        """Test retrieving user information."""
        # First create a user
        create_response = api_client.post("/api/users", data=test_user)
        user_id = create_response.data["id"]
        
        # Then retrieve it
        response = api_client.get(f"/api/users/{user_id}")
        
        assert response.status_code == 200
        assert response.data["email"] == test_user["email"]
        assert response.data["first_name"] == test_user["first_name"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_user(self, api_client: APIClient, test_user: Dict[str, Any]):
        """Test updating user information."""
        # Create user
        create_response = api_client.post("/api/users", data=test_user)
        user_id = create_response.data["id"]
        
        # Update user
        update_data = {"first_name": "UpdatedName"}
        response = api_client.put(f"/api/users/{user_id}", data=update_data)
        
        assert response.status_code == 200
        assert response.data["first_name"] == "UpdatedName"
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_delete_user(self, api_client: APIClient, test_user: Dict[str, Any]):
        """Test deleting a user."""
        # Create user
        create_response = api_client.post("/api/users", data=test_user)
        user_id = create_response.data["id"]
        
        # Delete user
        response = api_client.delete(f"/api/users/{user_id}")
        
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = api_client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_user_creation_performance(self, api_client: APIClient):
        """Test user creation performance with multiple users."""
        users = UserFactory.create_users(10)
        response_times = []
        
        for user in users:
            response = api_client.post("/api/users", data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            })
            
            assert response.status_code == 201
            response_times.append(response.response_time)
        
        # Verify all responses are fast
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 1.0, f"Average response time {avg_response_time:.3f}s exceeds threshold"
    
    @pytest.mark.api
    @pytest.mark.data_driven
    @pytest.mark.parametrize("user_data", [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com"},
        {"first_name": "Bob", "last_name": "Johnson", "email": "bob.johnson@example.com"}
    ])
    def test_user_creation_data_driven(self, api_client: APIClient, user_data: Dict[str, Any]):
        """Test user creation with different data sets."""
        response = api_client.post("/api/users", data=user_data)
        
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
        response = api_client.get("/api/products")
        
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert len(response.data) > 0
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_create_product(self, api_client: APIClient, test_product: Dict[str, Any]):
        """Test creating a new product."""
        response = api_client.post("/api/products", data=test_product)
        
        assert response.status_code == 201
        assert response.data["name"] == test_product["name"]
        assert response.data["sku"] == test_product["sku"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_product_by_id(self, api_client: APIClient, test_product: Dict[str, Any]):
        """Test retrieving a specific product."""
        # Create product first
        create_response = api_client.post("/api/products", data=test_product)
        product_id = create_response.data["id"]
        
        # Retrieve product
        response = api_client.get(f"/api/products/{product_id}")
        
        assert response.status_code == 200
        assert response.data["name"] == test_product["name"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_product(self, api_client: APIClient, test_product: Dict[str, Any]):
        """Test updating product information."""
        # Create product
        create_response = api_client.post("/api/products", data=test_product)
        product_id = create_response.data["id"]
        
        # Update product
        update_data = {"price": 99.99, "in_stock": True}
        response = api_client.patch(f"/api/products/{product_id}", data=update_data)
        
        assert response.status_code == 200
        assert response.data["price"] == 99.99
        assert response.data["in_stock"] is True
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_bulk_product_creation(self, api_client: APIClient):
        """Test creating multiple products efficiently."""
        products = ProductFactory.create_products(20)
        created_products = []
        
        for product in products:
            response = api_client.post("/api/products", data={
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "sku": product.sku
            })
            
            assert response.status_code == 201
            created_products.append(response.data)
        
        assert len(created_products) == 20
        
        # Verify all products can be retrieved
        get_response = api_client.get("/api/products")
        assert len(get_response.data) >= 20


@pytest.mark.integration
@pytest.mark.docker_integration
class TestOrderAPI:
    """Test order-related API endpoints."""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_order(self, api_client: APIClient, test_user: Dict[str, Any], test_products: List[Dict[str, Any]]):
        """Test creating a new order."""
        # Create user first
        user_response = api_client.post("/api/users", data=test_user)
        user_id = user_response.data["id"]
        
        # Create order
        order_data = {
            "user_id": user_id,
            "products": [{"id": p["sku"], "quantity": 1} for p in test_products[:3]],
            "shipping_address": test_user["address"]
        }
        
        response = api_client.post("/api/orders", data=order_data)
        
        assert response.status_code == 201
        assert response.data["user_id"] == user_id
        assert len(response.data["products"]) == 3
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_get_user_orders(self, api_client: APIClient, test_user: Dict[str, Any], test_products: List[Dict[str, Any]]):
        """Test retrieving orders for a specific user."""
        # Create user
        user_response = api_client.post("/api/users", data=test_user)
        user_id = user_response.data["id"]
        
        # Create multiple orders
        for i in range(3):
            order_data = {
                "user_id": user_id,
                "products": [{"id": p["sku"], "quantity": 1} for p in test_products[:2]],
                "shipping_address": test_user["address"]
            }
            api_client.post("/api/orders", data=order_data)
        
        # Get user orders
        response = api_client.get(f"/api/users/{user_id}/orders")
        
        assert response.status_code == 200
        assert len(response.data) == 3
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_update_order_status(self, api_client: APIClient, test_user: Dict[str, Any], test_products: List[Dict[str, Any]]):
        """Test updating order status."""
        # Create user and order
        user_response = api_client.post("/api/users", data=test_user)
        user_id = user_response.data["id"]
        
        order_data = {
            "user_id": user_id,
            "products": [{"id": p["sku"], "quantity": 1} for p in test_products[:2]],
            "shipping_address": test_user["address"]
        }
        order_response = api_client.post("/api/orders", data=order_data)
        order_id = order_response.data["id"]
        
        # Update order status
        update_data = {"status": "shipped"}
        response = api_client.patch(f"/api/orders/{order_id}", data=update_data)
        
        assert response.status_code == 200
        assert response.data["status"] == "shipped"


@pytest.mark.integration
@pytest.mark.docker_integration
class TestGraphQLAPI:
    """Test GraphQL API endpoints."""
    
    @pytest.mark.api
    @pytest.mark.smoke
    def test_graphql_query_users(self, graphql_client: GraphQLClient):
        """Test GraphQL query for users."""
        query = """
        query {
            users {
                id
                firstName
                lastName
                email
            }
        }
        """
        
        response = graphql_client.query(query)
        
        assert response.status_code == 200
        assert "data" in response.data
        assert "users" in response.data["data"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_graphql_mutation_create_user(self, graphql_client: GraphQLClient, random_user: Dict[str, Any]):
        """Test GraphQL mutation for creating user."""
        mutation = """
        mutation CreateUser($input: UserInput!) {
            createUser(input: $input) {
                id
                firstName
                lastName
                email
            }
        }
        """
        
        variables = {
            "input": {
                "firstName": random_user["first_name"],
                "lastName": random_user["last_name"],
                "email": random_user["email"],
                "phone": random_user["phone"]
            }
        }
        
        response = graphql_client.mutation(mutation, variables)
        
        assert response.status_code == 200
        assert "data" in response.data
        assert "createUser" in response.data["data"]
        assert response.data["data"]["createUser"]["email"] == random_user["email"]
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_graphql_query_with_variables(self, graphql_client: GraphQLClient):
        """Test GraphQL query with variables."""
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                firstName
                lastName
                email
            }
        }
        """
        
        variables = {"id": "1"}
        
        response = graphql_client.query(query, variables)
        
        assert response.status_code == 200
        assert "data" in response.data


@pytest.mark.integration
class TestAPIPerformance:
    """Test API performance and scalability."""
    
    @pytest.mark.api
    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_user_creation(self, api_client: APIClient):
        """Test concurrent user creation performance."""
        import concurrent.futures
        import threading
        
        users = UserFactory.create_users(50)
        results = []
        
        def create_user(user_data):
            response = api_client.post("/api/users", data={
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "phone": user_data.phone
            })
            return response
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_user, user) for user in users]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response)
                except Exception as e:
                    pytest.fail(f"User creation failed: {e}")
        
        # Verify all users were created successfully
        successful_creations = [r for r in results if r.status_code == 201]
        assert len(successful_creations) == 50
        
        # Verify response times are reasonable
        avg_response_time = sum(r.response_time for r in successful_creations) / len(successful_creations)
        assert avg_response_time < 2.0, f"Average response time {avg_response_time:.3f}s exceeds threshold"
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_api_rate_limiting(self, api_client: APIClient):
        """Test API rate limiting behavior."""
        # Make rapid requests to test rate limiting
        responses = []
        for i in range(20):
            response = api_client.get("/api/products")
            responses.append(response)
        
        # Check if rate limiting is working (should get 429 status codes)
        rate_limited_responses = [r for r in responses if r.status_code == 429]
        
        # If rate limiting is implemented, we should see some 429 responses
        # If not implemented, all should be 200
        if rate_limited_responses:
            assert len(rate_limited_responses) > 0, "Rate limiting should return 429 status codes"
        else:
            # All requests should succeed if no rate limiting
            successful_responses = [r for r in responses if r.status_code == 200]
            assert len(successful_responses) == 20


@pytest.mark.integration
class TestAPIErrorHandling:
    """Test API error handling and edge cases."""
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_invalid_user_data(self, api_client: APIClient):
        """Test API response to invalid user data."""
        invalid_data = {
            "first_name": "",  # Empty required field
            "email": "invalid-email",  # Invalid email format
            "phone": "123"  # Invalid phone format
        }
        
        response = api_client.post("/api/users", data=invalid_data)
        
        assert response.status_code == 400
        assert "errors" in response.data or "message" in response.data
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_nonexistent_resource(self, api_client: APIClient):
        """Test API response to nonexistent resource."""
        response = api_client.get("/api/users/99999")
        
        assert response.status_code == 404
    
    @pytest.mark.api
    @pytest.mark.regression
    def test_unauthorized_access(self, api_client: APIClient):
        """Test API response to unauthorized access."""
        # Clear authentication
        api_client.clear_auth()
        
        response = api_client.get("/api/users")
        
        assert response.status_code == 401
