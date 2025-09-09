# AI Test Generation Framework

A comprehensive Python package that provides structured guidance templates for AI-powered test generation across multiple testing frameworks and languages. This framework enables developers to create, customize, and deploy testing guidance that AI coding assistants can follow to generate high-quality, consistent tests.

## Overview

This package contains curated rule sets for generating tests across multiple languages and frameworks:

- **Python Testing**: pytest, unittest, FastAPI, Django
- **TypeScript/JavaScript**: Jest, Playwright, Cypress, Vitest
- **API Testing**: REST APIs, GraphQL, OpenAPI/Swagger
- **Contract Testing**: Pact consumer/provider tests
- **End-to-End Testing**: Playwright, Cypress, Selenium
- **Performance Testing**: k6, Artillery, JMeter

## Installation

### Prerequisites

This package requires Python 3.13. We recommend using pyenv to manage Python versions. The project includes a `.python-version` file that specifies the required Python version.

```bash
# Install pyenv (if not already installed)
curl https://pyenv.run | bash

# Install Python 3.13
pyenv install 3.13

# Set Python 3.13 as the local version for this project
pyenv local 3.13
```

### Install the Package

```bash
# Clone the repository
git clone https://github.com/danholman/ai-test-generation.git
cd ai-test-generation

# Install the package
pip install -e .

# Or install from PyPI (when published)
pip install ai-test-generation
```

### Development Setup

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Generate example rules
make examples
```

## Quick Start

### Generate AI Assistant Guidance

```bash
# Generate all guidance templates for Cursor
ai-test-gen generate cursor --output .cursor/rules

# Generate specific test type guidance
ai-test-gen generate cursor --type python --type api --output .cursor/rules
```

### Generate GitHub Copilot Guidance

```bash
# Generate all guidance templates for GitHub Copilot
ai-test-gen generate copilot --output .github/instructions

# Generate specific test type guidance
ai-test-gen generate copilot --type typescript --type contract --output .github/instructions
```

### Use in Your Project

1. Install the package: `pip install ai-test-generation`
2. Generate rules for your preferred AI tool
3. Add the generated files to your project
4. Start asking your AI assistant to generate tests following the rules

## Available Testing Guidance Templates

### Python Testing Guidance
- **pytest**: Modern Python testing with fixtures, parametrization, and plugins
- **unittest**: Standard library testing with proper setup/teardown
- **FastAPI**: API testing with test client and dependency injection
- **Django**: Model, view, and form testing patterns

### TypeScript/JavaScript Testing Guidance
- **Jest**: Unit testing with mocking and snapshots
- **Playwright**: End-to-end testing with page object model
- **Cypress**: Component and E2E testing patterns
- **Vitest**: Fast unit testing with Vite integration

### API Testing Guidance
- **REST APIs**: Request/response validation, status codes, headers
- **GraphQL**: Query/mutation testing, schema validation
- **OpenAPI**: Contract-based testing with Swagger/OpenAPI specs

### Contract Testing Guidance
- **Pact Consumer**: Consumer-driven contract testing
- **Pact Provider**: Provider verification and state management
- **API Contracts**: Request/response schema validation

## Package Structure

```
ai-test-generation/
├── src/
│   └── ai_test_generation/
│       ├── templates/       # Testing guidance templates
│       │   ├── python/      # Python testing guidance
│       │   ├── typescript/  # TypeScript/JS testing guidance
│       │   ├── api/         # API testing guidance
│       │   └── contract/    # Contract testing guidance
│       ├── renderers/       # Template rendering tools
│       │   ├── cursor.py    # Cursor guidance renderer
│       │   └── copilot.py   # GitHub Copilot renderer
│       └── cli.py           # Command-line interface
├── examples/                # Example generated guidance
├── docs/                    # Documentation
└── tests/                   # Package tests
```

## Guidance Template Format

Each guidance template follows a consistent structure:

```yaml
metadata:
  name: "Python pytest Testing Guidance"
  version: "1.0.0"
  description: "Comprehensive guidance for generating pytest-based tests"
  languages: ["python"]
  frameworks: ["pytest"]
  categories: ["unit", "integration"]

guidance:
  - name: "Test Structure"
    description: "Define proper test file and function structure"
    content: |
      # Test files should be named test_*.py or *_test.py
      # Test functions should start with test_
      # Use descriptive test names that explain the behavior
      
  - name: "Fixtures"
    description: "Use pytest fixtures for setup and teardown"
    content: |
      # Use @pytest.fixture for reusable test data
      # Scope fixtures appropriately (function, class, module, session)
      # Use parametrized fixtures for multiple test cases
```

## Integration Examples

### With Cursor

1. Generate guidance: `ai-test-gen generate cursor --type python`
2. Add to `.cursor/rules/` directory
3. Ask Cursor: "Generate unit tests for this Python function following the pytest guidance"

### With GitHub Copilot

1. Generate guidance: `ai-test-gen generate copilot --type typescript`
2. Add to `.github/instructions/` directory
3. Use Copilot to generate tests with the provided guidance patterns

### With Custom AI Tools

```python
from ai_test_generation import GuidanceTemplate, CursorRenderer

# Load a specific guidance template
template = GuidanceTemplate.load("python", "pytest")

# Generate Cursor-compatible guidance
renderer = CursorRenderer()
cursor_guidance = renderer.render(template)

# Save to file
with open(".cursor/rules/python-pytest.mdc", "w") as f:
    f.write(cursor_guidance)
```

## Examples

### Creating Custom Guidance Templates

See our comprehensive examples showing how to:

- [Create custom guidance templates](examples/create-custom-guidance.md) - Step-by-step guide
- [Generate FastAPI guidance](examples/create_fastapi_guidance.py) - Working script example
- [Sample FastAPI app](examples/sample_fastapi_app.py) - Test application
- [Generated tests example](examples/generated_tests_example.py) - AI-generated tests

### Quick Example

```python
from ai_test_generation.core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem

# Create a custom guidance template
metadata = GuidanceTemplateMetadata(
    name="My Custom Testing Guidance",
    version="1.0.0",
    description="Custom testing patterns for my project",
    languages=["python"],
    frameworks=["pytest"],
    categories=["unit", "integration"]
)

template = GuidanceTemplate(metadata=metadata)
template.add_guidance(GuidanceItem(
    name="Custom Test Pattern",
    description="My team's specific testing pattern",
    content="# Custom testing guidance here...",
    tags=["custom", "patterns"],
    priority=1
))

# Generate AI assistant guidance
from ai_test_generation.renderers import CursorRenderer
renderer = CursorRenderer()
guidance = renderer.render(template)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Adding new guidance templates
- Improving existing guidance
- Adding support for new AI tools
- Testing and validation

## License

MIT License - see [LICENSE](LICENSE) for details.
