# AI Test Generation Architecture

This document describes the architecture and design decisions for the AI Test Generation package.

## Overview

The AI Test Generation package provides a structured approach to creating rule sets that can be used with AI coding assistants like Cursor, GitHub Copilot, and others to generate high-quality tests. The package is designed to be:

- **Modular**: Rule sets can be mixed and matched based on project needs
- **Extensible**: Easy to add new rule sets for different frameworks and languages
- **Consistent**: Standardized format ensures consistent rule structure
- **Reusable**: Rule sets can be shared across projects and teams

## Core Components

### 1. Rule System

The core of the package is built around the concept of rules and rule sets:

- **Rule**: A single, atomic piece of testing guidance
- **RuleSet**: A collection of related rules for a specific testing framework or language
- **RuleSetMetadata**: Metadata describing the rule set (languages, frameworks, categories)

### 2. Generators

Generators convert rule sets into formats compatible with different AI tools:

- **CursorGenerator**: Creates `.mdc` files for Cursor
- **CopilotGenerator**: Creates `.instructions.md` files for GitHub Copilot
- **Future generators**: Can be added for other AI tools

### 3. CLI Interface

A command-line interface provides easy access to rule generation:

```bash
# Generate Cursor rules
ai-test-gen generate cursor --type python --output .cursor/rules

# Generate GitHub Copilot instructions
ai-test-gen generate copilot --type typescript --output .github/instructions
```

## Rule Set Structure

Each rule set follows a consistent YAML structure:

```yaml
metadata:
  name: "Python pytest Testing Rules"
  version: "1.0.0"
  description: "Comprehensive rules for generating pytest-based tests"
  languages: ["python"]
  frameworks: ["pytest"]
  categories: ["unit", "integration"]
  author: "Dan Holman"
  license: "MIT"

rules:
  - name: "Test Structure"
    description: "Define proper test file and function structure"
    content: |
      # Test files should be named test_*.py or *_test.py
      # Test functions should start with test_
      # Use descriptive test names that explain the behavior
    tags: ["structure", "naming"]
    priority: 1
```

## Design Principles

### 1. Separation of Concerns

- **Rule Definition**: Pure YAML files with testing guidance
- **Rule Processing**: Python code that loads and processes rules
- **Output Generation**: Templates that format rules for specific AI tools

### 2. Extensibility

- New rule sets can be added by creating YAML files
- New generators can be added by implementing the generator interface
- New AI tools can be supported by creating new generators

### 3. Consistency

- All rule sets follow the same structure
- All generators produce consistent output formats
- All rules include proper metadata and tagging

### 4. Reusability

- Rule sets can be shared across projects
- Rules can be filtered by tags or categories
- Generated files can be customized for specific needs

## File Organization

```
ai-test-generation/
├── src/
│   └── ai_test_generation/
│       ├── core.py              # Core data structures
│       ├── generators/          # Output generators
│       │   ├── cursor.py        # Cursor generator
│       │   └── copilot.py       # GitHub Copilot generator
│       ├── rules/               # Rule set definitions
│       │   ├── python/          # Python testing rules
│       │   ├── typescript/      # TypeScript testing rules
│       │   ├── api/             # API testing rules
│       │   └── contract/        # Contract testing rules
│       └── cli.py               # Command-line interface
├── examples/                    # Usage examples
├── docs/                        # Documentation
└── tests/                       # Package tests
```

## Rule Categories

Rules are organized into categories based on their purpose:

### 1. Structure Rules
- Test file organization
- Naming conventions
- Code structure patterns

### 2. Setup Rules
- Fixtures and test data
- Mocking and stubbing
- Test environment setup

### 3. Assertion Rules
- Test assertions
- Error handling
- Validation patterns

### 4. Integration Rules
- API testing
- Database testing
- External service testing

### 5. Performance Rules
- Load testing
- Performance monitoring
- Resource optimization

## Generator Architecture

Each generator follows a consistent pattern:

1. **Template Loading**: Load Jinja2 templates for output formatting
2. **Rule Processing**: Process rule sets and apply transformations
3. **Output Generation**: Generate formatted output for the target AI tool
4. **File Writing**: Write generated files to the specified output directory

### Template System

Generators use Jinja2 templates to format rule sets:

```jinja2
# &#123;&#123; metadata.name &#125;&#125;

&#123;&#123; metadata.description &#125;&#125;

## Languages
&#123;% for lang in metadata.languages %&#125;- &#123;&#123; lang &#125;&#125;
&#123;% endfor %&#125;

---

&#123;% for rule in rules %&#125;
## &#123;&#123; rule.name &#125;&#125;

&#123;&#123; rule.description &#125;&#125;

```&#123;&#123; language &#125;&#125;
&#123;&#123; rule.content &#125;&#125;
```

&#123;% endfor %&#125;
```

## CLI Design

The CLI is built using Click and provides:

- **Subcommands**: `generate` for different AI tools
- **Options**: `--type` for rule types, `--output` for output directory
- **Help**: Built-in help and usage information

### Command Structure

```bash
ai-test-gen generate <tool> [options]
ai-test-gen list-rules [options]
```

## Testing Strategy

The package includes comprehensive tests:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

### Test Organization

```
tests/
├── test_core.py              # Core functionality tests
├── test_generators.py        # Generator tests
├── test_cli.py              # CLI tests
└── test_rules.py            # Rule set tests
```

## Future Enhancements

### 1. Additional AI Tools
- VS Code Copilot
- JetBrains AI Assistant
- Custom AI tool integrations

### 2. Advanced Features
- Rule set validation
- Custom rule creation tools
- Rule set marketplace
- Team collaboration features

### 3. Integration Features
- IDE plugins
- CI/CD integration
- Automated rule updates
- Analytics and metrics

## Contributing

The package is designed to be easily extensible:

1. **Adding New Rule Sets**: Create YAML files in the appropriate directory
2. **Adding New Generators**: Implement the generator interface
3. **Adding New Features**: Follow the established patterns and conventions

## Security Considerations

- Rule sets are stored as plain YAML files
- No sensitive information should be included in rule sets
- Generated files should be reviewed before use
- Consider using private repositories for sensitive rule sets

## Performance Considerations

- Rule sets are loaded on-demand
- Templates are cached for performance
- Large rule sets are processed efficiently
- Generated files are optimized for readability

This architecture provides a solid foundation for AI-powered test generation while maintaining flexibility and extensibility for future enhancements.
