#!/usr/bin/env python3
"""
Generate test matrix for parallel testing in GitHub Actions.

This script creates a dynamic test matrix based on available test configurations,
similar to the plans_matrix.yaml approach but for AI test generation framework.
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Any


def generate_test_matrix(scope: str = "all") -> List[Dict[str, Any]]:
    """
    Generate test matrix based on scope and available test configurations.
    
    Args:
        scope: Test scope (all, python, typescript, api, contract)
        
    Returns:
        List of test configurations for matrix strategy
    """
    # Base test configurations
    test_configs = []
    
    # Python testing configurations
    if scope in ["all", "python"]:
        python_configs = [
            {
                "type": "unit",
                "framework": "pytest",
                "language": "python",
                "category": "core",
                "test_path": "tests/unit",
                "markers": ["unit", "python"]
            },
            {
                "type": "component",
                "framework": "pytest", 
                "language": "python",
                "category": "integration",
                "test_path": "tests/component",
                "markers": ["component", "python"]
            },
            {
                "type": "integration",
                "framework": "pytest",
                "language": "python", 
                "category": "api",
                "test_path": "tests/integration",
                "markers": ["integration", "api", "python"]
            },
            {
                "type": "e2e",
                "framework": "pytest",
                "language": "python",
                "category": "end-to-end",
                "test_path": "tests/e2e",
                "markers": ["e2e", "python"]
            }
        ]
        test_configs.extend(python_configs)
    
    # TypeScript/JavaScript testing configurations
    if scope in ["all", "typescript"]:
        typescript_configs = [
            {
                "type": "unit",
                "framework": "jest",
                "language": "typescript",
                "category": "core",
                "test_path": "tests/unit",
                "markers": ["unit", "typescript"]
            },
            {
                "type": "integration",
                "framework": "jest",
                "language": "typescript",
                "category": "api",
                "test_path": "tests/integration", 
                "markers": ["integration", "api", "typescript"]
            }
        ]
        test_configs.extend(typescript_configs)
    
    # API testing configurations
    if scope in ["all", "api"]:
        api_configs = [
            {
                "type": "api",
                "framework": "pytest",
                "language": "python",
                "category": "rest",
                "test_path": "tests/integration",
                "markers": ["api", "rest", "python"]
            },
            {
                "type": "api",
                "framework": "pytest", 
                "language": "python",
                "category": "graphql",
                "test_path": "tests/integration",
                "markers": ["api", "graphql", "python"]
            }
        ]
        test_configs.extend(api_configs)
    
    # Contract testing configurations
    if scope in ["all", "contract"]:
        contract_configs = [
            {
                "type": "contract",
                "framework": "pytest",
                "language": "python",
                "category": "pact",
                "test_path": "tests/integration",
                "markers": ["contract", "pact", "python"]
            }
        ]
        test_configs.extend(contract_configs)
    
    # Add environment-specific configurations
    environments = ["staging", "production"]
    expanded_configs = []
    
    for config in test_configs:
        for env in environments:
            expanded_config = config.copy()
            expanded_config["environment"] = env
            expanded_config["job_name"] = f"{config['type']}_{config['framework']}_{config['language']}_{config['category']}_{env}"
            expanded_configs.append(expanded_config)
    
    return expanded_configs


def main():
    """Main function to generate and save test matrix."""
    parser = argparse.ArgumentParser(description="Generate test matrix for parallel testing")
    parser.add_argument(
        "--scope",
        default="all",
        choices=["all", "python", "typescript", "api", "contract"],
        help="Test scope to include in matrix"
    )
    parser.add_argument(
        "--output",
        default="test_matrix.json",
        help="Output file for test matrix JSON"
    )
    parser.add_argument(
        "--max-jobs",
        type=int,
        default=20,
        help="Maximum number of parallel jobs"
    )
    
    args = parser.parse_args()
    
    # Generate test matrix
    matrix = generate_test_matrix(args.scope)
    
    # Limit number of jobs if specified
    if len(matrix) > args.max_jobs:
        print(f"Warning: Generated {len(matrix)} jobs, limiting to {args.max_jobs}")
        matrix = matrix[:args.max_jobs]
    
    # Save matrix to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(matrix, f, indent=2)
    
    print(f"Generated test matrix with {len(matrix)} configurations:")
    for i, config in enumerate(matrix[:5]):  # Show first 5
        print(f"  {i+1}. {config['job_name']}")
    
    if len(matrix) > 5:
        print(f"  ... and {len(matrix) - 5} more")
    
    print(f"Matrix saved to: {output_path.absolute()}")


if __name__ == "__main__":
    main()
