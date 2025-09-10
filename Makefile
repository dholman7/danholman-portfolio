# Portfolio Makefile - Comprehensive development and testing commands
.PHONY: help install test lint fmt ci allure-serve allure-generate allure-clean test-regression quality-check quality-readmes quality-workflows quality-tests quality-versions quality-fix

# Default target
help: ## Show this help message
	@echo "Dan Holman Portfolio - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install all dependencies (Python + Node.js) for all modules
	@echo "🚀 Installing all dependencies for Dan Holman Portfolio..."
	@echo ""
	@echo "⚠️  WARNING: This will create a virtual environment in ./venv/"
	@echo "   This is safe and isolated from your system Python."
	@echo ""
	@echo "📦 Installing Python dependencies..."
	@echo "  - Setting up virtual environment in ./venv/..."
	@python3 -m venv venv
	@. venv/bin/activate && pip install -U pip
	@echo "  - Installing ai-rulesets package..."
	@. venv/bin/activate && cd ai-rulesets && pip install -e .
	@echo "  - Installing automation-framework dependencies..."
	@. venv/bin/activate && cd automation-framework && pip install -r requirements.txt
	@echo ""
	@echo "📦 Installing Node.js dependencies..."
	@echo "  - Installing cloud-native-app dependencies..."
	@cd cloud-native-app && yarn install
	@echo "  - Installing react-playwright-demo dependencies..."
	@cd react-playwright-demo && yarn install
	@echo ""
	@echo "✅ All dependencies installed successfully!"
	@echo ""
	@echo "💡 Next steps:"
	@echo "  - Activate virtual environment: . venv/bin/activate"
	@echo "  - Run 'make test' to run all tests"
	@echo "  - Run 'make quality-check' to check code quality"
	@echo "  - Run 'make allure-serve' to view test reports"

install-dev: ## Install development dependencies for all modules
	@echo "🚀 Installing development dependencies for Dan Holman Portfolio..."
	@echo ""
	@echo "📦 Installing Python development dependencies..."
	@echo "  - Setting up virtual environment..."
	@python3 -m venv venv
	@. venv/bin/activate && pip install -U pip
	@echo "  - Installing ai-rulesets with dev dependencies..."
	@. venv/bin/activate && cd ai-rulesets && pip install -e ".[dev]"
	@echo "  - Installing automation-framework with dev dependencies..."
	@. venv/bin/activate && cd automation-framework && pip install -e ".[dev,test,api,web,performance]"
	@echo ""
	@echo "📦 Installing Node.js development dependencies..."
	@echo "  - Installing cloud-native-app dependencies..."
	@cd cloud-native-app && yarn install
	@echo "  - Installing react-playwright-demo dependencies..."
	@cd react-playwright-demo && yarn install
	@echo ""
	@echo "✅ All development dependencies installed successfully!"

install-quick: ## Quick install (assumes venv exists, just installs packages)
	@echo "⚡ Quick install (updating existing packages)..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		exit 1; \
	fi
	@. venv/bin/activate && cd ai-rulesets && pip install -e .
	@. venv/bin/activate && cd automation-framework && pip install -r requirements.txt
	@cd cloud-native-app && yarn install
	@cd react-playwright-demo && yarn install
	@echo "✅ Quick install completed!"

setup: ## Complete setup with explicit instructions
	@echo "🚀 Dan Holman Portfolio - Complete Setup"
	@echo "========================================"
	@echo ""
	@echo "This will set up everything you need to run the portfolio:"
	@echo "  ✅ Python virtual environment (isolated from system)"
	@echo "  ✅ All Python dependencies"
	@echo "  ✅ All Node.js dependencies"
	@echo "  ✅ Quality checker ready to use"
	@echo ""
	@echo "⚠️  This creates a virtual environment in ./venv/ (safe and isolated)"
	@echo ""
	@read -p "Continue? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo ""
	@echo "📦 Step 1: Installing Python dependencies..."
	@python3 -m venv venv
	@. venv/bin/activate && pip install -U pip
	@. venv/bin/activate && cd ai-rulesets && pip install -e .
	@. venv/bin/activate && cd automation-framework && pip install -r requirements.txt
	@echo "✅ Python dependencies installed!"
	@echo ""
	@echo "📦 Step 2: Installing Node.js dependencies..."
	@cd cloud-native-app && yarn install
	@cd react-playwright-demo && yarn install
	@echo "✅ Node.js dependencies installed!"
	@echo ""
	@echo "🎉 Setup complete! Here's what you can do now:"
	@echo ""
	@echo "1. Activate the virtual environment:"
	@echo "   . venv/bin/activate"
	@echo ""
	@echo "2. Run quality checks:"
	@echo "   make quality-check"
	@echo ""
	@echo "3. Run tests:"
	@echo "   make test"
	@echo ""
	@echo "4. View test reports:"
	@echo "   make allure-serve"
	@echo ""
	@echo "💡 The virtual environment is isolated and safe - it won't affect your system Python!"

