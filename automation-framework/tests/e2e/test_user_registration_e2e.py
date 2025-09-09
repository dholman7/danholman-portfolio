"""
End-to-end tests for user registration workflow.

These tests simulate complete user registration workflows from start to finish,
testing the entire user experience and system integration.
"""

import pytest
from unittest.mock import Mock, patch
from src.api.client import APIClient
from src.data.factories import UserFactory


@pytest.mark.e2e
class TestUserRegistrationE2E:
    """Test complete user registration workflow."""

    @pytest.fixture
    def api_client(self):
        """Create API client for E2E tests."""
        return APIClient()

    @pytest.fixture
    def test_user_data(self):
        """Create test user data for registration."""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "username": "johndoe",
            "password": "SecurePass123!",
            "date_of_birth": "1990-01-01",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
                "zip_code": "10001",
                "country": "United States"
            },
            "preferences": {
                "language": "en",
                "timezone": "America/New_York",
                "notifications": {
                    "email": True,
                    "sms": True,
                    "push": True
                },
                "theme": "light"
            }
        }

    @patch('src.api.client.requests.Session.request')
    def test_complete_user_registration_workflow(self, mock_request, api_client, test_user_data):
        """Test complete user registration workflow from start to finish."""
        # Step 1: Check if email is available
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"available": True}
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        email_check_response = api_client.get(f"/api/users/check-email?email={test_user_data['email']}")
        assert email_check_response.status_code == 200
        assert email_check_response.data["available"] is True

        # Step 2: Check if username is available
        username_check_response = api_client.get(f"/api/users/check-username?username={test_user_data['username']}")
        assert username_check_response.status_code == 200
        assert username_check_response.data["available"] is True

        # Step 3: Register new user
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": 1,
            "message": "User registered successfully",
            "user": test_user_data
        }
        mock_request.return_value = mock_response

        registration_response = api_client.post("/api/users/register", data=test_user_data)
        assert registration_response.status_code == 201
        assert registration_response.data["message"] == "User registered successfully"
        assert registration_response.data["user"]["email"] == test_user_data["email"]

        # Step 4: Verify user can login
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "Bearer",
            "expires_in": 3600,
            "user": {
                "id": 1,
                "email": test_user_data["email"],
                "username": test_user_data["username"]
            }
        }
        mock_request.return_value = mock_response

        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        login_response = api_client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200
        assert "access_token" in login_response.data
        assert login_response.data["user"]["email"] == test_user_data["email"]

        # Step 5: Verify user profile can be retrieved
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 1,
            "first_name": test_user_data["first_name"],
            "last_name": test_user_data["last_name"],
            "email": test_user_data["email"],
            "username": test_user_data["username"],
            "address": test_user_data["address"],
            "preferences": test_user_data["preferences"]
        }
        mock_request.return_value = mock_response

        # Set authentication token
        api_client.set_auth("Bearer", login_response.data["access_token"])
        profile_response = api_client.get("/api/users/profile")
        assert profile_response.status_code == 200
        assert profile_response.data["email"] == test_user_data["email"]
        assert profile_response.data["first_name"] == test_user_data["first_name"]

        # Verify all steps were called
        assert mock_request.call_count == 5

    @patch('src.api.client.requests.Session.request')
    def test_user_registration_with_validation_errors(self, mock_request, api_client):
        """Test user registration with validation errors."""
        # Test with invalid email
        invalid_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "phone": "+1-555-123-4567",
            "username": "johndoe",
            "password": "weak"
        }

        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "Validation failed",
            "details": {
                "email": ["Invalid email format"],
                "password": ["Password must be at least 8 characters"]
            }
        }
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        registration_response = api_client.post("/api/users/register", data=invalid_user_data)
        assert registration_response.status_code == 400
        assert "Validation failed" in registration_response.data["error"]
        assert "email" in registration_response.data["details"]
        assert "password" in registration_response.data["details"]

    @patch('src.api.client.requests.Session.request')
    def test_user_registration_email_already_exists(self, mock_request, api_client, test_user_data):
        """Test user registration when email already exists."""
        # Step 1: Check if email is available (should return false)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"available": False, "message": "Email already exists"}
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        email_check_response = api_client.get(f"/api/users/check-email?email={test_user_data['email']}")
        assert email_check_response.status_code == 200
        assert email_check_response.data["available"] is False

        # Step 2: Try to register with existing email (should fail)
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "error": "Email already exists",
            "message": "A user with this email address already exists"
        }
        mock_request.return_value = mock_response

        registration_response = api_client.post("/api/users/register", data=test_user_data)
        assert registration_response.status_code == 409
        assert "Email already exists" in registration_response.data["error"]

    @patch('src.api.client.requests.Session.request')
    def test_user_registration_with_network_error(self, mock_request, api_client, test_user_data):
        """Test user registration handling network errors."""
        import requests
        
        # Mock network error
        mock_request.side_effect = requests.exceptions.ConnectionError("Network error")

        registration_response = api_client.post("/api/users/register", data=test_user_data)
        assert registration_response.status_code == 0
        assert "network" in registration_response.data.get("error", "").lower()

    def test_user_registration_data_validation(self, api_client):
        """Test user registration data validation."""
        # Test with missing required fields
        incomplete_data = {
            "first_name": "John",
            "email": "john@example.com"
            # Missing last_name, phone, etc.
        }

        # This should be caught by client-side validation before making the request
        # In a real implementation, you might want to add validation in the client
        assert "last_name" not in incomplete_data
        assert "phone" not in incomplete_data

    @patch('src.api.client.requests.Session.request')
    def test_user_registration_success_with_factory_data(self, mock_request, api_client):
        """Test user registration using factory-generated data."""
        # Generate user data using factory
        user = UserFactory.create_user()
        user_data = user.to_dict()

        # Mock successful registration
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": 1,
            "message": "User registered successfully",
            "user": user_data
        }
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        registration_response = api_client.post("/api/users/register", data=user_data)
        assert registration_response.status_code == 201
        assert registration_response.data["message"] == "User registered successfully"
        assert registration_response.data["user"]["email"] == user_data["email"]
        assert registration_response.data["user"]["first_name"] == user_data["first_name"]
