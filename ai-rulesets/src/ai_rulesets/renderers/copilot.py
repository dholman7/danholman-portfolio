"""
GitHub Copilot ruleset renderer for organizational AI standards.
"""

from typing import List, Optional
from pathlib import Path
from jinja2 import Template

from ..core import Ruleset


class CopilotRenderer:
    """Renders GitHub Copilot-compatible ruleset files (.md format)."""
    
    def __init__(self):
        self.template = Template("""# {{ metadata.name }} - GitHub Copilot Instructions

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

## Development Standards and Guidelines

{% for rule in rules %}
### {{ rule.name }}

{{ rule.description }}

{{ rule.content }}

{% if rule.tags %}
**Related concepts:** {{ rule.tags | join(", ") }}
{% endif %}

{% endfor %}

## Usage Instructions

When writing code, please follow these organizational standards:

1. **Code Quality**: Follow the code quality standards defined above
2. **Naming**: Use descriptive names that follow organizational conventions
3. **Structure**: Organize code according to the patterns defined
4. **Testing**: Follow the testing guidelines and patterns
5. **Documentation**: Include appropriate documentation and comments
6. **Security**: Adhere to security best practices and guidelines

## Example Prompts

- "Create a new Python class following our organizational standards"
- "Write unit tests for this function using our testing guidelines"
- "Refactor this code to follow our code quality standards"
- "Add error handling following our security guidelines"

Remember to adapt these standards to the specific context and requirements of your project.
""")
    
    def render_ruleset(self, ruleset: Ruleset) -> str:
        """Render GitHub Copilot ruleset content from a ruleset."""
        return self.template.render(
            metadata=ruleset.metadata,
            rules=ruleset.rules
        )
    
    def render_file(self, ruleset: Ruleset, output_path: Path) -> None:
        """Render and save a GitHub Copilot ruleset file."""
        content = self.render_ruleset(ruleset)
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def render_multiple(self, rulesets: List[Ruleset], output_dir: Path) -> None:
        """Render multiple GitHub Copilot ruleset files."""
        for ruleset in rulesets:
            # Create filename from ruleset name
            filename = self._sanitize_filename(ruleset.metadata.name) + ".instructions.md"
            output_path = output_dir / filename
            self.render_file(ruleset, output_path)
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name for use as a filename."""
        # Replace spaces and special characters with hyphens
        import re
        sanitized = re.sub(r'[^\w\s-]', '', name.lower())
        sanitized = re.sub(r'[-\s]+', '-', sanitized)
        return sanitized.strip('-')
