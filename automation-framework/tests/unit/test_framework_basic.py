"""
Basic framework tests to verify the testing infrastructure works.
"""

import pytest
from src.api.client import APIClient
from src.data.factories import UserFactory, ProductFactory


class TestFrameworkBasic:
    """Test basic framework functionality."""

    @pytest.mark.unit
    def test_pytest_working(self):
        """Test that pytest is working correctly."""
        assert True

    @pytest.mark.unit
    def test_api_client_creation(self):
        """Test that APIClient can be instantiated."""
        client = APIClient()
        assert client is not None
        assert hasattr(client, 'get')
        assert hasattr(client, 'post')
        assert hasattr(client, 'put')
        assert hasattr(client, 'delete')

    @pytest.mark.unit
    def test_user_factory(self):
        """Test that UserFactory works."""
        user = UserFactory.create_user()
        assert user is not None
        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')
        assert hasattr(user, 'email')

    @pytest.mark.unit
    def test_product_factory(self):
        """Test that ProductFactory works."""
        product = ProductFactory.create_product()
        assert product is not None
        assert hasattr(product, 'name')
        assert hasattr(product, 'description')
        assert hasattr(product, 'price')

    @pytest.mark.unit
    def test_user_factory_batch(self):
        """Test UserFactory batch creation."""
        users = UserFactory.create_users(5)
        assert len(users) == 5
        for user in users:
            assert hasattr(user, 'first_name')
            assert hasattr(user, 'email')

    @pytest.mark.unit
    def test_product_factory_batch(self):
        """Test ProductFactory batch creation."""
        products = ProductFactory.create_products(3)
        assert len(products) == 3
        for product in products:
            assert hasattr(product, 'name')
            assert hasattr(product, 'price')

    @pytest.mark.smoke
    @pytest.mark.unit
    def test_smoke_marker(self):
        """Test that smoke marker works."""
        assert True

    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit marker works."""
        assert True

    @pytest.mark.unit
    @pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
    def test_parametrized(self, number):
        """Test parametrized testing."""
        assert number > 0
        assert number <= 5
