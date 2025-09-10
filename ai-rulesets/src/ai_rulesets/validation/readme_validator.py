"""README validation utilities."""

import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .base import ValidationResult, BaseValidator


class ReadmeValidator(BaseValidator):
    """Validates README files for accuracy and completeness."""
    
    def __init__(self, project_root: str = "."):
        """Initialize validator with project root."""
        super().__init__(project_root)
        self.project_root = Path(project_root)
    
    def validate(self) -> List[ValidationResult]:
        """Validate all README files in the project."""
        return self.validate_all_readmes()
    
    def validate_all_readmes(self) -> List[ValidationResult]:
        """Validate all README files in the project."""
        self.issues = []
        
        # Find all README files, excluding certain directories
        readme_files = []
        for readme_file in self.project_root.rglob("README.md"):
            # Skip README files in excluded directories
            if any(excluded in str(readme_file) for excluded in [
                "node_modules", ".git", ".venv", "__pycache__", 
                "htmlcov", "reports", "dist", "build", ".next"
            ]):
                continue
            readme_files.append(readme_file)
        
        for readme_file in readme_files:
            self._validate_readme_file(readme_file)
        
        return self.issues
    
    def _validate_readme_file(self, readme_path: Path) -> None:
        """Validate a single README file."""
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for basic structure
            self._check_readme_structure(readme_path, content)
            
            # Check for broken links
            self._check_broken_links(readme_path, content)
            
            # Check for outdated references
            self._check_outdated_references(readme_path, content)
            
            # Check for code examples
            self._check_code_examples(readme_path, content)
            
            # Check for proper formatting
            self._check_formatting(readme_path, content)
            
        except Exception as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Error reading README file: {e}",
                file_path=str(readme_path),
                severity="error"
            ))
    
    def _check_readme_structure(self, file_path: Path, content: str) -> None:
        """Check README file structure."""
        lines = content.split('\n')
        
        # Check for title
        if not lines or not lines[0].startswith('#'):
            self.issues.append(ValidationResult(
                is_valid=False,
                message="README should start with a title (# heading)",
                file_path=str(file_path),
                line_number=1,
                severity="warning"
            ))
        
        # Check for essential sections
        essential_sections = [
            "## 🚀", "## 🛠️", "## 📁", "## 🧪", "## 📚", "## 🔧"
        ]
        
        content_lower = content.lower()
        for section in essential_sections:
            if section.lower() not in content_lower:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message=f"README missing essential section: {section}",
                    file_path=str(file_path),
                    severity="info"
                ))
    
    def _check_broken_links(self, file_path: Path, content: str) -> None:
        """Check for broken internal links."""
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # Skip external links
            if link_url.startswith(('http://', 'https://', 'mailto:')):
                continue
            
            # Check internal links
            if link_url.startswith('./') or not link_url.startswith('/'):
                # Skip anchor links (starting with #)
                if link_url.startswith('#'):
                    # Check if anchor exists in the same file
                    anchor_name = link_url[1:].lower()
                    if not re.search(rf'#+\s+{re.escape(anchor_name)}\b', content, re.IGNORECASE):
                        self.issues.append(ValidationResult(
                            is_valid=False,
                            message=f"Broken internal link: {link_url}",
                            file_path=str(file_path),
                            severity="error"
                        ))
                else:
                    # Relative file link
                    target_path = file_path.parent / link_url
                    if not target_path.exists():
                        self.issues.append(ValidationResult(
                            is_valid=False,
                            message=f"Broken internal link: {link_url}",
                            file_path=str(file_path),
                            severity="error"
                        ))
    
    def _check_outdated_references(self, file_path: Path, content: str) -> None:
        """Check for outdated references."""
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
    
    def _check_code_examples(self, file_path: Path, content: str) -> None:
        """Check code examples for basic syntax."""
        # Find code blocks
        code_block_pattern = r'```(\w+)?\n(.*?)\n```'
        code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
        
        for language, code in code_blocks:
            # Basic validation for common languages
            if language in ['bash', 'sh']:
                self._validate_bash_code(file_path, code)
            elif language in ['python', 'py']:
                self._validate_python_code(file_path, code)
            elif language in ['yaml', 'yml']:
                self._validate_yaml_code(file_path, code)
    
    def _validate_bash_code(self, file_path: Path, code: str) -> None:
        """Validate bash code examples."""
        lines = code.strip().split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Check for common bash issues
            if '&&' in line and '||' in line:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message="Complex bash command with both && and || - consider splitting",
                    file_path=str(file_path),
                    line_number=i,
                    severity="warning"
                ))
    
    def _validate_python_code(self, file_path: Path, code: str) -> None:
        """Validate Python code examples."""
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"Python syntax error: {e}",
                file_path=str(file_path),
                severity="error"
            ))
    
    def _validate_yaml_code(self, file_path: Path, code: str) -> None:
        """Validate YAML code examples."""
        try:
            import yaml
            yaml.safe_load(code)
        except ImportError:
            # YAML not available, skip validation
            pass
        except yaml.YAMLError as e:
            self.issues.append(ValidationResult(
                is_valid=False,
                message=f"YAML syntax error: {e}",
                file_path=str(file_path),
                severity="error"
            ))
    
    def _check_formatting(self, file_path: Path, content: str) -> None:
        """Check README formatting."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for lines that are too long
            if len(line) > 120:
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message="Line too long (over 120 characters)",
                    file_path=str(file_path),
                    line_number=i,
                    severity="warning"
                ))
            
            # Check for trailing whitespace
            if line.endswith(' '):
                self.issues.append(ValidationResult(
                    is_valid=False,
                    message="Trailing whitespace",
                    file_path=str(file_path),
                    line_number=i,
                    severity="warning"
                ))
    
    def get_summary(self) -> Dict[str, int]:
        """Get validation summary."""
        summary = {"total": len(self.issues), "errors": 0, "warnings": 0, "info": 0}
        
        for issue in self.issues:
            summary[issue.severity + "s"] += 1
        
        return summary
