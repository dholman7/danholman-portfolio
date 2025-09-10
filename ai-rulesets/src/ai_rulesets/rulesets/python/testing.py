"""
Python testing standards ruleset.

This ruleset is generated from source markdown files and provides
organizational Python testing standards.
"""

from pathlib import Path
from typing import Optional
from ai_rulesets.core import Ruleset, RulesetMetadata, RulesetItem
from ai_rulesets.renderers import CursorRenderer, CopilotRenderer
from ai_rulesets.sources.processor import SourceProcessor


class TestingRuleset:
    """Python testing standards ruleset."""
    
    def __init__(self):
        self.sources_dir = Path(__file__).parent.parent.parent / "sources"
        self.processor = SourceProcessor(self.sources_dir)
        
        # Load from source markdown file
        source_file = self.sources_dir / "python" / "testing.md"
        self.ruleset = self.processor.process_markdown_file(
            source_file, 
            domain="python", 
            category="testing"
        )
    
    def apply(self, output_dir: str = ".cursor/rules", format: str = "cursor"):
        """Apply the testing ruleset to the specified output directory."""
        output_path = Path(output_dir)
        
        if format == "cursor":
            renderer = CursorRenderer()
            filename = "python-testing-standards.mdc"
        elif format == "copilot":
            renderer = CopilotRenderer()
            filename = "python-testing-standards.instructions.md"
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        output_file = output_path / filename
        renderer.render_file(self.ruleset, output_file)
    
    def get_rules(self):
        """Get all rules in this ruleset."""
        return self.ruleset.rules
    
    def get_rules_by_category(self, category: str):
        """Get rules by category."""
        return self.ruleset.get_rules_by_category(category)
    
    def reload_from_source(self):
        """Reload ruleset from source markdown file."""
        source_file = self.sources_dir / "python" / "testing.md"
        self.ruleset = self.processor.process_markdown_file(
            source_file, 
            domain="python", 
            category="testing"
        )