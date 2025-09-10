"""Issue fixing utilities for automatic correction of common problems."""

import re
import os
from pathlib import Path
from typing import List, Dict, Optional
from readme_validator import ValidationResult


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
            "Deprecated action used"
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
