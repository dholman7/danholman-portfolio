"""
Command-line interface for AI rulesets and organizational standards.
"""

import click
from pathlib import Path
from typing import List, Optional

from .core import Ruleset, RulesetMetadata, RulesetItem, RulesetManager
from .renderers import CursorRenderer, CopilotRenderer, GenericRenderer
from .cli.generate import generate_rulesets, generate_from_sources


@click.group()
def main():
    """AI Rulesets - Organizational development standards and utilities."""
    pass


@main.command()
@click.option("--output", "-o", type=click.Path(), default=".cursor/rules", 
              help="Output directory for Cursor rulesets")
@click.option("--type", "-t", "ruleset_types", multiple=True, 
              help="Ruleset types to generate (python, typescript, testing, cicd, security)")
@click.option("--all", "generate_all", is_flag=True, help="Generate all available rulesets")
def generate_cursor(output: str, ruleset_types: List[str], generate_all: bool):
    """Generate Cursor ruleset files."""
    output_path = Path(output)
    
    if generate_all:
        ruleset_types = ["python", "typescript", "testing", "cicd", "security"]
    elif not ruleset_types:
        ruleset_types = ["python", "testing"]
    
    click.echo(f"Generating Cursor rulesets for: {', '.join(ruleset_types)}")
    click.echo(f"Output directory: {output_path}")
    
    # Create rulesets
    rulesets = []
    
    for ruleset_type in ruleset_types:
        if ruleset_type == "python":
            ruleset = _create_python_development_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "typescript":
            ruleset = _create_typescript_development_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "testing":
            ruleset = _create_testing_guidelines_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "cicd":
            ruleset = _create_cicd_infrastructure_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "security":
            ruleset = _create_security_standards_ruleset()
            rulesets.append(ruleset)
    
    # Render files
    renderer = CursorRenderer()
    renderer.render_multiple(rulesets, output_path)
    
    click.echo(f"Generated {len(rulesets)} Cursor ruleset files in {output_path}")


@main.command()
@click.option("--output", "-o", type=click.Path(), default=".github/instructions", 
              help="Output directory for GitHub Copilot instructions")
@click.option("--type", "-t", "ruleset_types", multiple=True, 
              help="Ruleset types to generate (python, typescript, testing, cicd, security)")
@click.option("--all", "generate_all", is_flag=True, help="Generate all available rulesets")
def generate_copilot(output: str, ruleset_types: List[str], generate_all: bool):
    """Generate GitHub Copilot instruction files."""
    output_path = Path(output)
    
    if generate_all:
        ruleset_types = ["python", "typescript", "testing", "cicd", "security"]
    elif not ruleset_types:
        ruleset_types = ["python", "testing"]
    
    click.echo(f"Generating GitHub Copilot instructions for: {', '.join(ruleset_types)}")
    click.echo(f"Output directory: {output_path}")
    
    # Create rulesets
    rulesets = []
    
    for ruleset_type in ruleset_types:
        if ruleset_type == "python":
            ruleset = _create_python_development_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "typescript":
            ruleset = _create_typescript_development_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "testing":
            ruleset = _create_testing_guidelines_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "cicd":
            ruleset = _create_cicd_infrastructure_ruleset()
            rulesets.append(ruleset)
        elif ruleset_type == "security":
            ruleset = _create_security_standards_ruleset()
            rulesets.append(ruleset)
    
    # Render files
    renderer = CopilotRenderer()
    renderer.render_multiple(rulesets, output_path)
    
    click.echo(f"Generated {len(rulesets)} GitHub Copilot instruction files in {output_path}")


@main.command()
@click.option("--input", "-i", type=click.Path(), required=True,
              help="Input directory or file containing documentation")
@click.option("--output", "-o", type=click.Path(), default=".cursor/rules",
              help="Output directory for generated rulesets")
@click.option("--type", "-t", "ruleset_type", default="generic",
              help="Type of ruleset to generate (generic, python, typescript)")
@click.option("--format", "-f", "output_format", type=click.Choice(["cursor", "copilot", "generic"]),
              default="cursor", help="Output format for rulesets")
