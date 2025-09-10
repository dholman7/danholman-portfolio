"""Main quality checker that orchestrates all validation."""

import sys
from pathlib import Path
from typing import List, Dict
from .readme_validator import ReadmeValidator, ValidationResult
from .workflow_validator import WorkflowValidator
from .test_validator import TestValidator


class QualityChecker:
    """Main quality checker that runs all validation checks."""
    
    def __init__(self, project_root: str = "."):
        """Initialize quality checker with project root."""
        self.project_root = project_root
        self.readme_validator = ReadmeValidator(project_root)
        self.workflow_validator = WorkflowValidator(project_root)
        self.test_validator = TestValidator(project_root)
        self.all_issues: List[ValidationResult] = []
    
    def run_all_checks(self) -> Dict[str, any]:
        """Run all quality checks and return results."""
        print("🔍 Running comprehensive code quality checks...")
        print("=" * 60)
        
        # Run README validation
        print("\n📚 Validating README files...")
        readme_issues = self.readme_validator.validate_all_readmes()
        self.all_issues.extend(readme_issues)
        self._print_validation_results("README", readme_issues)
        
        # Run workflow validation
        print("\n⚙️ Validating GitHub workflows...")
        workflow_issues = self.workflow_validator.validate_all_workflows()
        self.all_issues.extend(workflow_issues)
        self._print_validation_results("Workflows", workflow_issues)
        
        # Run test validation
        print("\n🧪 Validating test execution...")
        test_issues = self.test_validator.validate_all_tests()
        self.all_issues.extend(test_issues)
        self._print_validation_results("Tests", test_issues)
        
        # Run Allure validation
        print("\n📊 Validating Allure reporting...")
        allure_issues = self.test_validator.validate_allure_reporting()
        self.all_issues.extend(allure_issues)
        self._print_validation_results("Allure", allure_issues)
        
        # Print summary
        self._print_summary()
        
        return {
            "total_issues": len(self.all_issues),
            "readme_issues": len(readme_issues),
            "workflow_issues": len(workflow_issues),
            "test_issues": len(test_issues),
            "allure_issues": len(allure_issues),
            "issues": self.all_issues
        }
    
    def _print_validation_results(self, category: str, issues: List[ValidationResult]) -> None:
        """Print validation results for a category."""
        if not issues:
            print(f"✅ {category}: No issues found")
            return
        
        print(f"❌ {category}: {len(issues)} issues found")
        
        # Group by severity
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]
        info = [i for i in issues if i.severity == "info"]
        
        if errors:
            print(f"  🔴 Errors: {len(errors)}")
            for issue in errors[:5]:  # Show first 5 errors
                self._print_issue(issue, "    ")
            if len(errors) > 5:
                print(f"    ... and {len(errors) - 5} more errors")
        
        if warnings:
            print(f"  🟡 Warnings: {len(warnings)}")
            for issue in warnings[:3]:  # Show first 3 warnings
                self._print_issue(issue, "    ")
            if len(warnings) > 3:
                print(f"    ... and {len(warnings) - 3} more warnings")
        
        if info:
            print(f"  🔵 Info: {len(info)}")
            for issue in info[:2]:  # Show first 2 info items
                self._print_issue(issue, "    ")
            if len(info) > 2:
                print(f"    ... and {len(info) - 2} more info items")
    
    def _print_issue(self, issue: ValidationResult, indent: str = "") -> None:
        """Print a single issue."""
        location = ""
        if issue.file_path:
            location = f" ({Path(issue.file_path).name}"
            if issue.line_number:
                location += f":{issue.line_number}"
            location += ")"
        
        print(f"{indent}{issue.message}{location}")
    
    def _print_summary(self) -> None:
        """Print overall summary."""
        print("\n" + "=" * 60)
        print("📋 QUALITY CHECK SUMMARY")
        print("=" * 60)
        
        # Count by severity
        errors = len([i for i in self.all_issues if i.severity == "error"])
        warnings = len([i for i in self.all_issues if i.severity == "warning"])
        info = len([i for i in self.all_issues if i.severity == "info"])
        
        print(f"Total Issues: {len(self.all_issues)}")
        print(f"  🔴 Errors: {errors}")
        print(f"  🟡 Warnings: {warnings}")
        print(f"  🔵 Info: {info}")
        
        if errors == 0:
            print("\n🎉 All critical issues resolved!")
        else:
            print(f"\n⚠️  {errors} critical issues need attention")
        
        if warnings > 0:
            print(f"💡 {warnings} warnings should be reviewed")
        
        if info > 0:
            print(f"ℹ️  {info} informational items noted")
    
    def get_issues_by_severity(self, severity: str) -> List[ValidationResult]:
        """Get issues filtered by severity."""
        return [issue for issue in self.all_issues if issue.severity == severity]
    
    def has_critical_issues(self) -> bool:
        """Check if there are any critical (error) issues."""
        return len(self.get_issues_by_severity("error")) > 0
    
    def export_results(self, output_file: str) -> None:
        """Export results to a file."""
        import json
        
        results = {
            "summary": {
                "total_issues": len(self.all_issues),
                "errors": len(self.get_issues_by_severity("error")),
                "warnings": len(self.get_issues_by_severity("warning")),
                "info": len(self.get_issues_by_severity("info"))
            },
            "issues": [
                {
                    "severity": issue.severity,
                    "message": issue.message,
                    "file_path": issue.file_path,
                    "line_number": issue.line_number
                }
                for issue in self.all_issues
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results exported to: {output_file}")


def main():
    """Main entry point for quality checker."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Code Quality Checker")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--export", help="Export results to JSON file")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit with error code if critical issues found")
    
    args = parser.parse_args()
    
    checker = QualityChecker(args.project_root)
    results = checker.run_all_checks()
    
    if args.export:
        checker.export_results(args.export)
    
    if args.fail_on_error and checker.has_critical_issues():
        print("\n❌ Critical issues found - exiting with error code")
        sys.exit(1)
    
    print("\n✅ Quality check completed")


if __name__ == "__main__":
    main()
