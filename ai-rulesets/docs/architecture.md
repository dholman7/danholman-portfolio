# AI Rulesets Architecture

This document describes the architecture and design decisions for the AI Rulesets package, designed to serve multiple user personas with different needs for organizational standards and AI-assisted development.

## Overview

The AI Rulesets package provides a comprehensive solution for organizational development standards and AI-assisted development. It serves four primary user personas:

- **Developers**: Import specific rulesets for immediate use in their projects
- **Staff Engineers**: Create and manage organizational rulesets from documentation
- **Engineering Managers**: Integrate with enterprise tools like Confluence via MCP
- **QA Engineers**: Generate rulesets from web-based documentation and standards

The package is designed to be:
- **Hierarchical**: Rulesets can be organized by domain, language, and purpose
- **Importable**: Developers can import specific rulesets as Python modules
- **Generative**: Create new rulesets from various documentation sources
- **Extensible**: Support multiple AI tools and output formats
- **Enterprise-Ready**: Integrate with Atlassian, web scraping, and MCP protocols

## User Personas & Use Cases

### 1. Developer - Import & Use
**Goal**: Quickly apply organizational standards to their project

```python
# Import specific rulesets
from ai_rulesets import ruleset
from ai_rulesets.standards import documentation

# Apply Python coding standards
ruleset.python.coding.apply_to_project()

# Apply testing standards
ruleset.python.test.apply_to_project()

# Apply documentation standards
standards.documentation.style.apply_to_project()

# Import all Python rulesets
ruleset.python.apply_all()
```

### 2. Staff Engineer - Create & Manage
**Goal**: Create organizational rulesets from internal documentation

```bash
# Create rulesets from local documentation
ai-rulesets generate-from-docs \
  --input ./company-standards/ \
  --output ./generated-rulesets/ \
  --format cursor,copilot

# Create rulesets from specific files
ai-rulesets generate-from-docs \
  --input ./docs/coding-standards.md \
  --type python \
  --output .cursor/rules
```

### 3. Engineering Manager - Enterprise Integration
**Goal**: Integrate with Confluence and other enterprise tools

```bash
# Generate rulesets from Confluence pages
ai-rulesets generate-from-confluence \
  --space "Engineering Standards" \
  --pages "Python Guidelines,Testing Standards" \
  --output ./enterprise-rulesets/

# Use MCP integration
ai-rulesets mcp-confluence \
  --server "https://company.atlassian.net" \
  --space "ENG" \
  --output ./confluence-rulesets/
```

### 4. QA Engineer - Web Documentation
**Goal**: Create rulesets from web-based documentation and standards

```bash
# Generate rulesets from web pages
ai-rulesets generate-from-web \
  --url "https://docs.pytest.org/en/stable/" \
  --type testing \
  --output ./web-rulesets/

# Generate from multiple sources
ai-rulesets generate-from-web \
  --urls "https://docs.pytest.org/,https://docs.python.org/3/tutorial/" \
  --type python \
  --output ./comprehensive-rulesets/
```

## Core Architecture

### 1. Hierarchical Ruleset System

Rulesets are organized in a hierarchical structure:

```
ai_rulesets/
├── rulesets/                    # Core organizational rulesets
│   ├── python/
│   │   ├── coding.yaml         # Python coding standards
│   │   ├── testing.yaml        # Python testing standards
│   │   └── security.yaml       # Python security standards
│   ├── typescript/
│   │   ├── coding.yaml
│   │   └── testing.yaml
│   └── standards/
│       ├── documentation/
│       │   ├── style.yaml
│       │   └── structure.yaml
│       └── ci-cd/
│           ├── github-actions.yaml
│           └── deployment.yaml
```

### 2. Import System

Developers can import rulesets at different levels:

```python
# Import entire domain
from ai_rulesets.rulesets import python
python.apply_all()

# Import specific ruleset
from ai_rulesets.rulesets.python import coding
coding.apply_to_project()

# Import by category
from ai_rulesets.rulesets.standards import documentation
documentation.style.apply_to_project()
```

### 3. Generator System

Multiple generators for different sources and outputs:

```
generators/
├── doc_processor.py          # Process local documentation
├── web_scraper.py            # Scrape web documentation
├── confluence_mcp.py         # Confluence MCP integration
├── confluence_api.py         # Confluence REST API
└── template_engine.py        # Template processing
```

### 4. Renderer System

Multiple renderers for different AI tools:

```
renderers/
├── cursor.py                 # Cursor .mdc format
├── copilot.py                # GitHub Copilot instructions
├── vscode.py                 # VS Code settings
├── jetbrains.py              # JetBrains AI Assistant
└── generic.py                # Generic markdown
```

## Detailed Component Design

### 1. Ruleset Hierarchy

