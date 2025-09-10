"""Issue fixing utilities for automatic correction of common problems."""

import re
import os
from pathlib import Path
from typing import List, Dict, Optional
from .base import ValidationResult


class IssueFixer:
    """Automatically fixes common issues found by the quality checker."""
    
    def __init__(self, project_root: str = "."):
        """Initialize fixer with project root."""
        self.project_root = Path(project_root)
        self.fixes_applied = []
        self.fixes_failed = []
    
    def fix_issues(self, issues: List[ValidationResult]) -> Dict[str, int]:
        """Fix all fixable issues."""
        fixable_issues = [issue for issue in issues if self._is_fixable(issue)]
        
        print(f"\n🔧 Attempting to fix {len(fixable_issues)} fixable issues...")
        
        for issue in fixable_issues:
            try:
                if self._fix_issue(issue):
                    self.fixes_applied.append(issue)
                    print(f"✅ Fixed: {issue.message}")
                else:
                    self.fixes_failed.append(issue)
                    print(f"❌ Could not fix: {issue.message}")
            except Exception as e:
                self.fixes_failed.append(issue)
                print(f"❌ Error fixing {issue.message}: {e}")
        
        return {
            "total_fixable": len(fixable_issues),
            "fixed": len(self.fixes_applied),
            "failed": len(self.fixes_failed)
        }
    
    def _is_fixable(self, issue: ValidationResult) -> bool:
        """Check if an issue can be automatically fixed."""
        fixable_patterns = [
            "Trailing whitespace",
            "Line too long",
            "Outdated reference found: AI Test Generation",
            "Missing required field: on",
            "Job.*step.*missing name or uses",
            "Deprecated action used",
            "Code formatting issue",
            "Import sorting issue",
            "Missing docstring",
            "Unused import",
            "Inconsistent quotes",
            "Missing type hint",
            "YAML.*indentation",
            "Markdown.*formatting"
        ]
        
        return any(pattern in issue.message for pattern in fixable_patterns)
    
    def _fix_issue(self, issue: ValidationResult) -> bool:
        """Fix a specific issue."""
        if not issue.file_path:
            return False
        
        file_path = Path(issue.file_path)
        if not file_path.exists():
            return False
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes based on issue type
        if "Trailing whitespace" in issue.message:
            content = self._fix_trailing_whitespace(content, issue.line_number)
        elif "Line too long" in issue.message:
            content = self._fix_long_lines(content, issue.line_number)
        elif "Outdated reference found: AI Test Generation" in issue.message:
            content = self._fix_outdated_references(content)
        elif "Missing required field: on" in issue.message:
            content = self._fix_missing_workflow_trigger(content)
        elif "Job" in issue.message and "step" in issue.message and "missing name or uses" in issue.message:
            content = self._fix_missing_step_name(content, issue.line_number)
        elif "Deprecated action used" in issue.message:
            content = self._fix_deprecated_actions(content)
        elif "Code formatting issue" in issue.message:
            content = self._fix_code_formatting(content, file_path)
        elif "Import sorting issue" in issue.message:
            content = self._fix_import_sorting(content, file_path)
        elif "Missing docstring" in issue.message:
            content = self._fix_missing_docstring(content, issue.line_number)
        elif "Unused import" in issue.message:
            content = self._fix_unused_imports(content)
        elif "Inconsistent quotes" in issue.message:
            content = self._fix_quote_consistency(content)
        elif "Missing type hint" in issue.message:
            content = self._fix_missing_type_hints(content, issue.line_number)
        elif "YAML" in issue.message and "indentation" in issue.message:
            content = self._fix_yaml_indentation(content)
        elif "Markdown" in issue.message and "formatting" in issue.message:
            content = self._fix_markdown_formatting(content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def _fix_trailing_whitespace(self, content: str, line_number: Optional[int]) -> str:
        """Fix trailing whitespace in content."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.endswith(' '):
                lines[i] = line.rstrip()
        return '\n'.join(lines)
    
    def _fix_long_lines(self, content: str, line_number: Optional[int]) -> str:
        """Fix lines that are too long by breaking them appropriately."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if len(line) > 120:
                # Try to break at logical points
                if ' - ' in line and len(line) > 120:
                    # Break at bullet points
                    parts = line.split(' - ')
                    if len(parts) > 1:
                        lines[i] = parts[0] + ' -'
                        lines.insert(i + 1, '  ' + ' - '.join(parts[1:]))
                elif ' | ' in line and len(line) > 120:
                    # Break at table separators
                    parts = line.split(' | ')
                    if len(parts) > 1:
                        lines[i] = parts[0] + ' |'
                        lines.insert(i + 1, '  ' + ' | '.join(parts[1:]))
                elif 'http' in line and len(line) > 120:
                    # Break long URLs
                    url_match = re.search(r'(https?://[^\s]+)', line)
                    if url_match:
                        url = url_match.group(1)
                        if len(url) > 80:
                            lines[i] = line.replace(url, url[:80] + '\n  ' + url[80:])
        
        return '\n'.join(lines)
    
    def _fix_outdated_references(self, content: str) -> str:
        """Fix outdated references to old module names."""
        replacements = {
            "AI Test Generation": "AI Rulesets",
            "ai-test-generation": "ai-rulesets",
            "ai_test_generation": "ai_rulesets"
        }
        
        for old_ref, new_ref in replacements.items():
            content = content.replace(old_ref, new_ref)
        
        return content
    
    def _fix_missing_workflow_trigger(self, content: str) -> str:
        """Fix missing workflow triggers by adding a default trigger."""
        if "on:" not in content and "name:" in content:
            # Find the name line and add trigger after it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('name:'):
                    # Add basic trigger
                    lines.insert(i + 1, 'on:')
                    lines.insert(i + 2, '  push:')
                    lines.insert(i + 3, '    branches: [ main ]')
                    lines.insert(i + 4, '  pull_request:')
                    lines.insert(i + 5, '    branches: [ main ]')
                    break
            return '\n'.join(lines)
        
        return content
    
    def _fix_missing_step_name(self, content: str, line_number: Optional[int]) -> str:
        """Fix missing step names in GitHub workflows."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if 'uses:' in line and not any(lines[j].strip().startswith('name:') for j in range(max(0, i-3), i)):
                # Add a generic name before the uses line
                action_name = line.split('uses:')[1].strip().split('@')[0].split('/')[-1]
                lines.insert(i, f'      - name: {action_name.replace("-", " ").title()}')
        
        return '\n'.join(lines)
    
    def _fix_deprecated_actions(self, content: str) -> str:
        """Fix deprecated GitHub Actions."""
        replacements = {
            "actions/checkout@v2": "actions/checkout@v4",
            "actions/setup-python@v2": "actions/setup-python@v5",
            "actions/setup-node@v2": "actions/setup-node@v4"
        }
        
        for old_action, new_action in replacements.items():
            content = content.replace(old_action, new_action)
        
        return content
    
    def _fix_code_formatting(self, content: str, file_path: Path) -> str:
        """Fix code formatting using Black."""
        try:
            import subprocess
            result = subprocess.run(
                ["black", "--quiet", str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # Read the formatted file
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return content
    
    def _fix_import_sorting(self, content: str, file_path: Path) -> str:
        """Fix import sorting using isort."""
        try:
            import subprocess
            result = subprocess.run(
                ["isort", "--quiet", str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                # Read the sorted file
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return content
    
    def _fix_missing_docstring(self, content: str, line_number: Optional[int]) -> str:
        """Add basic docstrings to functions and classes."""
        lines = content.split('\n')
        
        # Look for function/class definitions without docstrings
        for i, line in enumerate(lines):
            if (line.strip().startswith('def ') or line.strip().startswith('class ')) and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if not next_line.startswith('"""') and not next_line.startswith("'''"):
                    # Add a basic docstring
                    indent = len(line) - len(line.lstrip())
                    docstring = ' ' * (indent + 4) + '"""TODO: Add docstring."""'
                    lines.insert(i + 1, docstring)
        
        return '\n'.join(lines)
    
    def _fix_unused_imports(self, content: str) -> str:
        """Remove obviously unused imports."""
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith('#'):
                new_lines.append(line)
                continue
            
            # Check if it's an import line
            if line.strip().startswith(('import ', 'from ')):
                # Simple heuristic: if the imported name isn't used in the rest of the file
                import_name = line.strip().split()[-1].split('.')[-1]
                if import_name not in content.replace(line, ''):
                    # Skip this import
                    continue
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _fix_quote_consistency(self, content: str) -> str:
        """Standardize quote usage (prefer double quotes)."""
        # Simple quote standardization
        content = re.sub(r"'([^']*)'", r'"\1"', content)
        return content
    
    def _fix_missing_type_hints(self, content: str, line_number: Optional[int]) -> str:
        """Add basic type hints to function parameters."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip().startswith('def ') and '->' not in line:
                # Try to add basic return type hint
                if 'return' in content[content.find(line):content.find(line) + 200]:
                    if 'return None' in content[content.find(line):content.find(line) + 200]:
                        lines[i] = line.rstrip() + ' -> None:'
                    elif 'return True' in content[content.find(line):content.find(line) + 200] or 'return False' in content[content.find(line):content.find(line) + 200]:
                        lines[i] = line.rstrip() + ' -> bool:'
                    elif 'return ""' in content[content.find(line):content.find(line) + 200] or 'return str(' in content[content.find(line):content.find(line) + 200]:
                        lines[i] = line.rstrip() + ' -> str:'
                    elif 'return 0' in content[content.find(line):content.find(line) + 200] or 'return int(' in content[content.find(line):content.find(line) + 200]:
                        lines[i] = line.rstrip() + ' -> int:'
        
        return '\n'.join(lines)
    
    def _fix_yaml_indentation(self, content: str) -> str:
        """Fix YAML indentation issues."""
        lines = content.split('\n')
        fixed_lines = []
        indent_stack = [0]
        
        for line in lines:
            if not line.strip():
                fixed_lines.append(line)
                continue
            
            current_indent = len(line) - len(line.lstrip())
            
            # Determine expected indentation
            if line.strip().startswith('- '):
                # List item
                expected_indent = indent_stack[-1]
            elif line.strip().endswith(':'):
                # Key with value
                expected_indent = indent_stack[-1]
                indent_stack.append(current_indent + 2)
            else:
                # Regular line
                expected_indent = indent_stack[-1]
            
            # Fix indentation
            if current_indent != expected_indent:
                fixed_line = ' ' * expected_indent + line.lstrip()
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _fix_markdown_formatting(self, content: str) -> str:
        """Fix common Markdown formatting issues."""
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Fix heading spacing
            if line.startswith('#'):
                # Ensure there's a space after #
                if not line.startswith('# '):
                    line = line.replace('#', '# ', 1)
                fixed_lines.append(line)
            # Fix list formatting
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                # Ensure consistent list markers
                if line.strip().startswith('* '):
                    line = line.replace('* ', '- ', 1)
                fixed_lines.append(line)
            # Fix code block formatting
            elif line.strip().startswith('```'):
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def get_fix_summary(self) -> str:
        """Get a summary of fixes applied."""
        if not self.fixes_applied and not self.fixes_failed:
            return "No fixes were attempted."
        
        summary = f"🔧 Fix Summary:\n"
        summary += f"  ✅ Successfully fixed: {len(self.fixes_applied)} issues\n"
        summary += f"  ❌ Failed to fix: {len(self.fixes_failed)} issues\n"
        
        if self.fixes_failed:
            summary += f"\nFailed fixes:\n"
            for issue in self.fixes_failed[:5]:  # Show first 5
                summary += f"  - {issue.message}\n"
            if len(self.fixes_failed) > 5:
                summary += f"  ... and {len(self.fixes_failed) - 5} more\n"
        
        return summary
