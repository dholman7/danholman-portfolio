"""
Test suite demonstrating parallel testing concepts and implementation.

This module contains tests that showcase how parallel testing works
in the automation framework, including matrix generation, test execution,
and result aggregation.
"""

import json
import os
import tempfile
import time
from pathlib import Path
import pytest
import allure

from tests.parallel_testing_example import (
    ParallelTestMatrixGenerator,
    ResultAggregator,
    ParallelTestRunner,
    ExecutionConfig
)


class TestParallelTestMatrixGenerator:
    """Test the parallel test matrix generator."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ParallelTestMatrixGenerator(self.temp_dir)
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_matrix_generation_all_scope(self):
        """Test matrix generation for 'all' scope."""
        # Create mock test directories
        test_dirs = ['unit', 'integration', 'e2e', 'performance']
        for test_dir in test_dirs:
            (Path(self.temp_dir) / test_dir).mkdir(parents=True, exist_ok=True)
        
        self.generator.discover_tests()
        matrix = self.generator.generate_matrix("all")
        
        assert len(matrix) > 0, "Should generate test configurations"
        assert all('test_type' in config for config in matrix)
        assert all('framework' in config for config in matrix)
        assert all('language' in config for config in matrix)
    
    def test_matrix_generation_unit_scope(self):
        """Test matrix generation for 'unit' scope."""
        # Create mock unit test directory
        (Path(self.temp_dir) / 'unit').mkdir(parents=True, exist_ok=True)
        
        self.generator.discover_tests()
        matrix = self.generator.generate_matrix("unit")
        
        assert len(matrix) > 0, "Should generate unit test configurations"
        assert all(config['test_type'] == 'unit' for config in matrix)
    
    def test_matrix_generation_e2e_scope(self):
        """Test matrix generation for 'e2e' scope with browser/device combinations."""
        # Create mock e2e test directory
        (Path(self.temp_dir) / 'e2e').mkdir(parents=True, exist_ok=True)
        
        self.generator.discover_tests()
        matrix = self.generator.generate_matrix("e2e")
        
        assert len(matrix) > 0, "Should generate e2e test configurations"
        
        # Check for browser and device combinations
        e2e_configs = [config for config in matrix if config['test_type'] == 'e2e']
        assert len(e2e_configs) > 0, "Should have e2e configurations"
        
        # Should have browser and device combinations
        browser_configs = [config for config in e2e_configs if config.get('browser')]
        device_configs = [config for config in e2e_configs if config.get('device')]
        
        assert len(browser_configs) > 0, "Should have browser configurations"
        assert len(device_configs) > 0, "Should have device configurations"
    
    def test_matrix_save_and_load(self):
        """Test saving and loading matrix to/from JSON."""
        # Create mock test directories
        (Path(self.temp_dir) / 'unit').mkdir(parents=True, exist_ok=True)
        (Path(self.temp_dir) / 'integration').mkdir(parents=True, exist_ok=True)
        
        self.generator.discover_tests()
        
        # Save matrix
        output_file = Path(self.temp_dir) / "test_matrix.json"
        self.generator.save_matrix(str(output_file), "all")
        
        assert output_file.exists(), "Matrix file should be created"
        
        # Load and verify matrix
        with open(output_file, 'r') as f:
            loaded_matrix = json.load(f)
        
        assert isinstance(loaded_matrix, list), "Matrix should be a list"
        assert len(loaded_matrix) > 0, "Matrix should not be empty"


class TestTestResultAggregator:
    """Test the test result aggregator."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.aggregator = ResultAggregator()
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_aggregator_initialization(self):
        """Test aggregator initialization."""
        assert self.aggregator.aggregated_results['total_tests'] == 0
        assert self.aggregator.aggregated_results['passed'] == 0
        assert self.aggregator.aggregated_results['failed'] == 0
        assert self.aggregator.aggregated_results['skipped'] == 0
        assert self.aggregator.aggregated_results['errors'] == 0
        assert self.aggregator.aggregated_results['execution_time'] == 0.0
        assert self.aggregator.aggregated_results['test_suites'] == []
    
    def test_generate_summary(self):
        """Test summary generation."""
        # Set up mock data
        self.aggregator.aggregated_results['total_tests'] = 100
        self.aggregator.aggregated_results['passed'] = 95
        self.aggregator.aggregated_results['failed'] = 5
        self.aggregator.aggregated_results['execution_time'] = 120.5
        
        summary = self.aggregator.generate_summary()
        
        assert summary['summary']['total_tests'] == 100
        assert summary['summary']['passed'] == 95
        assert summary['summary']['failed'] == 5
        assert summary['summary']['success_rate'] == 95.0
        assert summary['summary']['execution_time'] == 120.5
    
    def test_save_aggregated_results(self):
        """Test saving aggregated results."""
        # Set up mock data
        self.aggregator.aggregated_results['total_tests'] = 50
        self.aggregator.aggregated_results['passed'] = 48
        self.aggregator.aggregated_results['failed'] = 2
        
        output_file = Path(self.temp_dir) / "aggregated_results.json"
        self.aggregator.save_aggregated_results(str(output_file))
        
        assert output_file.exists(), "Results file should be created"
        
        # Verify content
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert data['summary']['total_tests'] == 50
        assert data['summary']['passed'] == 48
        assert data['summary']['failed'] == 2