```python
class RulesetHierarchy:
    """Manages hierarchical ruleset organization."""
    
    def __init__(self):
        self.domains = {}  # python, typescript, standards
        self.categories = {}  # coding, testing, security
        self.rulesets = {}  # individual rulesets
    
    def get_domain(self, domain: str) -> DomainRuleset:
        """Get all rulesets for a domain."""
        pass
    
    def get_category(self, domain: str, category: str) -> CategoryRuleset:
        """Get all rulesets for a category within a domain."""
        pass
    
    def get_ruleset(self, domain: str, category: str, name: str) -> Ruleset:
        """Get a specific ruleset."""
        pass
```

### 2. Import System

```python
# ai_rulesets/__init__.py
from .rulesets import python, typescript, standards

# ai_rulesets/rulesets/__init__.py
from .python import coding, testing, security
from .typescript import coding as ts_coding, testing as ts_testing
from .standards import documentation, ci_cd

# ai_rulesets/rulesets/python/__init__.py
from .coding import CodingRuleset
from .testing import TestingRuleset
from .security import SecurityRuleset

class PythonDomain:
    """Python domain rulesets."""
    
    def __init__(self):
        self.coding = CodingRuleset()
        self.testing = TestingRuleset()
        self.security = SecurityRuleset()
    
    def apply_all(self):
        """Apply all Python rulesets."""
        self.coding.apply()
        self.testing.apply()
        self.security.apply()
```

### 3. Document Processing

```python
class DocumentProcessor:
    """Process various documentation sources."""
    
    def process_markdown(self, file_path: Path) -> Ruleset:
        """Process Markdown documentation."""
        pass
    
    def process_confluence(self, page_id: str) -> Ruleset:
        """Process Confluence page via MCP."""
        pass
    
    def process_web(self, url: str) -> Ruleset:
        """Process web documentation."""
        pass
    
    def process_directory(self, dir_path: Path) -> List[Ruleset]:
        """Process entire directory of documentation."""
        pass
```

### 4. MCP Integration

```python
class ConfluenceMCP:
    """Confluence integration via MCP protocol."""
    
    def __init__(self, server_url: str, space_key: str):
        self.server_url = server_url
        self.space_key = space_key
        self.mcp_client = MCPClient(server_url)
    
    def get_page_content(self, page_id: str) -> str:
        """Get page content via MCP."""
        pass
    
    def search_pages(self, query: str) -> List[str]:
        """Search for pages matching query."""
        pass
    
    def generate_rulesets(self, page_ids: List[str]) -> List[Ruleset]:
        """Generate rulesets from multiple pages."""
        pass
```

### 5. Web Scraping

```python
class WebScraper:
    """Scrape web documentation for ruleset generation."""
    
    def __init__(self):
        self.session = requests.Session()
        self.parsers = {
            'pytest': PytestParser(),
            'python': PythonParser(),
            'react': ReactParser(),
        }
    
    def scrape_documentation(self, url: str, doc_type: str) -> Ruleset:
        """Scrape documentation and generate ruleset."""
        parser = self.parsers.get(doc_type)
        if not parser:
            raise ValueError(f"Unknown documentation type: {doc_type}")
        
        content = self.session.get(url).text
        return parser.parse(content)
```

## CLI Design

### Command Structure

```bash
# Developer commands
ai-rulesets import <ruleset> [options]
ai-rulesets apply <ruleset> [options]

# Staff Engineer commands
ai-rulesets generate-from-docs [options]
ai-rulesets generate-from-files [options]

# Engineering Manager commands
ai-rulesets generate-from-confluence [options]
ai-rulesets mcp-confluence [options]

# QA Engineer commands
ai-rulesets generate-from-web [options]
ai-rulesets scrape-documentation [options]

# General commands
ai-rulesets list [options]
ai-rulesets validate [options]
ai-rulesets serve [options]
```

### Detailed Commands

#### Developer Commands

```bash
# Import and apply rulesets
ai-rulesets import python.coding --output .cursor/rules
ai-rulesets import python.testing --output .cursor/rules
ai-rulesets import standards.documentation --output .cursor/rules

# Apply all rulesets for a domain
ai-rulesets import python --output .cursor/rules

# List available rulesets
ai-rulesets list --domain python
ai-rulesets list --category testing
```

#### Staff Engineer Commands

```bash
# Generate from local documentation
ai-rulesets generate-from-docs \
  --input ./company-standards/ \
  --output ./generated-rulesets/ \
  --format cursor,copilot \
  --domain python

# Generate from specific files
ai-rulesets generate-from-files \
  --files ./docs/coding-standards.md,./docs/testing-guidelines.md \
  --output .cursor/rules \
  --type python
```

#### Engineering Manager Commands

```bash
# Generate from Confluence pages
ai-rulesets generate-from-confluence \
  --server "https://company.atlassian.net" \
  --space "Engineering Standards" \
  --pages "Python Guidelines,Testing Standards,Security Guidelines" \
  --output ./enterprise-rulesets/ \
  --format cursor,copilot

# Use MCP integration
ai-rulesets mcp-confluence \
  --server "https://company.atlassian.net" \
  --space "ENG" \
  --query "python OR testing OR security" \
  --output ./confluence-rulesets/
```

