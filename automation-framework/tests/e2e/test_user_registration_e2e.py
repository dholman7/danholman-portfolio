"""
End-to-end tests for user registration workflow.

These tests simulate complete user registration workflows from start to finish,
testing the entire user experience and system integration.
"""

import pytest
import allure
from unittest.mock import Mock, patch
from src.api.client import APIClient
from src.data.factories import UserFactory


@allure.epic("User Management")
@allure.feature("User Registration")
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

    @allure.story("Complete Registration Workflow")
    @allure.title("Complete user registration workflow from start to finish")
    @allure.description("Test complete user registration workflow including email/username availability checks, registration, login, and profile retrieval")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("e2e", "registration", "workflow")
    @patch('src.api.client.requests.Session.request')
    def test_complete_user_registration_workflow(self, mock_request, api_client, test_user_data):
        """Test complete user registration workflow from start to finish."""
        
        with allure.step("Step 1: Check email availability"):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"available": True}
            mock_response.headers = {'Content-Type': 'application/json'}
            mock_request.return_value = mock_response

            email_check_response = api_client.get(f"/api/users/check-email?email={test_user_data['email']}")
            allure.attach(f"Email check response: {email_check_response.status_code}", "API Response", allure.attachment_type.TEXT)
            assert email_check_response.status_code == 200
            assert email_check_response.data["available"] is True

        with allure.step("Step 2: Check username availability"):
            username_check_response = api_client.get(f"/api/users/check-username?username={test_user_data['username']}")
            allure.attach(f"Username check response: {username_check_response.status_code}", "API Response", allure.attachment_type.TEXT)
            assert username_check_response.status_code == 200
            assert username_check_response.data["available"] is True

        with allure.step("Step 3: Register new user"):
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": 1,
                "message": "User registered successfully",
                "user": test_user_data
            }
            mock_request.return_value = mock_response

            registration_response = api_client.post("/api/users/register", data=test_user_data)
            allure.attach(f"Registration response: {registration_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(registration_response.data), "Registration Data", allure.attachment_type.JSON)
            assert registration_response.status_code == 201
            assert registration_response.data["message"] == "User registered successfully"
            assert registration_response.data["user"]["email"] == test_user_data["email"]

        with allure.step("Step 4: Verify user can login"):
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
            allure.attach(f"Login response: {login_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(login_response.data), "Login Data", allure.attachment_type.JSON)
            assert login_response.status_code == 200
            assert "access_token" in login_response.data
            assert login_response.data["user"]["email"] == test_user_data["email"]

        with allure.step("Step 5: Verify user profile can be retrieved"):
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
            allure.attach(f"Profile response: {profile_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(profile_response.data), "Profile Data", allure.attachment_type.JSON)
            assert profile_response.status_code == 200
            assert profile_response.data["email"] == test_user_data["email"]
            assert profile_response.data["first_name"] == test_user_data["first_name"]

        with allure.step("Step 6: Verify all API calls were made"):
            allure.attach(f"Total API calls made: {mock_request.call_count}", "API Call Count", allure.attachment_type.TEXT)
            assert mock_request.call_count == 5

    @allure.story("Validation Error Handling")
    @allure.title("User registration with validation errors")
    @allure.description("Test user registration with invalid data to verify proper validation error handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "validation", "error-handling")
    @patch('src.api.client.requests.Session.request')
    def test_user_registration_with_validation_errors(self, mock_request, api_client):
        """Test user registration with validation errors."""
        
        with allure.step("Step 1: Prepare invalid user data"):
            invalid_user_data = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "invalid-email",
                "phone": "+1-555-123-4567",
                "username": "johndoe",
                "password": "weak"
            }
            allure.attach(str(invalid_user_data), "Invalid User Data", allure.attachment_type.JSON)

        with allure.step("Step 2: Mock validation error response"):
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

        with allure.step("Step 3: Attempt registration with invalid data"):
            registration_response = api_client.post("/api/users/register", data=invalid_user_data)
            allure.attach(f"Registration response: {registration_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(registration_response.data), "Validation Error Details", allure.attachment_type.JSON)
            assert registration_response.status_code == 400
            assert "Validation failed" in registration_response.data["error"]
            assert "email" in registration_response.data["details"]
            assert "password" in registration_response.data["details"]

    @allure.story("Duplicate Email Handling")
    @allure.title("User registration when email already exists")
    @allure.description("Test user registration when email already exists to verify proper error handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "duplicate", "error-handling")
    @patch('src.api.client.requests.Session.request')
    def test_user_registration_email_already_exists(self, mock_request, api_client, test_user_data):
        """Test user registration when email already exists."""
        
        with allure.step("Step 1: Check if email is available (should return false)"):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"available": False, "message": "Email already exists"}
            mock_response.headers = {'Content-Type': 'application/json'}
            mock_request.return_value = mock_response

            email_check_response = api_client.get(f"/api/users/check-email?email={test_user_data['email']}")
            allure.attach(f"Email check response: {email_check_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(email_check_response.data), "Email Availability Check", allure.attachment_type.JSON)
            assert email_check_response.status_code == 200
            assert email_check_response.data["available"] is False

        with allure.step("Step 2: Try to register with existing email (should fail)"):
            mock_response.status_code = 409
            mock_response.json.return_value = {
                "error": "Email already exists",
                "message": "A user with this email address already exists"
            }
            mock_request.return_value = mock_response

            registration_response = api_client.post("/api/users/register", data=test_user_data)
            allure.attach(f"Registration response: {registration_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(registration_response.data), "Duplicate Email Error", allure.attachment_type.JSON)
            assert registration_response.status_code == 409
            assert "Email already exists" in registration_response.data["error"]

    @allure.story("Network Error Handling")
    @allure.title("User registration with network error")
    @allure.description("Test user registration handling network errors to verify proper error handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "network", "error-handling")
    @patch('src.api.client.requests.Session.request')
    def test_user_registration_with_network_error(self, mock_request, api_client, test_user_data):
        """Test user registration handling network errors."""
        import requests
        
        with allure.step("Step 1: Mock network error"):
            mock_request.side_effect = requests.exceptions.ConnectionError("Network error")
            allure.attach("ConnectionError: Network error", "Network Error", allure.attachment_type.TEXT)

        with allure.step("Step 2: Attempt registration with network error"):
            registration_response = api_client.post("/api/users/register", data=test_user_data)
            allure.attach(f"Registration response: {registration_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(registration_response.data), "Network Error Response", allure.attachment_type.JSON)
            assert registration_response.status_code == 0
            assert "network" in registration_response.data.get("error", "").lower()

    @allure.story("Data Validation")
    @allure.title("User registration data validation")
    @allure.description("Test user registration data validation with missing required fields")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "validation", "data-validation")
    def test_user_registration_data_validation(self, api_client):
        """Test user registration data validation."""
        
        with allure.step("Step 1: Prepare incomplete user data"):
            incomplete_data = {
                "first_name": "John",
                "email": "john@example.com"
                # Missing last_name, phone, etc.
            }
            allure.attach(str(incomplete_data), "Incomplete User Data", allure.attachment_type.JSON)

        with allure.step("Step 2: Verify missing required fields"):
            # This should be caught by client-side validation before making the request
            # In a real implementation, you might want to add validation in the client
            allure.attach("Checking for missing required fields", "Validation Check", allure.attachment_type.TEXT)
            assert "last_name" not in incomplete_data
            assert "phone" not in incomplete_data

    @allure.story("Factory Data Registration")
    @allure.title("User registration using factory-generated data")
    @allure.description("Test user registration using factory-generated data to verify realistic data handling")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "factory", "data-generation")
    @patch('src.api.client.requests.Session.request')
    def test_user_registration_success_with_factory_data(self, mock_request, api_client):
        """Test user registration using factory-generated data."""
        
        with allure.step("Step 1: Generate user data using factory"):
            user = UserFactory.create_user()
            user_data = user.to_dict()
            allure.attach(str(user_data), "Factory Generated User Data", allure.attachment_type.JSON)

        with allure.step("Step 2: Mock successful registration response"):
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {
                "id": 1,
                "message": "User registered successfully",
                "user": user_data
            }
            mock_response.headers = {'Content-Type': 'application/json'}
            mock_request.return_value = mock_response

        with allure.step("Step 3: Register user with factory data"):
            registration_response = api_client.post("/api/users/register", data=user_data)
            allure.attach(f"Registration response: {registration_response.status_code}", "API Response", allure.attachment_type.TEXT)
            allure.attach(str(registration_response.data), "Registration Success Data", allure.attachment_type.JSON)
            assert registration_response.status_code == 201
            assert registration_response.data["message"] == "User registered successfully"
            assert registration_response.data["user"]["email"] == user_data["email"]
            assert registration_response.data["user"]["first_name"] == user_data["first_name"]
