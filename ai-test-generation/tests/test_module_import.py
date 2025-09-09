"""
Simple test to ensure the ai_test_generation module can be imported.
This satisfies coverage requirements and ensures the module is properly installed.
"""

import pytest
import allure


@allure.epic("AI Test Generation")
@allure.feature("Module Import")
class TestModuleImport:
    """Test that the ai_test_generation module can be imported and used."""

    @allure.story("Module Import")
    @allure.title("Import ai_test_generation module")
    @allure.description("Test that the ai_test_generation module can be imported successfully.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("import", "module")
    def test_import_module(self):
        """Test that the module can be imported."""
        try:
            import ai_test_generation
            assert ai_test_generation is not None
            allure.attach("Module imported successfully", "Import Status", allure.attachment_type.TEXT)
        except ImportError as e:
            pytest.fail(f"Failed to import ai_test_generation: {e}")

    @allure.story("Module Import")
    @allure.title("Import core components")
    @allure.description("Test that core components can be imported from the module.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("import", "core")
    def test_import_core_components(self):
        """Test that core components can be imported."""
        try:
            from ai_test_generation import core
            assert core is not None
            allure.attach("Core module imported successfully", "Import Status", allure.attachment_type.TEXT)
        except ImportError as e:
            pytest.fail(f"Failed to import core module: {e}")

    @allure.story("Module Import")
    @allure.title("Import CLI components")
    @allure.description("Test that CLI components can be imported from the module.")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("import", "cli")
    def test_import_cli_components(self):
        """Test that CLI components can be imported."""
        try:
            from ai_test_generation import cli
            assert cli is not None
            allure.attach("CLI module imported successfully", "Import Status", allure.attachment_type.TEXT)
        except ImportError as e:
            pytest.fail(f"Failed to import CLI module: {e}")