class TestParallelTestRunner:
    """Test the parallel test runner."""
    
    def test_runner_initialization(self):
        """Test runner initialization."""
        config = ExecutionConfig(
            test_type="unit",
            framework="pytest",
            language="python",
            category="unit",
            module="unit",
            test_path="tests/unit",
            environment="staging"
        )
        
        runner = ParallelTestRunner(config)
        assert runner.config == config
        assert runner.results == {}
    
    def test_environment_setup(self):
        """Test environment variable setup."""
        config = ExecutionConfig(
            test_type="e2e",
            framework="pytest",
            language="python",
            category="ui",
            module="e2e",
            test_path="tests/e2e",
            environment="production",
            browser="chrome",
            device="desktop"
        )
        
        runner = ParallelTestRunner(config)
        
        # Mock the environment setup
        original_env = os.environ.copy()
        try:
            runner._setup_environment()
            
            assert os.environ['TEST_TYPE'] == 'e2e'
            assert os.environ['TEST_FRAMEWORK'] == 'pytest'
            assert os.environ['TEST_LANGUAGE'] == 'python'
            assert os.environ['TEST_CATEGORY'] == 'ui'
            assert os.environ['TEST_MODULE'] == 'e2e'
            assert os.environ['TEST_ENVIRONMENT'] == 'production'
            assert os.environ['BROWSER'] == 'chrome'
            assert os.environ['DEVICE'] == 'desktop'
        finally:
            # Restore original environment
            os.environ.clear()
            os.environ.update(original_env)


class TestParallelTestingIntegration:
    """Integration tests for parallel testing functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create mock test structure
        test_structure = {
            'unit': ['test_helpers.py', 'test_validation.py'],
            'integration': ['test_api.py', 'test_database.py'],
            'e2e': ['test_ui.py', 'test_workflow.py'],
            'performance': ['test_load.py', 'test_stress.py']
        }
        
        for test_type, files in test_structure.items():
            test_dir = Path(self.temp_dir) / test_type
            test_dir.mkdir(parents=True, exist_ok=True)
            
            for file in files:
                (test_dir / file).write_text(f"# Mock {test_type} test file")
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_end_to_end_matrix_generation(self):
        """Test end-to-end matrix generation process."""
        generator = ParallelTestMatrixGenerator(self.temp_dir)
        generator.discover_tests()
        
        # Test different scopes
        scopes = ['all', 'unit', 'integration', 'e2e', 'performance']
        
        for scope in scopes:
            matrix = generator.generate_matrix(scope)
            assert len(matrix) > 0, f"Should generate configurations for {scope} scope"
            
            if scope != 'all':
                # Verify scope filtering
                for config in matrix:
                    if scope in ['unit', 'integration', 'e2e', 'performance']:
                        assert config['test_type'] == scope, f"All configs should be {scope} type"
    
    def test_matrix_with_environment_variations(self):
        """Test matrix generation with environment variations."""
        generator = ParallelTestMatrixGenerator(self.temp_dir)
        generator.discover_tests()
        
        matrix = generator.generate_matrix("all")
        
        # Should have different environments for integration and e2e tests
        environments = set(config['environment'] for config in matrix)
        assert len(environments) > 1, "Should have multiple environments"
        
        # Should have staging and production
        assert 'staging' in environments, "Should include staging environment"
        assert 'production' in environments, "Should include production environment"
    
    def test_e2e_browser_device_combinations(self):
        """Test e2e test configurations with browser and device combinations."""
        generator = ParallelTestMatrixGenerator(self.temp_dir)
        generator.discover_tests()
        
        matrix = generator.generate_matrix("e2e")
        
        # Should have browser and device combinations
        e2e_configs = [config for config in matrix if config['test_type'] == 'e2e']
        
        browsers = set(config.get('browser') for config in e2e_configs if config.get('browser'))
        devices = set(config.get('device') for config in e2e_configs if config.get('device'))
        
        assert len(browsers) > 0, "Should have browser configurations"
        assert len(devices) > 0, "Should have device configurations"
        
        # Should have common browsers
        expected_browsers = {'chrome', 'firefox', 'edge'}
        assert browsers.intersection(expected_browsers), "Should include common browsers"
        
        # Should have common devices
        expected_devices = {'desktop', 'mobile', 'tablet'}
        assert devices.intersection(expected_devices), "Should include common devices"


# Allure test annotations for demonstration
@allure.epic("Parallel Testing")
@allure.feature("Matrix Generation")
@allure.story("Test Configuration Discovery")
class TestAllureIntegration:
    """Test Allure integration with parallel testing."""
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test that matrix generation discovers all available test types")
    def test_matrix_discovers_all_test_types(self):
        """Test that matrix generation discovers all available test types."""
        temp_dir = tempfile.mkdtemp()
        try:
            # Create comprehensive test structure
            test_types = ['unit', 'component', 'integration', 'e2e', 'performance']
            for test_type in test_types:
                (Path(temp_dir) / test_type).mkdir(parents=True, exist_ok=True)
            
            generator = ParallelTestMatrixGenerator(temp_dir)
            generator.discover_tests()
            
            matrix = generator.generate_matrix("all")
            
            discovered_types = set(config['test_type'] for config in matrix)
            expected_types = set(test_types)
            
            assert discovered_types == expected_types, f"Should discover all test types: {expected_types}"
            
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test that parallel execution configuration is valid")
    def test_parallel_execution_configuration(self):
        """Test that parallel execution configuration is valid."""
        config = ExecutionConfig(
            test_type="integration",
            framework="pytest",
            language="python",
            category="api",
            module="integration",
            test_path="tests/integration",
            environment="staging"
        )
        
        runner = ParallelTestRunner(config)
        results = runner.run_tests()
        
        assert 'execution_time' in results, "Should include execution time"
        assert 'config' in results, "Should include configuration"
        assert results['config']['test_type'] == 'integration'
        assert results['config']['environment'] == 'staging'


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])
