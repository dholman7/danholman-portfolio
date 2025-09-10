"""Contract tests for Product Service API using Pact v3."""

import pytest
import requests
from typing import Any, Dict, cast
from src.contract import PactClient, MockExternalService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class TestProductServiceContract:
    """Contract tests for Product Service consumer."""
    
    @pytest.fixture(scope="class")
    def pact_client(self):
        """Create Pact client for Product Service."""
        client = PactClient("product-service-consumer", "product-service-provider")
        yield client
        client.stop_service()
        
    @pytest.fixture(scope="class")
    def mock_service(self):
        """Create mock external service."""
        return MockExternalService("http://localhost:1234")
        
    @pytest.fixture(scope="class")
    def product_endpoints(self, mock_service):
        """Get product service endpoints."""
        return mock_service.get_product_endpoints()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_get_products_contract(self, pact_client, product_endpoints):
        """Test contract for getting all products."""
        # Setup contract interaction
        endpoint_config = product_endpoints["GET:/api/products"]
        request = {
            "method": endpoint_config["method"],
            "path": endpoint_config["path"],
            "headers": endpoint_config["headers"]
        }
        response = endpoint_config["response"]
        
        pact_client.setup_interaction(
            description="Get all products",
            provider_state="products exist",
            request=request,
            response=response
        )
        
        # Start mock service
        pact_client.start_service(port=1238)
        
        try:
            # Setup the interaction
            pact_client.pact.setup()
            
            # Make actual request to mock service
            response = requests.get("http://localhost:1238/api/products", headers={"Content-Type": "application/json"})
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert "products" in data
            assert isinstance(data["products"], list)
            assert len(data["products"]) >= 1
            
            # Verify product structure
            product = data["products"][0]
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "category" in product
            assert "in_stock" in product
            
            logger.info("GET /api/products contract test passed")
        finally:
            # Stop the service
            pact_client.stop_service()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_get_product_by_id_contract(self, pact_client, product_endpoints):
        """Test contract for getting product by ID."""
        # Setup contract interaction
        endpoint_config = product_endpoints["GET:/api/products/{id}"]
        request = {
            "method": endpoint_config["method"],
            "path": endpoint_config["path"],
            "headers": endpoint_config["headers"]
        }
        response = endpoint_config["response"]
        
        pact_client.setup_interaction(
            description="Get product by ID",
            provider_state="product with ID 123 exists",
            request=request,
            response=response
        )
        
        # Start mock service
        pact_client.start_service(port=1239)
        
        try:
            # Setup the interaction
            pact_client.pact.setup()
            
            # Make actual request to mock service
            response = requests.get("http://localhost:1239/api/products/123", headers={"Content-Type": "application/json"})
            
            # Verify response
            assert response.status_code == 200
            data = response.json()
            assert "id" in data
            assert "name" in data
            assert "price" in data
            assert "category" in data
            assert "in_stock" in data
            
            logger.info("GET /api/products/{id} contract test passed")
        finally:
            # Stop the service
            pact_client.stop_service()
        
    @pytest.mark.contract
    @pytest.mark.pact
    def test_product_service_contract_verification(self, pact_client):
        """Verify the complete product service contract."""
        # Setup all interactions
        product_endpoints = MockExternalService().get_product_endpoints()
        
        for endpoint_name, config in product_endpoints.items():
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
        pact_client.start_service(port=1240)
        
        try:
            # Verify contract
            verification_result = pact_client.verify_contract()
            assert verification_result, "Contract verification failed"
            
            # Write pact file
            pact_client.write_pact()
            
            logger.info("Product service contract verification completed successfully")
        finally:
            # Stop the service
            pact_client.stop_service()
