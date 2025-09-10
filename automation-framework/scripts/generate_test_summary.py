#!/usr/bin/env python3
"""
Generate a comprehensive test summary from parallel test execution results.

This script analyzes test artifacts from parallel execution and creates
a markdown summary with statistics, trends, and insights.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
from typing import Dict, List, Any, Tuple
from datetime import datetime
import re


def find_test_artifacts(input_dir: Path) -> Dict[str, List[Path]]:
    """Find and categorize test artifacts."""
    artifacts = {
        "html_reports": [],
        "xml_reports": [],
        "coverage_reports": [],
        "json_reports": []
    }
    
    for file_path in input_dir.rglob("*"):
        if file_path.is_file():
            if file_path.suffix == ".html" and "coverage" not in file_path.name:
                artifacts["html_reports"].append(file_path)
            elif file_path.suffix == ".xml" and "coverage" not in file_path.name:
                artifacts["xml_reports"].append(file_path)
            elif "coverage" in file_path.name:
                artifacts["coverage_reports"].append(file_path)
            elif file_path.suffix == ".json":
                artifacts["json_reports"].append(file_path)
    
    return artifacts


def parse_junit_xml(xml_path: Path) -> Dict[str, Any]:
    """Parse JUnit XML report and extract statistics."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Handle both testsuites and testsuite elements
        if root.tag == "testsuites":
            total_tests = int(root.get("tests", 0))
            total_failures = int(root.get("failures", 0))
            total_errors = int(root.get("errors", 0))
            total_time = float(root.get("time", 0))
        else:
            total_tests = int(root.get("tests", 0))
            total_failures = int(root.get("failures", 0))
            total_errors = int(root.get("errors", 0))
            total_time = float(root.get("time", 0))
        
        return {
            "file": xml_path.name,
            "tests": total_tests,
            "failures": total_failures,
            "errors": total_errors,
            "time": total_time,
            "success_rate": ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
        }
    except Exception as e:
        print(f"Warning: Could not parse {xml_path}: {e}")
        return {
            "file": xml_path.name,
            "tests": 0,
            "failures": 0,
            "errors": 0,
            "time": 0,
            "success_rate": 0
        }


def parse_coverage_report(coverage_path: Path) -> Dict[str, Any]:
    """Parse coverage report and extract coverage statistics."""
    try:
        if coverage_path.suffix == ".xml":
            tree = ET.parse(coverage_path)
            root = tree.getroot()
            
            # Look for coverage data in the XML
            coverage_data = {}
            for line in root.findall(".//line"):
                hits = int(line.get("hits", 0))
                if hits > 0:
                    coverage_data["covered_lines"] = coverage_data.get("covered_lines", 0) + 1
                coverage_data["total_lines"] = coverage_data.get("total_lines", 0) + 1
            
            if coverage_data.get("total_lines", 0) > 0:
                coverage_data["percentage"] = (coverage_data["covered_lines"] / coverage_data["total_lines"]) * 100
            else:
                coverage_data["percentage"] = 0
                
            return coverage_data
        else:
            # For other coverage formats, return basic info
            return {"file": coverage_path.name, "percentage": 0}
    except Exception as e:
        print(f"Warning: Could not parse coverage {coverage_path}: {e}")
        return {"file": coverage_path.name, "percentage": 0}


