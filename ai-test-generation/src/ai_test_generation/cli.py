"""
Command-line interface for AI test generation.
"""

import click
from pathlib import Path
from typing import List, Optional

from .core import GuidanceTemplate
from .renderers import CursorRenderer, CopilotRenderer


@click.group()
def main():
    """AI Test Generation Framework - Guidance templates for AI-powered test generation."""
    pass


@main.command()
@click.option("--output", "-o", type=click.Path(), default=".cursor/rules", 
              help="Output directory for Cursor guidance")
@click.option("--type", "-t", "template_types", multiple=True, 
              help="Template types to generate (python, typescript, api, contract)")
@click.option("--language", "-l", help="Target language for code blocks")
def generate_cursor(output: str, template_types: List[str], language: Optional[str]):
    """Generate Cursor guidance files."""
    output_path = Path(output)
    
    if not template_types:
        template_types = ["python", "typescript", "api", "contract"]
    
    click.echo(f"Generating Cursor guidance for: {', '.join(template_types)}")
    click.echo(f"Output directory: {output_path}")
    
    # For now, create placeholder templates
    # In a real implementation, these would be loaded from the templates directory
    templates = []
    
    for template_type in template_types:
        if template_type == "python":
            template = _create_python_pytest_template()
            templates.append(template)
        elif template_type == "typescript":
            template = _create_typescript_jest_template()
            templates.append(template)
        elif template_type == "api":
            template = _create_api_rest_template()
            templates.append(template)
        elif template_type == "contract":
            template = _create_contract_pact_template()
            templates.append(template)
    
    # Render files
    renderer = CursorRenderer()
    renderer.render_multiple(templates, output_path, language)
    
    click.echo(f"Generated {len(templates)} Cursor guidance files in {output_path}")


@main.command()
@click.option("--output", "-o", type=click.Path(), default=".github/instructions", 
              help="Output directory for GitHub Copilot guidance")
@click.option("--type", "-t", "template_types", multiple=True, 
              help="Template types to generate (python, typescript, api, contract)")
@click.option("--language", "-l", help="Target language for code blocks")
def generate_copilot(output: str, template_types: List[str], language: Optional[str]):
    """Generate GitHub Copilot guidance files."""
    output_path = Path(output)
    
    if not template_types:
        template_types = ["python", "typescript", "api", "contract"]
    
    click.echo(f"Generating GitHub Copilot guidance for: {', '.join(template_types)}")
    click.echo(f"Output directory: {output_path}")
    
    # For now, create placeholder templates
    templates = []
    
    for template_type in template_types:
        if template_type == "python":
            template = _create_python_pytest_template()
            templates.append(template)
        elif template_type == "typescript":
            template = _create_typescript_jest_template()
            templates.append(template)
        elif template_type == "api":
            template = _create_api_rest_template()
            templates.append(template)
        elif template_type == "contract":
            template = _create_contract_pact_template()
            templates.append(template)
    
    # Render files
    renderer = CopilotRenderer()
    renderer.render_multiple(templates, output_path, language)
    
    click.echo(f"Generated {len(templates)} GitHub Copilot guidance files in {output_path}")


@main.command()
@click.option("--type", "-t", "template_types", multiple=True, 
              help="Template types to list (python, typescript, api, contract)")
def list_templates(template_types: List[str]):
    """List available guidance templates."""
    if not template_types:
        template_types = ["python", "typescript", "api", "contract"]
    
    click.echo("Available guidance templates:")
    for template_type in template_types:
        click.echo(f"  - {template_type}")


# Placeholder template creators
# In a real implementation, these would load from YAML files

def _create_python_pytest_template() -> GuidanceTemplate:
    """Create a Python pytest guidance template."""
    from .core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem
    
    metadata = GuidanceTemplateMetadata(
        name="Python pytest Testing Guidance",
        version="1.0.0",
        description="Comprehensive guidance for generating pytest-based tests",
        languages=["python"],
        frameworks=["pytest"],
        categories=["unit", "integration"],
        author="Dan Holman"
    )
    
    template = GuidanceTemplate(metadata=metadata)
    
    # Test structure guidance
    template.add_guidance(GuidanceItem(
        name="Test Structure",
        description="Define proper test file and function structure",
        content="""# Test files should be named test_*.py or *_test.py
# Test functions should start with test_
# Use descriptive test names that explain the behavior

def test_user_can_login_with_valid_credentials():
    \"\"\"Test that user can login with valid credentials.\"\"\"
    pass

def test_user_cannot_login_with_invalid_credentials():
    \"\"\"Test that user cannot login with invalid credentials.\"\"\"
    pass""",
        tags=["structure", "naming"],
        priority=1
    ))
    
    # Fixtures guidance
    template.add_guidance(GuidanceItem(
        name="Fixtures",
        description="Use pytest fixtures for setup and teardown",
        content="""# Use @pytest.fixture for reusable test data
# Scope fixtures appropriately (function, class, module, session)
# Use parametrized fixtures for multiple test cases

import pytest

@pytest.fixture
def sample_user():
    \"\"\"Create a sample user for testing.\"\"\"
    return User(name="Test User", email="test@example.com")

@pytest.fixture(scope="module")
def database():
    \"\"\"Create a test database.\"\"\"
    db = create_test_database()
    yield db
    db.cleanup()

@pytest.fixture(params=["admin", "user", "guest"])
def user_role(request):
    \"\"\"Create users with different roles.\"\"\"
    return create_user(role=request.param)""",
        tags=["fixtures", "setup"],
        priority=1
    ))
    
    return template


