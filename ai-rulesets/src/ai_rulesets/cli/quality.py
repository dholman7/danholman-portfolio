"""Quality checking CLI commands."""

import click
from ai_rulesets.validation.quality_checker import QualityChecker


@click.command()
@click.option("--project-root", default=".", help="Project root directory")
@click.option("--export", help="Export results to JSON file")
@click.option("--fail-on-error", is_flag=True, help="Exit with error code if critical issues found")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def check_quality(project_root: str, export: str, fail_on_error: bool, verbose: bool):
    """Run comprehensive code quality checks."""
    checker = QualityChecker(project_root)
    results = checker.run_all_checks()
    
    if export:
        checker.export_results(export)
    
    if fail_on_error and checker.has_critical_issues():
        click.echo("\n❌ Critical issues found - exiting with error code")
        raise click.Abort()
    
    click.echo("\n✅ Quality check completed")


@click.command()
@click.option("--project-root", default=".", help="Project root directory")
def check_readmes(project_root: str):
    """Check README files for accuracy and completeness."""
    from ai_rulesets.validation.readme_validator import ReadmeValidator
    
    validator = ReadmeValidator(project_root)
    issues = validator.validate_all_readmes()
    
    if not issues:
        click.echo("✅ All README files are valid")
    else:
        click.echo(f"❌ Found {len(issues)} README issues")
        for issue in issues:
            location = ""
            if issue.file_path:
                location = f" ({issue.file_path}"
                if issue.line_number:
                    location += f":{issue.line_number}"
                location += ")"
            
            click.echo(f"  {issue.severity.upper()}: {issue.message}{location}")


@click.command()
@click.option("--project-root", default=".", help="Project root directory")
def check_workflows(project_root: str):
    """Check GitHub workflow files for accuracy and completeness."""
    from ai_rulesets.validation.workflow_validator import WorkflowValidator
    
    validator = WorkflowValidator(project_root)
    issues = validator.validate_all_workflows()
    
    if not issues:
        click.echo("✅ All workflow files are valid")
    else:
        click.echo(f"❌ Found {len(issues)} workflow issues")
        for issue in issues:
            location = ""
            if issue.file_path:
                location = f" ({issue.file_path}"
                if issue.line_number:
                    location += f":{issue.line_number}"
                location += ")"
            
            click.echo(f"  {issue.severity.upper()}: {issue.message}{location}")


@click.command()
@click.option("--project-root", default=".", help="Project root directory")
def check_tests(project_root: str):
    """Check test execution and reporting."""
    from ai_rulesets.validation.test_validator import TestValidator
    
    validator = TestValidator(project_root)
    issues = validator.validate_all_tests()
    
    if not issues:
        click.echo("✅ All tests are valid")
    else:
        click.echo(f"❌ Found {len(issues)} test issues")
        for issue in issues:
            location = ""
            if issue.file_path:
                location = f" ({issue.file_path}"
                if issue.line_number:
                    location += f":{issue.line_number}"
                location += ")"
            
            click.echo(f"  {issue.severity.upper()}: {issue.message}{location}")


@click.group()
def quality():
    """Code quality checking commands."""
    pass


# Add commands to the group
quality.add_command(check_quality, name="check")
quality.add_command(check_readmes, name="readmes")
quality.add_command(check_workflows, name="workflows")
quality.add_command(check_tests, name="tests")
