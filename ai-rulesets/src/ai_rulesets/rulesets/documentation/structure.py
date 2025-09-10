"""
Documentation structure standards ruleset.
"""

from pathlib import Path
from typing import Optional
from ...core import Ruleset, RulesetMetadata, RulesetItem
from ...renderers import CursorRenderer, CopilotRenderer


class StructureRuleset:
    """Documentation structure standards ruleset."""
    
    def __init__(self):
        self.metadata = RulesetMetadata(
            name="Documentation Structure Standards",
            version="1.0.0",
            description="Organizational documentation structure guidelines and best practices",
            categories=["documentation", "structure"],
            tags=["documentation", "structure", "organization", "navigation"],
            author="Dan Holman",
            maintainer="engineering@company.com"
        )
        
        self.ruleset = Ruleset(metadata=self.metadata)
        self._load_rules()
    
    def _load_rules(self):
        """Load documentation structure rules."""
        
        # File organization rule
        self.ruleset.add_rule(RulesetItem(
            name="File Organization",
            description="Documentation file organization standards",
            content="""# Use consistent file naming conventions
# Organize documentation by topic and audience
# Use README.md for project overview
# Use docs/ directory for detailed documentation
# Use examples/ directory for code examples
# Use CHANGELOG.md for version history

project/
├── README.md              # Project overview
├── CHANGELOG.md           # Version history
├── docs/                  # Detailed documentation
│   ├── installation.md
│   ├── usage.md
│   └── api/
├── examples/              # Code examples
│   ├── basic-usage.py
│   └── advanced-features.py
└── tests/                 # Test documentation
    └── README.md""",
            tags=["organization", "files", "structure"],
            priority=1,
            category="organization"
        ))
        
        # Content structure rule
        self.ruleset.add_rule(RulesetItem(
            name="Content Structure",
            description="Documentation content structure guidelines",
            content="""# Start with an overview and purpose
# Include installation and setup instructions
# Provide usage examples and tutorials
# Document all public APIs
# Include troubleshooting and FAQ sections
# End with contributing guidelines

# Example README structure:
# 1. Project Title and Description
# 2. Features
# 3. Installation
# 4. Quick Start
# 5. Usage Examples
# 6. API Documentation
# 7. Contributing
# 8. License
# 9. Changelog""",
            tags=["content", "structure", "readme"],
            priority=1,
            category="content"
        ))
        
        # Navigation rule
        self.ruleset.add_rule(RulesetItem(
            name="Navigation",
            description="Documentation navigation and linking standards",
            content="""# Use consistent navigation patterns
# Include table of contents for long documents
# Use cross-references between related documents
# Provide breadcrumb navigation
# Use anchor links for section references
# Include search functionality when possible

# Table of Contents example:
# ## Table of Contents
# - [Installation](#installation)
# - [Usage](#usage)
#   - [Basic Usage](#basic-usage)
#   - [Advanced Usage](#advanced-usage)
# - [API Reference](#api-reference)
# - [Contributing](#contributing)""",
            tags=["navigation", "links", "toc"],
            priority=2,
            category="navigation"
        ))
    
    def apply(self, output_dir: str = ".cursor/rules", format: str = "cursor"):
        """Apply the structure ruleset to the specified output directory."""
        output_path = Path(output_dir)
        
        if format == "cursor":
            renderer = CursorRenderer()
            filename = "documentation-structure-standards.mdc"
        elif format == "copilot":
            renderer = CopilotRenderer()
            filename = "documentation-structure-standards.instructions.md"
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
