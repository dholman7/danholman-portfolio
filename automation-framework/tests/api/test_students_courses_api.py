"""
Students & Courses API Test Suite

This module contains comprehensive API tests for the students and courses system.
Tests are designed to run in parallel using GitHub Actions matrix strategy.
"""

import json
import logging
import os
import pytest
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

import allure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test configuration from environment variables
API_BASE_URL = os.getenv('API_BASE_URL', 'https://staging-api.university.edu')
API_TYPE = os.getenv('API_TYPE', 'students')
ENDPOINT = os.getenv('ENDPOINT', '/api/v1/students')
METHOD = os.getenv('METHOD', 'GET')
TEST_SCENARIO = os.getenv('TEST_SCENARIO', 'list_students')
EXPECTED_STATUS = int(os.getenv('EXPECTED_STATUS', '200'))
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging')

# Test data
@dataclass
class TestData:
    """Test data for API testing"""
    student_id: str = "test_student_123"
    course_id: str = "test_course_456"
    student_payload: Dict[str, Any] = None
    course_payload: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.student_payload is None:
            self.student_payload = {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@university.edu",
                "student_id": self.student_id,
                "major": "Computer Science",
                "year": "Junior",
                "gpa": 3.8
            }
        
        if self.course_payload is None:
            self.course_payload = {
                "course_code": "CS101",
                "title": "Introduction to Computer Science",
                "description": "Basic concepts in computer science",
                "credits": 3,
                "instructor": "Dr. Smith",
                "semester": "Fall 2024",
                "max_enrollment": 50
            }

