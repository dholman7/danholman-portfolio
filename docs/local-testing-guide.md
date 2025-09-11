# Local Testing with Allure Reports

This guide covers how to run tests locally with Allure reporting and maintain test execution history for trend analysis.

## 🚀 Quick Start

### Prerequisites

- **Node.js** (for Allure commandline)
- **Python 3.13** (for test execution)
- **Git** (for version control)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/dholman7/danholman-portfolio.git
cd danholman-portfolio

# 2. Setup Allure commandline
make allure-setup

# 3. Install dependencies
make install-dev

# 4. Run tests with Allure
make test-allure-local

# 5. Serve reports locally
make allure-serve-local
```

## 📊 Allure Report Features

### Interactive Test Reports
- **Test Results**: Pass/fail status with detailed error messages
- **Test Steps**: Step-by-step execution breakdown
- **Attachments**: Screenshots, logs, and other test artifacts
- **Categories**: Test categorization (smoke, regression, etc.)
- **Tags**: Test tagging for filtering and organization

### History and Trends
- **Execution History**: Track test results over time
- **Trend Charts**: Visual representation of test stability
- **Flaky Test Detection**: Identify unstable tests
- **Performance Metrics**: Test execution time tracking
- **Failure Analysis**: Pattern recognition in test failures

## 🔧 Available Commands

### Setup Commands
```bash
make allure-setup          # Install Allure commandline
make install-dev           # Install development dependencies
```

### Testing Commands
```bash
make test-allure-local     # Run all tests with Allure and history
make test-allure-quick     # Quick test run (smoke tests only)
make test-regression       # Run comprehensive regression tests
```

### Report Commands
```bash
make allure-serve-local    # Serve all reports with history
make allure-serve-single MODULE=<name>  # Serve specific module
make allure-generate       # Generate static HTML reports
make allure-history        # Copy history for trend analysis
```

### Cleanup Commands
```bash
make allure-clean          # Clean all Allure reports and history
make clean                 # Clean all generated files
```

## 📁 Directory Structure

```
danholman-portfolio/
├── allure-history/                    # Allure history storage
│   ├── automation-framework/
│   ├── ai-rulesets/
│   └── cloud-native-app/
├── automation-framework/
│   └── reports/
│       ├── allure-results/           # Raw Allure results
│       └── allure-report/            # Generated HTML reports
├── ai-rulesets/
│   └── reports/
│       ├── allure-results/
│       └── allure-report/
├── cloud-native-app/
│   └── reports/
│       ├── allure-results/
│       └── allure-report/
└── scripts/
    └── setup-local-allure.sh         # Allure setup script
```

## 🎯 Module-Specific Testing

### Automation Framework
```bash
# Navigate to module
cd automation-framework

# Run specific test types
make test-unit              # Unit tests only
make test-component         # Component tests only
make test-integration       # Integration tests only
make test-e2e              # End-to-end tests only

# Run with Allure
make test-allure           # All tests with Allure
make allure-serve          # Serve reports locally
```

### AI Rulesets
```bash
# Navigate to module
cd ai-rulesets

# Run specific test types
make test-unit              # Unit tests only
make test-component         # Component tests only
make test-integration       # Integration tests only

# Run with Allure
make test-allure           # All tests with Allure
make allure-serve          # Serve reports locally
```

### Cloud Native App
```bash
# Navigate to module
cd cloud-native-app

# Run tests
make test                  # All tests
make test-allure          # Tests with Allure

# Serve reports
make allure-serve         # Serve reports locally
```

## 📈 History Management

### Automatic History
The local setup automatically maintains test execution history:
- **Trend Analysis**: Track test stability over time
- **Performance Monitoring**: Monitor test execution times
- **Failure Patterns**: Identify recurring issues
- **Flaky Test Detection**: Spot unstable tests

### Manual History Management
```bash
# Copy history for trend analysis
make allure-history

# Clean history
make allure-clean
```

## 🔍 Report Analysis

### Accessing Reports
After running `make allure-serve-local`, access reports at:
- **Automation Framework**: http://localhost:5050
- **AI Rulesets**: http://localhost:5051
- **Cloud Native App**: http://localhost:5052

### Report Features
- **Overview**: Test execution summary
- **Categories**: Test categorization and filtering
- **Suites**: Test suite organization
- **Graphs**: Visual test result analysis
- **Timeline**: Test execution timeline
- **Behaviors**: BDD-style test organization
- **Packages**: Test package structure

### Filtering and Search
- **By Status**: Pass, fail, broken, skipped
- **By Category**: Smoke, regression, integration
- **By Tag**: Custom test tags
- **By Time**: Date range filtering
- **By Duration**: Execution time filtering

## 🐛 Troubleshooting

### Common Issues

#### Allure Command Not Found
```bash
# Install Allure commandline
make allure-setup

# Or install manually
npm install -g allure-commandline
```

#### Port Already in Use
```bash
# Kill existing processes
pkill -f allure

# Or use different ports
allure serve reports/allure-results --port 5053
```

#### Permission Denied
```bash
# Make setup script executable
chmod +x scripts/setup-local-allure.sh
```

#### Python Version Issues
```bash
# Check Python version
python --version

# Install correct version
pyenv install 3.13
pyenv local 3.13
```

### Debug Mode
```bash
# Run with verbose output
make test-allure-local VERBOSE=1

# Check Allure version
allure --version

# Validate Allure results
allure validate reports/allure-results
```

## 🔄 CI/CD Integration

### Local CI Simulation
```bash
# Run full CI pipeline locally
make ci-regression

# Run specific CI steps
make lint                  # Code quality checks
make test                  # Test execution
make allure-generate       # Report generation
```

### Artifact Management
```bash
# Generate CI artifacts
make allure-generate

# Archive reports
tar -czf allure-reports.tar.gz */reports/allure-report/
```

## 📚 Advanced Usage

### Custom Allure Configuration
Create `allure.properties` in each module:
```properties
allure.results.directory=reports/allure-results
allure.link.issue.pattern=https://github.com/dholman7/danholman-portfolio/issues/{}
allure.link.tms.pattern=https://github.com/dholman7/danholman-portfolio/issues/{}
```

### Environment-Specific Testing
```bash
# Test against different environments
TEST_ENVIRONMENT=dev make test-allure-local
TEST_ENVIRONMENT=staging make test-allure-local
TEST_ENVIRONMENT=prod make test-allure-local
```

### Parallel Test Execution
```bash
# Run tests in parallel
make test-parallel

# Run with specific worker count
pytest -n 4 --alluredir=reports/allure-results
```

## 🎨 Customization

### Custom Report Themes
```bash
# Generate with custom theme
allure generate reports/allure-results --clean -o reports/allure-report --theme dark
```

### Custom Categories
Edit `allure-categories.json` in each module:
```json
[
  {
    "name": "Test defects",
    "matchedStatuses": ["failed"]
  },
  {
    "name": "Product defects", 
    "matchedStatuses": ["broken"]
  }
]
```

## 📞 Support

For issues or questions:
- **GitHub Issues**: [Create an issue](https://github.com/dholman7/danholman-portfolio/issues)
- **Email**: danxholman@gmail.com
- **LinkedIn**: [Dan Holman](https://linkedin.com/in/danxholman)
