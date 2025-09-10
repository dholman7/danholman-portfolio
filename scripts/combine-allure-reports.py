#!/usr/bin/env python3
"""
Script to combine Allure reports from all modules into a single comprehensive report.
This script merges Allure results from multiple modules and generates a unified report.
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Any
import uuid
from datetime import datetime


def combine_allure_results(source_dirs: List[str], output_dir: str) -> None:
    """
    Combine Allure results from multiple source directories into a single output directory.
    
    Args:
        source_dirs: List of directories containing Allure results
        output_dir: Output directory for combined results
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Track processed files to avoid duplicates
    processed_files = set()
    
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"Warning: Source directory {source_dir} does not exist, skipping...")
            continue
            
        print(f"Processing {source_dir}...")
        
        # Copy all result files
        for result_file in source_path.glob("*-result.json"):
            if result_file.name not in processed_files:
                shutil.copy2(result_file, output_path / result_file.name)
                processed_files.add(result_file.name)
        
        # Copy all container files
        for container_file in source_path.glob("*-container.json"):
            if container_file.name not in processed_files:
                shutil.copy2(container_file, output_path / container_file.name)
                processed_files.add(container_file.name)
        
        # Copy all attachment files
        for attachment_file in source_path.glob("*-attachment.*"):
            if attachment_file.name not in processed_files:
                shutil.copy2(attachment_file, output_path / attachment_file.name)
                processed_files.add(attachment_file.name)
    
    print(f"Combined {len(processed_files)} files into {output_dir}")


def create_combined_summary(allure_results_dir: str, output_file: str) -> None:
    """
    Create a summary of the combined Allure results.
    
    Args:
        allure_results_dir: Directory containing combined Allure results
        output_file: Path to output summary file
    """
    results_path = Path(allure_results_dir)
    
    # Collect statistics
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    broken_tests = 0
    skipped_tests = 0
    modules = set()
    
    for result_file in results_path.glob("*-result.json"):
        try:
            with open(result_file, 'r') as f:
                data = json.load(f)
                
            total_tests += 1
            
            # Extract module name from test name or file path
            test_name = data.get('name', '')
            if 'automation-framework' in test_name.lower():
                modules.add('Automation Framework')
            elif 'ai-rulesets' in test_name.lower():
                modules.add('AI Rulesets')
            elif 'cloud-native' in test_name.lower():
                modules.add('Cloud Native App')
            elif 'playwright' in test_name.lower() or 'react' in test_name.lower():
                modules.add('React Playwright Demo')
            
            # Count test status
            status = data.get('status', 'unknown')
            if status == 'passed':
                passed_tests += 1
            elif status == 'failed':
                failed_tests += 1
            elif status == 'broken':
                broken_tests += 1
            elif status == 'skipped':
                skipped_tests += 1
                
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not process {result_file}: {e}")
            continue
    
    # Calculate pass rate
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Create summary
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "broken_tests": broken_tests,
        "skipped_tests": skipped_tests,
        "pass_rate": round(pass_rate, 2),
        "modules": list(modules),
        "generated_by": "combine-allure-reports.py"
    }
    
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary created: {output_file}")
    print(f"Total tests: {total_tests}")
    print(f"Pass rate: {pass_rate:.2f}%")
    print(f"Modules: {', '.join(modules)}")


def main():
    parser = argparse.ArgumentParser(description='Combine Allure reports from multiple modules')
    parser.add_argument('--sources', nargs='+', required=True,
                       help='Source directories containing Allure results')
    parser.add_argument('--output', required=True,
                       help='Output directory for combined results')
    parser.add_argument('--summary', 
                       help='Path for summary JSON file')
    
    args = parser.parse_args()
    
    # Combine results
    combine_allure_results(args.sources, args.output)
    
    # Create summary if requested
    if args.summary:
        create_combined_summary(args.output, args.summary)


if __name__ == "__main__":
    main()