def generate_from_docs(input: str, output: str, ruleset_type: str, output_format: str):
    """Generate rulesets from company documentation."""
    input_path = Path(input)
    output_path = Path(output)
    
    if not input_path.exists():
        click.echo(f"Error: Input path {input_path} does not exist")
        return
    
    click.echo(f"Generating {ruleset_type} rulesets from: {input_path}")
    click.echo(f"Output format: {output_format}")
    click.echo(f"Output directory: {output_path}")
    
    # For now, create a placeholder ruleset
    # In a real implementation, this would process the documentation
    ruleset = _create_generic_ruleset_from_docs(input_path, ruleset_type)
    
    # Choose renderer based on format
    if output_format == "cursor":
        renderer = CursorRenderer()
        filename = f"{ruleset.metadata.name}.mdc"
    elif output_format == "copilot":
        renderer = CopilotRenderer()
        filename = f"{ruleset.metadata.name}.instructions.md"
    else:
        renderer = GenericRenderer()
        filename = f"{ruleset.metadata.name}.md"
    
    output_file = output_path / filename
    renderer.render_file(ruleset, output_file)
    
    click.echo(f"Generated ruleset: {output_file}")


@main.command()
@click.option("--input", "-i", type=click.Path(), required=True,
              help="Input directory containing rulesets to validate")
def validate(input: str):
    """Validate rulesets for completeness and correctness."""
    input_path = Path(input)
    
    if not input_path.exists():
        click.echo(f"Error: Input path {input_path} does not exist")
        return
    
    click.echo(f"Validating rulesets in: {input_path}")
    
    manager = RulesetManager()
    issues_found = False
    
    # Find all ruleset files
    for ruleset_file in input_path.rglob("*.yaml"):
        try:
            ruleset = manager.load_ruleset_from_file(ruleset_file)
            issues = manager.validate_ruleset(ruleset)
            
            if issues:
                click.echo(f"❌ {ruleset_file}: {len(issues)} issues found")
                for issue in issues:
                    click.echo(f"  - {issue}")
                issues_found = True
            else:
                click.echo(f"✅ {ruleset_file}: Valid")
                
        except Exception as e:
            click.echo(f"❌ {ruleset_file}: Error loading - {e}")
            issues_found = True
    
    if not issues_found:
        click.echo("All rulesets are valid!")
    else:
        click.echo("Some rulesets have issues that need to be fixed.")


@main.command()
@click.option("--type", "-t", "ruleset_types", multiple=True, 
              help="Ruleset types to list (python, typescript, testing, cicd, security)")
def list_rulesets(ruleset_types: List[str]):
    """List available rulesets."""
    if not ruleset_types:
        ruleset_types = ["python", "typescript", "testing", "cicd", "security"]
    
    click.echo("Available rulesets:")
    for ruleset_type in ruleset_types:
        click.echo(f"  - {ruleset_type}")


# Add generate commands
main.add_command(generate_rulesets, name="generate-rulesets")
main.add_command(generate_from_sources, name="generate-from-sources")


# Ruleset creators
# In a real implementation, these would load from YAML files

def _create_python_development_ruleset() -> Ruleset:
    """Create a Python development standards ruleset."""
    metadata = RulesetMetadata(
        name="Python Development Standards",
        version="1.0.0",
        description="Organizational Python development standards and best practices",
        categories=["development", "python", "standards"],
        tags=["python", "pytest", "black", "ruff", "mypy"],
        author="Dan Holman",
        maintainer="engineering@company.com"
    )
    
    ruleset = Ruleset(metadata=metadata)
    
    # Code style rule
    ruleset.add_rule(RulesetItem(
        name="Code Style",
        description="Python code style guidelines",
        content="""# Use Black for code formatting with 88-character line limit
# Use Ruff for linting and code analysis
# Follow PEP 8 with organizational modifications
# Use type hints extensively for better IDE support
# Use meaningful variable and function names
# Group imports: standard library, third-party, local imports""",
        tags=["style", "formatting", "linting"],
        priority=1,
        category="code-quality"
    ))
    
    # Testing rule
    ruleset.add_rule(RulesetItem(
        name="Testing Standards",
        description="Python testing guidelines and patterns",
        content="""# Use pytest for all testing
# Write descriptive test names that explain behavior
# Use fixtures for test data and setup
# Aim for 80%+ test coverage
# Use parametrized tests for multiple test cases
# Mock external dependencies appropriately""",
        tags=["testing", "pytest", "coverage"],
        priority=1,
        category="testing"
    ))
    
    return ruleset


def _create_typescript_development_ruleset() -> Ruleset:
    """Create a TypeScript development standards ruleset."""
    metadata = RulesetMetadata(
        name="TypeScript Development Standards",
        version="1.0.0",
        description="Organizational TypeScript development standards and best practices",
        categories=["development", "typescript", "standards"],
        tags=["typescript", "jest", "eslint", "prettier"],
        author="Dan Holman",
        maintainer="engineering@company.com"
    )
    
    ruleset = Ruleset(metadata=metadata)
    
    # Code style rule
    ruleset.add_rule(RulesetItem(
        name="TypeScript Code Style",
        description="TypeScript code style guidelines",
        content="""# Use ESLint and Prettier for code formatting
# Follow Airbnb TypeScript style guide
# Use strict type checking and strict mode
# Leverage modern ES6+ features: arrow functions, destructuring, template literals
# Use meaningful variable and function names
# Implement proper interfaces and type definitions""",
        tags=["style", "formatting", "typescript"],
        priority=1,
        category="code-quality"
    ))
    
    return ruleset


