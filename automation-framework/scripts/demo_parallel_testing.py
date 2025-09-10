#!/usr/bin/env python3
"""
Parallel Testing Demo Script

This script demonstrates how to use the parallel testing system
to generate test matrices and simulate parallel test execution.

Usage:
    python scripts/demo_parallel_testing.py
    python scripts/demo_parallel_testing.py --scope e2e
    python scripts/demo_parallel_testing.py --scope all --output demo_matrix.json
"""

import argparse
import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.parallel_testing_example import (
    ParallelTestMatrixGenerator,
    TestResultAggregator,
    ParallelTestRunner,
    TestConfig
)


def demo_matrix_generation(scope: str = "all", output_file: str = None):
    """Demonstrate test matrix generation."""
    print(f"🔍 Generating test matrix for scope: {scope}")
    
    # Create generator and discover tests
    generator = ParallelTestMatrixGenerator("tests")
    generator.discover_tests()
    
    # Generate matrix
    matrix = generator.generate_matrix(scope)
    
    print(f"✅ Generated {len(matrix)} test configurations")
    
    # Display summary
    test_types = {}
    frameworks = {}
    environments = {}
    browsers = {}
    devices = {}
    
    for config in matrix:
        test_type = config['test_type']
        framework = config['framework']
        environment = config['environment']
        browser = config.get('browser')
        device = config.get('device')
        
        test_types[test_type] = test_types.get(test_type, 0) + 1
        frameworks[framework] = frameworks.get(framework, 0) + 1
        environments[environment] = environments.get(environment, 0) + 1
        
        if browser:
            browsers[browser] = browsers.get(browser, 0) + 1
        if device:
            devices[device] = devices.get(device, 0) + 1
    
    print(f"\n📊 Matrix Summary:")
    print(f"  Test Types: {dict(test_types)}")
    print(f"  Frameworks: {dict(frameworks)}")
    print(f"  Environments: {dict(environments)}")
    
    if browsers:
        print(f"  Browsers: {dict(browsers)}")
    if devices:
        print(f"  Devices: {dict(devices)}")
    
    # Save matrix if output file specified
    if output_file:
        generator.save_matrix(output_file, scope)
        print(f"\n💾 Matrix saved to: {output_file}")
    
    return matrix


def demo_test_execution(matrix: list, max_tests: int = 3):
    """Demonstrate parallel test execution simulation."""
    print(f"\n🚀 Simulating parallel test execution (max {max_tests} tests)")
    
    results = []
    
    for i, config_dict in enumerate(matrix[:max_tests]):
        print(f"\n📋 Test {i+1}/{min(len(matrix), max_tests)}: {config_dict['test_type']} - {config_dict.get('browser', 'N/A')} - {config_dict.get('device', 'N/A')}")
        
        # Create test configuration
        config = TestConfig(**config_dict)
        
        # Create and run test runner
        runner = ParallelTestRunner(config)
        result = runner.run_tests()
        
        results.append(result)
        
        print(f"  ⏱️  Execution time: {result.get('execution_time', 0):.2f}s")
        print(f"  📈 Results: {result.get('total', 0)} total, {result.get('passed', 0)} passed, {result.get('failed', 0)} failed")
    
    return results


def demo_result_aggregation(results: list):
    """Demonstrate result aggregation."""
    print(f"\n📊 Aggregating results from {len(results)} test executions")
    
    # Create aggregator
    aggregator = TestResultAggregator()
    
    # Simulate adding results to aggregator
    for result in results:
        if 'total' in result:
            aggregator.aggregated_results['total_tests'] += result.get('total', 0)
            aggregator.aggregated_results['passed'] += result.get('passed', 0)
            aggregator.aggregated_results['failed'] += result.get('failed', 0)
            aggregator.aggregated_results['skipped'] += result.get('skipped', 0)
            aggregator.aggregated_results['execution_time'] += result.get('execution_time', 0.0)
    
    # Generate summary
    summary = aggregator.generate_summary()
    
    print(f"✅ Aggregated Results:")
    print(f"  Total Tests: {summary['summary']['total_tests']}")
    print(f"  Passed: {summary['summary']['passed']}")
    print(f"  Failed: {summary['summary']['failed']}")
    print(f"  Skipped: {summary['summary']['skipped']}")
    print(f"  Success Rate: {summary['summary']['success_rate']}%")
    print(f"  Total Execution Time: {summary['summary']['execution_time']:.2f}s")
    
    return summary


def demo_github_actions_workflow():
    """Demonstrate GitHub Actions workflow concepts."""
    print(f"\n🔧 GitHub Actions Workflow Concepts:")
    print(f"  1. Generate Matrix Job:")
    print(f"     - Discovers available tests")
    print(f"     - Generates test configurations")
    print(f"     - Outputs matrix for parallel execution")
    print(f"")
    print(f"  2. Parallel Tests Job:")
    print(f"     - Runs tests in parallel using matrix strategy")
    print(f"     - Each job runs specific test configuration")
    print(f"     - Generates individual test reports")
    print(f"")
    print(f"  3. Merge Results Job:")
    print(f"     - Downloads all test artifacts")
    print(f"     - Merges Allure reports")
    print(f"     - Combines HTML and XML reports")
    print(f"     - Generates comprehensive summary")
    print(f"")
    print(f"🎯 Benefits:")
    print(f"  - Faster execution through parallelization")
    print(f"  - Comprehensive test coverage")
    print(f"  - Detailed reporting and analytics")
    print(f"  - Scalable test execution")


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(description='Demonstrate parallel testing system')
    parser.add_argument(
        '--scope',
        choices=['all', 'unit', 'integration', 'e2e', 'performance', 'api', 'ui'],
        default='all',
        help='Test scope to demonstrate'
    )
    parser.add_argument(
        '--output',
        help='Output file for test matrix'
    )
    parser.add_argument(
        '--max-tests',
        type=int,
        default=3,
        help='Maximum number of tests to simulate'
    )
    parser.add_argument(
        '--workflow-only',
        action='store_true',
        help='Show only GitHub Actions workflow concepts'
    )
    
    args = parser.parse_args()
    
    print("🧪 Parallel Testing Demo")
    print("=" * 50)
    
    if args.workflow_only:
        demo_github_actions_workflow()
        return
    
    # Generate test matrix
    matrix = demo_matrix_generation(args.scope, args.output)
    
    if not matrix:
        print("❌ No test configurations found")
        return
    
    # Simulate test execution
    results = demo_test_execution(matrix, args.max_tests)
    
    # Aggregate results
    summary = demo_result_aggregation(results)
    
    # Show workflow concepts
    demo_github_actions_workflow()
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"   Generated {len(matrix)} test configurations")
    print(f"   Simulated {len(results)} test executions")
    print(f"   Aggregated results with {summary['summary']['success_rate']}% success rate")


if __name__ == "__main__":
    main()
