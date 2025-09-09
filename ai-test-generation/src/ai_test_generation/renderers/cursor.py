"""
Cursor guidance renderer for AI test generation.
"""

from typing import List, Optional
from pathlib import Path
from jinja2 import Template

from ..core import GuidanceTemplate


class CursorRenderer:
    """Renders Cursor-compatible guidance files (.mdc format)."""
    
    def __init__(self):
        self.template = Template("""# {{ metadata.name }}

{{ metadata.description }}

## Languages
{% for lang in metadata.languages %}- {{ lang }}
{% endfor %}

## Frameworks
{% for framework in metadata.frameworks %}- {{ framework }}
{% endfor %}

## Categories
{% for category in metadata.categories %}- {{ category }}
{% endfor %}

---

{% for item in guidance %}
## {{ item.name }}

{{ item.description }}

```{{ language }}
{{ item.content }}
```

{% if item.tags %}
**Tags:** {{ item.tags | join(", ") }}
{% endif %}

---

{% endfor %}
""")
    
    def render(self, template: GuidanceTemplate, language: Optional[str] = None) -> str:
        """Render Cursor guidance content from a guidance template."""
        if language is None:
            # Use the first language from the template
            language = template.metadata.languages[0] if template.metadata.languages else "text"
        
        return self.template.render(
            metadata=template.metadata,
            guidance=template.guidance,
            language=language
        )
    
    def render_file(self, template: GuidanceTemplate, output_path: Path, language: Optional[str] = None) -> None:
        """Render and save a Cursor guidance file."""
        content = self.render(template, language)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def render_multiple(self, templates: List[GuidanceTemplate], output_dir: Path, language: Optional[str] = None) -> None:
        """Render multiple Cursor guidance files."""
        for template in templates:
            # Create filename from template name
            filename = self._sanitize_filename(template.metadata.name) + ".mdc"
            output_path = output_dir / filename
            self.render_file(template, output_path, language)
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name for use as a filename."""
        # Replace spaces and special characters with hyphens
        import re
        sanitized = re.sub(r'[^\w\s-]', '', name.lower())
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        return sanitized.strip('-')
