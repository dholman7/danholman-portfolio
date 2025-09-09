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

### 🔹 [AI Test Generation](./ai-test-generation)
Comprehensive AI-powered testing framework featuring:
- LLM-driven test case generation from API schemas
- GitHub Actions matrix strategies for high-scale parallel testing
- Dynamic test matrix generation and artifact merging
- Production-ready CI/CD patterns for test automation

---

### 🔹 [Case Studies](./case-studies)
Technical writeups and lessons learned:
- [Contract Testing Strategy](./case-studies/contract-testing.md)  
- [Scaling Test Data with AWS Step Functions](./case-studies/test-data-at-scale.md)  
- [Improving Reliability with CI/CD Quality Gates](./case-studies/ci-cd-quality-gates.md)  

---

## 🔧 Tech Stack

- **Languages:** Python, TypeScript, GraphQL  
- **Cloud & DevOps:** AWS (Lambda, S3, CloudFormation, Step Functions, RDS), GitHub Actions, Jenkins, TeamCity, Datadog  
- **Testing Tools:** pytest, Selenium, Pact, Jest, requests, Allure  
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

---

## 🧪 Local Testing with Allure Reports

This portfolio includes comprehensive local testing capabilities with Allure reporting and history support for trend analysis.

### **Quick Start**

#### Option 1: Native Allure (requires Java)
```bash
# 1. Setup Allure commandline
make allure-setup

# 2. Run tests with Allure reports
make test-allure-local

# 3. Serve reports locally with history
make allure-serve-local
```

#### Option 2: Docker-based Allure (no Java required)
```bash
# 1. Run tests with Allure reports
make test-allure-local

# 2. Serve reports using Docker
make allure-docker-serve
```

### **Available Commands**

| Command | Description |
|---------|-------------|
| `make allure-setup` | Install Allure commandline for local development |
| `make test-allure-local` | Run all tests with Allure reports and history |
| `make test-allure-quick` | Quick test run (smoke tests only) with Allure |
| `make allure-serve-local` | Serve Allure reports with history support |
| `make allure-serve-single MODULE=<name>` | Serve reports for specific module |
| `make allure-history` | Copy Allure history for trend analysis |
| `make allure-clean` | Clean all Allure reports and history |
| `make allure-docker-serve` | Serve Allure reports using Docker (no Java required) |
| `make allure-docker-generate` | Generate Allure reports using Docker |
| `make allure-docker-clean` | Clean Docker-based Allure containers |

### **Local Report URLs**

After running `make allure-serve-local`, access reports at:
- **Automation Framework**: http://localhost:5050
- **AI Test Generation**: http://localhost:5051  
- **Cloud Native App**: http://localhost:5052

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
make -C ai-test-generation test-allure  
make -C cloud-native-app test-allure

# Serve individual module reports
make allure-serve-single MODULE=automation-framework
```

### **Development Workflow**

```bash
# Complete development workflow
make install-dev          # Install dependencies
make test-allure-local    # Run tests with Allure
make allure-serve-local   # View reports with history
```

---

## 📫 Connect

- 💼 [LinkedIn](https://linkedin.com/in/danxholman)  
- 📧 [danxholman@gmail.com](mailto:danxholman@gmail.com)

---

## AI Testing: Concepts and How-To

### What are agent rules?
Agent rules constrain and guide model behavior (tone, safety, allowed tools).
- Public rules live in `ai-test-generation/agents/*.public.yaml`.


### Using code and docs as context
- Put code/docs in the prompt or reference files that your runner loads.
- Example: `evals/cases/summarize.jsonl` points to `evals/example-cf.yaml` as context.
- Your real runner would read the context file and include it in the model input.

### Public vs private content
- Public: sanitized prompts, agent configs, eval harness.
- Private: original prompts/agents/datasets in `ai-private/` (private submodule).
- Generate redacted artifacts: `make redacted` inside `ai-test-generation/`.

### Running the demo flow
1. `cd ai-test-generation`
2. `make install`
3. `make eval-run` (simulates a model call and scores output)
4. Inspect `evals/reports/scores.jsonl`

### Env and secrets
- Copy `.env.example` to `.env` and set keys locally.
- Never commit real secrets. Pre-commit hooks help prevent this.


## Working in Cursor
- See the comprehensive documentation in each module for detailed usage examples.
- Keep changes mock-only; no API calls are required.

### Cursor Rules Configuration
This repository includes a modular [`.cursor/rules/`](.cursor/rules/) configuration that provides Cursor with project-specific context and coding standards. The rules are organized by domain for better maintainability:

- **[my-project-rule.mdc](.cursor/rules/my-project-rule.mdc)**: Main project overview and general guidelines
- **[python-development.mdc](.cursor/rules/python-development.mdc)**: Python 3.13 development rules and best practices
- **[typescript-development.mdc](.cursor/rules/typescript-development.mdc)**: TypeScript/Node.js rules and modern ES6+ patterns
- **[testing-guidelines.mdc](.cursor/rules/testing-guidelines.mdc)**: Comprehensive testing guidelines for pytest, Jest, and automation
- **[git-workflow.mdc](.cursor/rules/git-workflow.mdc)**: Git workflow, pull request, and version control rules
- **[ci-cd-infrastructure.mdc](.cursor/rules/ci-cd-infrastructure.mdc)**: CI/CD, infrastructure, and deployment rules

This modular approach provides focused, domain-specific guidance that helps Cursor understand the codebase context and generate code that follows the project's standards and patterns.

> Cursor is an AI code editor with repo-wide code awareness, natural language editing, and fast autocomplete. See the official site: https://cursor.com/.

