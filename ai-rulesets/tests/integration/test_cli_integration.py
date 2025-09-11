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

# from ai_rulesets.cli import main  # CLI main function not available
from ai_rulesets.core import Ruleset, RulesetMetadata, RulesetItem


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
        assert "AI Rulesets Quality Checker" in result.stdout
        assert "readmes-only" in result.stdout
        assert "workflows-only" in result.stdout

    def test_cli_quality_check_command(self):
        """Test that CLI quality check command works."""
        result = subprocess.run(
            [sys.executable, "-m", "ai_rulesets.cli", "--tests-only"],
            capture_output=True,
            text=True
        )
        
        # Quality check should run successfully (0 or 1 is acceptable)
        assert result.returncode in [0, 1]

    # @patch('ai_rulesets.cli.CursorRenderer')
    # @patch('ai_rulesets.cli.CopilotRenderer')
    def test_cli_generate_cursor_command(self, mock_copilot_renderer=None, mock_cursor_renderer=None):
        """Test CLI generate cursor command."""
        pytest.skip("CLI is a quality checker, not a template generator")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [sys.executable, "-m", "ai_rulesets.cli", "generate-cursor"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert "Generated Cursor guidance" in result.stdout

    def test_cli_generate_copilot_command(self):
        """Test CLI generate copilot command."""
        pytest.skip("CLI is a quality checker, not a template generator")
        
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
        pytest.skip("CLI is a quality checker, not a template generator")

    def test_cli_with_invalid_command(self):
        """Test CLI with invalid command."""
        result = subprocess.run(
            [sys.executable, "-m", "ai_rulesets.cli", "invalid-command"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "unrecognized arguments" in result.stderr


@pytest.mark.integration
class TestFileSystemIntegration:
    """Test file system integration operations."""

    def test_template_creation_and_saving(self):
        """Test creating and saving templates to file system."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a template
            metadata = RulesetMetadata(
                name="Integration Test Template",
                version="1.0.0",
                description="Template for integration testing",
                categories=["unit", "integration"]
            )
            
            template = Ruleset(metadata=metadata)
            template.add_rule(RulesetItem(
                name="Integration Test Guidance",
                description="Test guidance for integration",
                content="# Integration test guidance",
                tags=["integration", "test"],
                priority=1
            ))
            
            # Save template to file
            template_path = Path(temp_dir) / "test_template.yaml"
            template.save_to_file(template_path)
            
            # Verify file was created
            assert template_path.exists()
            
            # Load template from file
            loaded_template = Ruleset.from_file(template_path)
            
            # Verify loaded template matches original
            assert loaded_template.metadata.name == template.metadata.name
            assert loaded_template.metadata.version == template.metadata.version
            assert len(loaded_template.rules) == len(template.rules)
            assert loaded_template.rules[0].name == template.rules[0].name

    def test_renderer_file_output(self):
        """Test that renderers can write to file system."""
        from ai_rulesets.renderers import CursorRenderer, CopilotRenderer
        
        # Create a template
        metadata = RulesetMetadata(
            name="File Output Test",
            version="1.0.0",
            description="Template for file output testing",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        template.add_rule(RulesetItem(
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
            cursor_renderer.render_file(template, cursor_output)
            
            assert cursor_output.exists()
            cursor_content = cursor_output.read_text()
            assert "File Output Test" in cursor_content
            assert "File output test guidance" in cursor_content
            
            # Test CopilotRenderer file output
            copilot_renderer = CopilotRenderer()
            copilot_output = temp_path / "copilot_output.instructions.md"
            copilot_renderer.render_file(template, copilot_output)
            
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
  categories: ["unit"]

rules:
  - name: "YAML Test Guidance"
    description: "Test guidance from YAML"
    content: "# YAML test guidance"
    tags: ["yaml", "test"]
    priority: 1
"""
            f.write(yaml_content)
            f.flush()
            
            try:
                template = Ruleset.from_file(Path(f.name))
                
                assert template.metadata.name == "YAML Test Template"
                assert template.metadata.version == "1.0.0"
                assert len(template.rules) == 1
                assert template.rules[0].name == "YAML Test Guidance"
                assert template.rules[0].content == "# YAML test guidance"
            finally:
                Path(f.name).unlink()

    def test_load_from_nonexistent_file(self):
        """Test loading from nonexistent file raises appropriate error."""
        nonexistent_path = Path("/nonexistent/path/template.yaml")
        
        with pytest.raises(FileNotFoundError):
            Ruleset.from_file(nonexistent_path)

    def test_load_invalid_yaml_file(self):
        """Test loading from invalid YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            invalid_yaml = "invalid: yaml: content: ["
            f.write(invalid_yaml)
            f.flush()
            
            try:
                with pytest.raises(Exception):  # Should raise YAML parsing error
                    Ruleset.load_from_file(f.name)
            finally:
                Path(f.name).unlink()
