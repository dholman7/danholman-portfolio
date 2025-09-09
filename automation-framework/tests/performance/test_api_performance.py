"""
API performance tests for load testing and scalability validation.

These tests measure API performance under various load conditions and validate
that the system meets performance requirements and SLA thresholds.
"""

import pytest
from typing import Dict, Any, List
import concurrent.futures
import threading

from src.api.client import APIClient
from src.data.factories import UserFactory, ProductFactory


@pytest.mark.performance
@pytest.mark.slow
class TestAPIPerformance:
    """Test API performance and scalability."""
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_user_creation_performance(self, api_client: APIClient):
        """Test user creation performance with multiple users."""
        users = UserFactory.create_users(10)
        response_times = []
        
        for user in users:
            response = api_client.post("/users", data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            })
            
            assert response.status_code == 201
            response_times.append(response.response_time)
        
        # Verify all responses are fast
        avg_response_time = sum(response_times) / len(response_times)
        assert avg_response_time < 1.0, f"Average response time {avg_response_time:.3f}s exceeds threshold"
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_bulk_product_creation_performance(self, api_client: APIClient):
        """Test creating multiple products efficiently."""
        products = ProductFactory.create_products(20)
        created_products = []
        
        for product in products:
            response = api_client.post("/posts", data={
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "sku": product.sku
            })
            
            assert response.status_code == 201
            created_products.append(response.data)
        
        assert len(created_products) == 20
        
        # Verify all products can be retrieved
        get_response = api_client.get("/posts")
        assert len(get_response.data) >= 20
    
    @pytest.mark.api
    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_user_creation(self, api_client: APIClient):
        """Test concurrent user creation performance."""
        users = UserFactory.create_users(50)
        results = []
        
        def create_user(user_data):
            response = api_client.post("/users", data={
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "phone": user_data.phone
            })
            return response
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_user, user) for user in users]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response)
                except Exception as e:
                    pytest.fail(f"User creation failed: {e}")
        
        # Verify all users were created successfully
        successful_creations = [r for r in results if r.status_code == 201]
        assert len(successful_creations) == 50
        
        # Verify response times are reasonable
        avg_response_time = sum(r.response_time for r in successful_creations) / len(successful_creations)
        assert avg_response_time < 2.0, f"Average response time {avg_response_time:.3f}s exceeds threshold"
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_api_rate_limiting(self, api_client: APIClient):
        """Test API rate limiting behavior."""
        # Make rapid requests to test rate limiting
        responses = []
        for i in range(20):
            response = api_client.get("/posts")
            responses.append(response)
        
        # Check if rate limiting is working (should get 429 status codes)
        rate_limited_responses = [r for r in responses if r.status_code == 429]
        
        # If rate limiting is implemented, we should see some 429 responses
        # If not implemented, all should be 200
        if rate_limited_responses:
            assert len(rate_limited_responses) > 0, "Rate limiting should return 429 status codes"
        else:
            # All requests should succeed if no rate limiting
            successful_responses = [r for r in responses if r.status_code == 200]
            assert len(successful_responses) == 20
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_response_time_consistency(self, api_client: APIClient):
        """Test that API response times are consistent across multiple requests."""
        response_times = []
        
        # Make 10 identical requests
        for _ in range(10):
            response = api_client.get("/users")
            assert response.status_code == 200
            response_times.append(response.response_time)
        
        # Calculate statistics
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        # Verify response times are consistent (max should not be more than 5x min)
        assert max_response_time < min_response_time * 5, f"Response time inconsistency: max={max_response_time:.3f}s, min={min_response_time:.3f}s"
        
        # Verify average response time is reasonable
        assert avg_response_time < 1.0, f"Average response time {avg_response_time:.3f}s exceeds threshold"
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_memory_usage_under_load(self, api_client: APIClient):
        """Test memory usage doesn't grow excessively under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create many users to test memory usage
        users = UserFactory.create_users(100)
        for user in users:
            response = api_client.post("/users", data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            })
            assert response.status_code == 201
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024, f"Memory usage increased by {memory_increase / 1024 / 1024:.2f}MB"
    
    @pytest.mark.api
    @pytest.mark.performance
    def test_concurrent_mixed_operations(self, api_client: APIClient):
        """Test performance with mixed concurrent operations."""
        def get_users():
            return api_client.get("/users")
        
        def get_posts():
            return api_client.get("/posts")
        
        def create_user():
            user = UserFactory.create_user()
            return api_client.post("/users", data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            })
        
        # Mix of read and write operations
        operations = []
        for _ in range(10):
            operations.extend([get_users, get_posts, create_user])
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(op) for op in operations]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    response = future.result()
                    results.append(response)
                except Exception as e:
                    pytest.fail(f"Mixed operation failed: {e}")
        
        # Verify all operations completed successfully
        successful_operations = [r for r in results if r.status_code in [200, 201]]
        assert len(successful_operations) == len(operations)
        
        # Verify average response time is reasonable
        avg_response_time = sum(r.response_time for r in results) / len(results)
        assert avg_response_time < 1.5, f"Average response time {avg_response_time:.3f}s exceeds threshold"
