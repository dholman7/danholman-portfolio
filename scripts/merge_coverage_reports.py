#!/usr/bin/env python3
"""
Merge coverage reports from multiple modules into a single combined report.
This script reads coverage data from multiple modules and creates a unified coverage report.
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List, Any
import xml.etree.ElementTree as ET


def find_coverage_files(coverage_dir: Path) -> Dict[str, Any]:
    """Find coverage files in a directory and return their types and paths."""
    coverage_files = {}
    
    # Look for common coverage file types
    coverage_patterns = {
        'lcov': 'lcov.info',
        'cobertura': 'cobertura.xml',
        'json': 'coverage-final.json',
        'html': 'index.html'
    }
    
    for coverage_type, filename in coverage_patterns.items():
        file_path = coverage_dir / filename
        if file_path.exists():
            coverage_files[coverage_type] = file_path
    
    return coverage_files


def parse_lcov_file(lcov_path: Path) -> Dict[str, Any]:
    """Parse LCOV coverage file and extract coverage data."""
    coverage_data = {
        'lines_covered': 0,
        'lines_total': 0,
        'branches_covered': 0,
        'branches_total': 0,
        'functions_covered': 0,
        'functions_total': 0,
        'files': []
    }
    
    try:
        with open(lcov_path, 'r') as f:
            content = f.read()
        
        # Simple LCOV parsing - look for summary lines
        lines = content.split('\n')
        for line in lines:
            if line.startswith('LF:'):  # Lines found
                coverage_data['lines_total'] += int(line.split(':')[1])
            elif line.startswith('LH:'):  # Lines hit
                coverage_data['lines_covered'] += int(line.split(':')[1])
            elif line.startswith('BF:'):  # Branches found
                coverage_data['branches_total'] += int(line.split(':')[1])
            elif line.startswith('BH:'):  # Branches hit
                coverage_data['branches_covered'] += int(line.split(':')[1])
            elif line.startswith('FNF:'):  # Functions found
                coverage_data['functions_total'] += int(line.split(':')[1])
            elif line.startswith('FNH:'):  # Functions hit
                coverage_data['functions_covered'] += int(line.split(':')[1])
    
    except Exception as e:
        print(f"Error parsing LCOV file {lcov_path}: {e}")
    
    return coverage_data


def parse_cobertura_file(cobertura_path: Path) -> Dict[str, Any]:
    """Parse Cobertura XML coverage file and extract coverage data."""
    coverage_data = {
        'lines_covered': 0,
        'lines_total': 0,
        'branches_covered': 0,
        'branches_total': 0,
        'functions_covered': 0,
        'functions_total': 0,
        'files': []
    }
    
    try:
        tree = ET.parse(cobertura_path)
        root = tree.getroot()
        
        # Extract coverage data from XML
        coverage_data['lines_covered'] = int(float(root.get('lines-covered', 0)))
        coverage_data['lines_total'] = int(float(root.get('lines-valid', 0)))
        coverage_data['branches_covered'] = int(float(root.get('branches-covered', 0)))
        coverage_data['branches_total'] = int(float(root.get('branches-valid', 0)))
        
    except Exception as e:
        print(f"Error parsing Cobertura file {cobertura_path}: {e}")
    
    return coverage_data


def parse_json_coverage_file(json_path: Path) -> Dict[str, Any]:
    """Parse JSON coverage file and extract coverage data."""
    coverage_data = {
        'lines_covered': 0,
        'lines_total': 0,
        'branches_covered': 0,
        'branches_total': 0,
        'functions_covered': 0,
        'functions_total': 0,
        'files': []
    }
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Extract coverage data from JSON
        for file_path, file_data in data.items():
            if 's' in file_data:  # Statement coverage
                coverage_data['lines_total'] += len(file_data['s'])
                coverage_data['lines_covered'] += sum(1 for v in file_data['s'].values() if v > 0)
            
            if 'b' in file_data:  # Branch coverage
                coverage_data['branches_total'] += len(file_data['b'])
                coverage_data['branches_covered'] += sum(1 for v in file_data['b'].values() if v > 0)
            
            if 'f' in file_data:  # Function coverage
                coverage_data['functions_total'] += len(file_data['f'])
                coverage_data['functions_covered'] += sum(1 for v in file_data['f'].values() if v > 0)
    
    except Exception as e:
        print(f"Error parsing JSON coverage file {json_path}: {e}")
    
    return coverage_data


def merge_coverage_data(module_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Merge coverage data from multiple modules."""
    merged_data = {
        'lines_covered': 0,
        'lines_total': 0,
        'branches_covered': 0,
        'branches_total': 0,
        'functions_covered': 0,
        'functions_total': 0,
        'modules': module_data,
        'files': []
    }
    
    # Sum up coverage data from all modules
    for module_name, module_coverage in module_data.items():
        merged_data['lines_covered'] += module_coverage.get('lines_covered', 0)
        merged_data['lines_total'] += module_coverage.get('lines_total', 0)
        merged_data['branches_covered'] += module_coverage.get('branches_covered', 0)
        merged_data['branches_total'] += module_coverage.get('branches_total', 0)
        merged_data['functions_covered'] += module_coverage.get('functions_covered', 0)
        merged_data['functions_total'] += module_coverage.get('functions_total', 0)
    
    return merged_data


def calculate_percentage(covered: int, total: int) -> float:
    """Calculate coverage percentage."""
    if total == 0:
        return 0.0
    return (covered / total) * 100


