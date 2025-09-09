"""
Example test file demonstrating Allure reporting capabilities.
This file showcases various Allure features and annotations.
"""

import pytest
import allure
from typing import Dict, Any
import time
import random


@allure.epic("Test Automation Framework")
@allure.feature("Allure Reporting")
class TestAllureExample:
    """Example test class demonstrating Allure reporting features."""

    @allure.story("Basic Test Reporting")
    @allure.title("Simple passing test")
    @allure.description("This test demonstrates basic Allure reporting with a simple assertion.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "regression")
    def test_simple_passing(self):
        """Test that demonstrates basic Allure reporting."""
        with allure.step("Verify basic assertion"):
            assert 1 + 1 == 2

    @allure.story("Test with Steps")
    @allure.title("Test with multiple steps")
    @allure.description("This test demonstrates how to use Allure steps for better test organization.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("functional")
    def test_with_steps(self):
        """Test that demonstrates Allure steps."""
        with allure.step("Setup test data"):
            data = {"user_id": 123, "username": "testuser"}
            allure.attach(str(data), "Test Data", allure.attachment_type.JSON)

        with allure.step("Validate user data"):
            assert data["user_id"] == 123
            assert data["username"] == "testuser"

        with allure.step("Cleanup test data"):
            data.clear()

    @allure.story("Test with Attachments")
    @allure.title("Test with various attachments")
    @allure.description("This test demonstrates different types of attachments in Allure reports.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("reporting")
    def test_with_attachments(self):
        """Test that demonstrates various attachment types."""
        # Text attachment
        allure.attach("This is a text attachment", "Text Content", allure.attachment_type.TEXT)

        # JSON attachment
        json_data = {"key": "value", "number": 42, "boolean": True}
        allure.attach(str(json_data), "JSON Data", allure.attachment_type.JSON)

        # HTML attachment
        html_content = "<h1>Test Report</h1><p>This is HTML content</p>"
        allure.attach(html_content, "HTML Content", allure.attachment_type.HTML)

        # CSV attachment
        csv_content = "Name,Age,City\nJohn,25,New York\nJane,30,London"
        allure.attach(csv_content, "CSV Data", allure.attachment_type.CSV)

        assert True

    @allure.story("Test with Parameters")
    @allure.title("Parameterized test")
    @allure.description("This test demonstrates parameterized testing with Allure.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("parameterized")
    @pytest.mark.parametrize("input_value,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
        (4, 8),
        (5, 10)
    ])
    def test_parameterized(self, input_value: int, expected: int):
        """Test that demonstrates parameterized testing."""
        with allure.step(f"Calculate result for input {input_value}"):
            result = input_value * 2
            allure.attach(f"Input: {input_value}, Result: {result}, Expected: {expected}", 
                         "Calculation Details", allure.attachment_type.TEXT)

        with allure.step("Verify result"):
            assert result == expected

    @allure.story("Test with Dynamic Title")
    @allure.title("Dynamic test title based on environment")
    @allure.description("This test demonstrates dynamic test titles.")
    @allure.severity(allure.severity_level.LOW)
    @allure.tag("dynamic")
    def test_dynamic_title(self):
        """Test with dynamic title based on environment."""
        import os
        environment = os.getenv("TEST_ENVIRONMENT", "local")
        
        # Update test title dynamically
        allure.dynamic.title(f"Test in {environment} environment")
        
        with allure.step(f"Verify environment is {environment}"):
            assert environment in ["local", "dev", "staging", "prod"]

    @allure.story("Test with Links")
    @allure.title("Test with external links")
    @allure.description("This test demonstrates how to add links to Allure reports.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("links")
    def test_with_links(self):
        """Test that demonstrates external links in Allure reports."""
        # Add issue link
        allure.link("https://github.com/danholman/danholman-portfolio/issues/1", 
                   "Related Issue", allure.link_type.ISSUE)
        
        # Add TMS link
        allure.link("https://github.com/danholman/danholman-portfolio/issues/2", 
                   "Test Management System", allure.link_type.TMS)
        
        # Add custom link
        allure.link("https://github.com/danholman/danholman-portfolio", 
                   "Repository", allure.link_type.LINK)

        assert True

    @allure.story("Test with Categories")
    @allure.title("Test that will be categorized")
    @allure.description("This test demonstrates how tests are categorized in Allure reports.")
    @allure.severity(allure.severity_level.HIGH)
    @allure.tag("categorization")
    def test_with_categories(self):
        """Test that demonstrates categorization."""
        with allure.step("Perform test operation"):
            # Simulate a test that might fail
            result = random.choice([True, False])
            
            if not result:
                raise AssertionError("Random test failure for demonstration")

        assert result

    @allure.story("Performance Test")
    @allure.title("Test with performance metrics")
    @allure.description("This test demonstrates performance testing with Allure.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("performance")
    def test_performance(self):
        """Test that demonstrates performance metrics."""
        with allure.step("Measure execution time"):
            start_time = time.time()
            
            # Simulate some work
            time.sleep(0.1)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            allure.attach(f"Execution time: {execution_time:.3f} seconds", 
                         "Performance Metrics", allure.attachment_type.TEXT)

        with allure.step("Verify performance requirements"):
            assert execution_time < 1.0  # Should complete within 1 second

    @allure.story("Test with Environment Info")
    @allure.title("Test with environment information")
    @allure.description("This test demonstrates environment information in Allure reports.")
    @allure.severity(allure.severity_level.LOW)
    @allure.tag("environment")
    def test_environment_info(self):
        """Test that demonstrates environment information."""
        import platform
        import sys
        
        with allure.step("Collect environment information"):
            env_info = {
                "Python Version": sys.version,
                "Platform": platform.platform(),
                "Architecture": platform.architecture(),
                "Machine": platform.machine(),
                "Processor": platform.processor()
            }
            
            allure.attach(str(env_info), "Environment Information", allure.attachment_type.JSON)

        assert True

    @allure.story("Test with Screenshots")
    @allure.title("Test with screenshot simulation")
    @allure.description("This test demonstrates how to attach screenshots to Allure reports.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("screenshots")
    def test_with_screenshots(self):
        """Test that demonstrates screenshot attachments."""
        with allure.step("Take screenshot before action"):
            # Simulate screenshot data
            screenshot_data = b"fake_screenshot_data"
            allure.attach(screenshot_data, "Screenshot Before", allure.attachment_type.PNG)

        with allure.step("Perform action"):
            # Simulate some action
            pass

        with allure.step("Take screenshot after action"):
            # Simulate screenshot data
            screenshot_data = b"fake_screenshot_data_after"
            allure.attach(screenshot_data, "Screenshot After", allure.attachment_type.PNG)

        assert True

    @allure.story("Test with Retry")
    @allure.title("Test that demonstrates retry mechanism")
    @allure.description("This test demonstrates retry mechanism with Allure reporting.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("retry")
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_with_retry(self):
        """Test that demonstrates retry mechanism."""
        with allure.step("Attempt test operation"):
            # Simulate flaky test
            success_rate = 0.7
            if random.random() > success_rate:
                raise AssertionError("Test failed, will be retried")

        assert True

    @allure.story("Test with Custom Markers")
    @allure.title("Test with custom pytest markers")
    @allure.description("This test demonstrates custom pytest markers with Allure.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("markers")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.api
    def test_with_custom_markers(self):
        """Test that demonstrates custom pytest markers."""
        with allure.step("Verify test markers"):
            # This test has multiple markers: smoke, regression, api
            assert True

    @allure.story("Test with Fixtures")
    @allure.title("Test with pytest fixtures")
    @allure.description("This test demonstrates pytest fixtures with Allure reporting.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("fixtures")
    def test_with_fixtures(self, sample_data: Dict[str, Any]):
        """Test that demonstrates pytest fixtures."""
        with allure.step("Use fixture data"):
            allure.attach(str(sample_data), "Fixture Data", allure.attachment_type.JSON)
            assert "key" in sample_data
            assert sample_data["value"] == "test"


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Sample fixture for testing."""
    return {"key": "value", "number": 42, "boolean": True}


@allure.epic("Test Automation Framework")
@allure.feature("Allure Reporting")
@allure.story("Test Suite Organization")
class TestAllureSuite:
    """Test suite demonstrating Allure organization features."""

    @allure.title("Suite setup test")
    @allure.description("This test demonstrates suite-level setup.")
    @allure.severity(allure.severity_level.LOW)
    def test_suite_setup(self):
        """Test that demonstrates suite setup."""
        with allure.step("Initialize suite"):
            pass

    @allure.title("Suite teardown test")
    @allure.description("This test demonstrates suite-level teardown.")
    @allure.severity(allure.severity_level.LOW)
    def test_suite_teardown(self):
        """Test that demonstrates suite teardown."""
        with allure.step("Cleanup suite"):
            pass
