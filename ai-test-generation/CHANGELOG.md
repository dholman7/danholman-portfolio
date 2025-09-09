# Changelog

All notable changes to the AI Test Generation package will be documented in this file.

## [0.1.0] - 2024-01-XX

### Added
- Initial release of AI Test Generation package
- Core rule system with Rule and RuleSet classes
- Cursor generator for creating `.mdc` rule files
- GitHub Copilot generator for creating `.instructions.md` files
- CLI interface for generating rules
- Comprehensive rule sets for:
  - Python testing (pytest)
  - TypeScript/JavaScript testing (Jest)
  - REST API testing
  - Contract testing (Pact)
- YAML-based rule set format
- Template system using Jinja2
- Comprehensive documentation and examples
- Makefile with development commands

### Features
- **Modular Design**: Mix and match rule sets based on project needs
- **Extensible**: Easy to add new rule sets and generators
- **Consistent**: Standardized format ensures consistent rule structure
- **Reusable**: Rule sets can be shared across projects and teams
- **CLI Interface**: Easy command-line access to rule generation
- **Multiple AI Tools**: Support for Cursor and GitHub Copilot

### Rule Sets Included
- **Python pytest**: Comprehensive pytest testing rules with fixtures, parametrization, and best practices
- **TypeScript Jest**: Jest testing rules with TypeScript support, mocking, and async testing
- **REST API**: API testing rules covering HTTP methods, status codes, validation, and error handling
- **Pact Contract**: Contract testing rules for consumer-driven contract testing

### CLI Commands
- `ai-test-gen generate cursor` - Generate Cursor rule files
- `ai-test-gen generate copilot` - Generate GitHub Copilot instruction files
- `ai-test-gen list-rules` - List available rule sets

### Development
- Python 3.8+ support
- Comprehensive test suite
- Type hints throughout
- Linting with Ruff
- Code formatting with Black
- Documentation with examples
