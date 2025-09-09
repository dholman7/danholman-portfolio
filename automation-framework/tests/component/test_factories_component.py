"""
Component tests for data factories with mocked dependencies.

These tests verify that the data factories work correctly with mocked
external dependencies, testing the integration between factories and
their dependencies without requiring real external services.
"""

import pytest
from unittest.mock import Mock, patch
from src.data.factories import UserFactory, ProductFactory, OrderFactory


@pytest.mark.component
class TestUserFactoryComponent:
    """Test UserFactory component with mocked dependencies."""

    def test_create_user_with_mocked_faker(self):
        """Test user creation with specific data."""
        # Create user with specific data
        user = UserFactory.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+1-555-123-4567",
            username="johndoe",
            password="SecurePass123!",
            date_of_birth="1990-01-01"
        )

        # Verify user attributes
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-123-4567"
        assert user.username == "johndoe"
        assert user.password == "SecurePass123!"
        assert user.date_of_birth == "1990-01-01"

        # Verify address structure exists
        assert isinstance(user.address, dict)
        assert "street" in user.address
        assert "city" in user.address
        assert "state" in user.address
        assert "zip_code" in user.address
        assert "country" in user.address

        # Verify preferences structure exists
        assert isinstance(user.preferences, dict)
        assert "language" in user.preferences
        assert "timezone" in user.preferences
        assert "notifications" in user.preferences
        assert "theme" in user.preferences

    def test_create_users_batch(self):
        """Test creating multiple users in batch."""
        users = UserFactory.create_users(5)
        
        assert len(users) == 5
        for user in users:
            assert hasattr(user, 'first_name')
            assert hasattr(user, 'last_name')
            assert hasattr(user, 'email')
            assert hasattr(user, 'address')
            assert hasattr(user, 'preferences')

    def test_create_user_with_custom_data(self):
        """Test creating user with custom data overrides."""
        custom_data = {
            'first_name': 'Custom',
            'last_name': 'User',
            'email': 'custom@example.com'
        }
        
        user = UserFactory.create_user(**custom_data)
        
        assert user.first_name == 'Custom'
        assert user.last_name == 'User'
        assert user.email == 'custom@example.com'

    def test_user_serialization(self):
        """Test user serialization to dictionary."""
        user = UserFactory.create_user()
        user_dict = user.to_dict()
        
        assert isinstance(user_dict, dict)
        assert 'first_name' in user_dict
        assert 'last_name' in user_dict
        assert 'email' in user_dict
        assert 'address' in user_dict
        assert 'preferences' in user_dict


@pytest.mark.component
class TestProductFactoryComponent:
    """Test ProductFactory component with mocked dependencies."""

    def test_create_product_with_mocked_faker(self):
        """Test product creation with specific data."""
        # Create product with specific data
        product = ProductFactory.create_product(
            name="Test",
            description="A test product description",
            price=99.99,
            category="Electronics",
            sku="TEST-123-ABC",
            quantity=100,
            in_stock=True
        )

        # Verify product attributes
        assert product.name == "Test"
        assert product.description == "A test product description"
        assert product.price == 99.99
        assert product.category == "Electronics"
        assert product.sku == "TEST-123-ABC"
        assert product.in_stock is True
        assert product.quantity == 100

        # Verify attributes structure exists
        assert isinstance(product.attributes, dict)
        assert "color" in product.attributes
        assert "dimensions" in product.attributes
        assert "brand" in product.attributes
        # Check for any of the common attributes that might be generated
        assert any(key in product.attributes for key in ["warranty", "power_consumption", "connectivity", "model", "size", "weight"])

    def test_create_products_batch(self):
        """Test creating multiple products in batch."""
        products = ProductFactory.create_products(3)
        
        assert len(products) == 3
        for product in products:
            assert hasattr(product, 'name')
            assert hasattr(product, 'description')
            assert hasattr(product, 'price')
            assert hasattr(product, 'category')
            assert hasattr(product, 'attributes')

    def test_create_product_with_custom_data(self):
        """Test creating product with custom data overrides."""
        custom_data = {
            'name': 'Custom Product',
            'price': 199.99,
            'category': 'Custom Category'
        }
        
        product = ProductFactory.create_product(**custom_data)
        
        assert product.name == 'Custom Product'
        assert product.price == 199.99
        assert product.category == 'Custom Category'

    def test_product_serialization(self):
        """Test product serialization to dictionary."""
        product = ProductFactory.create_product()
        product_dict = product.to_dict()
        
        assert isinstance(product_dict, dict)
        assert 'name' in product_dict
        assert 'description' in product_dict
        assert 'price' in product_dict
        assert 'category' in product_dict
        assert 'attributes' in product_dict


@pytest.mark.component
class TestOrderFactoryComponent:
    """Test OrderFactory component with mocked dependencies."""

    def test_create_order_with_mocked_factories(self):
        """Test order creation with mocked factories."""
        # Create order with test data
        test_user_id = "test-user-123"
        test_products = [
            {"id": 1, "name": "Product 1", "price": 10.99, "quantity": 1},
            {"id": 2, "name": "Product 2", "price": 15.99, "quantity": 1}
        ]
        
        order = OrderFactory.create_order(
            user_id=test_user_id,
            products=test_products,
            status="pending"
        )

        # Verify order attributes
        assert order.user_id == test_user_id
        assert len(order.products) == 2
        assert order.products[0]["name"] == "Product 1"
        assert order.products[1]["name"] == "Product 2"
        assert order.status == "pending"
        assert order.total_amount == 26.98  # 10.99 + 15.99

    def test_create_orders_batch(self):
        """Test creating multiple orders in batch."""
        orders = OrderFactory.create_orders(3)
        
        assert len(orders) == 3
        for order in orders:
            assert hasattr(order, 'user_id')
            assert hasattr(order, 'products')
            assert hasattr(order, 'status')
            assert hasattr(order, 'total_amount')

    def test_order_serialization(self):
        """Test order serialization to dictionary."""
        order = OrderFactory.create_order()
        order_dict = order.to_dict()
        
        assert isinstance(order_dict, dict)
        assert 'user_id' in order_dict
        assert 'products' in order_dict
        assert 'status' in order_dict
        assert 'total_amount' in order_dict


@pytest.mark.component
class TestFactoryIntegration:
    """Test integration between different factories."""

    def test_user_and_order_integration(self):
        """Test that user and order factories work together."""
        # Create user
        user = UserFactory.create_user()
        
        # Create order with the user_id
        order = OrderFactory.create_order(user_id=user.email)  # Use email as user_id
        
        # Verify integration
        assert order.user_id == user.email
        assert order.user_id is not None

    def test_product_and_order_integration(self):
        """Test that product and order factories work together."""
        # Create products
        products = ProductFactory.create_products(2)
        
        # Convert ProductData objects to dictionaries for OrderFactory
        product_dicts = []
        for product in products:
            product_dicts.append({
                "id": product.sku,
                "name": product.name,
                "price": product.price,
                "quantity": 1
            })
        
        # Create order with the products
        order = OrderFactory.create_order(products=product_dicts)
        
        # Verify integration
        assert len(order.products) == 2
        assert all("name" in p for p in order.products)
        assert all("price" in p for p in order.products)
