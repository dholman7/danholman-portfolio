"""Contract tests for User Service API using Pact v3."""

import pytest
import requests
from typing import Any, Dict, cast
from src.contract import PactClient, MockExternalService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TestUserServiceContract:
    """Contract tests for User Service consumer."""
    
    @pytest.fixture(scope="class")
    def pact_client(self):
        """Create Pact client for User Service."""
        client = PactClient("user-service-consumer", "user-service-provider")
        yield client
        client.stop_service()
        
    @pytest.fixture(scope="class")
    def mock_service(self):
        """Create mock external service."""
        return MockExternalService("http://localhost:1234")
        
    @pytest.fixture(scope="class")
    def user_endpoints(self, mock_service):
        """Get user service endpoints."""
        return mock_service.get_user_endpoints()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_get_users_contract(self, pact_client, user_endpoints):
        """Test contract for getting all users."""
        # Setup contract interaction
        endpoint_config = user_endpoints["GET:/api/users"]
        request = {
            "method": endpoint_config["method"],
            "path": endpoint_config["path"],
            "headers": endpoint_config["headers"]
        }
        response = endpoint_config["response"]
        
        pact_client.setup_interaction(
            description="Get all users",
            provider_state="users exist",
            request=request,
            response=response
        )
        
        # Start mock service
        pact_client.start_service(port=1234)
        
        try:
            # Setup the interaction
            pact_client.pact.setup()
            
            # Make actual request to mock service
            response = requests.get("http://localhost:1234/api/users", headers={"Content-Type": "application/json"})
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert "users" in data
            assert isinstance(data["users"], list)
            assert len(data["users"]) >= 1
            
            # Verify user structure
            user = data["users"][0]
            assert "id" in user
            assert "name" in user
            assert "email" in user
            assert "active" in user
            
            logger.info("GET /api/users contract test passed")
        finally:
            # Stop the service
            pact_client.stop_service()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_get_user_by_id_contract(self, pact_client, user_endpoints):
        """Test contract for getting user by ID."""
        # Setup contract interaction
        endpoint_config = user_endpoints["GET:/api/users/{id}"]
        request = {
            "method": endpoint_config["method"],
            "path": endpoint_config["path"],
            "headers": endpoint_config["headers"]
        }
        response = endpoint_config["response"]
        
        pact_client.setup_interaction(
            description="Get user by ID",
            provider_state="user with ID 123 exists",
            request=request,
            response=response
        )
        
        # Start mock service
        pact_client.start_service(port=1235)
        
        try:
            # Setup the interaction
            pact_client.pact.setup()
            
            # Make actual request to mock service
            response = requests.get("http://localhost:1235/api/users/123", headers={"Content-Type": "application/json"})
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert "id" in data
            assert "name" in data
            assert "email" in data
            assert "active" in data
            
            logger.info("GET /api/users/{id} contract test passed")
        finally:
            # Stop the service
            pact_client.stop_service()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_create_user_contract(self, pact_client, user_endpoints):
        """Test contract for creating a new user."""
        # Setup contract interaction
        endpoint_config = user_endpoints["POST:/api/users"]
        request = {
            "method": endpoint_config["method"],
            "path": endpoint_config["path"],
            "headers": endpoint_config["headers"],
            "body": endpoint_config["body"]
        }
        response = endpoint_config["response"]
        
        pact_client.setup_interaction(
            description="Create new user",
            provider_state="user can be created",
            request=request,
            response=response
        )
        
        # Start mock service
        pact_client.start_service(port=1236)
        
        try:
            # Setup the interaction
            pact_client.pact.setup()
            
            # Make actual request to mock service
            user_data = {
                "name": "Jane Doe",
                "email": "jane@example.com"
            }
            response = requests.post(
                "http://localhost:1236/api/users",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )
            
            # Verify response
            assert response.status_code == 201
            data = response.json()
            assert "id" in data
            assert data["name"] == "Jane Doe"
            assert data["email"] == "jane@example.com"
            assert "active" in data
            
            logger.info("POST /api/users contract test passed")
        finally:
            # Stop the service
            pact_client.stop_service()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_user_service_contract_verification(self, pact_client):
        """Verify the complete user service contract."""
        # Setup all interactions
        user_endpoints = MockExternalService().get_user_endpoints()
        
        for endpoint_name, config in user_endpoints.items():
            request = {
                "method": config["method"],
                "path": config["path"],
                "headers": config.get("headers", {}),
                "body": config.get("body")
            }
            response = config["response"]
            
            pact_client.setup_interaction(
                description=f"Contract for {endpoint_name}",
                provider_state=f"Service ready for {endpoint_name}",
                request=request,
                response=response
            )
        
        # Start service and verify
        pact_client.start_service(port=1237)
        
        try:
            # Verify contract
            verification_result = pact_client.verify_contract()
            assert verification_result, "Contract verification failed"
            
            # Write pact file
            pact_client.write_pact()
            
            logger.info("User service contract verification completed successfully")
        finally:
            # Stop the service
            pact_client.stop_service()
