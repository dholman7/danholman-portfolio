"""Version validation utilities for ensuring consistency across configuration files."""

import re
import json
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from readme_validator import ValidationResult


@dataclass
class VersionInfo:
    """Version information for a specific technology."""
    technology: str
    version: str
    file_path: str
    line_number: int
    context: str


class VersionValidator:
    """Validates version consistency across configuration files."""
    
    def __init__(self, project_root: str = "."):
        """Initialize version validator with project root."""
        self.project_root = Path(project_root)
        self.issues: List[ValidationResult] = []
        self.version_info: Dict[str, List[VersionInfo]] = {}
        
        # Define version patterns for different technologies
        self.version_patterns = {
            'python': [
                r'python-version:\s*[\'"]?(\d+\.\d+)[\'"]?',
                r'python\s*=\s*[\'"]?(\d+\.\d+)[\'"]?',
                r'Python\s+(\d+\.\d+)',
                r'python(\d+\.\d+)',
                r'py(\d+\.\d+)',
            ],
            'node': [
                r'node-version:\s*[\'"]?(\d+)[\'"]?',
                r'node\s*=\s*[\'"]?(\d+)[\'"]?',
                r'Node\.?js\s+(\d+)',
                r'node(\d+)',
            ],
            'typescript': [
                r'"typescript":\s*"[\^~]?(\d+\.\d+\.\d+)"',
                r'typescript\s*=\s*[\'"]?(\d+\.\d+\.\d+)[\'"]?',
                r'TypeScript\s+(\d+\.\d+\.\d+)',
            ],
            'react': [
                r'"react":\s*"[\^~]?(\d+\.\d+\.\d+)"',
                r'"react-dom":\s*"[\^~]?(\d+\.\d+\.\d+)"',
                r'React\s+(\d+)',
            ],
            'vite': [
                r'"vite":\s*"[\^~]?(\d+\.\d+\.\d+)"',
                r'Vite\s+(\d+\.\d+\.\d+)',
            ],
            'playwright': [
                r'"@playwright/test":\s*"[\^~]?(\d+\.\d+\.\d+)"',
                r'Playwright\s+(\d+\.\d+\.\d+)',
            ],
        }
    
    def validate_all_versions(self) -> List[ValidationResult]:
        """Validate version consistency across all configuration files."""
        self.issues = []
        self.version_info = {}
        
        # Collect version information from all files
        self._collect_versions_from_workflows()
        self._collect_versions_from_package_files()
        self._collect_versions_from_python_files()
        self._collect_versions_from_readmes()
        self._collect_versions_from_cloudformation()
        
        # Check for version inconsistencies
        self._check_version_consistency()
        
        return self.issues
    
    def _collect_versions_from_workflows(self) -> None:
        """Collect version information from GitHub workflow files."""
        workflow_files = list(self.project_root.rglob(".github/workflows/*.yml")) + \
                        list(self.project_root.rglob(".github/workflows/*.yaml"))
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for line_num, line in enumerate(lines, 1):
                    # Check for Python versions
                    for pattern in self.version_patterns['python']:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            self._add_version_info('python', match.group(1), 
                                                 str(workflow_file), line_num, line.strip())
                    
                    # Check for Node.js versions
                    for pattern in self.version_patterns['node']:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            self._add_version_info('node', match.group(1), 
                                                 str(workflow_file), line_num, line.strip())
                                                
            except Exception as e:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Error reading workflow file: {e}",
                    file_path=str(workflow_file),
                    severity="error"
                ))
    
    def _collect_versions_from_package_files(self) -> None:
        """Collect version information from package.json files."""
        package_files = list(self.project_root.rglob("package.json"))
        
        for package_file in package_files:
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check dependencies and devDependencies
                for deps_key in ['dependencies', 'devDependencies']:
                    if deps_key in data:
                        for dep_name, version in data[deps_key].items():
                            # Extract version number (remove ^, ~, etc.)
                            version_num = re.sub(r'[\^~>=<]', '', version)
                            
                            if dep_name == 'react':
                                self._add_version_info('react', version_num, 
                                                     str(package_file), 0, f'"{dep_name}": "{version}"')
                            elif dep_name == 'typescript':
                                self._add_version_info('typescript', version_num, 
                                                     str(package_file), 0, f'"{dep_name}": "{version}"')
                            elif dep_name == 'vite':
                                self._add_version_info('vite', version_num, 
                                                     str(package_file), 0, f'"{dep_name}": "{version}"')
                            elif dep_name == '@playwright/test':
                                self._add_version_info('playwright', version_num, 
                                                     str(package_file), 0, f'"{dep_name}": "{version}"')
                                                
            except Exception as e:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Error reading package.json: {e}",
                    file_path=str(package_file),
                    severity="error"
                ))
    
    def _collect_versions_from_python_files(self) -> None:
        """Collect version information from Python configuration files."""
        # Check pyproject.toml files
        pyproject_files = list(self.project_root.rglob("pyproject.toml"))
        for pyproject_file in pyproject_files:
            self._parse_toml_file(pyproject_file)
        
        # Check requirements.txt files
        requirements_files = list(self.project_root.rglob("requirements.txt"))
        for req_file in requirements_files:
            self._parse_requirements_file(req_file)
        
        # Check .python-version files
        python_version_files = list(self.project_root.rglob(".python-version"))
        for pyver_file in python_version_files:
            self._parse_python_version_file(pyver_file)
    
    def _parse_toml_file(self, file_path: Path) -> None:
        """Parse TOML file for version information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            for line_num, line in enumerate(lines, 1):
                # Look for Python version requirements
                if 'python_requires' in line or 'python-version' in line:
                    match = re.search(r'[\'"]?(\d+\.\d+)[\'"]?', line)
                    if match:
                        self._add_version_info('python', match.group(1), 
                                             str(file_path), line_num, line.strip())
                                            
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error reading TOML file: {e}",
                file_path=str(file_path),
                severity="error"
            ))
    
    def _parse_requirements_file(self, file_path: Path) -> None:
        """Parse requirements.txt for version information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            for line_num, line in enumerate(lines, 1):
                # Look for Python version specifications
                if 'python' in line.lower() and any(char.isdigit() for char in line):
                    match = re.search(r'python[\s>=<]+(\d+\.\d+)', line, re.IGNORECASE)
                    if match:
                        self._add_version_info('python', match.group(1), 
                                             str(file_path), line_num, line.strip())
                                            
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error reading requirements file: {e}",
                file_path=str(file_path),
                severity="error"
            ))
    
    def _parse_python_version_file(self, file_path: Path) -> None:
        """Parse .python-version file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                version = f.read().strip()
                if version:
                    self._add_version_info('python', version, 
                                         str(file_path), 1, version)
                                        
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error reading .python-version file: {e}",
                file_path=str(file_path),
                severity="error"
            ))
    
    def _collect_versions_from_readmes(self) -> None:
        """Collect version information from README files."""
        readme_files = list(self.project_root.rglob("README.md"))
        
        for readme_file in readme_files:
            try:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for line_num, line in enumerate(lines, 1):
                    # Check for various technology versions
                    for tech, patterns in self.version_patterns.items():
                        for pattern in patterns:
                            match = re.search(pattern, line, re.IGNORECASE)
                            if match:
                                self._add_version_info(tech, match.group(1), 
                                                     str(readme_file), line_num, line.strip())
                                                
            except Exception as e:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Error reading README file: {e}",
                    file_path=str(readme_file),
                    severity="error"
                ))
    
    def _collect_versions_from_cloudformation(self) -> None:
        """Collect version information from CloudFormation templates."""
        cf_files = list(self.project_root.rglob("*.yaml")) + list(self.project_root.rglob("*.yml"))
        cf_files = [f for f in cf_files if 'cloudformation' in str(f).lower() or 'cf' in str(f).lower()]
        
        for cf_file in cf_files:
            try:
                with open(cf_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for line_num, line in enumerate(lines, 1):
                    # Look for Python runtime versions
                    if 'python' in line.lower() and 'runtime' in line.lower():
                        match = re.search(r'python(\d+\.\d+)', line, re.IGNORECASE)
                        if match:
                            self._add_version_info('python', match.group(1), 
                                                 str(cf_file), line_num, line.strip())
                                                
            except Exception as e:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Error reading CloudFormation file: {e}",
                    file_path=str(cf_file),
                    severity="error"
                ))
    
    def _add_version_info(self, technology: str, version: str, file_path: str, 
                         line_number: int, context: str) -> None:
        """Add version information to the collection."""
        if technology not in self.version_info:
            self.version_info[technology] = []
        
        version_info = VersionInfo(
            technology=technology,
            version=version,
            file_path=file_path,
            line_number=line_number,
            context=context
        )
        self.version_info[technology].append(version_info)
    
    def _check_version_consistency(self) -> None:
        """Check for version inconsistencies across files."""
        for technology, versions in self.version_info.items():
            if len(versions) <= 1:
                continue
            
            # Group by version
            version_groups = {}
            for version_info in versions:
                if version_info.version not in version_groups:
                    version_groups[version_info.version] = []
                version_groups[version_info.version].append(version_info)
            
            # If we have multiple different versions, report inconsistency
            if len(version_groups) > 1:
                version_list = list(version_groups.keys())
                primary_version = max(version_list, key=lambda v: len(version_groups[v]))
                
                for version, version_infos in version_groups.items():
                    if version != primary_version:
                        for version_info in version_infos:
                            self.issues.append(ValidationResult(
                                is_valid=False,
                                message=f"Version inconsistency: {technology} {version} found, but {primary_version} is used elsewhere",
                                file_path=version_info.file_path,
                                line_number=version_info.line_number,
                                severity="warning"
                            ))
    
    def get_summary(self) -> Dict[str, int]:
        """Get validation summary."""
        summary = {"total": len(self.issues), "errors": 0, "warnings": 0, "info": 0}
        
        for issue in self.issues:
            summary[issue.severity + "s"] += 1
        
        return summary