# Code Quality
lint:
	$(MAKE) -C automation-framework lint || true
	$(MAKE) -C cloud-native-app lint || true
	$(MAKE) -C ai-rulesets lint || true
	$(MAKE) -C react-playwright-demo lint || true

fmt:
	$(MAKE) -C automation-framework fmt || true
	$(MAKE) -C cloud-native-app fmt || true
	$(MAKE) -C ai-rulesets fmt || true
	$(MAKE) -C react-playwright-demo fmt || true

# Testing
test:
	$(MAKE) -C automation-framework test || true
	$(MAKE) -C cloud-native-app test || true
	$(MAKE) -C ai-rulesets test || true
	$(MAKE) -C react-playwright-demo test || true

test-regression: ## Run comprehensive regression tests for all modules
	@echo "Running regression tests for all modules..."
	$(MAKE) -C automation-framework test-regression || true
	$(MAKE) -C cloud-native-app test-regression || true
	$(MAKE) -C ai-rulesets test-regression || true
	$(MAKE) -C react-playwright-demo test-regression || true
	@echo "Regression tests completed for all modules"

# Allure Reporting
allure-results: ## Generate Allure test results for all modules
	@echo "Generating Allure results for all modules..."
	$(MAKE) -C automation-framework allure-results || true
	$(MAKE) -C cloud-native-app allure-results || true
	$(MAKE) -C ai-rulesets allure-results || true
	$(MAKE) -C react-playwright-demo allure-results || true
	@echo "Allure results generated for all modules"

allure-generate: allure-results ## Generate Allure HTML reports for all modules
	@echo "Generating Allure HTML reports for all modules..."
	$(MAKE) -C automation-framework allure-generate || true
	$(MAKE) -C cloud-native-app allure-generate || true
	$(MAKE) -C ai-rulesets allure-generate || true
	$(MAKE) -C react-playwright-demo allure-generate || true
	@echo "Allure HTML reports generated for all modules"

allure-serve: ## Serve Allure reports locally for all modules
	@echo "Starting Allure report server for all modules..."
	@echo "Available reports:"
	@echo "  - Automation Framework: http://localhost:5050/automation-framework"
	@echo "  - AI Rulesets: http://localhost:5051/ai-rulesets"
	@echo "  - Cloud Native App: http://localhost:5052/cloud-native-app"
	@echo "  - React Playwright Demo: http://localhost:5053/react-playwright-demo"
	@echo ""
	@echo "Starting servers in background..."
	$(MAKE) -C automation-framework allure-serve &
	$(MAKE) -C ai-rulesets allure-serve &
	$(MAKE) -C cloud-native-app allure-serve &
	$(MAKE) -C react-playwright-demo allure-serve &
	@echo "Allure servers started. Press Ctrl+C to stop all servers."

allure-serve-single: ## Serve Allure reports for a specific module (usage: make allure-serve-single MODULE=automation-framework)
	@if [ -z "$(MODULE)" ]; then \
		echo "Usage: make allure-serve-single MODULE=<module-name>"; \
		echo "Available modules: automation-framework, ai-rulesets, cloud-native-app, react-playwright-demo"; \
		exit 1; \
	fi
	@echo "Starting Allure server for $(MODULE)..."
	$(MAKE) -C $(MODULE) allure-serve

allure-serve-local: allure-generate ## Serve Allure reports with history support locally
	@echo "🚀 Starting local Allure report server with history support..."
	@echo "📊 Available reports:"
	@echo "  - Automation Framework: http://localhost:5050"
	@echo "  - AI Rulesets: http://localhost:5051" 
	@echo "  - Cloud Native App: http://localhost:5052"
	@echo "  - React Playwright Demo: http://localhost:5053"
	@echo ""
	@echo "Starting servers with history support..."
	@if command -v allure >/dev/null 2>&1; then \
		allure serve automation-framework/reports/allure-results --port 5050 --host 0.0.0.0 & \
		allure serve ai-rulesets/reports/allure-results --port 5051 --host 0.0.0.0 & \
		allure serve cloud-native-app/reports/allure-results --port 5052 --host 0.0.0.0 & \
		allure serve react-playwright-demo/reports/allure-results --port 5053 --host 0.0.0.0 & \
		echo "✅ Allure servers started with history support"; \
		echo "Press Ctrl+C to stop all servers"; \
		wait; \
	else \
		echo "❌ Allure command not found. Run 'make setup-allure' first."; \
		exit 1; \
	fi

allure-setup: ## Setup Allure commandline for local development
	@echo "🔧 Setting up Allure for local development..."
	@if [ -f "scripts/setup-local-allure.sh" ]; then \
		./scripts/setup-local-allure.sh; \
	else \
		echo "❌ Setup script not found. Installing Allure manually..."; \
		yarn global add allure-commandline; \
	fi

