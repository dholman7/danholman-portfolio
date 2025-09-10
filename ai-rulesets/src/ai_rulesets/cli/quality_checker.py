#!/usr/bin/env python3
"""
AI Rulesets Quality Checker CLI.

This is a standalone quality checker that can be used independently
or as part of the ai-rulesets package.
"""

import sys
import os
import argparse
from pathlib import Path
from typing import List

# Add the ai_rulesets package to the path
script_dir = Path(__file__).parent
package_dir = script_dir.parent.parent
sys.path.insert(0, str(package_dir))

from ai_rulesets.validation.base import ValidationResult
from ai_rulesets.validation.readme_validator import ReadmeValidator
from ai_rulesets.validation.workflow_validator import WorkflowValidator
from ai_rulesets.validation.test_validator import TestValidator
from ai_rulesets.validation.version_validator import VersionValidator
from ai_rulesets.validation.issue_fixer import IssueFixer


class QualityChecker:
    """Main quality checker orchestrator."""
    
    def __init__(self, project_root: str = "."):
        """Initialize quality checker with project root."""
        self.project_root = Path(project_root)
        self.all_issues: List[ValidationResult] = []
        
        # Initialize validators
        self.readme_validator = ReadmeValidator(str(project_root))
        self.workflow_validator = WorkflowValidator(str(project_root))
        self.test_validator = TestValidator(str(project_root))
        self.version_validator = VersionValidator(str(project_root))
    
    def run_all_checks(self) -> List[ValidationResult]:
        """Run all quality checks."""
        self.all_issues = []
        
        # Run all validators
        self.all_issues.extend(self.readme_validator.validate())
        self.all_issues.extend(self.workflow_validator.validate())
        self.all_issues.extend(self.test_validator.validate())
        self.all_issues.extend(self.test_validator.validate_allure_reporting())
        self.all_issues.extend(self.version_validator.validate())
        
        return self.all_issues
    
    def _print_validation_results(self, category: str, issues: List[ValidationResult]) -> None:
        """Print validation results for a category."""
        if not issues:
            print(f"✅ {category}: No issues found")
            return
        
        # Categorize issues by severity
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]
        info = [i for i in issues if i.severity == "info"]
        
        print(f"❌ {category}: {len(issues)} issues found")
        
        if errors:
            print(f"  🔴 Errors: {len(errors)}")
            for issue in errors[:5]:  # Show first 5
                print(f"    {issue.message} ({issue.file_path})")
            if len(errors) > 5:
                print(f"    ... and {len(errors) - 5} more errors")
        
        if warnings:
            print(f"  🟡 Warnings: {len(warnings)}")
            for issue in warnings[:5]:  # Show first 5
                print(f"    {issue.message} ({issue.file_path})")
            if len(warnings) > 5:
                print(f"    ... and {len(warnings) - 5} more warnings")
        
        if info:
            print(f"  🔵 Info: {len(info)}")
            for issue in info[:5]:  # Show first 5
                print(f"    {issue.message} ({issue.file_path})")
            if len(info) > 5:
                print(f"    ... and {len(info) - 5} more info items")
    
    def _print_summary(self) -> None:
        """Print overall summary."""
        if not self.all_issues:
            print("\n✅ No quality issues found!")
            return
        
        # Categorize all issues
        errors = [i for i in self.all_issues if i.severity == "error"]
        warnings = [i for i in self.all_issues if i.severity == "warning"]
        info = [i for i in self.all_issues if i.severity == "info"]
        
        print("\n" + "=" * 60)
        print("📋 QUALITY CHECK SUMMARY")
        print("=" * 60)
        print(f"Total Issues: {len(self.all_issues)}")
        print(f"  🔴 Errors: {len(errors)}")
        print(f"  🟡 Warnings: {len(warnings)}")
        print(f"  🔵 Info: {len(info)}")
        
        if errors:
            print(f"\n⚠️  {len(errors)} critical issues need attention")
        if warnings:
            print(f"💡 {len(warnings)} warnings should be reviewed")
        if info:
            print(f"ℹ️  {len(info)} informational items noted")
    
    def has_critical_issues(self) -> bool:
        """Check if there are any critical issues."""
        return any(issue.severity == "error" for issue in self.all_issues)
    
    def export_results(self, filename: str) -> None:
        """Export results to JSON file."""
        import json
        
        results = {
            "summary": {
                "total": len(self.all_issues),
                "errors": len([i for i in self.all_issues if i.severity == "error"]),
                "warnings": len([i for i in self.all_issues if i.severity == "warning"]),
                "info": len([i for i in self.all_issues if i.severity == "info"])
            },
            "issues": [
                {
                    "severity": issue.severity,
                    "message": issue.message,
                    "file_path": issue.file_path,
                    "line_number": issue.line_number,
                    "rule": issue.rule
                }
                for issue in self.all_issues
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results exported to {filename}")


def main():
    """Main entry point for the quality checker CLI."""
    parser = argparse.ArgumentParser(description="AI Rulesets Quality Checker")
    parser.add_argument("--readmes-only", action="store_true", help="Check only README files")
    parser.add_argument("--workflows-only", action="store_true", help="Check only GitHub workflows")
    parser.add_argument("--tests-only", action="store_true", help="Check only test execution")
    parser.add_argument("--versions-only", action="store_true", help="Check only version consistency")
    parser.add_argument("--fix", action="store_true", help="Automatically fix issues where possible")
    parser.add_argument("--export", help="Export results to JSON file")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit with error code if critical issues found")
    parser.add_argument("--project-root", default=".", help="Project root directory to check")
    
    args = parser.parse_args()
    
    print("🔍 AI Rulesets Quality Checker")
    print("=" * 60)
    print(f"Checking quality in: {Path(args.project_root).absolute()}")
    print()
    
    # Initialize the quality checker
    checker = QualityChecker(args.project_root)
    
    # Run specific checks based on arguments
    if args.readmes_only:
        print("📚 Validating README files...")
        issues = checker.readme_validator.validate()
        checker.all_issues = issues
        checker._print_validation_results("README", issues)
    elif args.workflows_only:
        print("⚙️ Validating GitHub workflows...")
        issues = checker.workflow_validator.validate()
        checker.all_issues = issues
        checker._print_validation_results("Workflows", issues)
    elif args.tests_only:
        print("🧪 Validating test execution...")
        issues = checker.test_validator.validate()
        allure_issues = checker.test_validator.validate_allure_reporting()
        checker.all_issues = issues + allure_issues
        checker._print_validation_results("Tests", issues)
        checker._print_validation_results("Allure", allure_issues)
    elif args.versions_only:
        print("🔢 Validating version consistency...")
        issues = checker.version_validator.validate()
        checker.all_issues = issues
        checker._print_validation_results("Versions", issues)
    else:
        # Run all checks
        print("🔍 Running comprehensive quality checks...")
        print("=" * 60)
        
        # Run README validation
        print("\n📚 Validating README files...")
        readme_issues = checker.readme_validator.validate()
        checker.all_issues.extend(readme_issues)
        checker._print_validation_results("README", readme_issues)
        
        # Run workflow validation
        print("\n⚙️ Validating GitHub workflows...")
        workflow_issues = checker.workflow_validator.validate()
        checker.all_issues.extend(workflow_issues)
        checker._print_validation_results("Workflows", workflow_issues)
        
        # Run test validation
        print("\n🧪 Validating test execution...")
        test_issues = checker.test_validator.validate()
        checker.all_issues.extend(test_issues)
        checker._print_validation_results("Tests", test_issues)
        
        # Run Allure validation
        print("\n📊 Validating Allure reporting...")
        allure_issues = checker.test_validator.validate_allure_reporting()
        checker.all_issues.extend(allure_issues)
        checker._print_validation_results("Allure", allure_issues)
        
        # Run version validation
        print("\n🔢 Validating version consistency...")
        version_issues = checker.version_validator.validate()
        checker.all_issues.extend(version_issues)
        checker._print_validation_results("Versions", version_issues)
    
    # Apply fixes if requested
    if args.fix and checker.all_issues:
        print("\n" + "=" * 60)
        print("🔧 APPLYING AUTOMATIC FIXES")
        print("=" * 60)
        
        fixer = IssueFixer(str(checker.project_root))
        fix_results = fixer.fix_issues(checker.all_issues)
        
        print(f"\n{fixer.get_fix_summary()}")
        
        # Re-run validation to see remaining issues
        if fix_results["fixed"] > 0:
            print("\n🔄 Re-running validation after fixes...")
            print("=" * 60)
            
            # Clear previous issues and re-run
            checker.all_issues = []
            if args.readmes_only:
                issues = checker.readme_validator.validate()
                checker.all_issues = issues
                checker._print_validation_results("README", issues)
            elif args.workflows_only:
                issues = checker.workflow_validator.validate()
                checker.all_issues = issues
                checker._print_validation_results("Workflows", issues)
            elif args.tests_only:
                issues = checker.test_validator.validate()
                allure_issues = checker.test_validator.validate_allure_reporting()
                checker.all_issues = issues + allure_issues
                checker._print_validation_results("Tests", issues)
                checker._print_validation_results("Allure", allure_issues)
            else:
                results = checker.run_all_checks()
    
    # Print summary
    checker._print_summary()
    
    # If using --fix, provide AI instructions for manual fixes
    if args.fix and checker.all_issues:
        print("\n" + "=" * 60)
        print("🤖 AI ASSISTANCE FOR MANUAL FIXES")
        print("=" * 60)
        print("\nThe following issues require manual attention. Here's how AI can help:")
        print("\n📋 **Issues That Need Manual Fixing:**")
        
        # Categorize issues for AI assistance
        critical_issues = [issue for issue in checker.all_issues if issue.severity == "error"]
        warning_issues = [issue for issue in checker.all_issues if issue.severity == "warning"]
        
        if critical_issues:
            print(f"\n🔴 **Critical Issues ({len(critical_issues)}):**")
            for issue in critical_issues[:5]:  # Show first 5
                print(f"  - {issue.message} ({issue.file_path})")
            if len(critical_issues) > 5:
                print(f"  ... and {len(critical_issues) - 5} more critical issues")
        
        if warning_issues:
            print(f"\n🟡 **Warnings ({len(warning_issues)}):**")
            for issue in warning_issues[:5]:  # Show first 5
                print(f"  - {issue.message} ({issue.file_path})")
            if len(warning_issues) > 5:
                print(f"  ... and {len(warning_issues) - 5} more warnings")
        
        print("\n" + "=" * 60)
        print("🤖 **AI PROMPT FOR MANUAL FIXES:**")
        print("=" * 60)
        print("\nCopy and paste this prompt to your AI assistant:")
        print("\n" + "─" * 60)
        print("I need help fixing quality issues in my codebase. Here are the specific issues:")
        print()
        
        # Generate detailed AI prompt
        for i, issue in enumerate(checker.all_issues[:10], 1):  # Limit to first 10 issues
            print(f"{i}. **{issue.severity.upper()}**: {issue.message}")
            print(f"   File: {issue.file_path}")
            if issue.line_number:
                print(f"   Line: {issue.line_number}")
            print()
        
        if len(checker.all_issues) > 10:
            print(f"... and {len(checker.all_issues) - 10} more issues")
            print()
        
        print("Please help me fix these issues systematically. For each issue:")
        print("1. Identify the root cause")
        print("2. Provide the specific fix")
        print("3. Explain why this fix is correct")
        print("4. Suggest prevention strategies")
        print()
        print("Focus on critical errors first, then warnings. Provide code examples")
        print("and step-by-step instructions where applicable.")
        print("─" * 60)
        print("\n💡 **Tip**: You can also run specific checks:")
        print("  - `ai-rulesets quality check --readmes-only`")
        print("  - `ai-rulesets quality check --workflows-only`")
        print("  - `ai-rulesets quality check --versions-only`")
        print("  - `ai-rulesets quality check --tests-only`")
    
    # Export results if requested
    if args.export:
        checker.export_results(args.export)
    
    # Exit with appropriate code
    if args.fail_on_error and checker.has_critical_issues():
        print("\n❌ Critical issues found - exiting with error code")
        sys.exit(1)
    else:
        print("\n✅ Quality check completed successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()