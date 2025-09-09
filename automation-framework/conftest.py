"""Pytest configuration and fixtures for the automation framework."""

import pytest
import os
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from src.config.settings import config, Browser
from src.api.client import APIClient, GraphQLClient
from src.data.factories import TestDataManager, UserFactory, ProductFactory, OrderFactory
from src.utils.logger import TestLogger, get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Provide test configuration."""
    return {
        "environment": config.test.environment.value,
        "browser": config.browser.browser.value,
        "headless": config.browser.headless,
        "parallel_workers": config.test.parallel_workers,
        "timeout": config.browser.explicit_wait,
        "base_url": config.api.base_url if config.api else None
    }


@pytest.fixture(scope="session")
def test_data_manager() -> TestDataManager:
    """Provide test data manager instance."""
    return TestDataManager()


@pytest.fixture(scope="session")
def test_dataset(test_data_manager: TestDataManager) -> Dict[str, Any]:
    """Generate and provide test dataset."""
    return test_data_manager.generate_test_dataset(
        user_count=50,
        product_count=25,
        order_count=100
    )


@pytest.fixture
def api_client() -> APIClient:
    """Provide API client instance."""
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def graphql_client() -> GraphQLClient:
    """Provide GraphQL client instance."""
    client = GraphQLClient()
    yield client
    client.close()


@pytest.fixture
def web_driver() -> Generator[webdriver.Remote, None, None]:
    """Provide WebDriver instance with proper setup and teardown."""
    driver = None
    
    try:
        # Create driver based on configuration
        if config.browser.browser == Browser.CHROME:
            options = ChromeOptions()
            if config.browser.headless:
                options.add_argument("--headless")
            options.add_argument(f"--window-size={config.browser.window_size[0]},{config.browser.window_size[1]}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            
            if config.browser.download_dir:
                options.add_experimental_option("prefs", {
                    "download.default_directory": config.browser.download_dir
                })
            
            driver = webdriver.Chrome(options=options)
            
        elif config.browser.browser == Browser.FIREFOX:
            options = FirefoxOptions()
            if config.browser.headless:
                options.add_argument("--headless")
            options.add_argument(f"--width={config.browser.window_size[0]}")
            options.add_argument(f"--height={config.browser.window_size[1]}")
            
            driver = webdriver.Firefox(options=options)
            
        elif config.browser.browser == Browser.SAFARI:
            options = SafariOptions()
            driver = webdriver.Safari(options=options)
            
        elif config.browser.browser == Browser.EDGE:
            options = EdgeOptions()
            if config.browser.headless:
                options.add_argument("--headless")
            options.add_argument(f"--window-size={config.browser.window_size[0]},{config.browser.window_size[1]}")
            
            driver = webdriver.Edge(options=options)
        
        else:
            raise ValueError(f"Unsupported browser: {config.browser.browser}")
        
        # Configure timeouts
        driver.implicitly_wait(config.browser.implicit_wait)
        driver.set_page_load_timeout(config.browser.page_load_timeout)
        driver.set_script_timeout(config.browser.script_timeout)
        
        logger.info(f"WebDriver initialized: {config.browser.browser.value}")
        yield driver
        
    except Exception as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver closed")


@pytest.fixture
def test_user() -> Dict[str, Any]:
    """Provide a single test user."""
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
def random_user() -> Dict[str, Any]:
    """Provide a random user."""
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
def test_product() -> Dict[str, Any]:
    """Provide a test product."""
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
def test_products(count: int = 5) -> Generator[list, None, None]:
    """Provide multiple test products."""
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
def test_order(test_user: Dict[str, Any], test_products: list) -> Dict[str, Any]:
    """Provide a test order."""
    products = [{
        "id": p["sku"],
        "name": p["name"],
        "price": p["price"],
        "quantity": 1
    } for p in test_products[:3]]  # Use first 3 products
    
    order = OrderFactory.create_order(
        user_id=test_user["email"],
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


@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def test_logger(request) -> TestLogger:
    """Provide test-specific logger."""
    test_name = request.node.name
    return TestLogger(test_name)


@pytest.fixture(autouse=True)
def test_setup_teardown(request, test_logger: TestLogger):
    """Automatic test setup and teardown."""
    # Setup
    test_logger.log_step("Test setup", f"Starting {request.node.name}")
    
    yield
    
    # Teardown
    test_logger.log_step("Test teardown", f"Completed {request.node.name}")


@pytest.fixture
def screenshot_on_failure(request, web_driver):
    """Take screenshot on test failure."""
    yield
    
    if request.node.rep_call.failed and config.test.screenshots_on_failure:
        screenshot_path = config.get_report_path(f"failure_{request.node.name}.png")
        web_driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment before running tests."""
    # Create necessary directories
    config.root_dir.mkdir(exist_ok=True)
    (config.root_dir / "reports").mkdir(exist_ok=True)
    (config.root_dir / "test_data").mkdir(exist_ok=True)
    (config.root_dir / "fixtures").mkdir(exist_ok=True)
    (config.root_dir / "logs").mkdir(exist_ok=True)
    
    logger.info("Test environment setup completed")


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_environment():
    """Clean up test environment after running tests."""
    yield
    
    logger.info("Test environment cleanup completed")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers and options."""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests for basic functionality"
    )
    config.addinivalue_line(
        "markers", "regression: Full regression test suite"
    )
    config.addinivalue_line(
        "markers", "api: API testing"
    )
    config.addinivalue_line(
        "markers", "ui: UI testing"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer than 30 seconds"
    )
    config.addinivalue_line(
        "markers", "flaky: Tests that may occasionally fail"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers and configuration."""
    # Skip slow tests if not explicitly requested
    if not config.getoption("--runslow", default=False):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    
    # Skip flaky tests in CI unless explicitly requested
    if config.getoption("--runflaky", default=False) or not os.getenv("CI"):
        skip_flaky = pytest.mark.skip(reason="need --runflaky option to run")
        for item in items:
            if "flaky" in item.keywords:
                item.add_marker(skip_flaky)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--runflaky", action="store_true", default=False, help="run flaky tests"
    )
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser to use for tests"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="run browser in headless mode"
    )
    parser.addoption(
        "--parallel", action="store", type=int, default=1, help="number of parallel workers"
    )
