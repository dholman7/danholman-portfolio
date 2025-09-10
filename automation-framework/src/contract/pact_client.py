"""Pact contract testing client for consumer-driven contract testing."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from pact import Consumer, Provider, Like, EachLike, Term
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PactClient:
    """Client for managing Pact contract tests."""
    
    def __init__(self, consumer_name: str, provider_name: str, pact_dir: str = "pacts"):
        """Initialize Pact client.
        
        Args:
            consumer_name: Name of the consumer service
            provider_name: Name of the provider service
            pact_dir: Directory to store pact files
        """
        self.consumer_name = consumer_name
        self.provider_name = provider_name
        self.pact_dir = Path(pact_dir)
        self.pact_dir.mkdir(exist_ok=True)
        
        # Initialize Pact
        self.pact = Consumer(consumer_name).has_pact_with(Provider(provider_name))
        self.pact_dir = str(self.pact_dir)
        
    def start_service(self, port: int = 1234) -> None:
        """Start the Pact mock service.
        
        Args:
            port: Port for the mock service
        """
        # Set the port before starting
        self.pact.port = port
        self.pact.start_service()
        logger.info(f"Pact mock service started on port {port}")
        
    def stop_service(self) -> None:
        """Stop the Pact mock service."""
        try:
            self.pact.stop_service()
            logger.info("Pact mock service stopped")
        except Exception as e:
            logger.warning(f"Error stopping Pact mock service: {e}")
            # Don't raise the exception to avoid test failures
        
    def write_pact(self) -> None:
        """Write the pact file to disk."""
        self.pact.write_file(self.pact_dir)
        logger.info(f"Pact file written to {self.pact_dir}")
        
    def setup_interaction(self, 
                         description: str,
                         provider_state: str,
                         request: Dict[str, Any],
                         response: Dict[str, Any]) -> None:
        """Setup a contract interaction.
        
        Args:
            description: Description of the interaction
            provider_state: State the provider should be in
            request: Request specification
            response: Response specification
        """
        self.pact.given(provider_state).upon_receiving(description).with_request(
            method=request.get("method", "GET"),
            path=request.get("path", "/"),
            headers=request.get("headers", {}),
            body=request.get("body")
        ).will_respond_with(
            status=response.get("status", 200),
            headers=response.get("headers", {}),
            body=response.get("body")
        )
        logger.info(f"Contract interaction setup: {description}")
        
    def verify_contract(self) -> bool:
        """Verify the contract against the provider.
        
        Returns:
            True if verification successful, False otherwise
        """
        try:
            self.pact.verify()
            logger.info("Contract verification successful")
            return True
        except Exception as e:
            logger.error(f"Contract verification failed: {e}")
            return False


class MockExternalService:
    """Mock external service for contract testing."""
    
    def __init__(self, base_url: str = "http://localhost:1234"):
        """Initialize mock service.
        
        Args:
            base_url: Base URL of the mock service
        """
        self.base_url = base_url
        self.endpoints = {}
        
    def add_endpoint(self, path: str, method: str, response: Dict[str, Any]) -> None:
        """Add an endpoint to the mock service.
        
        Args:
            path: API endpoint path
            method: HTTP method
            response: Response data
        """
        key = f"{method.upper()}:{path}"
        self.endpoints[key] = response
        logger.info(f"Added mock endpoint: {key}")
        
    def get_user_endpoints(self) -> Dict[str, Any]:
        """Get user-related endpoints for contract testing."""
        return {
            "GET:/api/users": {
                "method": "GET",
                "path": "/api/users",
                "headers": {"Content-Type": "application/json"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "users": EachLike({
                            "id": Like(1),
                            "name": Like("John Doe"),
                            "email": Like("john@example.com"),
                            "active": Like(True)
                        }, minimum=1)
                    }
                }
            },
            "GET:/api/users/{id}": {
                "method": "GET",
                "path": Term(r"/api/users/\d+", "/api/users/123"),
                "headers": {"Content-Type": "application/json"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "id": Like(1),
                        "name": Like("John Doe"),
                        "email": Like("john@example.com"),
                        "active": Like(True)
                    }
                }
            },
            "POST:/api/users": {
                "method": "POST",
                "path": "/api/users",
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "name": Like("John Doe"),
                    "email": Like("john@example.com")
                },
                "response": {
                    "status": 201,
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "id": Like(1),
                        "name": Like("John Doe"),
                        "email": Like("john@example.com"),
                        "active": Like(True)
                    }
                }
            }
        }
        
    def get_product_endpoints(self) -> Dict[str, Any]:
        """Get product-related endpoints for contract testing."""
        return {
            "GET:/api/products": {
                "method": "GET",
                "path": "/api/products",
                "headers": {"Content-Type": "application/json"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "products": EachLike({
                            "id": Like(1),
                            "name": Like("Product Name"),
                            "price": Like(99.99),
                            "category": Like("Electronics"),
                            "in_stock": Like(True)
                        }, minimum=1)
                    }
                }
            },
            "GET:/api/products/{id}": {
                "method": "GET",
                "path": Term(r"/api/products/\d+", "/api/products/123"),
                "headers": {"Content-Type": "application/json"},
                "response": {
                    "status": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": {
                        "id": Like(1),
                        "name": Like("Product Name"),
                        "price": Like(99.99),
                        "category": Like("Electronics"),
                        "in_stock": Like(True)
                    }
                }
            }
        }
