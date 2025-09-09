"""
End-to-end tests for complete guidance generation workflows.

These tests simulate real user interactions and test complete workflows from
start to finish, verifying that the entire system works correctly from
the user's perspective.
"""

import pytest
import tempfile
import subprocess
import sys
from pathlib import Path
from ai_test_generation.core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem
from ai_test_generation.renderers import CursorRenderer, CopilotRenderer


@pytest.mark.e2e
class TestGuidanceGenerationE2E:
    """Test complete guidance generation workflow."""

    def test_complete_guidance_generation_workflow(self):
        """Test complete workflow from template creation to file generation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Step 1: Create a comprehensive guidance template
            metadata = GuidanceTemplateMetadata(
                name="E2E Test Template",
                version="1.0.0",
                description="Comprehensive template for E2E testing",
                languages=["python", "typescript"],
                frameworks=["pytest", "jest", "playwright"],
                categories=["unit", "integration", "e2e"],
                author="Test Author",
                license="MIT"
            )
            
            template = GuidanceTemplate(metadata=metadata)
            
            # Add multiple guidance items with different priorities
            template.add_guidance(GuidanceItem(
                name="High Priority Testing Guidance",
                description="Critical testing patterns",
                content="# High Priority Testing\n\nAlways write tests for critical business logic.",
                tags=["critical", "testing", "patterns"],
                priority=3
            ))
            
            template.add_guidance(GuidanceItem(
                name="Medium Priority API Testing",
                description="API testing best practices",
                content="# API Testing\n\nTest all API endpoints with proper error handling.",
                tags=["api", "testing", "best-practices"],
                priority=2
            ))
            
            template.add_guidance(GuidanceItem(
                name="Low Priority Documentation",
                description="Documentation guidelines",
                content="# Documentation\n\nWrite clear, concise test documentation.",
                tags=["documentation", "guidelines"],
                priority=1
            ))
            
            # Step 2: Save template to file
            template_path = temp_path / "e2e_template.yaml"
            template.save(template_path)
            
            # Verify template was saved
            assert template_path.exists()
            
            # Step 3: Load template from file
            loaded_template = GuidanceTemplate.load_from_file(template_path)
            
            # Verify loaded template matches original
            assert loaded_template.metadata.name == template.metadata.name
            assert len(loaded_template.guidance) == 3
            
            # Step 4: Generate Cursor guidance
            cursor_renderer = CursorRenderer()
            cursor_output = temp_path / "cursor_guidance.mdc"
            cursor_renderer.render_to_file(loaded_template, cursor_output)
            
            # Verify Cursor guidance was generated
            assert cursor_output.exists()
            cursor_content = cursor_output.read_text()
            assert "E2E Test Template" in cursor_content
            assert "High Priority Testing" in cursor_content
            assert "API Testing" in cursor_content
            assert "Documentation" in cursor_content
            assert "python" in cursor_content
            assert "typescript" in cursor_content
            assert "pytest" in cursor_content
            assert "jest" in cursor_content
            assert "playwright" in cursor_content
            
            # Step 5: Generate Copilot guidance
            copilot_renderer = CopilotRenderer()
            copilot_output = temp_path / "copilot_guidance.instructions.md"
            copilot_renderer.render_to_file(loaded_template, copilot_output)
            
            # Verify Copilot guidance was generated
            assert copilot_output.exists()
            copilot_content = copilot_output.read_text()
            assert "E2E Test Template" in copilot_content
            assert "High Priority Testing" in copilot_content
            assert "API Testing" in copilot_content
            assert "Documentation" in copilot_content
            assert "python" in copilot_content
            assert "typescript" in copilot_content
            assert "pytest" in copilot_content
            assert "jest" in copilot_content
            assert "playwright" in copilot_content
            
            # Step 6: Verify guidance items are in priority order (highest first)
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
            
            # Verify priority order (high priority should come first)
            assert high_priority_line is not None
            assert medium_priority_line is not None
            assert low_priority_line is not None
            assert high_priority_line < medium_priority_line < low_priority_line

    def test_cli_complete_workflow(self):
        """Test complete workflow using CLI commands."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Step 1: Test list templates command
            result = subprocess.run(
                [sys.executable, "-m", "ai_test_generation.cli", "list-templates"],
                cwd=temp_path,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Available guidance templates:" in result.stdout
            
            # Step 2: Test generate cursor command
            result = subprocess.run(
                [sys.executable, "-m", "ai_test_generation.cli", "generate-cursor"],
                cwd=temp_path,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated Cursor guidance" in result.stdout
            
            # Verify cursor file was created
            cursor_files = list(temp_path.glob("*.mdc"))
            assert len(cursor_files) > 0
            
            # Step 3: Test generate copilot command
            result = subprocess.run(
                [sys.executable, "-m", "ai_test_generation.cli", "generate-copilot"],
                cwd=temp_path,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated GitHub Copilot guidance" in result.stdout
            
            # Verify copilot file was created
            copilot_files = list(temp_path.glob("*.instructions.md"))
            assert len(copilot_files) > 0
            
            # Step 4: Test generate all command
            result = subprocess.run(
                [sys.executable, "-m", "ai_test_generation.cli", "generate-all"],
                cwd=temp_path,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated all guidance files" in result.stdout

    def test_multi_language_template_workflow(self):
        """Test workflow with multi-language template."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create multi-language template
            metadata = GuidanceTemplateMetadata(
                name="Multi-Language Template",
                version="2.0.0",
                description="Template supporting multiple languages",
                languages=["python", "typescript", "java", "go"],
                frameworks=["pytest", "jest", "junit", "testing"],
                categories=["unit", "integration", "performance"],
                author="Multi-Lang Author",
                license="Apache-2.0"
            )
            
            template = GuidanceTemplate(metadata=metadata)
            
            # Add language-specific guidance
            template.add_guidance(GuidanceItem(
                name="Python Testing",
                description="Python-specific testing patterns",
                content="# Python Testing\n\nUse pytest fixtures and parametrize tests.",
                tags=["python", "pytest", "fixtures"],
                priority=3
            ))
            
            template.add_guidance(GuidanceItem(
                name="TypeScript Testing",
                description="TypeScript-specific testing patterns",
                content="# TypeScript Testing\n\nUse Jest with TypeScript and proper type checking.",
                tags=["typescript", "jest", "types"],
                priority=3
            ))
            
            template.add_guidance(GuidanceItem(
                name="Java Testing",
                description="Java-specific testing patterns",
                content="# Java Testing\n\nUse JUnit 5 and Mockito for comprehensive testing.",
                tags=["java", "junit", "mockito"],
                priority=3
            ))
            
            template.add_guidance(GuidanceItem(
                name="Go Testing",
                description="Go-specific testing patterns",
                content="# Go Testing\n\nUse table-driven tests and testify for assertions.",
                tags=["go", "testing", "testify"],
                priority=3
            ))
            
            # Generate both Cursor and Copilot guidance
            cursor_renderer = CursorRenderer()
            copilot_renderer = CopilotRenderer()
            
            cursor_output = temp_path / "multi_lang_cursor.mdc"
            copilot_output = temp_path / "multi_lang_copilot.instructions.md"
            
            cursor_renderer.render_to_file(template, cursor_output)
            copilot_renderer.render_to_file(template, copilot_output)
            
            # Verify both files were created
            assert cursor_output.exists()
            assert copilot_output.exists()
            
            # Verify content contains all languages and frameworks
            cursor_content = cursor_output.read_text()
            copilot_content = copilot_output.read_text()
            
            for language in ["python", "typescript", "java", "go"]:
                assert language in cursor_content
                assert language in copilot_content
            
            for framework in ["pytest", "jest", "junit", "testing"]:
                assert framework in cursor_content
                assert framework in copilot_content
            
            # Verify language-specific guidance is present
            assert "Python Testing" in cursor_content
            assert "TypeScript Testing" in cursor_content
            assert "Java Testing" in cursor_content
            assert "Go Testing" in cursor_content
            
            assert "Python Testing" in copilot_content
            assert "TypeScript Testing" in copilot_content
            assert "Java Testing" in copilot_content
            assert "Go Testing" in copilot_content

    def test_error_handling_workflow(self):
        """Test error handling in complete workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test with invalid template data
            metadata = GuidanceTemplateMetadata(
                name="",  # Empty name should be handled
                version="1.0.0",
                description="Template with invalid data",
                languages=[],  # Empty languages list
                frameworks=[],  # Empty frameworks list
                categories=[],  # Empty categories list
            )
            
            template = GuidanceTemplate(metadata=metadata)
            
            # Add guidance with empty content
            template.add_guidance(GuidanceItem(
                name="",  # Empty name
                description="",  # Empty description
                content="",  # Empty content
                tags=[],  # Empty tags
                priority=0  # Zero priority
            ))
            
            # Should still be able to render without errors
            cursor_renderer = CursorRenderer()
            copilot_renderer = CopilotRenderer()
            
            cursor_output = temp_path / "error_test_cursor.mdc"
            copilot_output = temp_path / "error_test_copilot.instructions.md"
            
            # These should not raise exceptions
            cursor_renderer.render_to_file(template, cursor_output)
            copilot_renderer.render_to_file(template, copilot_output)
            
            # Files should still be created
            assert cursor_output.exists()
            assert copilot_output.exists()
