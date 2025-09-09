"""
GitHub Copilot guidance renderer for AI test generation.
"""

from typing import List, Optional
from pathlib import Path
from jinja2 import Template

from ..core import GuidanceTemplate


class CopilotRenderer:
    """Renders GitHub Copilot-compatible guidance files (.md format)."""
    
    def __init__(self):
        self.template = Template("""# {{ metadata.name }} - GitHub Copilot Guidance

{{ metadata.description }}

## Supported Languages
{% for lang in metadata.languages %}- {{ lang }}
{% endfor %}

## Supported Frameworks
{% for framework in metadata.frameworks %}- {{ framework }}
{% endfor %}

## Test Categories
{% for category in metadata.categories %}- {{ category }}
{% endfor %}

---

## Testing Guidance and Patterns

{% for item in guidance %}
### {{ item.name }}

{{ item.description }}

```{{ language }}
{{ item.content }}
```

{% if item.tags %}
**Related concepts:** {{ item.tags | join(", ") }}
{% endif %}

{% endfor %}

## Usage Instructions

When generating tests, please follow these guidance patterns:

1. **Structure**: Follow the test structure patterns defined above
2. **Naming**: Use descriptive test names that explain the expected behavior
3. **Coverage**: Ensure comprehensive test coverage including edge cases
4. **Maintainability**: Write tests that are easy to read, understand, and maintain
5. **Best Practices**: Follow the specific best practices for the chosen framework

## Example Prompts

- "Generate unit tests for this Python function using pytest"
- "Create integration tests for this API endpoint"
- "Write end-to-end tests for this user flow using Playwright"
- "Generate contract tests for this service using Pact"

Remember to adapt these guidance patterns to the specific context and requirements of your project.
""")
    
    def render(self, template: GuidanceTemplate, language: Optional[str] = None) -> str:
        """Render GitHub Copilot guidance content from a guidance template."""
        if language is None:
            # Use the first language from the template
            language = template.metadata.languages[0] if template.metadata.languages else "text"
        
        return self.template.render(
            metadata=template.metadata,
            guidance=template.guidance,
            language=language
        )
    
    def render_file(self, template: GuidanceTemplate, output_path: Path, language: Optional[str] = None) -> None:
        """Render and save a GitHub Copilot guidance file."""
        content = self.render(template, language)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def render_multiple(self, templates: List[GuidanceTemplate], output_dir: Path, language: Optional[str] = None) -> None:
        """Render multiple GitHub Copilot guidance files."""
        for template in templates:
            # Create filename from template name
            filename = self._sanitize_filename(template.metadata.name) + ".instructions.md"
            output_path = output_dir / filename
            self.render_file(template, output_path, language)
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name for use as a filename."""
        # Replace spaces and special characters with hyphens
        import re
        sanitized = re.sub(r'[^\w\s-]', '', name.lower())
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        return sanitized.strip('-')
