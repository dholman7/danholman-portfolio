"""API client for testing REST and GraphQL APIs."""

import json
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config.settings import config
from ..utils.helpers import retry_on_exception, get_environment_variable
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class APIResponse:
    """API response wrapper."""
    status_code: int
    headers: Dict[str, str]
    data: Any
    response_time: float
    url: str
    method: str
    request_data: Optional[Dict[str, Any]] = None


class APIClient:
    """HTTP client for API testing with retry logic and authentication."""
    
    def __init__(
        self,
        base_url: str = None,
        timeout: int = None,
        retry_attempts: int = None,
        retry_delay: float = None,
        verify_ssl: bool = None,
        api_key: str = None,
        auth_token: str = None
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts
            retry_delay: Delay between retries
            verify_ssl: Whether to verify SSL certificates
            api_key: API key for authentication
            auth_token: Bearer token for authentication
        """
        self.base_url = base_url or (config.api.base_url if config.api else "")
        self.timeout = timeout or (config.api.timeout if config.api else 30)
        self.retry_attempts = retry_attempts or (config.api.retry_attempts if config.api else 3)
        self.retry_delay = retry_delay or (config.api.retry_delay if config.api else 1.0)
        self.verify_ssl = verify_ssl if verify_ssl is not None else (config.api.verify_ssl if config.api else True)
        self.api_key = api_key or (config.api.api_key if config.api else None)
        self.auth_token = auth_token or (config.api.auth_token if config.api else None)
        
        # Create session with retry strategy
        self.session = requests.Session()
        self._setup_retry_strategy()
        self._setup_authentication()
        self._setup_headers()
    
    def _setup_retry_strategy(self) -> None:
        """Set up retry strategy for requests."""
        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=self.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _setup_authentication(self) -> None:
        """Set up authentication for requests."""
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})
        
        if self.auth_token:
            self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
    
    def _setup_headers(self) -> None:
        """Set up default headers."""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Pytest-Automation-Framework/1.0.0"
        })
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get current headers."""
        return dict(self.session.headers)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            APIResponse instance
        """
        # Handle URL construction properly
        if self.base_url:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        else:
            # If no base_url, use endpoint as-is (for relative URLs in tests)
            url = endpoint
        timeout = timeout or self.timeout
        
        # Prepare headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        # Prepare request data
        request_data = None
        if data is not None:
            if isinstance(data, dict):
                request_data = json.dumps(data)
            else:
                request_data = data
        
        start_time = time.time()
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                data=request_data,
                params=params,
                headers=request_headers,
                timeout=timeout,
                verify=self.verify_ssl
            )
            
            response_time = time.time() - start_time
            
            # Parse response data
            try:
                response_data = response.json()
            except (ValueError, json.JSONDecodeError):
                response_data = response.text
            
            api_response = APIResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                data=response_data,
                response_time=response_time,
                url=url,
                method=method.upper(),
                request_data=data
            )
            
            logger.debug(f"{method.upper()} {url} - {response.status_code} ({response_time:.3f}s)")
            return api_response
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            logger.error(f"Request failed: {method.upper()} {url} - {e}")
            
            # Normalize error message for timeout
            error_msg = str(e)
            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                error_msg = "Request timeout"
            
            # Return error response
            return APIResponse(
                status_code=0,
                headers={},
                data={"error": error_msg},
                response_time=response_time,
                url=url,
                method=method.upper(),
                request_data=data
            )
    
    @retry_on_exception(exceptions=(requests.exceptions.RequestException,), max_attempts=3)
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """Make GET request."""
        return self._make_request("GET", endpoint, params=params, headers=headers, timeout=timeout)
    
    @retry_on_exception(exceptions=(requests.exceptions.RequestException,), max_attempts=3)
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """Make POST request."""
        return self._make_request("POST", endpoint, data=data, params=params, headers=headers, timeout=timeout)
    
    @retry_on_exception(exceptions=(requests.exceptions.RequestException,), max_attempts=3)
    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """Make PUT request."""
        return self._make_request("PUT", endpoint, data=data, params=params, headers=headers, timeout=timeout)
    
    @retry_on_exception(exceptions=(requests.exceptions.RequestException,), max_attempts=3)
    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """Make PATCH request."""
        return self._make_request("PATCH", endpoint, data=data, params=params, headers=headers, timeout=timeout)
    
    @retry_on_exception(exceptions=(requests.exceptions.RequestException,), max_attempts=3)
    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """Make DELETE request."""
        return self._make_request("DELETE", endpoint, params=params, headers=headers, timeout=timeout)
    
    def upload_file(
        self,
        endpoint: str,
        file_path: str,
        field_name: str = "file",
        additional_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """
        Upload file via POST request.
        
        Args:
            endpoint: API endpoint
            file_path: Path to file to upload
            field_name: Form field name for file
            additional_data: Additional form data
            headers: Additional headers
            timeout: Request timeout
            
        Returns:
            APIResponse instance
        """
        # Handle URL construction properly
        if self.base_url:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        else:
            # If no base_url, use endpoint as-is (for relative URLs in tests)
            url = endpoint
        timeout = timeout or self.timeout
        
        # Prepare files
        files = {field_name: open(file_path, 'rb')}
        
        # Prepare additional data
        data = additional_data or {}
        
        # Prepare headers (remove Content-Type to let requests set it)
        request_headers = {k: v for k, v in self.session.headers.items() if k.lower() != 'content-type'}
        if headers:
            request_headers.update(headers)
        
        start_time = time.time()
        
        try:
            response = self.session.post(
                url=url,
                files=files,
                data=data,
                headers=request_headers,
                timeout=timeout,
                verify=self.verify_ssl
            )
            
            response_time = time.time() - start_time
            
            # Parse response data
            try:
                response_data = response.json()
            except (ValueError, json.JSONDecodeError):
                response_data = response.text
            
            api_response = APIResponse(
                status_code=response.status_code,
                headers=dict(response.headers),
                data=response_data,
                response_time=response_time,
                url=url,
                method="POST",
                request_data={"file": file_path, **data}
            )
            
            logger.debug(f"POST {url} (file upload) - {response.status_code} ({response_time:.3f}s)")
            return api_response
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            logger.error(f"File upload failed: POST {url} - {e}")
            
            return APIResponse(
                status_code=0,
                headers={},
                data={"error": str(e)},
                response_time=response_time,
                url=url,
                method="POST",
                request_data={"file": file_path, **data}
            )
        finally:
            # Close file
            files[field_name].close()
    
    def set_auth_token(self, token: str) -> None:
        """Set authentication token."""
        self.auth_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.debug("Authentication token updated")
    
    def set_auth(self, auth_type: str, token: str) -> None:
        """Set authentication with type and token."""
        if auth_type.lower() == "bearer":
            self.set_auth_token(token)
        elif auth_type.lower() == "api_key":
            self.set_api_key(token)
        else:
            raise ValueError(f"Unsupported auth type: {auth_type}")
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set custom headers."""
        self.session.headers.update(headers)
        logger.debug(f"Headers updated: {headers}")
    
    def set_api_key(self, key: str) -> None:
        """Set API key."""
        self.api_key = key
        self.session.headers.update({"X-API-Key": key})
        logger.debug("API key updated")
    
    def clear_auth(self) -> None:
        """Clear authentication headers."""
        self.auth_token = None
        self.api_key = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
        if "X-API-Key" in self.session.headers:
            del self.session.headers["X-API-Key"]
        logger.debug("Authentication cleared")
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
        logger.debug("API client session closed")


class GraphQLClient(APIClient):
    """GraphQL client extending APIClient for GraphQL queries."""
    
    def __init__(self, *args, **kwargs):
        """Initialize GraphQL client."""
        super().__init__(*args, **kwargs)
        self._setup_graphql_headers()
    
    def _setup_graphql_headers(self) -> None:
        """Set up GraphQL-specific headers."""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """
        Execute GraphQL query.
        
        Args:
            query: GraphQL query string
            variables: Query variables
            operation_name: Operation name
            timeout: Request timeout
            
        Returns:
            APIResponse instance
        """
        data = {
            "query": query,
            "variables": variables or {},
            "operationName": operation_name
        }
        
        return self.post("graphql", data=data, timeout=timeout)
    
    def mutation(
        self,
        mutation: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """
        Execute GraphQL mutation.
        
        Args:
            mutation: GraphQL mutation string
            variables: Mutation variables
            operation_name: Operation name
            timeout: Request timeout
            
        Returns:
            APIResponse instance
        """
        return self.query(mutation, variables, operation_name, timeout)
    
    def subscription(
        self,
        subscription: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
        timeout: Optional[int] = None
    ) -> APIResponse:
        """
        Execute GraphQL subscription.
        
        Args:
            subscription: GraphQL subscription string
            variables: Subscription variables
            operation_name: Operation name
            timeout: Request timeout
            
        Returns:
            APIResponse instance
        """
        return self.query(subscription, variables, operation_name, timeout)
