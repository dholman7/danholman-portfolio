# AI Rulesets - Examples and Quality Checker

This directory contains comprehensive examples showing how to use the AI Rulesets package to create custom guidance templates, generate rulesets, and validate code quality across all modules.

## 📁 Files Overview

### **Documentation**
- **[create-custom-guidance.md](create-custom-guidance.md)** -
  Complete step-by-step guide for creating custom guidance templates
- **[cursor-rules-example.md](cursor-rules-example.md)** - Example of using generated Cursor rules
- **[copilot-instructions-example.md](copilot-instructions-example.md)** -
  Example of using generated GitHub Copilot instructions
- **[quality-checker.md](../docs/quality-checker.md)** - Comprehensive code quality validation system

### **Working Examples**
- **[create_fastapi_guidance.py](create_fastapi_guidance.py)** - Script that creates a FastAPI testing guidance template
- **[sample_fastapi_app.py](sample_fastapi_app.py)** - Sample FastAPI application for testing
- **[generated_tests_example.py](generated_tests_example.py)** - Example tests generated using the guidance

### **Generated Files** (created by running examples)
- **[fastapi-testing-guidance.yaml](fastapi-testing-guidance.yaml)** - YAML guidance template
- **.cursor/rules/fastapi-testing-guidance.mdc** - Cursor guidance file
- **.github/instructions/fastapi-testing-guidance.instructions.md** - GitHub Copilot guidance file

## 🔍 Code Quality Checker

The AI Rulesets package includes a comprehensive code quality checker that automates validation of:
- **README files**: Content accuracy, broken links, outdated references
- **GitHub workflows**: YAML syntax, required fields, best practices
- **Test execution**: Coverage, reporting, and integration
- **Allure reporting**: Configuration and report generation

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

### **Quality Check Features**
- **37 different validation checks** across all aspects of code quality
- **Severity levels**: Errors (critical), Warnings (should fix), Info (nice to have)
- **CI/CD integration** with fail-on-error and JSON export options
- **Detailed reporting** with file paths, line numbers, and actionable feedback
- **Extensible design** for custom validation rules and organizational standards

## 🚀 Quick Start

### 1. Run the FastAPI Example

```bash
# Install dependencies
pip install fastapi pytest httpx uvicorn

# Run the example script
python examples/create_fastapi_guidance.py

# Test the sample app
python examples/sample_fastapi_app.py

# Run the generated tests
pytest examples/generated_tests_example.py -v
```

### 2. Use with AI Assistants

#### **Cursor**
1. Copy `.cursor/rules/fastapi-testing-guidance.mdc` to your project's `.cursor/rules/` directory
2. Open Cursor in your project
3. Ask: "Generate comprehensive tests for this FastAPI application following the FastAPI testing guidance"

#### **GitHub Copilot**
1. Copy `.github/instructions/fastapi-testing-guidance.instructions.md` to your project's `.github/instructions/` directory
2. Start writing test code and let Copilot suggest completions following the guidance patterns

## 📋 Example Workflow

### **Step 1: Create Guidance Template**
```python
from ai_rulesets.core import GuidanceTemplate, GuidanceTemplateMetadata, GuidanceItem

# Define metadata
metadata = GuidanceTemplateMetadata(
    name="My Custom Testing Guidance",
    version="1.0.0",
    description="Custom testing patterns for my project",
    languages=["python"],
    frameworks=["pytest"],
    categories=["unit", "integration"]
)

# Create template
template = GuidanceTemplate(metadata=metadata)

# Add guidance items
template.add_guidance(GuidanceItem(
    name="Test Structure",
    description="Define proper test structure",
    content="# Your testing guidance here...",
    tags=["structure", "patterns"],
    priority=1
))
```

### **Step 2: Generate AI Assistant Guidance**
```python
from ai_rulesets.renderers import CursorRenderer, CopilotRenderer

# Generate Cursor guidance
cursor_renderer = CursorRenderer()
cursor_guidance = cursor_renderer.render(template)
with open(".cursor/rules/my-guidance.mdc", "w") as f:
    f.write(cursor_guidance)

# Generate GitHub Copilot guidance
copilot_renderer = CopilotRenderer()
copilot_guidance = copilot_renderer.render(template)
with open(".github/instructions/my-guidance.instructions.md", "w") as f:
    f.write(copilot_guidance)
```

### **Step 3: Use with AI Assistants**
- **Cursor**: Ask to generate tests following your guidance
- **GitHub Copilot**: Let it suggest test code using your patterns
- **Result**: Consistent, high-quality tests that follow your team's standards

## 🎯 Key Benefits

1. **Consistency**: All generated tests follow the same patterns
2. **Customization**: Create guidance specific to your team's needs
3. **AI Integration**: Works seamlessly with Cursor and GitHub Copilot
4. **Maintainability**: Easy to update and share guidance templates
5. **Quality**: Ensures comprehensive test coverage and best practices

## 🔧 Customization

### **Adding New Guidance Items**
```python
template.add_guidance(GuidanceItem(
    name="New Pattern",
    description="Description of the pattern",
    content="""# Your guidance content
def example_test():
    # Example code here
    pass""",
    tags=["new", "pattern"],
    priority=2
))
```

### **Filtering Guidance**
```python
# Get high-priority guidance only
high_priority = template.get_guidance_by_priority(min_priority=1)

# Get guidance by tag
api_guidance = template.get_guidance_by_tag("api")
```

### **Saving and Loading**
```python
# Save template
template.save_to_file("my-guidance.yaml")

# Load template
loaded_template = GuidanceTemplate.from_file("my-guidance.yaml")
```

## 📚 Next Steps

1. **Explore the examples** to understand the framework
2. **Create your own guidance templates** for your specific needs
3. **Integrate with your AI tools** (Cursor, GitHub Copilot)
4. **Share templates** across your team for consistency
5. **Contribute** new guidance patterns to the community

## 🤝 Contributing

We welcome contributions! See the main [Contributing Guide](../CONTRIBUTING.md) for details on:
- Adding new guidance templates
- Improving existing examples
- Adding support for new AI tools
- Testing and validation

---

**Happy Testing! 🧪✨**
