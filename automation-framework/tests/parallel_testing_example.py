"""
Parallel Testing Example for Automation Framework

This module demonstrates how to implement parallel testing strategies
in GitHub Actions with proper test matrix generation, execution,
and result aggregation.

Key Concepts Demonstrated:
1. Dynamic test matrix generation
2. Parallel test execution with GitHub Actions matrix strategy
3. Test result aggregation and reporting
4. Artifact collection and merging
5. Comprehensive test coverage across different test types
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import pytest
import allure


@dataclass
class ExecutionConfig:
    """Configuration for a single test execution unit."""
    test_type: str
    framework: str
    language: str
    category: str
    module: str
    test_path: str
    environment: str
    browser: str = None
    device: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class ParallelTestMatrixGenerator:
    """Generates test matrices for parallel execution in GitHub Actions."""
    
    def __init__(self, base_path: str = "tests"):
        self.base_path = Path(base_path)
        self.test_configs: List[ExecutionConfig] = []
    
    def discover_tests(self) -> None:
        """Discover all available tests and create configurations."""
        test_types = {
            "unit": {
                "framework": "pytest",
                "language": "python",
                "path": "unit"
            },
            "component": {
                "framework": "pytest", 
                "language": "python",
                "path": "component"
            },
            "integration": {
                "framework": "pytest",
                "language": "python", 
                "path": "integration"
            },
            "e2e": {
                "framework": "pytest",
                "language": "python",
                "path": "e2e"
            },
            "performance": {
                "framework": "pytest",
                "language": "python",
                "path": "performance"
            }
        }
        
        environments = ["staging", "production"]
        browsers = ["chrome", "firefox", "edge"]
        devices = ["desktop", "mobile", "tablet"]
        
        for test_type, config in test_types.items():
            test_dir = self.base_path / config["path"]
            if test_dir.exists():
                # Add base configuration
                self.test_configs.append(ExecutionConfig(
                    test_type=test_type,
                    framework=config["framework"],
                    language=config["language"],
                    category="api" if test_type in ["integration", "e2e"] else "unit",
                    module=test_type,
                    test_path=str(test_dir),
                    environment="staging"
                ))
                
                # Add environment-specific configs for integration and e2e tests
                if test_type in ["integration", "e2e"]:
                    for env in environments:
                        self.test_configs.append(ExecutionConfig(
                            test_type=test_type,
                            framework=config["framework"],
                            language=config["language"],
                            category="api",
                            module=test_type,
                            test_path=str(test_dir),
                            environment=env
                        ))
                
                # Add browser-specific configs for e2e tests
                if test_type == "e2e":
                    for browser in browsers:
                        for device in devices:
                            self.test_configs.append(ExecutionConfig(
                                test_type=test_type,
                                framework=config["framework"],
                                language=config["language"],
                                category="ui",
                                module=test_type,
                                test_path=str(test_dir),
                                environment="staging",
                                browser=browser,
                                device=device
                            ))
    
    def filter_by_scope(self, scope: str = "all") -> List[ExecutionConfig]:
        """Filter test configurations by scope."""
        if scope == "all":
            return self.test_configs
        
        scope_mapping = {
            "python": lambda config: config.language == "python",
            "api": lambda config: config.category == "api",
            "ui": lambda config: config.category == "ui",
            "unit": lambda config: config.test_type == "unit",
            "integration": lambda config: config.test_type == "integration",
            "e2e": lambda config: config.test_type == "e2e",
            "performance": lambda config: config.test_type == "performance"
        }
        
        if scope in scope_mapping:
            return [config for config in self.test_configs if scope_mapping[scope](config)]
        
        return self.test_configs
    
    def generate_matrix(self, scope: str = "all") -> List[Dict[str, Any]]:
        """Generate test matrix for GitHub Actions."""
        filtered_configs = self.filter_by_scope(scope)
        return [config.to_dict() for config in filtered_configs]
    
    def save_matrix(self, output_file: str, scope: str = "all") -> None:
        """Save test matrix to JSON file."""
        matrix = self.generate_matrix(scope)
        with open(output_file, 'w') as f:
            json.dump(matrix, f, indent=2)
        print(f"Generated {len(matrix)} test configurations")
        print(f"Matrix saved to: {output_file}")


class ResultAggregator:
    """Aggregates and merges test results from parallel execution."""
    
    def __init__(self, results_dir: str = "test_results"):
        self.results_dir = Path(results_dir)
        self.aggregated_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "execution_time": 0.0,
            "test_suites": []
        }
    
    def collect_results(self, artifacts_dir: str) -> None:
        """Collect results from downloaded artifacts."""
        artifacts_path = Path(artifacts_dir)
        
        if not artifacts_path.exists():
            print(f"Artifacts directory not found: {artifacts_dir}")
            return
        
        # Find all result files
        result_files = list(artifacts_path.rglob("*.json")) + list(artifacts_path.rglob("*.xml"))
        
        for result_file in result_files:
            self._process_result_file(result_file)
    
    def _process_result_file(self, file_path: Path) -> None:
        """Process a single result file."""
        try:
            if file_path.suffix == '.json':
                self._process_json_result(file_path)
            elif file_path.suffix == '.xml':
                self._process_xml_result(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    def _process_json_result(self, file_path: Path) -> None:
        """Process JSON result file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if 'test_results' in data:
            suite = data['test_results']
            self.aggregated_results['test_suites'].append(suite)
            self.aggregated_results['total_tests'] += suite.get('total', 0)
            self.aggregated_results['passed'] += suite.get('passed', 0)
            self.aggregated_results['failed'] += suite.get('failed', 0)
            self.aggregated_results['skipped'] += suite.get('skipped', 0)
            self.aggregated_results['execution_time'] += suite.get('execution_time', 0.0)
    
    def _process_xml_result(self, file_path: Path) -> None:
        """Process XML result file (JUnit format)."""
        # This would parse JUnit XML files
        # For now, we'll just count it as a processed file
        print(f"Processed XML result: {file_path}")
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate test execution summary."""
        total = self.aggregated_results['total_tests']
        passed = self.aggregated_results['passed']
        failed = self.aggregated_results['failed']
        skipped = self.aggregated_results['skipped']
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        return {
            "summary": {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "success_rate": round(success_rate, 2),
                "execution_time": round(self.aggregated_results['execution_time'], 2)
            },
            "test_suites": self.aggregated_results['test_suites']
        }
    
    def save_aggregated_results(self, output_file: str) -> None:
        """Save aggregated results to file."""
        summary = self.generate_summary()
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Aggregated results saved to: {output_file}")
        print(f"Total tests: {summary['summary']['total_tests']}")
        print(f"Success rate: {summary['summary']['success_rate']}%")


class ParallelTestRunner:
    """Runs tests in parallel with proper configuration."""
    
    def __init__(self, config: ExecutionConfig):
        self.config = config
        self.results = {}
    
    def run_tests(self) -> Dict[str, Any]:
        """Run tests based on configuration."""
        start_time = time.time()
        
        try:
            # Set up environment variables
            self._setup_environment()
            
            # Run tests based on configuration
            if self.config.framework == "pytest":
                results = self._run_pytest_tests()
            else:
                results = self._run_generic_tests()
            
            execution_time = time.time() - start_time
            results['execution_time'] = execution_time
            results['config'] = self.config.to_dict()
            
            return results
            
        except Exception as e:
            return {
                "error": str(e),
                "execution_time": time.time() - start_time,
                "config": self.config.to_dict()
            }
    
    def _setup_environment(self) -> None:
        """Set up environment variables for test execution."""
        os.environ['TEST_TYPE'] = self.config.test_type
        os.environ['TEST_FRAMEWORK'] = self.config.framework
        os.environ['TEST_LANGUAGE'] = self.config.language
        os.environ['TEST_CATEGORY'] = self.config.category
        os.environ['TEST_MODULE'] = self.config.module
        os.environ['TEST_ENVIRONMENT'] = self.config.environment
        
        if self.config.browser:
            os.environ['BROWSER'] = self.config.browser
        if self.config.device:
            os.environ['DEVICE'] = self.config.device
    
    def _run_pytest_tests(self) -> Dict[str, Any]:
        """Run pytest tests with proper configuration."""
        # This would integrate with pytest programmatically
        # For demonstration, we'll return mock results
        return {
            "total": 10,
            "passed": 8,
            "failed": 1,
            "skipped": 1,
            "errors": 0
        }
    
    def _run_generic_tests(self) -> Dict[str, Any]:
        """Run generic tests."""
        return {
            "total": 5,
            "passed": 5,
            "failed": 0,
            "skipped": 0,
            "errors": 0
        }


# Example usage and test functions
def test_matrix_generation():
    """Test the matrix generation functionality."""
    generator = ParallelTestMatrixGenerator()
    generator.discover_tests()
    
    # Test all scope
    all_matrix = generator.generate_matrix("all")
    assert len(all_matrix) > 0, "Should generate test configurations"
    
    # Test filtered scope
    unit_matrix = generator.generate_matrix("unit")
    assert all(config['test_type'] == 'unit' for config in unit_matrix), "Should filter unit tests"
    
    # Test API scope
    api_matrix = generator.generate_matrix("api")
    assert all(config['category'] == 'api' for config in api_matrix), "Should filter API tests"


def test_result_aggregation():
    """Test the result aggregation functionality."""
    aggregator = ResultAggregator()
    
    # Mock some test results
    aggregator.aggregated_results['total_tests'] = 100
    aggregator.aggregated_results['passed'] = 95
    aggregator.aggregated_results['failed'] = 5
    aggregator.aggregated_results['execution_time'] = 120.5
    
    summary = aggregator.generate_summary()
    
    assert summary['summary']['total_tests'] == 100
    assert summary['summary']['success_rate'] == 95.0
    assert summary['summary']['execution_time'] == 120.5


def test_parallel_runner():
    """Test the parallel test runner."""
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
    results = runner.run_tests()
    
    assert 'execution_time' in results
    assert 'config' in results
    assert results['config']['test_type'] == 'unit'


if __name__ == "__main__":
    # Example usage
    generator = ParallelTestMatrixGenerator()
    generator.discover_tests()
    
    # Generate matrix for different scopes
    scopes = ["all", "unit", "api", "e2e"]
    
    for scope in scopes:
        matrix = generator.generate_matrix(scope)
        print(f"\n{scope.upper()} scope: {len(matrix)} configurations")
        
        # Save matrix to file
        output_file = f"test_matrix_{scope}.json"
        generator.save_matrix(output_file, scope)
