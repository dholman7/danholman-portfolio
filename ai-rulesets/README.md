# AI Rulesets - Organizational Development Standards

A comprehensive Python package that provides organizational AI rulesets and utilities for creating custom development standards and guidelines. This package enables teams to establish consistent coding practices, testing standards, and development workflows that AI coding assistants can follow across all projects.

## 🎯 Purpose

This package serves two primary functions:

1. **Organizational Standards Client**: Import this package into any Python project to get access to standardized development rules and guidelines
2. **Ruleset Generation Utility**: Process company documentation and standards to create custom AI rulesets for any development team

## 🚀 Key Features

### **Organizational Standards**
- **Pre-built Rulesets**: Curated rulesets for Python, TypeScript, testing, CI/CD, and more
- **Cursor Integration**: Generate `.cursor/rules/` files for consistent AI assistance
- **GitHub Copilot**: Create instruction files for team-wide Copilot guidance
- **Customizable**: Extend and modify rulesets for your organization's needs

### **Ruleset Generation**
- **Document Processing**: Convert company docs into structured AI rulesets
- **Template System**: Create reusable ruleset templates
- **Multi-format Support**: Generate rulesets for Cursor, Copilot, and other AI tools
- **Validation**: Ensure rulesets are properly formatted and complete

### **Code Quality Validation**
- **Comprehensive Checker**: Automated validation of README files, GitHub workflows, test execution, and Allure reporting
- **37 Validation Checks**: Covers content accuracy, broken links, outdated references, syntax validation, and best practices
- **Severity Levels**: Errors (critical), Warnings (should fix), Info (nice to have) with detailed reporting
- **CI/CD Integration**: Fail-on-error, JSON export, and automated quality gates
- **Extensible Design**: Custom validation rules and organizational standards

### **CI/CD Integration**
- **Automated Generation**: Generate rulesets as part of your CI/CD pipeline
- **Version Management**: Track and version your organizational standards
- **Distribution**: Share rulesets across teams and projects
- **Quality Gates**: Validate ruleset quality and completeness

## 📦 Installation

### Prerequisites

This package requires Python 3.13. We recommend using pyenv to manage Python versions.

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
git clone https://github.com/danholman/ai-rulesets.git
cd ai-rulesets

# Install the package
pip install -e .

# Or install from PyPI (when published)
pip install ai-rulesets
```

### Development Setup

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Generate example rulesets
make examples
```

## 🔍 Code Quality Validation

The AI Rulesets package includes a comprehensive code quality checker that automates the validation of documentation, workflows, tests, and reporting across all modules.

### **Quick Quality Check**
```bash
# Run comprehensive quality validation
make quality-check

# Check specific aspects
make quality-readmes      # README validation
make quality-workflows    # Workflow validation
make quality-tests        # Test execution validation
```

### **CLI Quality Commands**
```bash
# Comprehensive quality check
ai-rulesets quality check --project-root . --fail-on-error

# Specific validations
ai-rulesets quality readmes --project-root .
ai-rulesets quality workflows --project-root .
ai-rulesets quality tests --project-root .

# Export results for CI/CD
ai-rulesets quality check --export results.json
```

### **What Gets Validated**

#### **📚 README Validation**
- Content accuracy and up-to-date information
- Broken internal and external links
- Outdated references and module names
- Code example syntax (Python, bash, YAML)
- Structure and formatting consistency

#### **⚙️ Workflow Validation**
- YAML syntax and required fields
- Job names, step names, and environment variables
- Deprecated GitHub Actions usage
- Security issues and best practices
- Naming conventions (ci-cd.yml vs ci.yaml)

#### **🧪 Test Validation**
- Test coverage and execution across all modules
- Test command availability and functionality
- Allure reporting configuration and generation
- Module integration and dependency resolution

#### **📊 Allure Reporting Validation**
- Configuration file presence and correctness
- Report generation and accessibility
- History support for trend analysis
- Integration across all modules

