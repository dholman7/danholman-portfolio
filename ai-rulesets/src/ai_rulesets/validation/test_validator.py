"""Test execution validation utilities."""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from .readme_validator import ValidationResult


class TestValidator:
    """Validates test execution and reporting across all modules."""
    
    def __init__(self, project_root: str = "."):
        """Initialize validator with project root."""
        self.project_root = Path(project_root)
        self.issues: List[ValidationResult] = []
        self.modules = ["automation-framework", "ai-rulesets", "cloud-native-app", "react-playwright-demo"]
    
    def validate_all_tests(self) -> List[ValidationResult]:
        """Validate test execution for all modules."""
        self.issues = []
        
        # Check each module
        for module in self.modules:
            module_path = self.project_root / module
            if module_path.exists():
                self._validate_module_tests(module_path, module)
        
        # Check main test execution
        self._validate_main_test_execution()
        
        return self.issues
    
    def _validate_module_tests(self, module_path: Path, module_name: str) -> None:
        """Validate tests for a specific module."""
        # Check if module has test configuration
        test_configs = [
            "pytest.ini",
            "pyproject.toml",
            "jest.config.js",
            "playwright.config.ts",
            "Makefile"
        ]
        
        has_test_config = any((module_path / config).exists() for config in test_configs)
        
        if not has_test_config:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Module {module_name} missing test configuration",
                file_path=str(module_path),
                severity="warning"
            ))
        
        # Check for test directories
        test_dirs = ["tests", "test", "e2e", "__tests__"]
        has_test_dir = any((module_path / test_dir).exists() for test_dir in test_dirs)
        
        if not has_test_dir:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Module {module_name} missing test directory",
                file_path=str(module_path),
                severity="warning"
            ))
        
        # Try to run tests if possible
        self._try_run_module_tests(module_path, module_name)
    
    def _try_run_module_tests(self, module_path: Path, module_name: str) -> None:
        """Try to run tests for a module."""
        try:
            # Check if it's a Python module
            if (module_path / "pyproject.toml").exists() or (module_path / "requirements.txt").exists():
                self._run_python_tests(module_path, module_name)
            
            # Check if it's a Node.js module
            elif (module_path / "package.json").exists():
                self._run_node_tests(module_path, module_name)
            
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error running tests for {module_name}: {e}",
                file_path=str(module_path),
                severity="warning"
            ))
    
    def _run_python_tests(self, module_path: Path, module_name: str) -> None:
        """Run Python tests for a module."""
        try:
            # Try to run pytest
            result = subprocess.run(
                ["python", "-m", "pytest", "--version"],
                cwd=module_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"pytest not available for {module_name}",
                    file_path=str(module_path),
                    severity="warning"
                ))
                return
            
            # Try to run tests
            result = subprocess.run(
                ["python", "-m", "pytest", "--collect-only", "-q"],
                cwd=module_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Test collection failed for {module_name}: {result.stderr}",
                    file_path=str(module_path),
                    severity="error"
                ))
            
        except subprocess.TimeoutExpired:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Test execution timeout for {module_name}",
                file_path=str(module_path),
                severity="warning"
            ))
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error running Python tests for {module_name}: {e}",
                file_path=str(module_path),
                severity="warning"
            ))
    
    def _run_node_tests(self, module_path: Path, module_name: str) -> None:
        """Run Node.js tests for a module."""
        try:
            # Check if yarn is available
            result = subprocess.run(
                ["yarn", "--version"],
                cwd=module_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                # Try npm
                result = subprocess.run(
                    ["npm", "--version"],
                    cwd=module_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    self.issues.append(ValidationResult(
                        is_valid=False,
                        message=f"No package manager available for {module_name}",
                        file_path=str(module_path),
                        severity="warning"
                    ))
                    return
            
            # Try to run tests
            package_manager = "yarn" if "yarn" in result.command else "npm"
            test_command = ["yarn", "test"] if package_manager == "yarn" else ["npm", "test"]
            
            result = subprocess.run(
                test_command + ["--dry-run"],
                cwd=module_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Test command failed for {module_name}: {result.stderr}",
                    file_path=str(module_path),
                    severity="warning"
                ))
            
        except subprocess.TimeoutExpired:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Test execution timeout for {module_name}",
                file_path=str(module_path),
                severity="warning"
            ))
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error running Node.js tests for {module_name}: {e}",
                file_path=str(module_path),
                severity="warning"
            ))
    
    def _validate_main_test_execution(self) -> None:
        """Validate main test execution commands."""
        try:
            # Check if Makefile exists
            makefile_path = self.project_root / "Makefile"
            if not makefile_path.exists():
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message="Main Makefile not found",
                    file_path=str(self.project_root),
                    severity="error"
                ))
                return
            
            # Try to run make help
            result = subprocess.run(
                ["make", "help"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"Make help command failed: {result.stderr}",
                    file_path=str(self.project_root),
                    severity="error"
                ))
            
            # Check for test commands in help output
            help_output = result.stdout
            test_commands = ["test", "test-regression", "test-allure"]
            
            for cmd in test_commands:
                if cmd not in help_output:
                    self.issues.append(ValidationResult(
                        is_valid=False,
                        message=f"Test command '{cmd}' not found in Makefile help",
                        file_path=str(makefile_path),
                        severity="warning"
                    ))
            
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error validating main test execution: {e}",
                file_path=str(self.project_root),
                severity="error"
            ))
    
    def validate_allure_reporting(self) -> List[ValidationResult]:
        """Validate Allure reporting configuration."""
        allure_issues = []
        
        # Check for Allure configuration files
        allure_configs = list(self.project_root.rglob("allure.properties"))
        
        if not allure_configs:
            allure_issues.append(ValidationResult(
                is_valid=False,
                message="No Allure configuration files found",
                file_path=str(self.project_root),
                severity="warning"
            ))
        
        # Check each module for Allure configuration
        for module in self.modules:
            module_path = self.project_root / module
            if module_path.exists():
                allure_props = module_path / "allure.properties"
                if not allure_props.exists():
                    allure_issues.append(ValidationResult(
                        is_valid=False,
                        message=f"Module {module} missing allure.properties",
                        file_path=str(module_path),
                        severity="warning"
                    ))
        
        return allure_issues
    
    def get_summary(self) -> Dict[str, int]:
        """Get validation summary."""
        summary = {"total": len(self.issues), "errors": 0, "warnings": 0, "info": 0}
        
        for issue in self.issues:
            summary[issue.severity + "s"] += 1
        
        return summary
