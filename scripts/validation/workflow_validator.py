"""GitHub workflow validation utilities."""

import os
import re
import yaml
import glob
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from readme_validator import ValidationResult


class WorkflowValidator:
    """Validates GitHub workflow files for accuracy and completeness."""
    
    def __init__(self, project_root: str = "."):
        """Initialize validator with project root."""
        self.project_root = Path(project_root)
        self.issues: List[ValidationResult] = []
    
    def validate_all_workflows(self) -> List[ValidationResult]:
        """Validate all workflow files in the project."""
        self.issues = []
        
        # Find all workflow files (exclude node_modules)
        workflow_files = list(self.project_root.glob(".github/workflows/*.yml")) + \
                        list(self.project_root.glob(".github/workflows/*.yaml"))
        
        # Also check module-specific workflow files
        for module in ["automation-framework", "ai-rulesets", "cloud-native-app", "react-playwright-demo"]:
            module_workflows = list(self.project_root.glob(f"{module}/.github/workflows/*.yml")) + \
                              list(self.project_root.glob(f"{module}/.github/workflows/*.yaml"))
            workflow_files.extend(module_workflows)
        
        # Filter out files in node_modules and other excluded directories
        excluded_dirs = {'node_modules', '.git', '.venv', '__pycache__', 'htmlcov', 'reports', 'dist', 'build', '.next'}
        workflow_files = [f for f in workflow_files if not any(excluded_dir in str(f) for excluded_dir in excluded_dirs)]
        
        for workflow_file in workflow_files:
            self._validate_workflow_file(workflow_file)
        
        return self.issues
    
    def _validate_workflow_file(self, workflow_path: Path) -> None:
        """Validate a single workflow file."""
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML
            try:
                workflow_data = yaml.safe_load(content)
            except yaml.YAMLError as e:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"YAML syntax error: {e}",
                    file_path=str(workflow_path),
                    severity="error"
                ))
                return
            
            # Check workflow structure
            self._check_workflow_structure(workflow_path, workflow_data)
            
            # Check for outdated references
            self._check_outdated_references(workflow_path, content)
            
            # Check job consistency
            self._check_job_consistency(workflow_path, workflow_data)
            
            # Check for security issues
            self._check_security_issues(workflow_path, workflow_data)
            
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error reading workflow file: {e}",
                file_path=str(workflow_path),
                severity="error"
            ))
    
    def _check_workflow_structure(self, file_path: Path, workflow_data: Dict) -> None:
        """Check workflow file structure."""
        # Check for required fields
        required_fields = ['name', 'on', 'jobs']
        
        for field in required_fields:
            if field not in workflow_data:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Missing required field: {field}",
                    file_path=str(file_path),
                    severity="error"
                ))
        
        # Check for jobs
        if 'jobs' in workflow_data:
            if not workflow_data['jobs']:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message="No jobs defined in workflow",
                    file_path=str(file_path),
                    severity="error"
                ))
    
    def _check_outdated_references(self, file_path: Path, content: str) -> None:
        """Check for outdated references in workflow files."""
        # Check for old module names
        outdated_refs = [
            "ai-test-generation",
            "ai_test_generation",
            "AI Test Generation"
        ]
        
        for ref in outdated_refs:
            if ref in content:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Outdated reference found: {ref}",
                    file_path=str(file_path),
                    severity="error"
                ))
        
        # Check for old file names
        if "ci.yaml" in content and "ci-cd.yml" not in str(file_path):
            self.issues.append(ValidationResult(
                is_valid=False,
                message="Workflow file should be named ci-cd.yml, not ci.yaml",
                file_path=str(file_path),
                severity="warning"
            ))
    
    def _check_job_consistency(self, file_path: Path, workflow_data: Dict) -> None:
        """Check job consistency and naming."""
        if 'jobs' not in workflow_data:
            return
        
        jobs = workflow_data['jobs']
        
        for job_name, job_config in jobs.items():
            # Check job name format
            if not self._is_valid_job_name(job_name):
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Job name should use kebab-case: {job_name}",
                    file_path=str(file_path),
                    severity="warning"
                ))
            
            # Check for required job fields
            if 'runs-on' not in job_config:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Job '{job_name}' missing 'runs-on' field",
                    file_path=str(file_path),
                    severity="error"
                ))
            
            # Check for steps
            if 'steps' in job_config:
                self._check_job_steps(file_path, job_name, job_config['steps'])
    
    def _is_valid_job_name(self, job_name: str) -> bool:
        """Check if job name follows naming conventions."""
        # Should be lowercase with hyphens
        return job_name.islower() and '-' in job_name or job_name.islower()
    
    def _check_job_steps(self, file_path: Path, job_name: str, steps: List[Dict]) -> None:
        """Check job steps for common issues."""
        for i, step in enumerate(steps):
            step_num = i + 1
            
            # Check for step name
            if 'name' not in step and 'uses' not in step:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Job '{job_name}' step {step_num} missing name or uses",
                    file_path=str(file_path),
                    severity="warning"
                ))
            
            # Check for deprecated actions
            if 'uses' in step:
                action = step['uses']
                deprecated_actions = [
                    "actions/checkout@v2",
                    "actions/setup-python@v2",
                    "actions/setup-node@v2"
                ]
                
                for deprecated in deprecated_actions:
                    if action.startswith(deprecated):
                        self.issues.append(ValidationResult(
                            is_valid=False,
                            message=f"Deprecated action used: {action}",
                            file_path=str(file_path),
                            severity="warning"
                        ))
    
    def _check_security_issues(self, file_path: Path, workflow_data: Dict) -> None:
        """Check for security issues in workflow files."""
        # Check for hardcoded secrets
        content = str(workflow_data)
        secret_patterns = [
            r'password\s*:\s*["\'][^"\']+["\']',
            r'secret\s*:\s*["\'][^"\']+["\']',
            r'token\s*:\s*["\'][^"\']+["\']',
            r'key\s*:\s*["\'][^"\']+["\']'
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message="Potential hardcoded secret found",
                    file_path=str(file_path),
                    severity="error"
                ))
    
    def get_summary(self) -> Dict[str, int]:
        """Get validation summary."""
        summary = {"total": len(self.issues), "errors": 0, "warnings": 0, "info": 0}
        
        for issue in self.issues:
            summary[issue.severity + "s"] += 1
        
        return summary
