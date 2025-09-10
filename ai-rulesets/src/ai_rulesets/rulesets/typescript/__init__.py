"""
TypeScript domain rulesets.

This module provides rulesets for TypeScript development including coding standards,
testing guidelines, and modern ES6+ patterns.
"""

from .coding import CodingRuleset
from .testing import TestingRuleset


class TypeScriptDomain:
    """TypeScript domain rulesets."""
    
    def __init__(self):
        self.coding = CodingRuleset()
        self.testing = TestingRuleset()
    
    def apply_all(self, output_dir: str = ".cursor/rules"):
        """Apply all TypeScript rulesets to the specified output directory."""
        self.coding.apply(output_dir)
        self.testing.apply(output_dir)
    
    def list_rulesets(self):
        """List all available TypeScript rulesets."""
        return {
            "coding": self.coding.metadata.name,
            "testing": self.testing.metadata.name,
        }


# Convenience imports
coding = CodingRuleset()
testing = TestingRuleset()

__all__ = [
    "TypeScriptDomain",
    "CodingRuleset",
    "TestingRuleset",
    "coding",
    "testing",
]