### **Quality Check Results**
The quality checker provides detailed reporting with:
- **Severity levels**: Errors (critical), Warnings (should fix), Info (nice to have)
- **File locations**: Exact file paths and line numbers
- **Actionable feedback**: Specific steps to fix issues
- **Summary statistics**: Total issues by severity level
- **CI/CD integration**: Exit codes and JSON export for automation

## 🚀 Quick Start

### Using Pre-built Rulesets

```bash
# Generate all standard rulesets for Cursor
ai-rulesets generate cursor --output .cursor/rules

# Generate specific ruleset types
ai-rulesets generate cursor --type python --type testing --output .cursor/rules

# Generate for GitHub Copilot
ai-rulesets generate copilot --output .github/instructions
```

### Creating Custom Rulesets

```bash
# Generate rulesets from company documentation
ai-rulesets generate-from-docs --input ./company-standards/ --output .cursor/rules

# Create ruleset from specific files
ai-rulesets generate-from-docs --input ./docs/coding-standards.md --type python --output .cursor/rules
```

### Using in Your Project

```python
from ai_rulesets import RulesetManager, CursorRenderer

# Load organizational rulesets
manager = RulesetManager()
manager.load_standard_rulesets()

# Generate Cursor rules
renderer = CursorRenderer()
rules = renderer.render_ruleset(manager.get_ruleset("python-pytest"))

# Save to project
with open(".cursor/rules/python-pytest.mdc", "w") as f:
    f.write(rules)
```

## 📚 Available Rulesets

### **Development Standards**
- **Python Development**: Code style, patterns, and best practices
- **TypeScript Development**: Modern ES6+ patterns and conventions
- **Testing Guidelines**: Comprehensive testing strategies and patterns
- **Git Workflow**: Version control and collaboration standards

### **Infrastructure & DevOps**
- **CI/CD Patterns**: GitHub Actions, Jenkins, and deployment automation
- **Docker Standards**: Containerization best practices
- **AWS Guidelines**: Cloud-native development patterns
- **Security Standards**: Security-first development practices

### **AI Integration**
- **Cursor Rules**: Comprehensive Cursor AI assistant configuration
- **Copilot Instructions**: GitHub Copilot guidance and examples
- **Prompt Engineering**: Best practices for AI tool interaction
- **Code Generation**: Standards for AI-generated code quality

## 🏗️ Package Structure

```
ai-rulesets/
├── src/
│   └── ai_rulesets/
│       ├── rulesets/          # Pre-built organizational rulesets
│       │   ├── python/        # Python development standards
│       │   ├── typescript/    # TypeScript/JS standards
│       │   ├── testing/       # Testing guidelines
│       │   ├── cicd/          # CI/CD patterns
│       │   └── security/      # Security standards
│       ├── generators/        # Ruleset generation utilities
│       │   ├── doc_processor.py  # Process company docs
│       │   ├── template_engine.py # Template system
│       │   └── validator.py   # Ruleset validation
│       ├── renderers/         # Output format renderers
│       │   ├── cursor.py      # Cursor .mdc format
│       │   ├── copilot.py     # GitHub Copilot format
│       │   └── generic.py     # Generic markdown format
│       └── cli.py             # Command-line interface
├── examples/                  # Example rulesets and usage
├── docs/                      # Documentation
└── tests/                     # Package tests
```

## 🔧 Ruleset Format

Each ruleset follows a consistent structure:

```yaml
metadata:
  name: "Python Development Standards"
  version: "1.0.0"
  description: "Organizational Python development standards"
  categories: ["development", "python", "standards"]
  tags: ["python", "pytest", "black", "ruff"]
  maintainer: "engineering@company.com"

rules:
  - name: "Code Style"
    description: "Python code style guidelines"
    content: |
      # Use Black for code formatting
      # Use Ruff for linting
      # Follow PEP 8 with 88-character line limit
      # Use type hints extensively

  - name: "Testing Standards"
    description: "Python testing guidelines"
    content: |
      # Use pytest for all testing
      # Write descriptive test names
      # Use fixtures for test data
      # Aim for 80%+ test coverage
```

