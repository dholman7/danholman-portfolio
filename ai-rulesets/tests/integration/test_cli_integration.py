"""
Integration tests for CLI functionality.

These tests verify that the CLI works correctly with real file system operations
and external dependencies, testing the actual integration points.
"""

import pytest
import tempfile
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from ai_rulesets.cli import main
from ai_rulesets.core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem


@pytest.mark.integration
class TestCLIIntegration:
    """Test CLI integration with real file system operations."""

    def test_cli_help_command(self):
        """Test that CLI help command works."""
        result = subprocess.run(
            [sys.executable, "-m", "ai_rulesets.cli", "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "AI Test Generation CLI" in result.stdout
        assert "generate-cursor" in result.stdout
        assert "generate-copilot" in result.stdout

    def test_cli_list_templates_command(self):
        """Test that CLI list templates command works."""
        result = subprocess.run(
            [sys.executable, "-m", "ai_rulesets.cli", "list-templates"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Available guidance templates:" in result.stdout

    @patch('ai_rulesets.cli.CursorRenderer')
    @patch('ai_rulesets.cli.CopilotRenderer')
    def test_cli_generate_cursor_command(self, mock_copilot_renderer, mock_cursor_renderer):
        """Test CLI generate cursor command."""
        # Mock the renderer
        mock_renderer_instance = mock_cursor_renderer.return_value
        mock_renderer_instance.render.return_value = "# Test cursor guidance"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "ai_rulesets.cli", "generate-cursor"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated Cursor guidance" in result.stdout

    @patch('ai_rulesets.cli.CursorRenderer')
    @patch('ai_rulesets.cli.CopilotRenderer')
    def test_cli_generate_copilot_command(self, mock_copilot_renderer, mock_cursor_renderer):
        """Test CLI generate copilot command."""
        # Mock the renderer
        mock_renderer_instance = mock_copilot_renderer.return_value
        mock_renderer_instance.render.return_value = "# Test copilot guidance"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "ai_rulesets.cli", "generate-copilot"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated GitHub Copilot guidance" in result.stdout

    def test_cli_generate_all_command(self):
        """Test CLI generate all command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "ai_rulesets.cli", "generate-all"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated all guidance files" in result.stdout

    def test_cli_with_invalid_command(self):
        """Test CLI with invalid command."""
        result = subprocess.run(
            [sys.executable, "-m", "ai_rulesets.cli", "invalid-command"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "No such command" in result.stdout or "Usage:" in result.stdout


@pytest.mark.integration
class TestFileSystemIntegration:
    """Test file system integration operations."""

    def test_template_creation_and_saving(self):
        """Test creating and saving templates to file system."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a template
            metadata = GuidanceTemplateMetadata(
                name="Integration Test Template",
                version="1.0.0",
                description="Template for integration testing",
                languages=["python"],
                frameworks=["pytest"],
                categories=["unit", "integration"]
            )
            
            template = GuidanceTemplate(metadata=metadata)
            template.add_guidance(GuidanceItem(
                name="Integration Test Guidance",
                description="Test guidance for integration",
                content="# Integration test guidance",
                tags=["integration", "test"],
                priority=1
            ))
            
            # Save template to file
            template_path = Path(temp_dir) / "test_template.yaml"
            template.save(template_path)
            
            # Verify file was created
            assert template_path.exists()
            
            # Load template from file
            loaded_template = GuidanceTemplate.load_from_file(template_path)
            
            # Verify loaded template matches original
            assert loaded_template.metadata.name == template.metadata.name
            assert loaded_template.metadata.version == template.metadata.version
            assert len(loaded_template.guidance) == len(template.guidance)
            assert loaded_template.guidance[0].name == template.guidance[0].name

    def test_renderer_file_output(self):
        """Test that renderers can write to file system."""
        from ai_rulesets.renderers import CursorRenderer, CopilotRenderer
        
        # Create a template
        metadata = GuidanceTemplateMetadata(
            name="File Output Test",
            version="1.0.0",
            description="Template for file output testing",
            languages=["python"],
            frameworks=["pytest"],
            categories=["unit"]
        )
        
        template = GuidanceTemplate(metadata=metadata)
        template.add_guidance(GuidanceItem(
            name="File Output Guidance",
            description="Test guidance for file output",
            content="# File output test guidance",
            tags=["file", "output"],
            priority=1
        ))
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test CursorRenderer file output
            cursor_renderer = CursorRenderer()
            cursor_output = temp_path / "cursor_output.mdc"
            cursor_renderer.render_to_file(template, cursor_output)
            
            assert cursor_output.exists()
            cursor_content = cursor_output.read_text()
            assert "File Output Test" in cursor_content
            assert "File output test guidance" in cursor_content
            
            # Test CopilotRenderer file output
            copilot_renderer = CopilotRenderer()
            copilot_output = temp_path / "copilot_output.instructions.md"
            copilot_renderer.render_to_file(template, copilot_output)
            
            assert copilot_output.exists()
            copilot_content = copilot_output.read_text()
            assert "File Output Test" in copilot_content
            assert "File output test guidance" in copilot_content


@pytest.mark.integration
class TestTemplateLoadingIntegration:
    """Test template loading from various sources."""

    def test_load_from_yaml_file(self):
        """Test loading template from YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml_content = """
metadata:
  name: "YAML Test Template"
  version: "1.0.0"
  description: "Template loaded from YAML"
  languages: ["python"]
  frameworks: ["pytest"]
  categories: ["unit"]

guidance:
  - name: "YAML Test Guidance"
    description: "Test guidance from YAML"
    content: "# YAML test guidance"
    tags: ["yaml", "test"]
    priority: 1
"""
            f.write(yaml_content)
            f.flush()
            
            try:
                template = GuidanceTemplate.load_from_file(f.name)
                
                assert template.metadata.name == "YAML Test Template"
                assert template.metadata.version == "1.0.0"
                assert len(template.guidance) == 1
                assert template.guidance[0].name == "YAML Test Guidance"
                assert template.guidance[0].content == "# YAML test guidance"
            finally:
                Path(f.name).unlink()

    def test_load_from_nonexistent_file(self):
        """Test loading from nonexistent file raises appropriate error."""
        nonexistent_path = Path("/nonexistent/path/template.yaml")
        
        with pytest.raises(FileNotFoundError):
            GuidanceTemplate.load_from_file(nonexistent_path)

    def test_load_invalid_yaml_file(self):
        """Test loading from invalid YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            invalid_yaml = "invalid: yaml: content: ["
            f.write(invalid_yaml)
            f.flush()
            
            try:
                with pytest.raises(Exception):  # Should raise YAML parsing error
                    GuidanceTemplate.load_from_file(f.name)
            finally:
                Path(f.name).unlink()
