# Code Quality Checker

A comprehensive automated validation system that ensures code quality, documentation accuracy, and consistency across all modules in the portfolio.

## 🎯 Overview

The Code Quality Checker is a powerful tool that automates the validation of:
- **README files**: Content accuracy, broken links, outdated references
- **GitHub workflows**: YAML syntax, required fields, best practices
- **Test execution**: Coverage, reporting, and integration
- **Allure reporting**: Configuration and report generation

## 🚀 Quick Start

### **Portfolio-Level Commands**
```bash
# Run comprehensive quality checks for all modules
make quality-check

# Check specific aspects
make quality-readmes      # README validation
make quality-workflows    # Workflow validation  
make quality-tests        # Test execution validation
```

### **Module-Level Commands**
```bash
# In ai-rulesets directory
make quality-check        # Full quality check
make quality-readmes      # README validation only
make quality-workflows    # Workflow validation only
make quality-tests        # Test validation only
```

### **CLI Commands**
```bash
# Comprehensive quality check
ai-rulesets quality check --project-root . --fail-on-error

# Specific validations
ai-rulesets quality readmes --project-root .
ai-rulesets quality workflows --project-root .
ai-rulesets quality tests --project-root .

# Export results
ai-rulesets quality check --export results.json
```

## 📋 Validation Categories

### **📚 README Validation**

#### **Content Accuracy**
- All README files must be up-to-date and accurate
- All references to modules, commands, and URLs must be correct
- All code examples must be tested and working
- All installation instructions must be verified

#### **Reference Validation**
- All internal links must be valid and working
- All external links must be accessible
- All file paths must exist and be correct
- All command examples must be executable

#### **Structure Standards**
- README files must follow consistent structure
- All sections must be properly formatted
- All code blocks must have proper syntax highlighting
- All tables must be properly formatted

#### **Code Example Validation**
- **Bash/Shell**: Validates command syntax and structure
- **Python**: Compiles code to check for syntax errors
- **YAML**: Validates YAML syntax and structure
- **Markdown**: Checks formatting and link validity

### **⚙️ GitHub Workflow Validation**

#### **File Structure**
- All workflow files must be in `.github/workflows/` directory
- All workflow files must have proper YAML syntax
- All workflow files must have descriptive names
- All workflow files must follow naming conventions (ci-cd.yml, not ci.yaml)

#### **Content Accuracy**
- All job names must be descriptive and consistent
- All step names must be clear and actionable
- All environment variables must be properly defined
- All secrets must be properly referenced

#### **Reference Validation**
- All module references must use current names
- All path references must be correct
- All artifact names must be consistent
- All service references must be current

#### **Security Validation**
- Checks for hardcoded secrets
- Validates proper secret management
- Ensures secure workflow practices
- Identifies potential security vulnerabilities

### **🧪 Test Execution Validation**

#### **Test Coverage**
- All modules must have comprehensive test coverage
- All critical functionality must be tested
- All edge cases must be covered
- All error conditions must be tested

#### **Test Execution**
- All tests must pass consistently
- All tests must be executable from command line
- All tests must have proper error reporting
- All tests must be properly isolated

#### **Test Reporting**
- All test results must be properly captured
- All test reports must be generated correctly
- All test artifacts must be properly stored
- All test metrics must be accurate

### **📊 Allure Reporting Validation**

#### **Configuration**
- All modules must have Allure reporting configured
- All test results must be properly formatted for Allure
- All test reports must be accessible
- All test history must be maintained

#### **Integration**
- Allure must be properly integrated across all modules
- Report generation must work consistently
- History support must be maintained
- Trend analysis must be available

## 🔧 Configuration

### **Quality Ruleset**
The quality checker uses a comprehensive ruleset defined in:
- `src/ai_rulesets/sources/quality/code-quality.md`
- `src/ai_rulesets/rulesets/quality/code_quality.py`

### **Validation Modules**
- `src/ai_rulesets/validation/readme_validator.py` - README validation
- `src/ai_rulesets/validation/workflow_validator.py` - Workflow validation
- `src/ai_rulesets/validation/test_validator.py` - Test validation
- `src/ai_rulesets/validation/quality_checker.py` - Main orchestrator