def categorize_tests(test_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Categorize tests by type and framework."""
    categories = {
        "unit": [],
        "integration": [],
        "component": [],
        "e2e": [],
        "api": [],
        "contract": []
    }
    
    for test in test_data:
        file_name = test["file"].lower()
        
        if "unit" in file_name:
            categories["unit"].append(test)
        elif "integration" in file_name:
            categories["integration"].append(test)
        elif "component" in file_name:
            categories["component"].append(test)
        elif "e2e" in file_name:
            categories["e2e"].append(test)
        elif "api" in file_name:
            categories["api"].append(test)
        elif "contract" in file_name:
            categories["contract"].append(test)
        else:
            # Default to unit if no category found
            categories["unit"].append(test)
    
    return categories


def generate_summary_markdown(
    test_data: List[Dict[str, Any]], 
    coverage_data: List[Dict[str, Any]], 
    artifacts: Dict[str, List[Path]]
) -> str:
    """Generate markdown summary of test results."""
    
    # Calculate overall statistics
    total_tests = sum(test["tests"] for test in test_data)
    total_failures = sum(test["failures"] for test in test_data)
    total_errors = sum(test["errors"] for test in test_data)
    total_time = sum(test["time"] for test in test_data)
    overall_success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
    
    # Calculate average coverage
    avg_coverage = sum(cov.get("percentage", 0) for cov in coverage_data) / len(coverage_data) if coverage_data else 0
    
    # Categorize tests
    categories = categorize_tests(test_data)
    
    # Generate markdown
    markdown = f"""# 🧪 Parallel Test Execution Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📊 Overall Statistics

| Metric | Value |
|--------|-------|
| **Total Tests** | {total_tests:,} |
| **Passed** | {total_tests - total_failures - total_errors:,} |
| **Failed** | {total_failures:,} |
| **Errors** | {total_errors:,} |
| **Success Rate** | {overall_success_rate:.1f}% |
| **Total Execution Time** | {total_time:.2f}s |
| **Average Coverage** | {avg_coverage:.1f}% |

## 📈 Test Categories

"""
    
    # Add category breakdown
    for category, tests in categories.items():
        if tests:
            cat_tests = sum(test["tests"] for test in tests)
            cat_failures = sum(test["failures"] for test in tests)
            cat_errors = sum(test["errors"] for test in tests)
            cat_time = sum(test["time"] for test in tests)
            cat_success_rate = ((cat_tests - cat_failures - cat_errors) / cat_tests * 100) if cat_tests > 0 else 0
            
            markdown += f"""### {category.title()} Tests
- **Tests:** {cat_tests:,}
- **Success Rate:** {cat_success_rate:.1f}%
- **Execution Time:** {cat_time:.2f}s
- **Job Count:** {len(tests)}

"""
    
    # Add artifact summary
    markdown += f"""## 📁 Generated Artifacts

| Type | Count |
|------|-------|
| HTML Reports | {len(artifacts['html_reports'])} |
| XML Reports | {len(artifacts['xml_reports'])} |
| Coverage Reports | {len(artifacts['coverage_reports'])} |
| JSON Reports | {len(artifacts['json_reports'])} |

## 🔍 Detailed Results

### Test Execution Details

| Job | Tests | Failures | Errors | Time (s) | Success Rate |
|-----|-------|----------|--------|----------|--------------|
"""
    
    # Add detailed test results
    for test in sorted(test_data, key=lambda x: x["file"]):
        markdown += f"| {test['file']} | {test['tests']} | {test['failures']} | {test['errors']} | {test['time']:.2f} | {test['success_rate']:.1f}% |\n"
    
    # Add coverage details if available
    if coverage_data:
        markdown += f"""
### Coverage Details

| Report | Coverage % |
|--------|------------|
"""
        for cov in coverage_data:
            markdown += f"| {cov.get('file', 'Unknown')} | {cov.get('percentage', 0):.1f}% |\n"
    
    # Add recommendations
    markdown += f"""
## 💡 Recommendations

"""
    
    if overall_success_rate < 95:
        markdown += "- ⚠️ **Low Success Rate**: Consider investigating failing tests and improving test stability\n"
    
    if avg_coverage < 80:
        markdown += "- 📊 **Low Coverage**: Consider adding more test cases to improve code coverage\n"
    
    if total_time > 300:  # 5 minutes
        markdown += "- ⏱️ **Long Execution Time**: Consider optimizing slow tests or increasing parallelization\n"
    
    if total_failures > 0 or total_errors > 0:
        markdown += "- 🐛 **Test Failures**: Review failed tests and fix underlying issues\n"
    
    markdown += "- ✅ **Parallel Execution**: Successfully executed tests in parallel for improved efficiency\n"
    
    return markdown


def main():
    """Main function to generate test summary."""
    parser = argparse.ArgumentParser(description="Generate test execution summary")
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing test artifacts"
    )
    parser.add_argument(
        "output_file",
        type=Path,
        help="Output file for test summary markdown"
    )
    
    args = parser.parse_args()
    
    # Find test artifacts
    artifacts = find_test_artifacts(args.input_dir)
    
    print(f"Found artifacts:")
    for artifact_type, files in artifacts.items():
        print(f"  {artifact_type}: {len(files)} files")
    
    # Parse test data
    test_data = []
    for xml_path in artifacts["xml_reports"]:
        test_data.append(parse_junit_xml(xml_path))
    
    # Parse coverage data
    coverage_data = []
    for cov_path in artifacts["coverage_reports"]:
        coverage_data.append(parse_coverage_report(cov_path))
    
    # Generate summary
    summary = generate_summary_markdown(test_data, coverage_data, artifacts)
    
    # Save summary
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_file, 'w') as f:
        f.write(summary)
    
    print(f"Test summary saved to: {args.output_file}")
    
    # Print quick stats
    total_tests = sum(test["tests"] for test in test_data)
    total_failures = sum(test["failures"] for test in test_data)
    total_errors = sum(test["errors"] for test in test_data)
    overall_success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nQuick Stats:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Success Rate: {overall_success_rate:.1f}%")
    print(f"  Execution Time: {sum(test['time'] for test in test_data):.2f}s")


if __name__ == "__main__":
    main()
