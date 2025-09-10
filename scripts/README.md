# Portfolio Scripts

This directory contains utility scripts for the Dan Holman Portfolio.

## 🔍 Code Quality Checker

The main script in this directory is the **Code Quality Checker** (`quality_checker.py`), which provides comprehensive validation of code quality across all modules in the portfolio.

### **Features**

- **README Validation**: Content accuracy, broken links, outdated references, and structure
- **GitHub Workflow Validation**: YAML syntax, required fields, and best practices
- **Test Execution Validation**: Coverage, reporting, and integration across all modules
- **Allure Reporting Validation**: Configuration and report generation

### **Usage**

#### **Command Line**
```bash
# Run comprehensive quality checks
python scripts/quality_checker.py

# Check specific aspects
python scripts/quality_checker.py --readmes-only
python scripts/quality_checker.py --workflows-only
python scripts/quality_checker.py --tests-only

# Automatically fix common issues
python scripts/quality_checker.py --fix
python scripts/quality_checker.py --readmes-only --fix

# Export results for CI/CD
python scripts/quality_checker.py --export results.json

# Fail on critical issues
python scripts/quality_checker.py --fail-on-error
```

#### **Makefile Commands**
```bash
# Run comprehensive quality checks
make quality-check

# Check specific aspects
make quality-readmes      # README validation
make quality-workflows    # Workflow validation  
make quality-tests        # Test execution validation

# Automatically fix common issues
make quality-fix          # Check and fix issues automatically
```

### **What Gets Validated**

#### **📚 README Files**
- Content accuracy and up-to-date information
- Broken internal and external links
- Outdated references and module names
- Code example syntax (Python, bash, YAML)
- Structure and formatting consistency

#### **⚙️ GitHub Workflows**
- YAML syntax and required fields
- Job names, step names, and environment variables
- Deprecated GitHub Actions usage
- Security issues and best practices
- Naming conventions (ci-cd.yml vs ci.yaml)

#### **🧪 Test Execution**
- Test coverage and execution across all modules
- Test command availability and functionality
- Allure reporting configuration and generation
- Module integration and dependency resolution

#### **📊 Allure Reporting**
- Configuration file presence and correctness
- Report generation and accessibility
- History support for trend analysis
- Integration across all modules

### **Automatic Fixing**

The quality checker can automatically fix common issues:

#### **Fixable Issues**
- **Trailing whitespace**: Removes trailing spaces from lines
- **Outdated references**: Updates old module names (AI Test Generation → AI Rulesets)
- **Long lines**: Breaks long lines at logical points (bullet points, URLs, tables)
- **Missing workflow triggers**: Adds basic GitHub Actions triggers
- **Missing step names**: Adds generic names for workflow steps
- **Deprecated actions**: Updates to current GitHub Actions versions

#### **Fix Process**
1. **Detection**: Identifies fixable issues during validation
2. **Fixing**: Applies automatic corrections to files
3. **Verification**: Re-runs validation to confirm fixes
4. **Reporting**: Shows summary of successful and failed fixes

#### **Usage**
```bash
# Fix all issues across all modules
make quality-fix

# Fix only README issues
python scripts/quality_checker.py --readmes-only --fix

# Fix and export results
python scripts/quality_checker.py --fix --export results.json
```

### **Results and Reporting**

The quality checker provides detailed reporting with:
- **Severity levels**: Errors (critical), Warnings (should fix), Info (nice to have)
- **File locations**: Exact file paths and line numbers
- **Actionable feedback**: Specific steps to fix issues
- **Summary statistics**: Total issues by severity level
- **Fix results**: Number of issues fixed automatically
- **CI/CD integration**: Exit codes and JSON export for automation

### **Example Output**

```
🔍 Dan Holman Portfolio - Code Quality Checker
============================================================
Checking quality across all modules in: /path/to/portfolio

📚 Validating README files...
❌ README: 107 issues found
  🔴 Errors: 8
    Broken internal link: LICENSE (README.md)
    Outdated reference found: AI Rulesets (README.md)
  🟡 Warnings: 66
    Line too long (over 120 characters) (README.md:4)
  🔵 Info: 33
    README missing essential section: ## 🛠️ (README.md)

============================================================
📋 QUALITY CHECK SUMMARY
============================================================
Total Issues: 133
  🔴 Errors: 18
  🟡 Warnings: 82
  🔵 Info: 33
```

### **Integration**

The quality checker is designed to be:
- **Portfolio-wide**: Validates all modules from the root directory
- **CI/CD ready**: Supports fail-on-error and JSON export
- **Extensible**: Easy to add new validation rules
- **Focused**: Excludes build artifacts and dependencies

### **Architecture**

The quality checker consists of:
- `quality_checker.py` - Main orchestrator script
- `validation/` - Validation modules
  - `readme_validator.py` - README validation
  - `workflow_validator.py` - Workflow validation
  - `test_validator.py` - Test validation
  - `quality_checker.py` - Main quality checker class

### **Benefits**

- **Automated Validation**: No more manual checking of documentation and workflows
- **Consistent Standards**: Ensures all modules follow the same quality standards
- **Early Detection**: Catches issues before they reach production
- **Time Savings**: Reduces time spent on manual quality checks
- **Team Sharing**: Can be used across all projects and teams