def _create_typescript_jest_template() -> GuidanceTemplate:
    """Create a TypeScript Jest guidance template."""
    from .core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem
    
    metadata = GuidanceTemplateMetadata(
        name="TypeScript Jest Testing Rules",
        version="1.0.0",
        description="Comprehensive rules for generating Jest-based tests",
        languages=["typescript", "javascript"],
        frameworks=["jest"],
        categories=["unit", "integration"],
        author="Dan Holman"
    )
    
    template = GuidanceTemplate(metadata=metadata)
    
    # Test structure rule
    template.add_guidance(GuidanceItem(
        name="Test Structure",
        description="Define proper test file and function structure",
        content="""// Test files should be named *.test.ts or *.spec.ts
// Test functions should use describe() and it() or test()
// Use descriptive test names that explain the behavior

describe('UserService', () => {
  it('should create a user with valid data', () => {
    // Test implementation
  });

  it('should throw error when creating user with invalid data', () => {
    // Test implementation
  });
});""",
        tags=["structure", "naming"],
        priority=1
    ))
    
    return template


def _create_api_rest_rule_set() -> GuidanceTemplate:
    """Create an API REST testing rule set."""
    from .core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem
    
    metadata = GuidanceTemplateMetadata(
        name="REST API Testing Rules",
        version="1.0.0",
        description="Comprehensive rules for testing REST APIs",
        languages=["python", "typescript", "javascript"],
        frameworks=["pytest", "jest", "requests"],
        categories=["api", "integration"],
        author="Dan Holman"
    )
    
    template = GuidanceTemplate(metadata=metadata)
    
    # API testing rule
    template.add_guidance(GuidanceItem(
        name="API Test Structure",
        description="Structure for testing REST API endpoints",
        content="""# Test API endpoints with proper request/response validation
# Test different HTTP methods (GET, POST, PUT, DELETE)
# Test status codes, headers, and response body structure

def test_get_user_returns_200():
    \"\"\"Test GET /users/{id} returns 200 with user data.\"\"\"
    response = requests.get(f"{BASE_URL}/users/1")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "email" in data

def test_create_user_returns_201():
    \"\"\"Test POST /users returns 201 with created user.\"\"\"
    user_data = {"name": "Test User", "email": "test@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]""",
        tags=["api", "rest", "http"],
        priority=1
    ))
    
    return template


def _create_contract_pact_rule_set() -> GuidanceTemplate:
    """Create a Pact contract testing rule set."""
    from .core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem
    
    metadata = GuidanceTemplateMetadata(
        name="Pact Contract Testing Rules",
        version="1.0.0",
        description="Comprehensive rules for Pact contract testing",
        languages=["python", "typescript", "javascript"],
        frameworks=["pact-python", "pact-js"],
        categories=["contract", "integration"],
        author="Dan Holman"
    )
    
    template = GuidanceTemplate(metadata=metadata)
    
    # Contract testing rule
    template.add_guidance(GuidanceItem(
        name="Pact Consumer Tests",
        description="Structure for Pact consumer contract tests",
        content="""# Define consumer expectations for API interactions
# Use Pact to mock provider responses
# Test that consumer can handle expected provider responses

from pact import Consumer, Provider

def test_get_user_contract():
    \"\"\"Test contract for getting a user.\"\"\"
    pact = Consumer('UserService').has_pact_with(Provider('UserAPI'))
    
    (pact
     .given('user exists')
     .upon_receiving('a request for user')
     .with_request('GET', '/users/1')
     .will_respond_with(200, body={
         'id': 1,
         'name': 'Test User',
         'email': 'test@example.com'
     }))
    
    with pact:
        # Test your consumer code here
        user = user_service.get_user(1)
        assert user.id == 1
        assert user.name == 'Test User'""",
        tags=["contract", "pact", "consumer"],
        priority=1
    ))
    
    return template


if __name__ == "__main__":
    main()
