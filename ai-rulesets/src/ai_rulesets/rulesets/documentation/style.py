"""
Documentation style standards ruleset.
"""

from pathlib import Path
from typing import Optional
from ...core import Ruleset, RulesetMetadata, RulesetItem
from ...renderers import CursorRenderer, CopilotRenderer


class StyleRuleset:
    """Documentation style standards ruleset."""
    
    def __init__(self):
        self.metadata = RulesetMetadata(
            name="Documentation Style Standards",
            version="1.0.0",
            description="Organizational documentation style guidelines and best practices",
            categories=["documentation", "style"],
            tags=["documentation", "style", "markdown", "writing"],
            author="Dan Holman",
            maintainer="engineering@company.com"
        )
        
        self.ruleset = Ruleset(metadata=self.metadata)
        self._load_rules()
    
    def _load_rules(self):
        """Load documentation style rules."""
        
        # Writing style rule
        self.ruleset.add_rule(RulesetItem(
            name="Writing Style",
            description="Documentation writing style guidelines",
            content="""# Use clear, concise language
# Write in active voice when possible
# Use present tense for current functionality
# Use future tense for planned features
# Be consistent with terminology
# Use proper grammar and spelling""",
            tags=["writing", "style", "clarity"],
            priority=1,
            category="writing"
        ))
        
        # Markdown formatting rule
        self.ruleset.add_rule(RulesetItem(
            name="Markdown Formatting",
            description="Markdown formatting standards",
            content="""# Use consistent heading hierarchy (H1, H2, H3)
# Use proper code block formatting with language specification
# Use bullet points for lists
# Use tables for structured data
# Use links for external references
# Use images with alt text

```python
# Code blocks should specify language
def example_function():
    return "Hello, World!"
```

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |""",
            tags=["markdown", "formatting", "structure"],
            priority=1,
            category="formatting"
        ))
        
        # Code documentation rule
        self.ruleset.add_rule(RulesetItem(
            name="Code Documentation",
            description="Code documentation standards",
            content="""# Document all public APIs
# Use docstrings for functions and classes
# Include parameter descriptions and return types
# Provide usage examples
# Document error conditions
# Keep documentation up to date

def calculate_total(items: List[Item], tax_rate: float) -> float:
    \"\"\"
    Calculate the total cost including tax.
    
    Args:
        items: List of items to calculate total for
        tax_rate: Tax rate as a decimal (e.g., 0.08 for 8%)
    
    Returns:
        Total cost including tax
    
    Raises:
        ValueError: If tax_rate is negative
    \"\"\"
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)""",
            tags=["docstrings", "api", "documentation"],
            priority=2,
            category="code-docs"
        ))
    
    def apply(self, output_dir: str = ".cursor/rules", format: str = "cursor"):
        """Apply the style ruleset to the specified output directory."""
        output_path = Path(output_dir)
        
        if format == "cursor":
            renderer = CursorRenderer()
            filename = "documentation-style-standards.mdc"
        elif format == "copilot":
            renderer = CopilotRenderer()
            filename = "documentation-style-standards.instructions.md"
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
