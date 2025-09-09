"""
Component tests for API client with mocked HTTP responses.

These tests verify that the API client works correctly with mocked HTTP responses,
testing the integration between the client and HTTP library without requiring
real external API calls.
"""

import pytest
from unittest.mock import Mock, patch
from src.api.client import APIClient, APIResponse


@pytest.mark.component
class TestAPIClientComponent:
    """Test API client component with mocked HTTP responses."""

    @pytest.fixture
    def api_client(self):
        """Create API client instance."""
        return APIClient()

    @pytest.fixture
    def mock_response_data(self):
        """Sample response data for mocking."""
        return {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "status": "active"
        }

    @patch('src.api.client.requests.Session.request')
    def test_get_request_success(self, mock_request, api_client, mock_response_data):
        """Test successful GET request with mocked response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Make request
        response = api_client.get("/api/users/1")

        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method='GET',
            url='/api/users/1',
            data=None,
            params=None,
            headers=api_client.headers,
            timeout=api_client.timeout,
            verify=True
        )

        # Verify response
        assert response.status_code == 200
        assert response.data == mock_response_data
        assert response.headers == {'Content-Type': 'application/json'}

    @patch('src.api.client.requests.Session.request')
    def test_post_request_success(self, mock_request, api_client, mock_response_data):
        """Test successful POST request with mocked response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = mock_response_data
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Test data
        test_data = {"name": "New User", "email": "new@example.com"}

        # Make request
        response = api_client.post("/api/users", data=test_data)

        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method='POST',
            url='/api/users',
            data='{"name": "New User", "email": "new@example.com"}',
            params=None,
            headers=api_client.headers,
            timeout=api_client.timeout,
            verify=True
        )

        # Verify response
        assert response.status_code == 201
        assert response.data == mock_response_data

    @patch('src.api.client.requests.Session.request')
    def test_put_request_success(self, mock_request, api_client, mock_response_data):
        """Test successful PUT request with mocked response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Test data
        test_data = {"name": "Updated User", "email": "updated@example.com"}

        # Make request
        response = api_client.put("/api/users/1", data=test_data)

        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method='PUT',
            url='/api/users/1',
            data='{"name": "Updated User", "email": "updated@example.com"}',
            params=None,
            headers=api_client.headers,
            timeout=api_client.timeout,
            verify=True
        )

        # Verify response
        assert response.status_code == 200
        assert response.data == mock_response_data

    @patch('src.api.client.requests.Session.request')
    def test_delete_request_success(self, mock_request, api_client):
        """Test successful DELETE request with mocked response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 204
        mock_response.json.return_value = None
        mock_response.headers = {}
        mock_request.return_value = mock_response

        # Make request
        response = api_client.delete("/api/users/1")

        # Verify request was made correctly
        mock_request.assert_called_once_with(
            method='DELETE',
            url='/api/users/1',
            data=None,
            params=None,
            headers=api_client.headers,
            timeout=api_client.timeout,
            verify=True
        )

        # Verify response
        assert response.status_code == 204
        assert response.data is None

    @patch('src.api.client.requests.Session.request')
    def test_request_with_authentication(self, mock_request, api_client, mock_response_data):
        """Test request with authentication headers."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Set authentication
        api_client.set_auth("Bearer", "test-token")

        # Make request
        response = api_client.get("/api/users/1")

        # Verify authentication header was included
        expected_headers = api_client.headers.copy()
        expected_headers['Authorization'] = 'Bearer test-token'
        
        mock_request.assert_called_once_with(
            method='GET',
            url='/api/users/1',
            data=None,
            params=None,
            headers=expected_headers,
            timeout=api_client.timeout,
            verify=True
        )

        assert response.status_code == 200

    @patch('src.api.client.requests.Session.request')
    def test_request_error_handling(self, mock_request, api_client):
        """Test request error handling with mocked error response."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Not Found"}
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        # Make request
        response = api_client.get("/api/users/999")

        # Verify error response
        assert response.status_code == 404
        assert response.data == {"error": "Not Found"}

    @patch('src.api.client.requests.Session.request')
    def test_request_timeout_handling(self, mock_request, api_client):
        """Test request timeout handling."""
        # Mock timeout exception
        import requests
        mock_request.side_effect = requests.exceptions.Timeout("Request timed out")

        # Make request
        response = api_client.get("/api/users/1")

        # Verify error response
        assert response.status_code == 0
        assert "timeout" in response.data.get("error", "").lower()

    @patch('src.api.client.requests.Session.request')
    def test_request_connection_error_handling(self, mock_request, api_client):
        """Test request connection error handling."""
        # Mock connection error
        import requests
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")

        # Make request
        response = api_client.get("/api/users/1")

        # Verify error response
        assert response.status_code == 0
        assert "connection" in response.data.get("error", "").lower()

    def test_clear_authentication(self, api_client):
        """Test clearing authentication."""
        # Set authentication
        api_client.set_auth("Bearer", "test-token")
        assert api_client.headers.get('Authorization') == 'Bearer test-token'

        # Clear authentication
        api_client.clear_auth()
        assert 'Authorization' not in api_client.headers

    def test_set_custom_headers(self, api_client):
        """Test setting custom headers."""
        custom_headers = {'X-Custom-Header': 'test-value'}
        api_client.set_headers(custom_headers)
        
        assert api_client.headers['X-Custom-Header'] == 'test-value'

    def test_merge_headers(self, api_client):
        """Test merging headers without overwriting existing ones."""
        # Set initial headers
        api_client.set_headers({'Content-Type': 'application/json'})
        
        # Merge additional headers
        api_client.set_headers({'X-API-Key': 'test-key'})
        
        # Verify both headers exist
        assert api_client.headers['Content-Type'] == 'application/json'
        assert api_client.headers['X-API-Key'] == 'test-key'