def generate_combined_html(merged_data: Dict[str, Any], output_dir: Path) -> None:
    """Generate combined HTML coverage report."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Code Coverage Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            border-left: 4px solid #007bff;
        }}
        .metric h3 {{
            margin: 0 0 10px 0;
            color: #555;
            font-size: 14px;
            text-transform: uppercase;
        }}
        .metric .percentage {{
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .metric .count {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}
        .modules {{
            margin-top: 30px;
        }}
        .module {{
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 6px;
            background: #fafafa;
        }}
        .module h3 {{
            margin: 0 0 15px 0;
            color: #333;
        }}
        .module-metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .module-metric {{
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 4px;
        }}
        .module-metric .label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .module-metric .value {{
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }}
        .overall {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin-bottom: 30px;
        }}
        .overall h2 {{
            margin: 0 0 20px 0;
            text-align: center;
        }}
        .overall .summary {{
            margin-bottom: 0;
        }}
        .overall .metric {{
            background: rgba(255,255,255,0.1);
            border-left: 4px solid rgba(255,255,255,0.3);
        }}
        .overall .metric h3 {{
            color: rgba(255,255,255,0.9);
        }}
        .overall .metric .percentage {{
            color: white;
        }}
        .overall .metric .count {{
            color: rgba(255,255,255,0.8);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Combined Code Coverage Report</h1>
        <p style="text-align: center; color: #666; margin-bottom: 30px;">
            Comprehensive coverage analysis from all modules in the portfolio
        </p>
        
        <div class="overall">
            <h2>Overall Coverage Summary</h2>
            <div class="summary">
                <div class="metric">
                    <h3>Lines</h3>
                    <div class="percentage">{calculate_percentage(merged_data['lines_covered'], merged_data['lines_total']):.1f}%</div>
                    <div class="count">{merged_data['lines_covered']} / {merged_data['lines_total']}</div>
                </div>
                <div class="metric">
                    <h3>Branches</h3>
                    <div class="percentage">{calculate_percentage(merged_data['branches_covered'], merged_data['branches_total']):.1f}%</div>
                    <div class="count">{merged_data['branches_covered']} / {merged_data['branches_total']}</div>
                </div>
                <div class="metric">
                    <h3>Functions</h3>
                    <div class="percentage">{calculate_percentage(merged_data['functions_covered'], merged_data['functions_total']):.1f}%</div>
                    <div class="count">{merged_data['functions_covered']} / {merged_data['functions_total']}</div>
                </div>
            </div>
        </div>
        
        <div class="modules">
            <h2>Module Breakdown</h2>"""

    # Add module details
    for module_name, module_data in merged_data['modules'].items():
        html_content += f"""
            <div class="module">
                <h3>{module_name.replace('-', ' ').title()}</h3>
                <div class="module-metrics">
                    <div class="module-metric">
                        <div class="label">Lines</div>
                        <div class="value">{calculate_percentage(module_data.get('lines_covered', 0), module_data.get('lines_total', 0)):.1f}%</div>
                    </div>
                    <div class="module-metric">
                        <div class="label">Branches</div>
                        <div class="value">{calculate_percentage(module_data.get('branches_covered', 0), module_data.get('branches_total', 0)):.1f}%</div>
                    </div>
                    <div class="module-metric">
                        <div class="label">Functions</div>
                        <div class="value">{calculate_percentage(module_data.get('functions_covered', 0), module_data.get('functions_total', 0)):.1f}%</div>
                    </div>
                </div>
            </div>"""

    html_content += """
        </div>
    </div>
</body>
</html>"""

    # Write HTML file
    output_file = output_dir / "index.html"
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"Combined coverage report generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Merge coverage reports from multiple modules')
    parser.add_argument('--coverage-dir', required=True, help='Directory containing coverage reports')
    parser.add_argument('--output-dir', required=True, help='Output directory for combined report')
    parser.add_argument('--modules', nargs='+', default=['automation-framework', 'ai-rulesets', 'cloud-native-app', 'react-playwright-demo'],
                       help='List of modules to process')
    
    args = parser.parse_args()
    
    coverage_dir = Path(args.coverage_dir)
    output_dir = Path(args.output_dir)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    module_data = {}
    
    # Process each module
    for module in args.modules:
        module_coverage_dir = coverage_dir / f"{module}-coverage-report"
        
        if not module_coverage_dir.exists():
            print(f"Warning: Coverage directory not found for module {module}: {module_coverage_dir}")
            continue
        
        print(f"Processing module: {module}")
        
        # Find coverage files
        coverage_files = find_coverage_files(module_coverage_dir)
        print(f"  Found coverage files: {list(coverage_files.keys())}")
        
        # Parse coverage data
        module_coverage = {
            'lines_covered': 0,
            'lines_total': 0,
            'branches_covered': 0,
            'branches_total': 0,
            'functions_covered': 0,
            'functions_total': 0
        }
        
        # Try to parse different coverage formats
        if 'lcov' in coverage_files:
            lcov_data = parse_lcov_file(coverage_files['lcov'])
            module_coverage.update(lcov_data)
        elif 'cobertura' in coverage_files:
            cobertura_data = parse_cobertura_file(coverage_files['cobertura'])
            module_coverage.update(cobertura_data)
        elif 'json' in coverage_files:
            json_data = parse_json_coverage_file(coverage_files['json'])
            module_coverage.update(json_data)
        else:
            print(f"  Warning: No recognized coverage format found for {module}")
            continue
        
        module_data[module] = module_coverage
        print(f"  Coverage: {module_coverage['lines_covered']}/{module_coverage['lines_total']} lines ({calculate_percentage(module_coverage['lines_covered'], module_coverage['lines_total']):.1f}%)")
    
    if not module_data:
        print("No coverage data found for any modules")
        return
    
    # Merge coverage data
    merged_data = merge_coverage_data(module_data)
    
    # Generate combined HTML report
    generate_combined_html(merged_data, output_dir)
    
    print(f"Combined coverage report generated successfully in {output_dir}")


if __name__ == "__main__":
    main()
