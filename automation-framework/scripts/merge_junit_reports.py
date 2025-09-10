#!/usr/bin/env python3
"""
Merge multiple JUnit XML reports into a single aggregated report.

This script combines JUnit XML reports from parallel test execution
into a single comprehensive report for better visibility.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
from typing import List, Dict, Any
from datetime import datetime


def find_junit_reports(input_dir: Path) -> List[Path]:
    """Find all JUnit XML reports in the input directory."""
    reports = []
    for xml_file in input_dir.rglob("*.xml"):
        if xml_file.name != "coverage.xml":  # Exclude coverage reports
            try:
                # Try to parse as JUnit XML
                tree = ET.parse(xml_file)
                root = tree.getroot()
                if root.tag in ["testsuites", "testsuite"]:
                    reports.append(xml_file)
            except ET.ParseError:
                continue
    return reports


def merge_junit_reports(report_paths: List[Path]) -> ET.Element:
    """Merge multiple JUnit XML reports into a single root element."""
    # Create root testsuites element
    root = ET.Element("testsuites")
    root.set("name", "Parallel Test Execution")
    root.set("timestamp", datetime.now().isoformat())
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_time = 0.0
    
    for report_path in report_paths:
        try:
            tree = ET.parse(report_path)
            report_root = tree.getroot()
            
            # Handle both testsuites and testsuite elements
            if report_root.tag == "testsuites":
                for testsuite in report_root.findall("testsuite"):
                    process_testsuite(testsuite, root, report_path.name)
                    total_tests += int(testsuite.get("tests", 0))
                    total_failures += int(testsuite.get("failures", 0))
                    total_errors += int(testsuite.get("errors", 0))
                    total_time += float(testsuite.get("time", 0))
            elif report_root.tag == "testsuite":
                process_testsuite(report_root, root, report_path.name)
                total_tests += int(report_root.get("tests", 0))
                total_failures += int(report_root.get("failures", 0))
                total_errors += int(report_root.get("errors", 0))
                total_time += float(report_root.get("time", 0))
                
        except ET.ParseError as e:
            print(f"Warning: Could not parse {report_path}: {e}")
            continue
    
    # Set aggregated attributes
    root.set("tests", str(total_tests))
    root.set("failures", str(total_failures))
    root.set("errors", str(total_errors))
    root.set("time", f"{total_time:.3f}")
    
    return root


def process_testsuite(testsuite: ET.Element, root: ET.Element, source_file: str):
    """Process a single testsuite element and add it to the root."""
    # Create a copy of the testsuite
    new_testsuite = ET.Element("testsuite")
    
    # Copy attributes
    for key, value in testsuite.attrib.items():
        new_testsuite.set(key, value)
    
    # Add source file information
    new_testsuite.set("source", source_file)
    
    # Copy all child elements (testcase, properties, etc.)
    for child in testsuite:
        new_testsuite.append(child)
    
    root.append(new_testsuite)


def format_xml(element: ET.Element) -> str:
    """Format XML element with proper indentation."""
    def indent(elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    indent(element)
    return ET.tostring(element, encoding='unicode')


def main():
    """Main function to merge JUnit reports."""
    parser = argparse.ArgumentParser(description="Merge JUnit XML reports")
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing JUnit XML reports"
    )
    parser.add_argument(
        "output_file",
        type=Path,
        help="Output file for merged report"
    )
    
    args = parser.parse_args()
    
    # Find all JUnit reports
    report_paths = find_junit_reports(args.input_dir)
    
    if not report_paths:
        print("No JUnit XML reports found in input directory")
        return
    
    print(f"Found {len(report_paths)} JUnit reports:")
    for report_path in report_paths:
        print(f"  - {report_path}")
    
    # Merge reports
    merged_root = merge_junit_reports(report_paths)
    
    # Format and save
    formatted_xml = format_xml(merged_root)
    
    # Ensure output directory exists
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(args.output_file, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(formatted_xml)
    
    print(f"Merged report saved to: {args.output_file}")
    
    # Print summary
    total_tests = int(merged_root.get("tests", 0))
    total_failures = int(merged_root.get("failures", 0))
    total_errors = int(merged_root.get("errors", 0))
    total_time = float(merged_root.get("time", 0))
    
    print(f"\nSummary:")
    print(f"  Total tests: {total_tests}")
    print(f"  Failures: {total_failures}")
    print(f"  Errors: {total_errors}")
    print(f"  Total time: {total_time:.3f}s")


if __name__ == "__main__":
    main()