# API Client
class APIClient:
    """Generic API client for testing"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'API-Test-Suite/1.0'
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Making {method} request to {url}")
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            logger.info(f"Response: {response.status_code} - {response.reason}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        return self._make_request('POST', endpoint, json=data, **kwargs)
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        return self._make_request('PUT', endpoint, json=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._make_request('DELETE', endpoint, **kwargs)

# Test fixtures
@pytest.fixture
def api_client():
    """API client fixture"""
    return APIClient(API_BASE_URL)

@pytest.fixture
def test_data():
    """Test data fixture"""
    return TestData()

@pytest.fixture
def sample_student():
    """Sample student data"""
    return {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@university.edu",
        "student_id": "student_789",
        "major": "Mathematics",
        "year": "Senior",
        "gpa": 3.9
    }

@pytest.fixture
def sample_course():
    """Sample course data"""
    return {
        "course_code": "MATH201",
        "title": "Calculus II",
        "description": "Advanced calculus concepts",
        "credits": 4,
        "instructor": "Dr. Johnson",
        "semester": "Fall 2024",
        "max_enrollment": 30
    }

# Test classes
class TestStudentsAPI:
    """Students API test class"""
    
    @allure.feature("Students API")
    @allure.story("List Students")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.students
    @pytest.mark.list
    def test_list_students(self, api_client, test_data):
        """Test listing all students"""
        with allure.step("GET /api/v1/students"):
            response = api_client.get('/api/v1/students')
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
        
        with allure.step("Verify response structure"):
            data = response.json()
            assert isinstance(data, (list, dict)), "Response should be a list or object"
            
            if isinstance(data, dict):
                assert 'students' in data or 'data' in data, "Response should contain students data"
    
    @allure.feature("Students API")
    @allure.story("Create Student")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.students
    @pytest.mark.create
    def test_create_student(self, api_client, test_data, sample_student):
        """Test creating a new student"""
        with allure.step("POST /api/v1/students"):
            response = api_client.post('/api/v1/students', data=sample_student)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
        
        with allure.step("Verify response contains student data"):
            data = response.json()
            assert 'student_id' in data or 'id' in data, "Response should contain student ID"
    
    @allure.feature("Students API")
    @allure.story("Get Student by ID")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.students
    @pytest.mark.get_by_id
    def test_get_student_by_id(self, api_client, test_data):
        """Test getting a student by ID"""
        student_id = test_data.student_id
        endpoint = f'/api/v1/students/{student_id}'
        
        with allure.step(f"GET {endpoint}"):
            response = api_client.get(endpoint)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
        
        with allure.step("Verify response contains student data"):
            data = response.json()
            assert 'student_id' in data or 'id' in data, "Response should contain student ID"
    
    @allure.feature("Students API")
    @allure.story("Update Student")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.students
    @pytest.mark.update
    def test_update_student(self, api_client, test_data, sample_student):
        """Test updating a student"""
        student_id = test_data.student_id
        endpoint = f'/api/v1/students/{student_id}'
        update_data = {**sample_student, "gpa": 4.0}
        
        with allure.step(f"PUT {endpoint}"):
            response = api_client.put(endpoint, data=update_data)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
    
    @allure.feature("Students API")
    @allure.story("Delete Student")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.students
    @pytest.mark.delete
    def test_delete_student(self, api_client, test_data):
        """Test deleting a student"""
        student_id = test_data.student_id
        endpoint = f'/api/v1/students/{student_id}'
        
        with allure.step(f"DELETE {endpoint}"):
            response = api_client.delete(endpoint)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"

class TestCoursesAPI:
    """Courses API test class"""
    
    @allure.feature("Courses API")
    @allure.story("List Courses")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.courses
    @pytest.mark.list
    def test_list_courses(self, api_client, test_data):
        """Test listing all courses"""
        with allure.step("GET /api/v1/courses"):
            response = api_client.get('/api/v1/courses')
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
        
        with allure.step("Verify response structure"):
            data = response.json()
            assert isinstance(data, (list, dict)), "Response should be a list or object"
    
    @allure.feature("Courses API")
    @allure.story("Create Course")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    @pytest.mark.courses
    @pytest.mark.create
    def test_create_course(self, api_client, test_data, sample_course):
        """Test creating a new course"""
        with allure.step("POST /api/v1/courses"):
            response = api_client.post('/api/v1/courses', data=sample_course)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
        
        with allure.step("Verify response contains course data"):
            data = response.json()
            assert 'course_id' in data or 'id' in data, "Response should contain course ID"
    
    @allure.feature("Courses API")
    @allure.story("Get Course by ID")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.courses
    @pytest.mark.get_by_id
    def test_get_course_by_id(self, api_client, test_data):
        """Test getting a course by ID"""
        course_id = test_data.course_id
        endpoint = f'/api/v1/courses/{course_id}'
        
        with allure.step(f"GET {endpoint}"):
            response = api_client.get(endpoint)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
    
    @allure.feature("Courses API")
    @allure.story("Update Course")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.courses
    @pytest.mark.update
    def test_update_course(self, api_client, test_data, sample_course):
        """Test updating a course"""
        course_id = test_data.course_id
        endpoint = f'/api/v1/courses/{course_id}'
        update_data = {**sample_course, "credits": 5}
        
        with allure.step(f"PUT {endpoint}"):
            response = api_client.put(endpoint, data=update_data)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
    
    @allure.feature("Courses API")
    @allure.story("Delete Course")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.courses
    @pytest.mark.delete
    def test_delete_course(self, api_client, test_data):
        """Test deleting a course"""
        course_id = test_data.course_id
        endpoint = f'/api/v1/courses/{course_id}'
        
        with allure.step(f"DELETE {endpoint}"):
            response = api_client.delete(endpoint)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"

class TestEnrollmentsAPI:
    """Enrollments API test class"""
    
    @allure.feature("Enrollments API")
    @allure.story("List Student Courses")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.enrollments
    @pytest.mark.list
    def test_list_student_courses(self, api_client, test_data):
        """Test listing courses for a student"""
        student_id = test_data.student_id
        endpoint = f'/api/v1/students/{student_id}/courses'
        
        with allure.step(f"GET {endpoint}"):
            response = api_client.get(endpoint)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"
    
    @allure.feature("Enrollments API")
    @allure.story("Enroll Student in Course")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    @pytest.mark.enrollments
    @pytest.mark.enroll
    def test_enroll_student_in_course(self, api_client, test_data):
        """Test enrolling a student in a course"""
        student_id = test_data.student_id
        course_id = test_data.course_id
        endpoint = f'/api/v1/students/{student_id}/courses'
        enrollment_data = {"course_id": course_id}
        
        with allure.step(f"POST {endpoint}"):
            response = api_client.post(endpoint, data=enrollment_data)
            
        with allure.step(f"Verify response status is {EXPECTED_STATUS}"):
            assert response.status_code == EXPECTED_STATUS, f"Expected {EXPECTED_STATUS}, got {response.status_code}"

# Test configuration and markers
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "students: Student API tests")
    config.addinivalue_line("markers", "courses: Course API tests")
    config.addinivalue_line("markers", "enrollments: Enrollment API tests")
    config.addinivalue_line("markers", "list: List operation tests")
    config.addinivalue_line("markers", "create: Create operation tests")
    config.addinivalue_line("markers", "get_by_id: Get by ID operation tests")
    config.addinivalue_line("markers", "update: Update operation tests")
    config.addinivalue_line("markers", "delete: Delete operation tests")
    config.addinivalue_line("markers", "enroll: Enrollment operation tests")

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment variables"""
    # Filter tests based on environment variables
    api_type = os.getenv('API_TYPE', 'all')
    test_scenario = os.getenv('TEST_SCENARIO', 'all')
    
    for item in items:
        # Skip tests that don't match the API type
        if api_type != 'all' and api_type not in item.keywords:
            item.add_marker(pytest.mark.skip(reason=f"API type {api_type} not in test markers"))
        
        # Skip tests that don't match the test scenario
        if test_scenario != 'all' and test_scenario not in item.keywords:
            item.add_marker(pytest.mark.skip(reason=f"Test scenario {test_scenario} not in test markers"))

# Allure configuration
allure.dynamic.feature(f"Students & Courses API - {ENVIRONMENT}")
allure.dynamic.story(f"API Type: {API_TYPE}")
allure.dynamic.severity(allure.severity_level.NORMAL)
allure.dynamic.description(f"Testing {TEST_SCENARIO} for {API_TYPE} API in {ENVIRONMENT} environment")
