# Dan Holman – Software Developer in Test Portfolio

Welcome to my professional portfolio!  
I’m a **Senior Software Developer in Test (SDET) & Automation Architect** with 13+ years of experience in building automation frameworks, cloud-native solutions, and quality platforms at scale.

This repo highlights examples of my work in **test automation, AWS cloud development, and AI-powered testing**.  
Each folder contains code samples or writeups demonstrating skills I use daily to improve developer velocity, reduce defects, and increase reliability.

---

## 📂 Projects

### 🔹 [Automation Framework](./automation-framework)
A sample Python/TypeScript test automation framework showing:
- Page Object design pattern
- GraphQL & REST API testing
- Contract testing with Pact
- CI/CD integration with GitHub Actions

---

### 🔹 [Cloud-Native App](./cloud-native-app)
An AWS serverless demo app with:
- Lambda + API Gateway + DynamoDB
- Infrastructure as Code (CloudFormation/CDK)
- Integration and contract tests
- GitHub Actions pipeline

---

### 🔹 [AI Rulesets](./ai-rulesets)
Organizational AI rulesets and utilities for creating custom development standards:
- Pre-built rulesets for Python, TypeScript, testing, CI/CD, and security
- Document processing utilities to create custom rulesets from company standards
- Cursor and GitHub Copilot integration for consistent AI assistance
- **🔍 Comprehensive Code Quality Checker**: Automated validation of README files, GitHub workflows, test execution, and Allure reporting across all modules
- Ruleset generation and validation tools for organizational standards

---

