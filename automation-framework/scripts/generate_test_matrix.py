#!/usr/bin/env python3
"""
Test Matrix Generator for Parallel Testing

This script generates test matrices for parallel execution in GitHub Actions.
It demonstrates how to dynamically create test configurations based on
available tests and desired scope.

Usage:
    python scripts/generate_test_matrix.py --scope all --output test_matrix.json
    python scripts/generate_test_matrix.py --scope unit --output unit_matrix.json
    python scripts/generate_test_matrix.py --scope e2e --output e2e_matrix.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.parallel_testing_example import ParallelTestMatrixGenerator


def main():
    """Main function to generate test matrix."""
    parser = argparse.ArgumentParser(description='Generate test matrix for parallel execution')
    parser.add_argument(
        '--scope',
        choices=['all', 'unit', 'integration', 'e2e', 'performance', 'api', 'ui'],
        default='all',
        help='Test scope to include in matrix'
    )
    parser.add_argument(
        '--output',
        default='test_matrix.json',
        help='Output file for the test matrix'
    )
    parser.add_argument(
        '--base-path',
        default='tests',
        help='Base path to search for tests'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Generating test matrix for scope: {args.scope}")
        print(f"Base path: {args.base_path}")
        print(f"Output file: {args.output}")
    
    # Create generator and discover tests
    generator = ParallelTestMatrixGenerator(args.base_path)
    generator.discover_tests()
    
    # Generate and save matrix
    generator.save_matrix(args.output, args.scope)
    
    # Load and display summary
    with open(args.output, 'r') as f:
        matrix = json.load(f)
    
    print(f"\n✅ Generated test matrix with {len(matrix)} configurations")
    print(f"📁 Saved to: {args.output}")
    
    if args.verbose:
        print("\n📋 Matrix Summary:")
        test_types = {}
        frameworks = {}
        environments = {}
        
        for config in matrix:
            test_type = config['test_type']
            framework = config['framework']
            environment = config['environment']
            
            test_types[test_type] = test_types.get(test_type, 0) + 1
            frameworks[framework] = frameworks.get(framework, 0) + 1
            environments[environment] = environments.get(environment, 0) + 1
        
        print(f"  Test Types: {dict(test_types)}")
        print(f"  Frameworks: {dict(frameworks)}")
        print(f"  Environments: {dict(environments)}")
        
        if args.scope == 'e2e':
            browsers = {}
            devices = {}
            for config in matrix:
                if config.get('browser'):
                    browsers[config['browser']] = browsers.get(config['browser'], 0) + 1
                if config.get('device'):
                    devices[config['device']] = devices.get(config['device'], 0) + 1
            
            if browsers:
                print(f"  Browsers: {dict(browsers)}")
            if devices:
                print(f"  Devices: {dict(devices)}")


if __name__ == "__main__":
    main()
