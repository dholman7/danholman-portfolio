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
from issue_fixer import IssueFixer


def main():
    """Main entry point for the portfolio quality checker."""
    parser = argparse.ArgumentParser(description="Portfolio-wide code quality checker")
    parser.add_argument("--readmes-only", action="store_true", help="Check only README files")
    parser.add_argument("--workflows-only", action="store_true", help="Check only GitHub workflows")
    parser.add_argument("--tests-only", action="store_true", help="Check only test execution")
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
    else:
        # Run all checks
        results = checker.run_all_checks()
    
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
