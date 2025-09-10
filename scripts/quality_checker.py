#!/usr/bin/env python3
"""
Portfolio-wide code quality checker.

This script validates code quality across all modules in the portfolio:
- README files: Content accuracy, broken links, outdated references
- GitHub workflows: YAML syntax, required fields, best practices
- Test execution: Coverage, reporting, and integration
- Allure reporting: Configuration and report generation
"""

import sys
import os
import argparse
from pathlib import Path

# Add the validation module to the path
script_dir = Path(__file__).parent
validation_dir = script_dir / "validation"
sys.path.insert(0, str(validation_dir))

from quality_checker import QualityChecker
from readme_validator import ReadmeValidator
from workflow_validator import WorkflowValidator
from test_validator import TestValidator
from version_validator import VersionValidator
# Linting is handled separately in each module's CI/CD
from issue_fixer import IssueFixer


def main():
    """Main entry point for the portfolio quality checker."""
    parser = argparse.ArgumentParser(description="Portfolio-wide code quality checker")
    parser.add_argument("--readmes-only", action="store_true", help="Check only README files")
    parser.add_argument("--workflows-only", action="store_true", help="Check only GitHub workflows")
    parser.add_argument("--tests-only", action="store_true", help="Check only test execution")
    parser.add_argument("--versions-only", action="store_true", help="Check only version consistency")
    parser.add_argument("--fix", action="store_true", help="Automatically fix issues where possible")
    parser.add_argument("--export", help="Export results to JSON file")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit with error code if critical issues found")
    
    args = parser.parse_args()
    
    # Get the portfolio root directory (parent of scripts directory)
    portfolio_root = script_dir.parent
    
    print("🔍 Dan Holman Portfolio - Code Quality Checker")
    print("=" * 60)
    print(f"Checking quality across all modules in: {portfolio_root}")
    print()
    
    # Initialize the quality checker
    checker = QualityChecker(str(portfolio_root))
    
    # Run specific checks based on arguments
    if args.readmes_only:
        print("📚 Validating README files...")
        issues = checker.readme_validator.validate_all_readmes()
        checker.all_issues = issues
        checker._print_validation_results("README", issues)
    elif args.workflows_only:
        print("⚙️ Validating GitHub workflows...")
        issues = checker.workflow_validator.validate_all_workflows()
        checker.all_issues = issues
        checker._print_validation_results("Workflows", issues)
    elif args.tests_only:
        print("🧪 Validating test execution...")
        issues = checker.test_validator.validate_all_tests()
        allure_issues = checker.test_validator.validate_allure_reporting()
        checker.all_issues = issues + allure_issues
        checker._print_validation_results("Tests", issues)
        checker._print_validation_results("Allure", allure_issues)
    elif args.versions_only:
        print("🔢 Validating version consistency...")
        version_validator = VersionValidator(str(portfolio_root))
        issues = version_validator.validate_all_versions()
        checker.all_issues = issues
        checker._print_validation_results("Versions", issues)
    else:
        # Run all checks including linting
        print("🔍 Running comprehensive quality checks...")
        print("=" * 60)
        
        # Run README validation
        print("\n📚 Validating README files...")
        readme_issues = checker.readme_validator.validate_all_readmes()
        checker.all_issues.extend(readme_issues)
        checker._print_validation_results("README", readme_issues)
        
        # Run workflow validation
        print("\n⚙️ Validating GitHub workflows...")
        workflow_issues = checker.workflow_validator.validate_all_workflows()
        checker.all_issues.extend(workflow_issues)
        checker._print_validation_results("Workflows", workflow_issues)
        
        # Run test validation
        print("\n🧪 Validating test execution...")
        test_issues = checker.test_validator.validate_all_tests()
        checker.all_issues.extend(test_issues)
        checker._print_validation_results("Tests", test_issues)
        
        # Run Allure validation
        print("\n📊 Validating Allure reporting...")
        allure_issues = checker.test_validator.validate_allure_reporting()
        checker.all_issues.extend(allure_issues)
        checker._print_validation_results("Allure", allure_issues)
        
        # Run version validation
        print("\n🔢 Validating version consistency...")
        version_validator = VersionValidator(str(portfolio_root))
        version_issues = version_validator.validate_all_versions()
        checker.all_issues.extend(version_issues)
        checker._print_validation_results("Versions", version_issues)
        
    
    # Apply fixes if requested
    if args.fix and checker.all_issues:
        print("\n" + "=" * 60)
        print("🔧 APPLYING AUTOMATIC FIXES")
        print("=" * 60)
        
        fixer = IssueFixer(str(portfolio_root))
        fix_results = fixer.fix_issues(checker.all_issues)
        
        print(f"\n{fixer.get_fix_summary()}")
        
        # Re-run validation to see remaining issues
        if fix_results["fixed"] > 0:
            print("\n🔄 Re-running validation after fixes...")
            print("=" * 60)
            
            # Clear previous issues and re-run
            checker.all_issues = []
            if args.readmes_only:
                issues = checker.readme_validator.validate_all_readmes()
                checker.all_issues = issues
                checker._print_validation_results("README", issues)
            elif args.workflows_only:
                issues = checker.workflow_validator.validate_all_workflows()
                checker.all_issues = issues
                checker._print_validation_results("Workflows", issues)
            elif args.tests_only:
                issues = checker.test_validator.validate_all_tests()
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
        print("  - `python scripts/quality_checker.py --readmes-only`")
        print("  - `python scripts/quality_checker.py --workflows-only`")
        print("  - `python scripts/quality_checker.py --versions-only`")
        print("  - `python scripts/quality_checker.py --tests-only`")
    
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
