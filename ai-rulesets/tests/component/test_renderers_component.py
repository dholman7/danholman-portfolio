"""
Component tests for renderers with mocked dependencies.

These tests verify that the renderers work correctly with mocked external
dependencies, testing the integration between renderers and their dependencies
without requiring real external services.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from ai_rulesets.core import Ruleset, RulesetMetadata, RulesetItem
from ai_rulesets.renderers import CursorRenderer, CopilotRenderer


@pytest.mark.component
class TestCursorRendererComponent:
    """Test CursorRenderer component with mocked dependencies."""

    @pytest.fixture
    def sample_template(self):
        """Create a sample guidance template for testing."""
        metadata = RulesetMetadata(
            name="Test Template",
            version="1.0.0",
            description="A test template",
            categories=["unit", "integration"]
        )
        
        template = Ruleset(metadata=metadata)
        template.add_rule(RulesetItem(
            name="Test Guidance",
            description="Test guidance item",
            content="# Test guidance content",
            tags=["test"],
            priority=1
        ))
        
        return template

    @pytest.fixture
    def cursor_renderer(self):
        """Create CursorRenderer instance."""
        return CursorRenderer()

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_render_to_file_success(self, mock_mkdir, mock_file, cursor_renderer, sample_template):
        """Test successful rendering to file."""
        output_path = Path("test_output.mdc")
        
        cursor_renderer.render_to_file(sample_template, output_path)
        
        # Verify file was opened for writing
        mock_file.assert_called_once_with(output_path, 'w', encoding='utf-8')
        
        # Verify content was written
        mock_file().write.assert_called()
        written_content = ''.join(call[0][0] for call in mock_file().write.call_args_list)
        
        # Check that key content is present
        assert "Test Template" in written_content
        assert "Test guidance content" in written_content
        assert "python" in written_content
        assert "pytest" in written_content

    def test_render_to_string(self, cursor_renderer, sample_template):
        """Test rendering to string."""
        result = cursor_renderer.render(sample_template)
        
        assert isinstance(result, str)
        assert "Test Template" in result
        assert "Test guidance content" in result
        assert "python" in result
        assert "pytest" in result

    def test_sanitize_filename(self, cursor_renderer):
        """Test filename sanitization."""
        # Test normal filename
        assert cursor_renderer._sanitize_filename("test-template") == "test-template"
        
        # Test filename with spaces
        assert cursor_renderer._sanitize_filename("test template") == "test_template"
        
        # Test filename with special characters
        assert cursor_renderer._sanitize_filename("test@template#1") == "test_template_1"
        
        # Test empty filename
        assert cursor_renderer._sanitize_filename("") == "untitled"

    def test_render_empty_template(self, cursor_renderer):
        """Test rendering empty template."""
        metadata = RulesetMetadata(
            name="Empty Template",
            version="1.0.0",
            description="An empty template",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        result = cursor_renderer.render(template)
        
        assert "Empty Template" in result
        assert "python" in result
        assert "pytest" in result


@pytest.mark.component
class TestCopilotRendererComponent:
    """Test CopilotRenderer component with mocked dependencies."""

    @pytest.fixture
    def sample_template(self):
        """Create a sample guidance template for testing."""
        metadata = RulesetMetadata(
            name="Test Template",
            version="1.0.0",
            description="A test template",
            categories=["unit", "integration"]
        )
        
        template = Ruleset(metadata=metadata)
        template.add_rule(RulesetItem(
            name="Test Guidance",
            description="Test guidance item",
            content="# Test guidance content",
            tags=["test"],
            priority=1
        ))
        
        return template

    @pytest.fixture
    def copilot_renderer(self):
        """Create CopilotRenderer instance."""
        return CopilotRenderer()

    @patch('builtins.open', new_callable=mock_open)
    @patch('pathlib.Path.mkdir')
    def test_render_to_file_success(self, mock_mkdir, mock_file, copilot_renderer, sample_template):
        """Test successful rendering to file."""
        output_path = Path("test_output.instructions.md")
        
        copilot_renderer.render_to_file(sample_template, output_path)
        
        # Verify file was opened for writing
        mock_file.assert_called_once_with(output_path, 'w', encoding='utf-8')
        
        # Verify content was written
        mock_file().write.assert_called()
        written_content = ''.join(call[0][0] for call in mock_file().write.call_args_list)
        
        # Check that key content is present
        assert "Test Template" in written_content
        assert "Test guidance content" in written_content
        assert "python" in written_content
        assert "pytest" in written_content

    def test_render_to_string(self, copilot_renderer, sample_template):
        """Test rendering to string."""
        result = copilot_renderer.render(sample_template)
        
        assert isinstance(result, str)
        assert "Test Template" in result
        assert "Test guidance content" in result
        assert "python" in result
        assert "pytest" in result

    def test_sanitize_filename(self, copilot_renderer):
        """Test filename sanitization."""
        # Test normal filename
        assert copilot_renderer._sanitize_filename("test-template") == "test-template"
        
        # Test filename with spaces
        assert copilot_renderer._sanitize_filename("test template") == "test_template"
        
        # Test filename with special characters
        assert copilot_renderer._sanitize_filename("test@template#1") == "test_template_1"
        
        # Test empty filename
        assert copilot_renderer._sanitize_filename("") == "untitled"

    def test_render_empty_template(self, copilot_renderer):
        """Test rendering empty template."""
        metadata = RulesetMetadata(
            name="Empty Template",
            version="1.0.0",
            description="An empty template",
            categories=["unit"]
        )
        
        template = Ruleset(metadata=metadata)
        result = copilot_renderer.render(template)
        
        assert "Empty Template" in result
        assert "python" in result
        assert "pytest" in result


@pytest.mark.component
class TestRendererIntegration:
    """Test integration between different renderers."""

    def test_renderer_compatibility(self):
        """Test that both renderers can handle the same template."""
        metadata = RulesetMetadata(
            name="Compatibility Test",
            version="1.0.0",
            description="Test template for compatibility",
            languages=["python", "typescript"],
            frameworks=["pytest", "jest"],
            categories=["unit", "integration", "e2e"]
        )
        
        template = Ruleset(metadata=metadata)
        template.add_rule(RulesetItem(
            name="High Priority Guidance",
            description="High priority test guidance",
            content="# High priority content",
            tags=["high", "priority"],
            priority=3
        ))
        template.add_rule(RulesetItem(
            name="Low Priority Guidance",
            description="Low priority test guidance",
            content="# Low priority content",
            tags=["low", "priority"],
            priority=1
        ))
        
        cursor_renderer = CursorRenderer()
        copilot_renderer = CopilotRenderer()
        
        cursor_result = cursor_renderer.render(template)
        copilot_result = copilot_renderer.render(template)
        
        # Both should contain the template name
        assert "Compatibility Test" in cursor_result
        assert "Compatibility Test" in copilot_result
        
        # Both should contain the guidance content
        assert "High priority content" in cursor_result
        assert "High priority content" in copilot_result
        assert "Low priority content" in cursor_result
        assert "Low priority content" in copilot_result
        
        # Both should contain languages and frameworks
        assert "python" in cursor_result
        assert "python" in copilot_result
        assert "typescript" in cursor_result
        assert "typescript" in copilot_result
        assert "pytest" in cursor_result
        assert "pytest" in copilot_result
        assert "jest" in cursor_result
        assert "jest" in copilot_result
