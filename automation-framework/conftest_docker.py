"""Docker-specific pytest configuration and fixtures for integration tests."""

import pytest
import os
import time
import requests
from typing import Generator, Dict, Any
from pathlib import Path

from src.config.settings import config
from src.api.client import APIClient, GraphQLClient
from src.data.factories import DataManager, UserFactory, ProductFactory, OrderFactory
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Docker-specific configuration
DOCKER_CONFIG = {
    "api_base_url": os.getenv("API_BASE_URL", "http://mock-api:1080"),
    "database_url": os.getenv("DATABASE_URL", "postgresql://test_user:test_password@test-db:5432/test_automation"),
    "redis_url": os.getenv("REDIS_URL", "redis://test-redis:6379"),
    "browser": os.getenv("BROWSER", "chrome"),
    "headless": os.getenv("HEADLESS", "true").lower() == "true",
    "timeout": int(os.getenv("PYTEST_TIMEOUT", "300")),
    "max_fail": int(os.getenv("PYTEST_MAX_FAIL", "5"))
}


@pytest.fixture(scope="session")
def docker_services_ready():
    """Wait for all Docker services to be ready before running tests."""
    services = [
        ("Mock API", f"{DOCKER_CONFIG['api_base_url']}/status"),
        ("Test Database", "postgresql://test_user:test_password@test-db:5432/test_automation"),
        ("Redis", DOCKER_CONFIG['redis_url'])
    ]
    
    for service_name, url in services:
        logger.info(f"Waiting for {service_name} to be ready...")
        max_retries = 30
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if service_name == "Test Database":
                    # For database, we'll just check if we can connect
                    import psycopg2
                    conn = psycopg2.connect(url)
                    conn.close()
                    logger.info(f"{service_name} is ready!")
                    break
                elif service_name == "Redis":
                    # For Redis, we'll check if we can connect
                    import redis
                    r = redis.from_url(url)
                    r.ping()
                    logger.info(f"{service_name} is ready!")
                    break
                else:
                    # For HTTP services
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        logger.info(f"{service_name} is ready!")
                        break
            except Exception as e:
                logger.debug(f"{service_name} not ready yet: {e}")
                time.sleep(2)
                retry_count += 1
        
        if retry_count >= max_retries:
            pytest.fail(f"{service_name} failed to start within {max_retries * 2} seconds")
    
    logger.info("All Docker services are ready!")


@pytest.fixture(scope="session")
def docker_test_config() -> Dict[str, Any]:
    """Provide Docker-specific test configuration."""
    return {
        "environment": "docker",
        "api_base_url": DOCKER_CONFIG["api_base_url"],
        "database_url": DOCKER_CONFIG["database_url"],
        "redis_url": DOCKER_CONFIG["redis_url"],
        "browser": DOCKER_CONFIG["browser"],
        "headless": DOCKER_CONFIG["headless"],
        "timeout": DOCKER_CONFIG["timeout"],
        "max_fail": DOCKER_CONFIG["max_fail"]
    }


@pytest.fixture
def docker_api_client(docker_services_ready) -> APIClient:
    """Provide API client configured for Docker environment."""
    client = APIClient()
    # Override base URL for Docker environment
    client.base_url = DOCKER_CONFIG["api_base_url"]
    yield client
    client.close()


@pytest.fixture
def docker_graphql_client(docker_services_ready) -> GraphQLClient:
    """Provide GraphQL client configured for Docker environment."""
    client = GraphQLClient()
    # Override base URL for Docker environment
    client.base_url = DOCKER_CONFIG["api_base_url"]
    yield client
    client.close()


@pytest.fixture(scope="session")
def docker_test_data_manager() -> DataManager:
    """Provide test data manager for Docker environment."""
    return DataManager()


@pytest.fixture(scope="session")
def docker_test_dataset(docker_test_data_manager: DataManager) -> Dict[str, Any]:
    """Generate and provide test dataset for Docker environment."""
    return docker_test_data_manager.generate_test_dataset(
        user_count=25,
        product_count=15,
        order_count=50
    )


@pytest.fixture
def docker_test_user() -> Dict[str, Any]:
    """Provide a single test user for Docker tests."""
    user = UserFactory.create_test_user()
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "username": user.username,
        "password": user.password,
        "date_of_birth": user.date_of_birth,
        "address": user.address
    }


@pytest.fixture
def docker_random_user() -> Dict[str, Any]:
    """Provide a random user for Docker tests."""
    user = UserFactory.create_user()
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "username": user.username,
        "password": user.password,
        "date_of_birth": user.date_of_birth,
        "address": user.address,
        "preferences": user.preferences
    }


@pytest.fixture
def docker_test_product() -> Dict[str, Any]:
    """Provide a test product for Docker tests."""
    product = ProductFactory.create_product()
    return {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "sku": product.sku,
        "in_stock": product.in_stock,
        "quantity": product.quantity,
        "attributes": product.attributes
    }


@pytest.fixture
def docker_test_products(count: int = 5) -> Generator[list, None, None]:
    """Provide multiple test products for Docker tests."""
    products = ProductFactory.create_products(count)
    yield [{
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "category": p.category,
        "sku": p.sku,
        "in_stock": p.in_stock,
        "quantity": p.quantity,
        "attributes": p.attributes
    } for p in products]


@pytest.fixture
def docker_test_order(docker_test_user: Dict[str, Any], docker_test_products: list) -> Dict[str, Any]:
    """Provide a test order for Docker tests."""
    products = [{
        "id": p["sku"],
        "name": p["name"],
        "price": p["price"],
        "quantity": 1
    } for p in docker_test_products[:3]]  # Use first 3 products
    
    order = OrderFactory.create_order(
        user_id=docker_test_user["email"],
        products=products
    )
    
    return {
        "order_id": order.order_id,
        "user_id": order.user_id,
        "products": order.products,
        "total_amount": order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address,
        "billing_address": order.billing_address,
        "payment_method": order.payment_method,
        "created_at": order.created_at,
        "updated_at": order.updated_at
    }


@pytest.fixture(scope="session", autouse=True)
def setup_docker_test_environment():
    """Set up Docker test environment before running tests."""
    # Create necessary directories
    Path("reports").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path("test_data").mkdir(exist_ok=True)
    Path("fixtures").mkdir(exist_ok=True)
    
    logger.info("Docker test environment setup completed")


@pytest.fixture(scope="session", autouse=True)
def cleanup_docker_test_environment():
    """Clean up Docker test environment after running tests."""
    yield
    
    logger.info("Docker test environment cleanup completed")


# Override the regular fixtures when running in Docker
@pytest.fixture(scope="session")
def test_config(docker_test_config):
    """Override test_config for Docker environment."""
    return docker_test_config


@pytest.fixture
def api_client(docker_api_client):
    """Override api_client for Docker environment."""
    return docker_api_client


@pytest.fixture
def graphql_client(docker_graphql_client):
    """Override graphql_client for Docker environment."""
    return docker_graphql_client


@pytest.fixture
def test_user(docker_test_user):
    """Override test_user for Docker environment."""
    return docker_test_user


@pytest.fixture
def random_user(docker_random_user):
    """Override random_user for Docker environment."""
    return docker_random_user


@pytest.fixture
def test_product(docker_test_product):
    """Override test_product for Docker environment."""
    return docker_test_product


@pytest.fixture
def test_products(docker_test_products):
    """Override test_products for Docker environment."""
    return docker_test_products


@pytest.fixture
def test_order(docker_test_order):
    """Override test_order for Docker environment."""
    return docker_test_order