### **CLI Commands**
- `src/ai_rulesets/cli/quality.py` - Quality checking CLI commands

## 📊 Results and Reporting

### **Severity Levels**
- **🔴 Errors**: Critical issues that must be fixed
- **🟡 Warnings**: Issues that should be addressed
- **🔵 Info**: Informational items and suggestions

### **Output Format**
```
🔍 Running comprehensive code quality checks...
============================================================

📚 Validating README files...
❌ README: 29 issues found
  🔴 Errors: 4
    Broken internal link: CONTRIBUTING.md (README.md)
    Outdated reference found: AI Test Generation (README.md)
  🟡 Warnings: 8
    Line too long (over 120 characters) (README.md:3)
  🔵 Info: 17
    README missing essential section: ## 🛠️ (README.md)

============================================================
📋 QUALITY CHECK SUMMARY
============================================================
Total Issues: 37
  🔴 Errors: 7
  🟡 Warnings: 10
  🔵 Info: 17
```

### **JSON Export**
```json
{
  "summary": {
    "total_issues": 37,
    "errors": 7,
    "warnings": 10,
    "info": 17
  },
  "issues": [
    {
      "severity": "error",
      "message": "Broken internal link: CONTRIBUTING.md",
      "file_path": "README.md",
      "line_number": null
    }
  ]
}
```

## 🔄 CI/CD Integration

### **GitHub Actions**
```yaml
- name: Run Quality Checks
  run: make quality-check
  continue-on-error: false
```

### **Pre-commit Hooks**
```yaml
repos:
  - repo: local
    hooks:
      - id: quality-check
        name: Code Quality Check
        entry: make quality-check
        language: system
        pass_filenames: false
```

### **Makefile Integration**
```makefile
# Quality Checks
quality-check: ## Run comprehensive code quality checks for all modules
	@echo "🔍 Running comprehensive code quality checks..."
	$(MAKE) -C ai-rulesets quality-check || true
	@echo "✅ Quality checks completed"
```

## 🛠️ Customization

### **Adding Custom Validators**
1. Create a new validator class in `src/ai_rulesets/validation/`
2. Implement the validation logic
3. Add CLI commands in `src/ai_rulesets/cli/quality.py`
4. Update the main quality checker to include your validator

### **Custom Rules**
1. Add rules to `src/ai_rulesets/sources/quality/code-quality.md`
2. Update the ruleset processor if needed
3. Test with `make quality-check`

### **Organizational Standards**
1. Create custom rulesets for your organization
2. Integrate with your CI/CD pipeline
3. Share across teams and projects
4. Maintain and update over time

## 🎯 Benefits

### **For Developers**
- **Automated Validation**: No more manual checking of documentation and workflows
- **Consistent Standards**: Ensures all modules follow the same quality standards
- **Early Detection**: Catches issues before they reach production
- **Time Savings**: Reduces time spent on manual quality checks

### **For Teams**
- **Standardization**: Ensures consistent practices across all projects
- **Quality Gates**: Prevents low-quality code from being merged
- **Documentation**: Maintains accurate and up-to-date documentation
- **Onboarding**: New team members get consistent guidance

### **For Organizations**
- **Compliance**: Maintains security and quality standards
- **Scalability**: Easily applies standards to new projects
- **Efficiency**: Reduces time spent on code review and standards discussions
- **Innovation**: Frees up time for more important development work

## 🚀 Future Enhancements

### **Planned Features**
- **Custom Rule Engine**: Allow teams to define custom validation rules
- **Integration APIs**: REST API for integration with other tools
- **Dashboard**: Web-based dashboard for quality metrics
- **Trend Analysis**: Historical quality trend reporting
- **Team Metrics**: Quality metrics by team and project

### **Extensibility**
- **Plugin System**: Support for custom validation plugins
- **Rule Templates**: Pre-built rule templates for common scenarios
- **Integration Hooks**: Hooks for integration with external tools
- **Custom Reports**: Customizable reporting formats and outputs

## 📚 Related Documentation

- [AI Rulesets Architecture](./architecture.md)
- [Allure Integration](./allure-integration.md)
- [Main README](../README.md)
- [Portfolio Overview](../../README.md)