### 🔹 [React Playwright Demo](./react-playwright-demo)
Modern React/TypeScript frontend demo with comprehensive E2E testing:
- React 18 with TypeScript and Vite for modern development
- Tailwind CSS for responsive, accessible UI design
- Playwright E2E testing with interactive HTML reports (http://localhost:9323/)
- Allure reporting integration for test analytics
- GitHub Actions PR preview deployment
- Form validation with react-hook-form and Zod
- Mock API integration for demonstration purposes
- Parallel test execution for faster feedback

---

### 🔹 [Case Studies](./case-studies)
Technical writeups and lessons learned:
- [Contract Testing Strategy](./case-studies/contract-testing.md)  
- [Scaling Test Data with AWS Step Functions](./case-studies/test-data-at-scale.md)  
- [Improving Reliability with CI/CD Quality Gates](./case-studies/ci-cd-quality-gates.md)  

---

## 🔧 Tech Stack

- **Languages:** Python, TypeScript, GraphQL, JavaScript  
- **Frontend:** React 18, Vite, Tailwind CSS, react-hook-form, Zod  
- **Cloud & DevOps:** AWS (Lambda, S3, CloudFormation, Step Functions, RDS), GitHub Actions, Jenkins, TeamCity, Datadog  
- **Testing Tools:** pytest, Playwright, Selenium, Pact, Jest, requests, Allure, Coverage Reports  
- **Other:** Docker, SQL, Git

## 🚀 CI/CD Pipeline

This portfolio demonstrates production-ready CI/CD practices across all modules:

### **Automated Testing & Quality Gates**
- **Multi-language Testing**: Python (pytest) and TypeScript (Jest) test suites
- **Parallel Test Execution**: GitHub Actions matrix strategies for high-scale testing
- **Code Quality**: Automated linting, formatting, type checking, and security scanning
- **Coverage Reporting**: Comprehensive test coverage tracking and reporting

### **Deployment Automation**
- **Infrastructure as Code**: AWS CDK and CloudFormation for reproducible deployments
- **Multi-Environment**: Automated deployments to dev, staging, and production
- **Security Scanning**: Automated dependency and vulnerability scanning
- **Rollback Capabilities**: Safe deployment practices with rollback strategies

### **CI/CD Features Demonstrated**
- **Path-based Triggers**: Efficient CI runs based on changed modules
- **Artifact Management**: Build artifact collection and distribution
- **Environment Management**: Proper secret and configuration management
- **Monitoring Integration**: Test result aggregation and reporting

📖 **[Detailed CI/CD Documentation](./docs/cicd-overview.md)** - Comprehensive overview of all CI/CD practices and patterns

## 🧪 Testing & Reporting Technologies

This portfolio showcases comprehensive testing strategies with multiple reporting formats and real-time feedback:

### **Test Execution & Reporting**
- **Allure Reports**: Comprehensive test reporting with trends, history, and detailed analytics
- **Playwright HTML Reports**: Interactive test results with screenshots, videos, and traces
- **Coverage Reports**: Code coverage analysis with HTML visualization
- **JUnit XML**: Standardized test results for CI/CD integration
- **JSON Reports**: Machine-readable test data for automation

### **Live Reporting URLs**

#### **GitHub Pages Reports** (CI/CD Generated - Updated on every push)
- **Allure Reports**: https://dholman7.github.io/danholman-portfolio/
- **Automation Framework**: https://dholman7.github.io/danholman-portfolio/automation-framework/
- **AI Rulesets**: https://dholman7.github.io/danholman-portfolio/ai-rulesets/
- **Cloud Native App**: https://dholman7.github.io/danholman-portfolio/cloud-native-app/
- **React Playwright Demo**: https://dholman7.github.io/danholman-portfolio/react-playwright-demo/

#### **Local Development Reports** (Interactive testing during development)
- **Playwright Reports**: http://localhost:9323/ (interactive test results with screenshots/videos)
- **Coverage Reports**: http://localhost:5173/ (code coverage visualization)
- **Allure Reports**: http://localhost:5050-5053 (comprehensive test analytics with trends)

#### **CI/CD Test Failure Diagnosis**
- **GitHub Actions**: View test results, logs, and artifacts directly in PRs
- **Allure Reports**: Historical trends and failure patterns from CI runs
- **Playwright Reports**: Screenshots and videos of failed tests in CI
- **Coverage Reports**: Code coverage changes between commits

### **Testing Technologies Demonstrated**

| Technology | Purpose | Reports | Local Demo | CI/CD Demo |
|------------|---------|---------|------------|------------|
| **Playwright** | E2E Testing | HTML + Allure | http://localhost:9323/ | GitHub Actions + Allure |
| **pytest** | Python Testing | Allure + Coverage | Local + Allure | GitHub Actions + Allure |
| **Jest** | JavaScript Testing | Coverage + Allure | Local + Allure | GitHub Actions + Allure |
| **Coverage.py** | Code Coverage | HTML Reports | http://localhost:5173/ | GitHub Actions |
| **Allure** | Test Analytics | Trend Analysis | Local + GitHub Pages | GitHub Actions + GitHub Pages |

### **Report Features**
- **Real-time Updates**: Reports update automatically with each test run
- **Historical Trends**: Track test performance and stability over time
- **Interactive Dashboards**: Click through test results, screenshots, and traces
- **Coverage Visualization**: See exactly which code is tested
- **Parallel Execution**: Fast test runs with comprehensive reporting

### **CI/CD Test Failure Diagnosis**

This portfolio demonstrates production-ready test failure diagnosis workflows:

#### **GitHub Actions Integration**
- **PR Status Checks**: Tests run automatically on every pull request
- **Artifact Collection**: Screenshots, videos, and logs uploaded for failed tests
- **Matrix Testing**: Parallel execution across multiple environments
- **Failure Notifications**: Immediate feedback on test failures

#### **Diagnostic Capabilities**
- **Screenshot Capture**: Visual evidence of test failures
- **Video Recording**: Step-by-step playback of failed test scenarios
- **Console Logs**: Detailed error messages and stack traces
- **Network Logs**: API call failures and timing issues
- **Coverage Reports**: Identify untested code paths

#### **Historical Analysis**
- **Allure Trends**: Track test stability over time
- **Flaky Test Detection**: Identify unreliable tests
- **Performance Monitoring**: Track test execution times
- **Failure Patterns**: Analyze recurring issues

#### **Quick Access to CI Results**
- **GitHub Actions**: Direct links to test runs in PRs
- **Allure Reports**: Comprehensive test analytics with history
- **Artifact Downloads**: Download test artifacts for local analysis
- **Integration Status**: Real-time test status in GitHub UI

---

### **Report URLs**

#### **Live GitHub Pages Reports**
- **All Reports**: https://dholman7.github.io/danholman-portfolio/
- **Automation Framework**: https://dholman7.github.io/danholman-portfolio/automation-framework/
- **AI Rulesets**: https://dholman7.github.io/danholman-portfolio/ai-rulesets/
- **Cloud Native App**: https://dholman7.github.io/danholman-portfolio/cloud-native-app/
- **React Playwright Demo**: https://dholman7.github.io/danholman-portfolio/react-playwright-demo/

#### **Local Development Reports**

After running `make allure-serve-local`, access reports at:
- **Automation Framework**: http://localhost:5050
- **AI Rulesets**: http://localhost:5051  
- **Cloud Native App**: http://localhost:5052
- **React Playwright Demo**: http://localhost:5053

### **History Support**

The local setup maintains test execution history for trend analysis:
- **Trend Charts**: Track test results over time
- **Flaky Test Detection**: Identify unstable tests
- **Performance Trends**: Monitor test execution times
- **Failure Patterns**: Analyze recurring test failures

### **Module-Specific Testing**

```bash
# Test specific modules
make -C automation-framework test-allure
make -C ai-rulesets test-allure
make -C cloud-native-app test-allure
make -C react-playwright-demo test-allure

# Serve individual module reports
make allure-serve-single MODULE=automation-framework
make allure-serve-single MODULE=react-playwright-demo
```

### **CI/CD Test Suite**

This portfolio includes a comprehensive CI/CD test suite that can be run manually or automatically:

#### **Manual Test Execution**
Visit the [GitHub Actions page](https://github.com/dholman7/danholman-portfolio/actions/workflows/portfolio-test-suite.yml) to run the complete test suite manually with custom options:

- **Module Selection**: Choose specific modules or run all
- **Test Type Filtering**: Unit, integration, E2E, or performance tests
- **Allure Reporting**: Enable/disable comprehensive test analytics
- **Real-time Results**: View live test execution and results

#### **Automatic Execution**
Tests run automatically on:
- **Push to main**: Full test suite execution
- **Pull Requests**: Comprehensive testing with path-based triggers
- **Code Changes**: Smart execution based on modified files

### **Development Workflow**

```bash
# Complete development workflow
make install-dev          # Install dependencies
make test-allure-local    # Run tests with Allure
make allure-serve-local   # View reports with history
```

## 🔍 Code Quality Validation

This portfolio includes a **comprehensive code quality checker** that automates the validation of:
- **README files**: Accuracy, broken links, outdated references, and structure
- **GitHub workflows**: YAML syntax, required fields, and best practices
- **Test execution**: Coverage, reporting, and integration across all modules
- **Allure reporting**: Configuration and report generation validation

### **Quick Quality Check**
```bash
# Run comprehensive quality validation
make quality-check

# Check specific aspects
make quality-readmes      # README validation
make quality-workflows    # Workflow validation  
make quality-tests        # Test execution validation
```

### **Quality Checker Features**
- **37 different validation checks** across all aspects of code quality
- **Severity levels**: Errors (critical), Warnings (should fix), Info (nice to have)
- **CI/CD integration** with fail-on-error and JSON export options
- **Detailed reporting** with file paths, line numbers, and actionable feedback
- **Extensible design** for custom validation rules and organizational standards

## 🚀 Running All Tests

This portfolio provides multiple ways to run tests across all modules:

### **Quick Test Execution**

```bash
# Run all tests for all modules
make test

# Run comprehensive regression tests
make test-regression

# Run tests with Allure reporting
make test-allure

# Quick smoke tests only
make test-allure-quick
```

### **Individual Module Testing**

```bash
# Test specific modules
make -C automation-framework test
make -C ai-rulesets test
make -C cloud-native-app test
make -C react-playwright-demo test

# Test with Allure reporting
make -C automation-framework test-allure
make -C ai-rulesets test-allure
make -C cloud-native-app test-allure
make -C react-playwright-demo test-allure
```

### **Allure Report Generation**

```bash
# Generate Allure reports for all modules
make allure-generate

# Serve reports locally with history
make allure-serve-local

# Serve reports using Docker (no Java required)
make allure-docker-serve

# Serve specific module reports
make allure-serve-single MODULE=automation-framework
make allure-serve-single MODULE=ai-rulesets
make allure-serve-single MODULE=cloud-native-app
make allure-serve-single MODULE=react-playwright-demo
```

### **Available Test Commands**

| Command | Description |
|---------|-------------|
| `make test` | Run all tests for all modules |
| `make test-regression` | Run comprehensive regression tests |
| `make test-allure` | Run tests and generate Allure reports |
| `make test-allure-local` | Run tests with Allure and maintain history |
| `make test-allure-quick` | Quick smoke tests with Allure |
| `make allure-serve-local` | Serve Allure reports with history |
| `make allure-docker-serve` | Serve reports using Docker |
| `make allure-clean` | Clean all Allure reports |

---

## 📫 Connect

- 💼 [LinkedIn](https://linkedin.com/in/danxholman)  
- 📧 [danxholman@gmail.com](mailto:danxholman@gmail.com)

---

## AI-Powered Development: Concepts and How-To

This portfolio demonstrates how AI tools can accelerate development workflows and improve code quality. Here's how to leverage AI effectively in your coding practice.

### GitHub Copilot Integration

GitHub Copilot is an AI pair programmer that helps you write code faster and with fewer errors. This portfolio shows practical examples of Copilot usage:

- **Code Generation**: Generate boilerplate code, tests, and documentation
- **Pattern Recognition**: Learn from existing code patterns in the repository
- **Multi-language Support**: Works across Python, TypeScript, JavaScript, and more
- **Context Awareness**: Understands your codebase and suggests relevant solutions

**Best Practices with Copilot:**
- Review all generated code before committing
- Use descriptive comments to guide Copilot's suggestions
- Leverage Copilot for repetitive tasks and test generation
- Combine with manual coding for complex logic

### Cursor AI Editor

Cursor is an AI-powered code editor that provides intelligent code completion and natural language editing capabilities. This repository is optimized for Cursor usage:

**Key Features Demonstrated:**
- **Repo-wide Code Awareness**: Cursor understands the entire codebase context
- **Natural Language Editing**: Describe what you want to build in plain English
- **Intelligent Autocomplete**: Context-aware code suggestions
- **Multi-file Editing**: Make changes across multiple files simultaneously

**Cursor Rules Configuration**
This repository includes a modular [`.cursor/rules/`](.cursor/rules/) configuration that provides Cursor with project-specific context and coding standards:

- **[my-project-rule.mdc](.cursor/rules/my-project-rule.mdc)**: Main project overview and general guidelines
- **[python-development.mdc](.cursor/rules/python-development.mdc)**: Python 3.13 development rules and best practices
- **[typescript-development.mdc](.cursor/rules/typescript-development.mdc)**: TypeScript/Node.js rules and modern ES6+ patterns
- **[testing-guidelines.mdc](.cursor/rules/testing-guidelines.mdc)**: Comprehensive testing guidelines for pytest, Jest, and automation
- **[git-workflow.mdc](.cursor/rules/git-workflow.mdc)**: Git workflow, pull request, and version control rules
- **[ci-cd-infrastructure.mdc](.cursor/rules/ci-cd-infrastructure.mdc)**: CI/CD, infrastructure, and deployment rules
- **[ai-rulesets](ai-rulesets/)**: Organizational AI rulesets and utilities for creating custom development standards

### AI-Assisted Testing

The [AI Rulesets](./ai-rulesets) module demonstrates how to create organizational AI standards:

- **Organizational Standards**: Pre-built rulesets for consistent development practices
- **Custom Ruleset Generation**: Process company documentation into AI-compatible rulesets
- **Multi-tool Integration**: Generate rulesets for Cursor, Copilot, and other AI tools
- **Team Distribution**: Share and maintain standards across development teams

### Getting Started with AI Development

1. **Choose Your AI Tool**: Start with GitHub Copilot for code completion or Cursor for full AI editing
2. **Set Up Context**: Use the `.cursor/rules/` configuration to provide project context
3. **Start Small**: Begin with simple tasks like generating tests or documentation
4. **Iterate and Learn**: Review AI suggestions and refine your prompts
5. **Scale Up**: Gradually use AI for more complex development tasks

### Best Practices

- **Always Review**: Never blindly accept AI-generated code
- **Provide Context**: Give clear, specific instructions to AI tools
- **Maintain Quality**: Use AI to enhance, not replace, good coding practices
- **Stay Updated**: AI tools evolve rapidly, keep up with new features
- **Security First**: Be cautious with AI-generated code in security-sensitive areas

> **Learn More**: Visit [Cursor.com](https://cursor.com/) for the latest AI coding features and [GitHub Copilot](https://github.com/features/copilot) for pair programming assistance.