#### QA Engineer Commands

```bash
# Generate from web documentation
ai-rulesets generate-from-web \
  --url "https://docs.pytest.org/en/stable/" \
  --type testing \
  --output ./web-rulesets/ \
  --format cursor,copilot

# Generate from multiple sources
ai-rulesets scrape-documentation \
  --sources "pytest:https://docs.pytest.org/,python:https://docs.python.org/3/tutorial/" \
  --output ./comprehensive-rulesets/
```

## File Organization

```
ai-rulesets/
├── src/
│   └── ai_rulesets/
│       ├── __init__.py
│       ├── core.py                    # Core data structures
│       ├── rulesets/                  # Hierarchical rulesets
│       │   ├── __init__.py
│       │   ├── python/
│       │   │   ├── __init__.py
│       │   │   ├── coding.py
│       │   │   ├── testing.py
│       │   │   └── security.py
│       │   ├── typescript/
│       │   │   ├── __init__.py
│       │   │   ├── coding.py
│       │   │   └── testing.py
│       │   └── standards/
│       │       ├── __init__.py
│       │       ├── documentation/
│       │       │   ├── __init__.py
│       │       │   ├── style.py
│       │       │   └── structure.py
│       │       └── ci-cd/
│       │           ├── __init__.py
│       │           ├── github-actions.py
│       │           └── deployment.py
│       ├── generators/                # Document processors
│       │   ├── __init__.py
│       │   ├── doc_processor.py
│       │   ├── web_scraper.py
│       │   ├── confluence_mcp.py
│       │   └── template_engine.py
│       ├── renderers/                 # Output renderers
│       │   ├── __init__.py
│       │   ├── cursor.py
│       │   ├── copilot.py
│       │   ├── vscode.py
│       │   └── jetbrains.py
│       ├── cli/                       # CLI commands
│       │   ├── __init__.py
│       │   ├── developer.py
│       │   ├── staff_engineer.py
│       │   ├── engineering_manager.py
│       │   └── qa_engineer.py
│       └── cli.py                     # Main CLI entry point
├── rulesets/                          # Default rulesets (not committed)
│   ├── python/
│   ├── typescript/
│   └── standards/
├── examples/                          # Usage examples
├── docs/                              # Documentation
└── tests/                             # Package tests
```

## Integration Points

### 1. MCP (Model Context Protocol) Integration

```python
class MCPIntegration:
    """MCP integration for enterprise tools."""
    
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.mcp_client = MCPClient(server_url)
    
    def connect_confluence(self, space_key: str) -> ConfluenceMCP:
        """Connect to Confluence via MCP."""
        pass
    
    def connect_jira(self, project_key: str) -> JiraMCP:
        """Connect to Jira via MCP."""
        pass
```

### 2. Web Scraping Integration

```python
class WebScrapingIntegration:
    """Web scraping for documentation sources."""
    
    def __init__(self):
        self.scrapers = {
            'pytest': PytestScraper(),
            'python': PythonScraper(),
            'react': ReactScraper(),
            'generic': GenericScraper(),
        }
    
    def scrape_documentation(self, url: str, doc_type: str) -> Ruleset:
        """Scrape documentation and generate ruleset."""
        pass
```

### 3. IDE Integration

```python
class IDEIntegration:
    """IDE integration for ruleset application."""
    
    def apply_to_cursor(self, ruleset: Ruleset, project_path: Path):
        """Apply ruleset to Cursor project."""
        pass
    
    def apply_to_vscode(self, ruleset: Ruleset, project_path: Path):
        """Apply ruleset to VS Code project."""
        pass
    
    def apply_to_jetbrains(self, ruleset: Ruleset, project_path: Path):
        """Apply ruleset to JetBrains project."""
        pass
```

## Security Considerations

- **MCP Authentication**: Secure authentication for enterprise tools
- **Web Scraping**: Respect robots.txt and rate limiting
- **Content Validation**: Validate scraped content before ruleset generation
- **Access Control**: Role-based access to different commands and features
- **Audit Logging**: Log all ruleset generation and application activities

## Performance Considerations

- **Caching**: Cache frequently accessed rulesets and generated content
- **Parallel Processing**: Process multiple documentation sources in parallel
- **Incremental Updates**: Only regenerate changed rulesets
- **Resource Management**: Efficient memory usage for large documentation sets

## Future Enhancements

### 1. Additional Integrations
- Jira MCP integration
- Slack integration for team notifications
- GitHub integration for PR comments
- Notion integration for documentation

### 2. Advanced Features
- AI-powered ruleset generation from natural language
- Ruleset versioning and migration
- Team collaboration features
- Analytics and usage metrics

### 3. Enterprise Features
- Single Sign-On (SSO) integration
- Role-based access control
- Audit trails and compliance reporting
- Multi-tenant support

This architecture provides a comprehensive solution for organizational standards management while serving the specific needs of different user personas in the development lifecycle.