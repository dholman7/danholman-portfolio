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

    @patch('src.data.factories.fake')
    def test_create_user_with_mocked_faker(self, mock_fake):
        """Test user creation with mocked Faker."""
        # Mock Faker methods
        mock_fake.first_name.return_value = "John"
        mock_fake.last_name.return_value = "Doe"
        mock_fake.email.return_value = "john.doe@example.com"
        mock_fake.phone_number.return_value = "+1-555-123-4567"
        mock_fake.user_name.return_value = "johndoe"
        mock_fake.password.return_value = "SecurePass123!"
        mock_fake.date_of_birth.return_value = "1990-01-01"
        mock_fake.street_address.return_value = "123 Main St"
        mock_fake.city.return_value = "New York"
        mock_fake.state.return_value = "NY"
        mock_fake.zipcode.return_value = "10001"
        mock_fake.country.return_value = "United States"
        mock_fake.language_code.return_value = "en"
        mock_fake.timezone.return_value = "America/New_York"
        mock_fake.boolean.return_value = True
        mock_fake.random_element.return_value = "light"

        # Create user
        user = UserFactory.create_user()

        # Verify user attributes
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-123-4567"
        assert user.username == "johndoe"
        assert user.password == "SecurePass123!"
        assert user.date_of_birth == "1990-01-01"

        # Verify address
        assert user.address.street == "123 Main St"
        assert user.address.city == "New York"
        assert user.address.state == "NY"
        assert user.address.zip_code == "10001"
        assert user.address.country == "United States"

        # Verify preferences
        assert user.preferences.language == "en"
        assert user.preferences.timezone == "America/New_York"
        assert user.preferences.notifications.email is True
        assert user.preferences.theme == "light"

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

    @patch('src.data.factories.fake')
    def test_create_product_with_mocked_faker(self, mock_fake):
        """Test product creation with mocked Faker."""
        # Mock Faker methods
        mock_fake.word.return_value = "Test"
        mock_fake.sentence.return_value = "A test product description"
        mock_fake.pyfloat.return_value = 99.99
        mock_fake.random_element.return_value = "Electronics"
        mock_fake.bothify.return_value = "TEST-123-ABC"
        mock_fake.boolean.return_value = True
        mock_fake.pyint.return_value = 100
        mock_fake.color_name.return_value = "Blue"
        mock_fake.pyfloat.return_value = 10.5
        mock_fake.word.return_value = "TestBrand"
        mock_fake.sentence.return_value = "Test care instructions"

        # Create product
        product = ProductFactory.create_product()

        # Verify product attributes
        assert product.name == "Test"
        assert product.description == "A test product description"
        assert product.price == 99.99
        assert product.category == "Electronics"
        assert product.sku == "TEST-123-ABC"
        assert product.in_stock is True
        assert product.stock_quantity == 100

        # Verify attributes
        assert product.attributes.color == "Blue"
        assert product.attributes.dimensions.height == 10.5
        assert product.attributes.brand == "TestBrand"
        assert product.attributes.care_instructions == "Test care instructions"

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

    @patch('src.data.factories.UserFactory')
    @patch('src.data.factories.ProductFactory')
    def test_create_order_with_mocked_factories(self, mock_product_factory, mock_user_factory):
        """Test order creation with mocked factories."""
        # Mock user
        mock_user = Mock()
        mock_user.id = 1
        mock_user.first_name = "John"
        mock_user.last_name = "Doe"
        mock_user.email = "john@example.com"
        mock_user_factory.create_user.return_value = mock_user

        # Mock products
        mock_product1 = Mock()
        mock_product1.id = 1
        mock_product1.name = "Product 1"
        mock_product1.price = 10.99
        mock_product1.sku = "PROD-001"

        mock_product2 = Mock()
        mock_product2.id = 2
        mock_product2.name = "Product 2"
        mock_product2.price = 15.99
        mock_product2.sku = "PROD-002"

        mock_product_factory.create_products.return_value = [mock_product1, mock_product2]

        # Create order
        order = OrderFactory.create_order()

        # Verify order attributes
        assert order.user == mock_user
        assert len(order.products) == 2
        assert order.products[0] == mock_product1
        assert order.products[1] == mock_product2
        assert order.status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        assert order.total_amount == 26.98  # 10.99 + 15.99

    def test_create_orders_batch(self):
        """Test creating multiple orders in batch."""
        orders = OrderFactory.create_orders(3)
        
        assert len(orders) == 3
        for order in orders:
            assert hasattr(order, 'user')
            assert hasattr(order, 'products')
            assert hasattr(order, 'status')
            assert hasattr(order, 'total_amount')

    def test_order_serialization(self):
        """Test order serialization to dictionary."""
        order = OrderFactory.create_order()
        order_dict = order.to_dict()
        
        assert isinstance(order_dict, dict)
        assert 'user' in order_dict
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
        
        # Create order with the user
        order = OrderFactory.create_order(user=user)
        
        # Verify integration
        assert order.user == user
        assert order.user.first_name == user.first_name
        assert order.user.email == user.email

    def test_product_and_order_integration(self):
        """Test that product and order factories work together."""
        # Create products
        products = ProductFactory.create_products(2)
        
        # Create order with the products
        order = OrderFactory.create_order(products=products)
        
        # Verify integration
        assert order.products == products
        assert len(order.products) == 2
        assert all(hasattr(p, 'name') for p in order.products)
        assert all(hasattr(p, 'price') for p in order.products)
