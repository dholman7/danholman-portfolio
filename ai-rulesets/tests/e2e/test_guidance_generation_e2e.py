"""
End-to-end tests for complete guidance generation workflows.

These tests simulate real user interactions and test complete workflows from
start to finish, verifying that the entire system works correctly from
the user's perspective.
"""

import pytest
import allure
import tempfile
import subprocess
import sys
from pathlib import Path
from ai_rulesets.core import Ruleset, RulesetMetadata, RulesetItem
from ai_rulesets.renderers import CursorRenderer, CopilotRenderer


@allure.epic("AI Rulesets")
@allure.feature("Guidance Generation")
@pytest.mark.e2e
class TestGuidanceGenerationE2E:
    """Test complete guidance generation workflow."""

    @allure.story("Complete Workflow")
    @allure.title("Complete guidance generation workflow from template creation to file generation")
    @allure.description("Test complete workflow from template creation to file generation including Cursor and Copilot guidance")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("e2e", "guidance", "workflow")
    def test_complete_guidance_generation_workflow(self):
        """Test complete workflow from template creation to file generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            with allure.step("Step 1: Create comprehensive guidance template"):
                metadata = RulesetMetadata(
                    name="E2E Test Template",
                    version="1.0.0",
                    description="Comprehensive template for E2E testing",
                    categories=["unit", "integration", "e2e"],
                    author="Test Author",
                    license="MIT"
                )
                allure.attach(str(metadata.__dict__), "Template Metadata", allure.attachment_type.JSON)
                
                template = Ruleset(metadata=metadata)
                
                # Add multiple guidance items with different priorities
                template.add_rule(RulesetItem(
                    name="High Priority Testing Guidance",
                    description="Critical testing patterns",
                    content="# High Priority Testing\n\nAlways write tests for critical business logic.",
                    tags=["critical", "testing", "patterns"],
                    priority=3
                ))
                
                template.add_rule(RulesetItem(
                    name="Medium Priority API Testing",
                    description="API testing best practices",
                    content="# API Testing\n\nTest all API endpoints with proper error handling.",
                    tags=["api", "testing", "best-practices"],
                    priority=2
                ))
                
                template.add_rule(RulesetItem(
                    name="Low Priority Documentation",
                    description="Documentation guidelines",
                    content="# Documentation\n\nWrite clear, concise test documentation.",
                    tags=["documentation", "guidelines"],
                    priority=1
                ))
                allure.attach(f"Added {len(template.rules)} guidance rules", "Rules Count", allure.attachment_type.TEXT)
            
            with allure.step("Step 2: Save template to file"):
                template_path = temp_path / "e2e_template.yaml"
                template.save_to_file(template_path)
                allure.attach(str(template_path), "Template File Path", allure.attachment_type.TEXT)
                assert template_path.exists()
            
            with allure.step("Step 3: Load template from file"):
                loaded_template = Ruleset.from_file(template_path)
                allure.attach(loaded_template.metadata.name, "Loaded Template Name", allure.attachment_type.TEXT)
                assert loaded_template.metadata.name == template.metadata.name
                assert len(loaded_template.rules) == 3
            
            with allure.step("Step 4: Generate Cursor guidance"):
                cursor_renderer = CursorRenderer()
                cursor_output = temp_path / "cursor_guidance.mdc"
                cursor_renderer.render_file(loaded_template, cursor_output)
                allure.attach(str(cursor_output), "Cursor Output Path", allure.attachment_type.TEXT)
                assert cursor_output.exists()
                
                cursor_content = cursor_output.read_text()
                allure.attach(cursor_content, "Cursor Guidance Content", allure.attachment_type.TEXT)
                assert "E2E Test Template" in cursor_content
                assert "High Priority Testing" in cursor_content
                assert "API Testing" in cursor_content
                assert "Documentation" in cursor_content
            
            with allure.step("Step 5: Generate Copilot guidance"):
                copilot_renderer = CopilotRenderer()
                copilot_output = temp_path / "copilot_guidance.instructions.md"
                copilot_renderer.render_file(loaded_template, copilot_output)
                allure.attach(str(copilot_output), "Copilot Output Path", allure.attachment_type.TEXT)
                assert copilot_output.exists()
                
                copilot_content = copilot_output.read_text()
                allure.attach(copilot_content, "Copilot Guidance Content", allure.attachment_type.TEXT)
                assert "E2E Test Template" in copilot_content
                assert "High Priority Testing" in copilot_content
                assert "API Testing" in copilot_content
                assert "Documentation" in copilot_content
            
            with allure.step("Step 6: Verify guidance items are in priority order"):
                cursor_lines = cursor_content.split('\n')
                high_priority_line = None
                medium_priority_line = None
                low_priority_line = None
                
                for i, line in enumerate(cursor_lines):
                    if "High Priority Testing" in line:
                        high_priority_line = i
                    elif "Medium Priority API Testing" in line:
                        medium_priority_line = i
                    elif "Low Priority Documentation" in line:
                        low_priority_line = i
                
                allure.attach(f"Priority order: High={high_priority_line}, Medium={medium_priority_line}, Low={low_priority_line}", 
                             "Priority Order", allure.attachment_type.TEXT)
                assert high_priority_line is not None
                assert medium_priority_line is not None
                assert low_priority_line is not None
                assert high_priority_line < medium_priority_line < low_priority_line

    def test_cli_complete_workflow(self):
        """Test complete workflow using CLI commands."""
        pytest.skip("CLI is a quality checker, not a template generator")

    @allure.story("Multi-Language Template")
    @allure.title("Workflow with multi-language template")
    @allure.description("Test workflow with multi-language template supporting Python, TypeScript, Java, and Go")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "multi-language", "templates")
    def test_multi_language_template_workflow(self):
        """Test workflow with multi-language template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            with allure.step("Step 1: Create multi-language template"):
                metadata = RulesetMetadata(
                    name="Multi-Language Template",
                    version="2.0.0",
                    description="Template supporting multiple languages",
                    categories=["unit", "integration", "performance"],
                    author="Multi-Lang Author",
                    license="Apache-2.0"
                )
                allure.attach(str(metadata.__dict__), "Multi-Language Metadata", allure.attachment_type.JSON)
                
                template = Ruleset(metadata=metadata)
                
                # Add language-specific guidance
                languages = ["Python", "TypeScript", "Java", "Go"]
                for lang in languages:
                    template.add_rule(RulesetItem(
                        name=f"{lang} Testing",
                        description=f"{lang}-specific testing patterns",
                        content=f"# {lang} Testing\n\nUse appropriate testing framework for {lang}.",
                        tags=[lang.lower(), "testing", "framework"],
                        priority=3
                    ))
                allure.attach(f"Added {len(template.rules)} language-specific rules", "Language Rules Count", allure.attachment_type.TEXT)
            
            with allure.step("Step 2: Generate both Cursor and Copilot guidance"):
                cursor_renderer = CursorRenderer()
                copilot_renderer = CopilotRenderer()
                
                cursor_output = temp_path / "multi_lang_cursor.mdc"
                copilot_output = temp_path / "multi_lang_copilot.instructions.md"
                
                cursor_renderer.render_file(template, cursor_output)
                copilot_renderer.render_file(template, copilot_output)
                allure.attach(str(cursor_output), "Cursor Output Path", allure.attachment_type.TEXT)
                allure.attach(str(copilot_output), "Copilot Output Path", allure.attachment_type.TEXT)
            
            with allure.step("Step 3: Verify both files were created"):
                assert cursor_output.exists()
                assert copilot_output.exists()
            
            with allure.step("Step 4: Verify content contains all languages and frameworks"):
                cursor_content = cursor_output.read_text()
                copilot_content = copilot_output.read_text()
                
                allure.attach(cursor_content, "Cursor Multi-Language Content", allure.attachment_type.TEXT)
                allure.attach(copilot_content, "Copilot Multi-Language Content", allure.attachment_type.TEXT)
                
                for language in ["python", "typescript", "java", "go"]:
                    assert language in cursor_content
                    assert language in copilot_content
                
                for framework in ["pytest", "jest", "junit", "testing"]:
                    assert framework in cursor_content
                    assert framework in copilot_content
                
                # Verify language-specific guidance is present
                for lang in ["Python Testing", "TypeScript Testing", "Java Testing", "Go Testing"]:
                    assert lang in cursor_content
                    assert lang in copilot_content

    @allure.story("Error Handling")
    @allure.title("Error handling in complete workflow")
    @allure.description("Test error handling in complete workflow with invalid template data")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("e2e", "error-handling", "robustness")
    def test_error_handling_workflow(self):
        """Test error handling in complete workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            with allure.step("Step 1: Create template with invalid data"):
                metadata = RulesetMetadata(
                    name="",  # Empty name should be handled
                    version="1.0.0",
                    description="Template with invalid data",
                    categories=[],  # Empty categories list
                )
                allure.attach(str(metadata.__dict__), "Invalid Template Metadata", allure.attachment_type.JSON)
                
                template = Ruleset(metadata=metadata)
                
                # Add guidance with empty content
                template.add_rule(RulesetItem(
                    name="",  # Empty name
                    description="",  # Empty description
                    content="",  # Empty content
                    tags=[],  # Empty tags
                    priority=0  # Zero priority
                ))
                allure.attach(f"Added {len(template.rules)} invalid rules", "Invalid Rules Count", allure.attachment_type.TEXT)
            
            with allure.step("Step 2: Attempt to render with invalid data"):
                cursor_renderer = CursorRenderer()
                copilot_renderer = CopilotRenderer()
                
                cursor_output = temp_path / "error_test_cursor.mdc"
                copilot_output = temp_path / "error_test_copilot.instructions.md"
                
                allure.attach(str(cursor_output), "Cursor Error Output Path", allure.attachment_type.TEXT)
                allure.attach(str(copilot_output), "Copilot Error Output Path", allure.attachment_type.TEXT)
                
                # These should not raise exceptions
                cursor_renderer.render_file(template, cursor_output)
                copilot_renderer.render_file(template, copilot_output)
            
            with allure.step("Step 3: Verify files were still created despite invalid data"):
                assert cursor_output.exists()
                assert copilot_output.exists()
                allure.attach("Files created successfully despite invalid data", "Error Handling Success", allure.attachment_type.TEXT)
