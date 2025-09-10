"""
Documentation standards rulesets.

This module provides documentation guidelines including style, structure,
and content standards.
"""

from .style import StyleRuleset
from .structure import StructureRuleset


class DocumentationDomain:
    """Documentation standards domain."""
    
    def __init__(self):
        self.style = StyleRuleset()
        self.structure = StructureRuleset()
    
    def apply_all(self, output_dir: str = ".cursor/rules"):
        """Apply all documentation rulesets to the specified output directory."""
        self.style.apply(output_dir)
        self.structure.apply(output_dir)
    
    def list_rulesets(self):
        """List all available documentation rulesets."""
        return {
            "style": self.style.metadata.name,
            "structure": self.structure.metadata.name,
        }


# Convenience imports
style = StyleRuleset()
structure = StructureRuleset()

__all__ = [
    "DocumentationDomain",
    "StyleRuleset",
    "StructureRuleset",
    "style",
    "structure",
]