## 🎯 Use Cases

### **For Development Teams**
- **Onboarding**: New developers get consistent guidance from day one
- **Code Reviews**: AI assistants follow organizational standards
- **Consistency**: All projects follow the same development patterns
- **Quality**: Automated enforcement of coding standards

### **For Engineering Managers**
- **Standardization**: Ensure consistent practices across teams
- **Scalability**: Easily distribute standards to new projects
- **Compliance**: Maintain security and quality standards
- **Efficiency**: Reduce time spent on code review and standards discussions

### **For AI Tool Users**
- **Cursor**: Get organization-specific guidance in your IDE
- **GitHub Copilot**: Receive suggestions that follow your standards
- **Custom Tools**: Generate rulesets for any AI development tool
- **Consistency**: AI suggestions align with team practices

## 🔄 Integration Examples

### **With Cursor**

1. Generate rulesets: `ai-rulesets generate cursor --type python --type testing`
2. Add to `.cursor/rules/` directory
3. Ask Cursor: "Create a new Python class following our organizational standards"

### **With GitHub Copilot**

1. Generate instructions: `ai-rulesets generate copilot --type typescript`
2. Add to `.github/instructions/` directory
3. Use Copilot with organization-specific guidance

### **With Custom AI Tools**

```python
from ai_rulesets import RulesetManager, GenericRenderer

# Load organizational standards
manager = RulesetManager()
manager.load_standard_rulesets()

# Generate generic markdown ruleset
renderer = GenericRenderer()
ruleset = renderer.render_ruleset(manager.get_ruleset("python-pytest"))

# Use with any AI tool
print(ruleset)
```

## 🏢 Organizational Setup

### **Initial Setup**

1. **Install Package**: `pip install ai-rulesets`
2. **Generate Base Rulesets**: `ai-rulesets generate cursor --all`
3. **Customize for Organization**: Modify generated rulesets
4. **Distribute to Teams**: Share rulesets across projects

### **Custom Ruleset Creation**

1. **Gather Documentation**: Collect company standards and guidelines
2. **Process Documents**: `ai-rulesets generate-from-docs --input ./standards/`
3. **Validate Rulesets**: Ensure quality and completeness
4. **Deploy**: Distribute to development teams

### **Maintenance**

1. **Version Control**: Track ruleset changes over time
2. **Regular Updates**: Keep rulesets current with best practices
3. **Team Feedback**: Collect and incorporate team suggestions
4. **Continuous Improvement**: Evolve standards based on experience

## 📈 Advanced Features

### **Ruleset Validation**

```bash
# Validate all rulesets
ai-rulesets validate --input .cursor/rules

# Validate specific ruleset
ai-rulesets validate --input .cursor/rules/python-pytest.mdc
```

### **Template System**

```python
from ai_rulesets import TemplateEngine

# Create custom template
template = TemplateEngine()
template.create_template("python-api", {
    "framework": "FastAPI",
    "testing": "pytest",
    "style": "black"
})

# Generate ruleset from template
ruleset = template.generate_ruleset("python-api")
```

### **Bulk Processing**

```bash
# Process multiple documentation sources
ai-rulesets generate-from-docs \
  --input ./docs/standards/ \
  --input ./docs/guidelines/ \
  --output .cursor/rules \
  --merge
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details on:

- Adding new standard rulesets
- Improving existing rulesets
- Adding support for new AI tools
- Creating custom generators and renderers

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Related Projects

- **[Dan Holman Portfolio](../README.md)**: Complete portfolio showcasing AI-powered development
- **[Automation Framework](../automation-framework/)**: Test automation framework with AI integration
- **[Cloud Native App](../cloud-native-app/)**: AWS serverless application with AI-enhanced testing
- **[React Playwright Demo](../react-playwright-demo/)**: Modern frontend with AI-powered E2E testing