allure-history: ## Copy Allure history for trend analysis
	@echo "📈 Copying Allure history for trend analysis..."
	@mkdir -p allure-history/automation-framework allure-history/ai-rulesets allure-history/cloud-native-app allure-history/react-playwright-demo
	@if [ -d "automation-framework/reports/allure-report/history" ]; then \
		cp -r automation-framework/reports/allure-report/history/* allure-history/automation-framework/ 2>/dev/null || true; \
		echo "✅ Automation framework history copied"; \
	fi
	@if [ -d "ai-rulesets/reports/allure-report/history" ]; then \
		cp -r ai-rulesets/reports/allure-report/history/* allure-history/ai-rulesets/ 2>/dev/null || true; \
		echo "✅ AI rulesets history copied"; \
	fi
	@if [ -d "cloud-native-app/reports/allure-report/history" ]; then \
		cp -r cloud-native-app/reports/allure-report/history/* allure-history/cloud-native-app/ 2>/dev/null || true; \
		echo "✅ Cloud native app history copied"; \
	fi
	@if [ -d "react-playwright-demo/reports/allure-report/history" ]; then \
		cp -r react-playwright-demo/reports/allure-report/history/* allure-history/react-playwright-demo/ 2>/dev/null || true; \
		echo "✅ React Playwright Demo history copied"; \
	fi
	@echo "📊 Allure history copied for trend analysis"

allure-clean: ## Clean Allure reports and results for all modules
	@echo "Cleaning Allure reports for all modules..."
	$(MAKE) -C automation-framework allure-clean || true
	$(MAKE) -C cloud-native-app allure-clean || true
	$(MAKE) -C ai-rulesets allure-clean || true
	$(MAKE) -C react-playwright-demo allure-clean || true
	rm -rf allure-history/
	@echo "Allure reports cleaned for all modules"

# Docker-based Allure (no Java required)
allure-docker-serve: allure-results ## Serve Allure reports using Docker (no Java required)
	@echo "🐳 Starting Allure report server using Docker..."
	@echo "📊 Available reports:"
	@echo "  - Automation Framework: http://localhost:5050"
	@echo "  - AI Rulesets: http://localhost:5051"
	@echo "  - Cloud Native App: http://localhost:5052"
	@echo "  - React Playwright Demo: http://localhost:5053"
	@echo ""
	@echo "Starting Docker containers..."
	@docker run -d --name allure-automation-framework -p 5050:5050 -v $(PWD)/automation-framework/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@docker run -d --name allure-ai-rulesets -p 5051:5050 -v $(PWD)/ai-rulesets/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@docker run -d --name allure-cloud-native-app -p 5052:5050 -v $(PWD)/cloud-native-app/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@docker run -d --name allure-react-playwright-demo -p 5053:5050 -v $(PWD)/react-playwright-demo/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@echo "✅ Docker-based Allure servers started"
	@echo "Press Ctrl+C to stop all servers"
	@trap 'docker stop allure-automation-framework allure-ai-rulesets allure-cloud-native-app allure-react-playwright-demo && docker rm allure-automation-framework allure-ai-rulesets allure-cloud-native-app allure-react-playwright-demo' INT
	@wait

allure-docker-generate: allure-results ## Generate Allure reports using Docker
	@echo "🐳 Generating Allure reports using Docker..."
	@$(MAKE) -C automation-framework allure-docker-generate || true
	@$(MAKE) -C ai-rulesets allure-docker-generate || true
	@$(MAKE) -C cloud-native-app allure-docker-generate || true
	@$(MAKE) -C react-playwright-demo allure-docker-generate || true
	@echo "✅ Docker-based Allure reports generated"

allure-docker-clean: ## Clean Docker-based Allure containers
	@echo "🧹 Cleaning Docker Allure containers..."
	@docker stop allure-automation-framework allure-ai-rulesets allure-cloud-native-app allure-react-playwright-demo 2>/dev/null || true
	@docker rm allure-automation-framework allure-ai-rulesets allure-cloud-native-app allure-react-playwright-demo 2>/dev/null || true
	@echo "✅ Docker Allure containers cleaned"

# Comprehensive Testing and Reporting
test-allure: test-regression allure-generate ## Run regression tests and generate Allure reports
	@echo "Regression testing and Allure reporting completed for all modules"

test-allure-local: test-regression allure-generate allure-history ## Run tests with Allure and maintain history
	@echo "✅ Local testing with Allure history completed for all modules"
	@echo "📊 Run 'make allure-serve-local' to view reports with history"

test-allure-quick: ## Quick test run with Allure (smoke tests only)
	@echo "🚀 Running quick tests with Allure..."
	$(MAKE) -C automation-framework test-smoke allure-results || true
	$(MAKE) -C ai-rulesets test-unit allure-results || true
	$(MAKE) -C cloud-native-app test-unit allure-results || true
	$(MAKE) -C react-playwright-demo test-unit allure-results || true
	@echo "✅ Quick tests with Allure completed"

# CI/CD
ci: install lint test

ci-regression: install test-regression allure-generate ## Run comprehensive CI with regression tests and Allure reports
	@echo "CI regression testing completed for all modules"

# Pre-commit
pre-commit-install:
	pre-commit install || true

pre-commit-run:
	pre-commit run --all-files || true

# Cleanup
clean: ## Clean up generated files for all modules
	$(MAKE) -C automation-framework clean || true
	$(MAKE) -C cloud-native-app clean || true
	$(MAKE) -C ai-rulesets clean || true
	$(MAKE) -C react-playwright-demo clean || true
	@echo "Cleanup completed for all modules"

# Status and Information
status: ## Show status of all modules
	@echo "Portfolio Status:"
	@echo "================="
	@echo "Automation Framework:"
	@$(MAKE) -C automation-framework status 2>/dev/null || echo "  Status unavailable"
	@echo ""
	@echo "Cloud Native App:"
	@$(MAKE) -C cloud-native-app status 2>/dev/null || echo "  Status unavailable"
	@echo ""
	@echo "AI Rulesets:"
	@$(MAKE) -C ai-rulesets status 2>/dev/null || echo "  Status unavailable"
	@echo ""
	@echo "React Playwright Demo:"
	@$(MAKE) -C react-playwright-demo status 2>/dev/null || echo "  Status unavailable"

info: ## Show portfolio information
	@echo "Dan Holman Portfolio"
	@echo "==================="
	@echo "Modules:"
	@echo "  - automation-framework: Python/TypeScript test automation framework"
	@echo "  - cloud-native-app: AWS serverless demo with Lambda and DynamoDB"
	@echo "  - ai-rulesets: Organizational AI rulesets and development standards"
	@echo "  - react-playwright-demo: Modern React demo with E2E testing"
	@echo ""
	@echo "Available Commands:"
	@echo "  make setup            - Complete setup with explicit instructions (RECOMMENDED)"
	@echo "  make install          - Install all dependencies (Python + Node.js)"
	@echo "  make install-dev      - Install development dependencies"
	@echo "  make install-quick    - Quick install (assumes venv exists)"
	@echo "  make test-regression  - Run comprehensive regression tests"
	@echo "  make allure-serve     - Serve Allure reports locally"
	@echo "  make allure-generate  - Generate Allure HTML reports"
	@echo "  make test-allure      - Run tests and generate reports"
	@echo "  make quality-check    - Run comprehensive code quality checks"
	@echo "  make quality-readmes  - Check README files for accuracy"
	@echo "  make quality-workflows - Check GitHub workflow files"
	@echo "  make quality-tests    - Check test execution and reporting"
	@echo "  make quality-versions - Check version consistency across modules"
	@echo "  make quality-fix      - Automatically fix common quality issues"

# Quality Checks
quality-check: ## Run comprehensive code quality checks for all modules
	@echo "🔍 Running comprehensive code quality checks..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		echo "Then activate it with: . venv/bin/activate"; \
		exit 1; \
	fi
	@. venv/bin/activate && ./quality-check

quality-readmes: ## Check README files for accuracy across all modules
	@echo "📚 Checking README files across all modules..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		echo "Then activate it with: . venv/bin/activate"; \
		exit 1; \
	fi
	@. venv/bin/activate && ./quality-check --readmes-only

quality-workflows: ## Check GitHub workflow files across all modules
	@echo "⚙️ Checking workflow files across all modules..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		echo "Then activate it with: . venv/bin/activate"; \
		exit 1; \
	fi
	@. venv/bin/activate && ./quality-check --workflows-only

quality-tests: ## Check test execution and reporting across all modules
	@echo "🧪 Checking test execution across all modules..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		echo "Then activate it with: . venv/bin/activate"; \
		exit 1; \
	fi
	@. venv/bin/activate && ./quality-check --tests-only

quality-versions: ## Check version consistency across all modules
	@echo "🔢 Checking version consistency across all modules..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		echo "Then activate it with: . venv/bin/activate"; \
		exit 1; \
	fi
	@. venv/bin/activate && ./quality-check --versions-only

quality-fix: ## Automatically fix common quality issues
	@echo "🔧 Running quality checks and applying automatic fixes..."
	@if [ ! -d "venv" ]; then \
		echo "❌ Error: Virtual environment not found!"; \
		echo "Please run 'make install' first to create the virtual environment."; \
		echo "Then activate it with: . venv/bin/activate"; \
		exit 1; \
	fi
	@. venv/bin/activate && ./quality-check --fix