def _create_testing_guidelines_ruleset() -> Ruleset:
    """Create a testing guidelines ruleset."""
    metadata = RulesetMetadata(
        name="Testing Guidelines",
        version="1.0.0",
        description="Comprehensive testing guidelines and best practices",
        categories=["testing", "quality", "standards"],
        tags=["testing", "pytest", "jest", "playwright", "coverage"],
        author="Dan Holman",
        maintainer="engineering@company.com"
    )
    
    ruleset = Ruleset(metadata=metadata)
    
    # Testing principles rule
    ruleset.add_rule(RulesetItem(
        name="Testing Principles",
        description="Core testing principles and best practices",
        content="""# Write tests that are fast, independent, repeatable, and self-validating
# Use the Arrange-Act-Assert pattern for test structure
# Implement proper test data management
# Use Page Object Model for UI testing
# Implement proper test isolation and cleanup
# Use appropriate test doubles (mocks, stubs, fakes)""",
        tags=["principles", "best-practices"],
        priority=1,
        category="testing"
    ))
    
    return ruleset


def _create_cicd_infrastructure_ruleset() -> Ruleset:
    """Create a CI/CD infrastructure ruleset."""
    metadata = RulesetMetadata(
        name="CI/CD Infrastructure Standards",
        version="1.0.0",
        description="CI/CD and infrastructure development standards",
        categories=["cicd", "infrastructure", "devops"],
        tags=["github-actions", "docker", "aws", "deployment"],
        author="Dan Holman",
        maintainer="engineering@company.com"
    )
    
    ruleset = Ruleset(metadata=metadata)
    
    # CI/CD rule
    ruleset.add_rule(RulesetItem(
        name="CI/CD Best Practices",
        description="CI/CD pipeline best practices and standards",
        content="""# Use path-based triggers to run only relevant jobs
# Implement proper caching for dependencies
# Use matrix strategies for multi-version testing
# Implement proper error handling and rollback strategies
# Use proper secret management
# Include linting, testing, and security scanning in all pipelines""",
        tags=["cicd", "pipelines", "automation"],
        priority=1,
        category="infrastructure"
    ))
    
    return ruleset


def _create_security_standards_ruleset() -> Ruleset:
    """Create a security standards ruleset."""
    metadata = RulesetMetadata(
        name="Security Standards",
        version="1.0.0",
        description="Security-first development standards and guidelines",
        categories=["security", "standards", "compliance"],
        tags=["security", "owasp", "vulnerability", "encryption"],
        author="Dan Holman",
        maintainer="security@company.com"
    )
    
    ruleset = Ruleset(metadata=metadata)
    
    # Security rule
    ruleset.add_rule(RulesetItem(
        name="Security Best Practices",
        description="Security-first development practices",
        content="""# Never commit secrets or sensitive data
# Use environment variables for configuration
# Implement proper authentication and authorization
# Use proper input validation
# Use encryption at rest and in transit
# Follow OWASP security guidelines
# Implement proper secret rotation strategies""",
        tags=["security", "secrets", "encryption"],
        priority=1,
        category="security"
    ))
    
    return ruleset


def _create_generic_ruleset_from_docs(input_path: Path, ruleset_type: str) -> Ruleset:
    """Create a generic ruleset from documentation (placeholder implementation)."""
    metadata = RulesetMetadata(
        name=f"Custom {ruleset_type.title()} Ruleset",
        version="1.0.0",
        description=f"Custom ruleset generated from {input_path}",
        categories=["custom", ruleset_type],
        tags=["custom", "generated"],
        author="AI Rulesets Generator"
    )
    
    ruleset = Ruleset(metadata=metadata)
    
    # Placeholder rule
    ruleset.add_rule(RulesetItem(
        name="Documentation Processing",
        description="Placeholder rule for documentation processing",
        content=f"# This ruleset was generated from documentation in {input_path}\n# In a real implementation, this would process the actual documentation content",
        tags=["placeholder", "generated"],
        priority=1,
        category="custom"
    ))
    
    return ruleset


if __name__ == "__main__":
    main()