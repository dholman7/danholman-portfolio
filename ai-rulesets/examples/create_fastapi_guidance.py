#!/usr/bin/env python3
"""
Example script showing how to create a custom FastAPI guidance template
and generate AI assistant guidance files.
"""

import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_rulesets.core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem
from ai_rulesets.renderers import CursorRenderer, CopilotRenderer


def create_fastapi_guidance_template():
    """Create a comprehensive FastAPI testing guidance template."""
    
    # Create metadata
    metadata = GuidanceTemplateMetadata(
        name="FastAPI Testing Guidance",
        version="1.0.0",
        description="Comprehensive guidance for testing FastAPI applications with pytest and httpx",
        languages=["python"],
        frameworks=["fastapi", "pytest", "httpx"],
        categories=["api", "integration", "unit"],
        author="AI Test Generation Framework",
        license="MIT"
    )
    
    # Create the template
    template = GuidanceTemplate(metadata=metadata)
    
    # Add guidance items
    template.add_guidance(GuidanceItem(
        name="API Endpoint Testing",
        description="Test FastAPI endpoints with proper request/response validation",
        content="""# Test FastAPI endpoints
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

# Use TestClient for synchronous testing
def test_get_endpoint():
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# Use AsyncClient for async testing
@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users/1")
        assert response.status_code == 200""",
        tags=["api", "endpoints", "fastapi"],
        priority=1
    ))
    
    template.add_guidance(GuidanceItem(
        name="Dependency Injection Testing",
        description="Test FastAPI dependencies and dependency overrides",
        content="""# Test FastAPI dependencies
from fastapi import Depends
from unittest.mock import Mock

# Override dependencies for testing
def test_with_dependency_override():
    def override_get_db():
        return Mock()
    
    app.dependency_overrides[get_db] = override_get_db
    
    client = TestClient(app)
    response = client.get("/protected-route")
    assert response.status_code == 200
    
    # Clean up
    app.dependency_overrides.clear()""",
        tags=["dependencies", "mocking", "fastapi"],
        priority=2
    ))
    
    template.add_guidance(GuidanceItem(
        name="Request Validation Testing",
        description="Test request body validation and error responses",
        content="""# Test request validation
def test_invalid_request_body():
    client = TestClient(app)
    response = client.post("/users", json={"invalid": "data"})
    assert response.status_code == 422
    assert "validation error" in response.json()["detail"][0]["msg"]

def test_missing_required_fields():
    client = TestClient(app)
    response = client.post("/users", json={})
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("field required" in error["msg"] for error in errors)""",
        tags=["validation", "errors", "pydantic"],
        priority=2
    ))
    
    template.add_guidance(GuidanceItem(
        name="Response Model Testing",
        description="Test response models and serialization",
        content="""# Test response models
def test_response_model_serialization():
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 200
    
    user = response.json()
    # Verify all expected fields are present
    assert "id" in user
    assert "name" in user
    assert "email" in user
    assert "age" in user
    
    # Verify data types
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["email"], str)""",
        tags=["serialization", "models", "pydantic"],
        priority=2
    ))
    
    template.add_guidance(GuidanceItem(
        name="Error Handling Testing",
        description="Test HTTP exceptions and error responses",
        content="""# Test error handling
def test_404_error():
    client = TestClient(app)
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_422_validation_error():
    client = TestClient(app)
    response = client.post("/users", json={"name": ""})  # Empty name
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("string too short" in error["msg"] for error in errors)""",
        tags=["errors", "exceptions", "http"],
        priority=2
    ))
    
    return template


def generate_guidance_files(template: GuidanceTemplate, output_dir: Path):
    """Generate guidance files for different AI assistants."""
    
    # Create output directories
    cursor_dir = output_dir / ".cursor" / "rules"
    copilot_dir = output_dir / ".github" / "instructions"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    copilot_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate Cursor guidance
    cursor_renderer = CursorRenderer()
    cursor_guidance = cursor_renderer.render(template, language="python")
    cursor_file = cursor_dir / "fastapi-testing-guidance.mdc"
    with open(cursor_file, "w", encoding="utf-8") as f:
        f.write(cursor_guidance)
    print(f"Generated Cursor guidance: {cursor_file}")
    
    # Generate GitHub Copilot guidance
    copilot_renderer = CopilotRenderer()
    copilot_guidance = copilot_renderer.render(template, language="python")
    copilot_file = copilot_dir / "fastapi-testing-guidance.instructions.md"
    with open(copilot_file, "w", encoding="utf-8") as f:
        f.write(copilot_guidance)
    print(f"Generated GitHub Copilot guidance: {copilot_file}")
    
    # Save the original template as YAML
    yaml_file = output_dir / "fastapi-testing-guidance.yaml"
    template.save_to_file(yaml_file)
    print(f"Saved template as YAML: {yaml_file}")


def main():
    """Main function to create and generate FastAPI guidance."""
    print("Creating FastAPI testing guidance template...")
    
    # Create the template
    template = create_fastapi_guidance_template()
    
    # Generate guidance files
    output_dir = Path(__file__).parent
    generate_guidance_files(template, output_dir)
    
    print("\n✅ FastAPI guidance template created successfully!")
    print("\nNext steps:")
    print("1. Copy the generated files to your project:")
    print("   - .cursor/rules/fastapi-testing-guidance.mdc")
    print("   - .github/instructions/fastapi-testing-guidance.instructions.md")
    print("2. Ask your AI assistant to generate tests for your FastAPI app")
    print("3. Use the guidance patterns to ensure consistent test structure")


if __name__ == "__main__":
    main()
