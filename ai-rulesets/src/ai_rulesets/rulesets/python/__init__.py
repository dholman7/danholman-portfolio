"""
Python domain rulesets.

This module provides rulesets for Python development including coding standards,
testing guidelines, and security practices.
"""

from .coding import CodingRuleset
from .testing import TestingRuleset
from .security import SecurityRuleset


class PythonDomain:
    """Python domain rulesets."""
    
    def __init__(self):
        self.coding = CodingRuleset()
        self.testing = TestingRuleset()
        self.security = SecurityRuleset()
    
    def apply_all(self, output_dir: str = ".cursor/rules"):
        """Apply all Python rulesets to the specified output directory."""
        self.coding.apply(output_dir)
        self.testing.apply(output_dir)
        self.security.apply(output_dir)
    
    def list_rulesets(self):
        """List all available Python rulesets."""
        return {
            "coding": self.coding.metadata.name,
            "testing": self.testing.metadata.name,
            "security": self.security.metadata.name,
        }


# Convenience imports
coding = CodingRuleset()
testing = TestingRuleset()
security = SecurityRuleset()

__all__ = [
    "PythonDomain",
    "CodingRuleset",
    "TestingRuleset", 
    "SecurityRuleset",
    "coding",
    "testing",
    "security",
]
