#!/usr/bin/env python3
"""
Demo script showing how to use the parallel testing matrix generation.

This script demonstrates the matrix generation capabilities and shows
how to customize test configurations for different scenarios.
"""

import json
import sys
from pathlib import Path

# Add the scripts directory to the path so we can import the matrix generator
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

from generate_test_matrix import generate_test_matrix


def demo_matrix_generation():
    """Demonstrate different matrix generation scenarios."""
    
    print("🧪 Parallel Testing Matrix Generation Demo")
    print("=" * 50)
    
    # Demo 1: All tests
    print("\n1. Generating matrix for ALL tests:")
    all_matrix = generate_test_matrix("all")
    print(f"   Generated {len(all_matrix)} test configurations")
    
    # Show first few configurations
    for i, config in enumerate(all_matrix[:3]):
        print(f"   - {config['job_name']}")
    if len(all_matrix) > 3:
        print(f"   ... and {len(all_matrix) - 3} more")
    
    # Demo 2: Python only
    print("\n2. Generating matrix for PYTHON tests only:")
    python_matrix = generate_test_matrix("python")
    print(f"   Generated {len(python_matrix)} test configurations")
    
    # Demo 3: API tests only
    print("\n3. Generating matrix for API tests only:")
    api_matrix = generate_test_matrix("api")
    print(f"   Generated {len(api_matrix)} test configurations")
    
    # Demo 4: Contract tests only
    print("\n4. Generating matrix for CONTRACT tests only:")
    contract_matrix = generate_test_matrix("contract")
    print(f"   Generated {len(contract_matrix)} test configurations")
    
    # Demo 5: Show matrix structure
    print("\n5. Matrix structure example:")
    if all_matrix:
        example_config = all_matrix[0]
        print("   Configuration structure:")
        for key, value in example_config.items():
            print(f"     {key}: {value}")
    
    # Demo 6: Save matrix to file
    print("\n6. Saving matrix to file:")
    output_file = Path("demo_test_matrix.json")
    with open(output_file, 'w') as f:
        json.dump(all_matrix, f, indent=2)
    print(f"   Matrix saved to: {output_file.absolute()}")
    
    # Demo 7: Show statistics
    print("\n7. Matrix statistics:")
    stats = analyze_matrix(all_matrix)
    for key, value in stats.items():
        print(f"   {key}: {value}")


def analyze_matrix(matrix):
    """Analyze matrix and return statistics."""
    stats = {
        "Total Configurations": len(matrix),
        "Test Types": len(set(config["type"] for config in matrix)),
        "Frameworks": len(set(config["framework"] for config in matrix)),
        "Languages": len(set(config["language"] for config in matrix)),
        "Categories": len(set(config["category"] for config in matrix)),
        "Environments": len(set(config["environment"] for config in matrix))
    }
    
    # Count by test type
    test_types = {}
    for config in matrix:
        test_type = config["type"]
        test_types[test_type] = test_types.get(test_type, 0) + 1
    
    stats["By Test Type"] = test_types
    
    return stats


def demo_custom_matrix():
    """Demonstrate how to create custom matrix configurations."""
    
    print("\n" + "=" * 50)
    print("🎯 Custom Matrix Configuration Demo")
    print("=" * 50)
    
    # Create a custom matrix for a specific scenario
    custom_matrix = [
        {
            "type": "smoke",
            "framework": "pytest",
            "language": "python",
            "category": "critical",
            "environment": "production",
            "job_name": "smoke_pytest_python_critical_production",
            "test_path": "tests/smoke",
            "markers": ["smoke", "critical", "production"],
            "timeout": 300,  # 5 minutes
            "retries": 2
        },
        {
            "type": "performance",
            "framework": "pytest",
            "language": "python", 
            "category": "load",
            "environment": "staging",
            "job_name": "performance_pytest_python_load_staging",
            "test_path": "tests/performance",
            "markers": ["performance", "load", "staging"],
            "timeout": 1800,  # 30 minutes
            "retries": 1
        }
    ]
    
    print("Custom matrix configuration:")
    for config in custom_matrix:
        print(f"\n  {config['job_name']}:")
        print(f"    Type: {config['type']}")
        print(f"    Framework: {config['framework']}")
        print(f"    Language: {config['language']}")
        print(f"    Category: {config['category']}")
        print(f"    Environment: {config['environment']}")
        print(f"    Timeout: {config['timeout']}s")
        print(f"    Retries: {config['retries']}")
    
    # Save custom matrix
    custom_file = Path("custom_test_matrix.json")
    with open(custom_file, 'w') as f:
        json.dump(custom_matrix, f, indent=2)
    print(f"\nCustom matrix saved to: {custom_file.absolute()}")


def demo_github_actions_integration():
    """Demonstrate GitHub Actions integration patterns."""
    
    print("\n" + "=" * 50)
    print("🚀 GitHub Actions Integration Demo")
    print("=" * 50)
    
    # Show how the matrix would be used in GitHub Actions
    github_actions_example = """
# Example GitHub Actions workflow using the matrix
jobs:
  generate-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - name: Generate test matrix
        run: |
          python scripts/generate_test_matrix.py \\
            --scope "${{ github.event.inputs.test_scope || 'all' }}" \\
            --output test_matrix.json
      - name: Set matrix data
        run: echo "matrix=$(jq -c . < test_matrix.json)" >> $GITHUB_OUTPUT

  parallel-tests:
    runs-on: ubuntu-latest
    needs: generate-matrix
    strategy:
      fail-fast: false
      max-parallel: 10
      matrix:
        test_config: ${{ fromJSON(needs.generate-matrix.outputs.matrix) }}
    steps:
      - name: Run tests
        run: |
          echo "Running ${{ matrix.test_config.type }} tests"
          echo "Framework: ${{ matrix.test_config.framework }}"
          echo "Language: ${{ matrix.test_config.language }}"
"""
    
    print("GitHub Actions workflow example:")
    print(github_actions_example)
    
    # Show environment variables that would be available
    print("Environment variables available in each job:")
    env_vars = [
        "TEST_TYPE",
        "TEST_FRAMEWORK", 
        "TEST_LANGUAGE",
        "TEST_CATEGORY",
        "ENVIRONMENT"
    ]
    
    for var in env_vars:
        print(f"  - {var}")


def main():
    """Main demo function."""
    try:
        demo_matrix_generation()
        demo_custom_matrix()
        demo_github_actions_integration()
        
        print("\n" + "=" * 50)
        print("✅ Demo completed successfully!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Review the generated matrix files")
        print("2. Customize the matrix generation script for your needs")
        print("3. Integrate with your GitHub Actions workflows")
        print("4. Set up parallel test execution")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
