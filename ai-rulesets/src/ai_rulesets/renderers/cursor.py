"""
Cursor ruleset renderer for organizational AI standards.
"""

from typing import List, Optional
from pathlib import Path
from jinja2 import Template

from ..core import Ruleset


class CursorRenderer:
    """Renders Cursor-compatible ruleset files (.mdc format)."""
    
    def __init__(self):
        self.template = Template("""---
description: {{ metadata.description }}
globs: ["**/*"]
alwaysApply: true
---

# {{ metadata.name }}

{{ metadata.description }}

## Categories
{% for category in metadata.categories %}- {{ category }}
{% endfor %}

{% if metadata.tags %}
## Tags
{% for tag in metadata.tags %}- {{ tag }}
{% endfor %}
{% endif %}

---

{% for rule in rules %}
## {{ rule.name }}

{{ rule.description }}

{{ rule.content }}

{% if rule.tags %}
**Tags:** {{ rule.tags | join(", ") }}
{% endif %}

---

{% endfor %}
""")
    
    def render_ruleset(self, ruleset: Ruleset) -> str:
        """Render Cursor ruleset content from a ruleset."""
        return self.template.render(
            metadata=ruleset.metadata,
            rules=ruleset.rules
        )
    
    def render_file(self, ruleset: Ruleset, output_path: Path) -> None:
        """Render and save a Cursor ruleset file."""
        content = self.render_ruleset(ruleset)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def render_multiple(self, rulesets: List[Ruleset], output_dir: Path) -> None:
        """Render multiple Cursor ruleset files."""
        for ruleset in rulesets:
            # Create filename from ruleset name
            filename = self._sanitize_filename(ruleset.metadata.name) + ".mdc"
            output_path = output_dir / filename
            self.render_file(ruleset, output_path)
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name for use as a filename."""
        # Replace spaces and special characters with hyphens
        import re
        sanitized = re.sub(r'[^\w\s-]', '', name.lower())
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        return sanitized.strip('-')
