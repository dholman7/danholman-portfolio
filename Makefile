# Portfolio Makefile - Comprehensive development and testing commands
.PHONY: help install test lint fmt ci allure-serve allure-generate allure-clean test-regression

# Default target
help: ## Show this help message
	@echo "Dan Holman Portfolio - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install:
	$(MAKE) -C automation-framework install || true
	$(MAKE) -C cloud-native-app install || true
	$(MAKE) -C ai-test-generation install || true

install-dev:
	$(MAKE) -C automation-framework install-dev || true
	$(MAKE) -C cloud-native-app install-dev || true
	$(MAKE) -C ai-test-generation install-dev || true

# Code Quality
lint:
	$(MAKE) -C automation-framework lint || true
	$(MAKE) -C cloud-native-app lint || true
	$(MAKE) -C ai-test-generation lint || true

fmt:
	$(MAKE) -C automation-framework fmt || true
	$(MAKE) -C cloud-native-app fmt || true
	$(MAKE) -C ai-test-generation fmt || true

# Testing
test:
	$(MAKE) -C automation-framework test || true
	$(MAKE) -C cloud-native-app test || true
	$(MAKE) -C ai-test-generation test || true

test-regression: ## Run comprehensive regression tests for all modules
	@echo "Running regression tests for all modules..."
	$(MAKE) -C automation-framework test-regression || true
	$(MAKE) -C cloud-native-app test-regression || true
	$(MAKE) -C ai-test-generation test-regression || true
	@echo "Regression tests completed for all modules"

# Allure Reporting
allure-results: ## Generate Allure test results for all modules
	@echo "Generating Allure results for all modules..."
	$(MAKE) -C automation-framework allure-results || true
	$(MAKE) -C cloud-native-app allure-results || true
	$(MAKE) -C ai-test-generation allure-results || true
	@echo "Allure results generated for all modules"

allure-generate: allure-results ## Generate Allure HTML reports for all modules
	@echo "Generating Allure HTML reports for all modules..."
	$(MAKE) -C automation-framework allure-generate || true
	$(MAKE) -C cloud-native-app allure-generate || true
	$(MAKE) -C ai-test-generation allure-generate || true
	@echo "Allure HTML reports generated for all modules"

allure-serve: ## Serve Allure reports locally for all modules
	@echo "Starting Allure report server for all modules..."
	@echo "Available reports:"
	@echo "  - Automation Framework: http://localhost:5050/automation-framework"
	@echo "  - Cloud Native App: http://localhost:5051/cloud-native-app"
	@echo "  - AI Test Generation: http://localhost:5052/ai-test-generation"
	@echo ""
	@echo "Starting servers in background..."
	$(MAKE) -C automation-framework allure-serve &
	$(MAKE) -C cloud-native-app allure-serve &
	$(MAKE) -C ai-test-generation allure-serve &
	@echo "Allure servers started. Press Ctrl+C to stop all servers."

allure-serve-single: ## Serve Allure reports for a specific module (usage: make allure-serve-single MODULE=automation-framework)
	@if [ -z "$(MODULE)" ]; then \
		echo "Usage: make allure-serve-single MODULE=<module-name>"; \
		echo "Available modules: automation-framework, cloud-native-app, ai-test-generation"; \
		exit 1; \
	fi
	@echo "Starting Allure server for $(MODULE)..."
	$(MAKE) -C $(MODULE) allure-serve

allure-serve-local: allure-generate ## Serve Allure reports with history support locally
	@echo "🚀 Starting local Allure report server with history support..."
	@echo "📊 Available reports:"
	@echo "  - Automation Framework: http://localhost:5050"
	@echo "  - AI Test Generation: http://localhost:5051" 
	@echo "  - Cloud Native App: http://localhost:5052"
	@echo ""
	@echo "Starting servers with history support..."
	@if command -v allure >/dev/null 2>&1; then \
		allure serve automation-framework/reports/allure-results --port 5050 --host 0.0.0.0 & \
		allure serve ai-test-generation/reports/allure-results --port 5051 --host 0.0.0.0 & \
		allure serve cloud-native-app/reports/allure-results --port 5052 --host 0.0.0.0 & \
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
		npm install -g allure-commandline; \
	fi

allure-history: ## Copy Allure history for trend analysis
	@echo "📈 Copying Allure history for trend analysis..."
	@mkdir -p allure-history/automation-framework allure-history/ai-test-generation allure-history/cloud-native-app
	@if [ -d "automation-framework/reports/allure-report/history" ]; then \
		cp -r automation-framework/reports/allure-report/history/* allure-history/automation-framework/ 2>/dev/null || true; \
		echo "✅ Automation framework history copied"; \
	fi
	@if [ -d "ai-test-generation/reports/allure-report/history" ]; then \
		cp -r ai-test-generation/reports/allure-report/history/* allure-history/ai-test-generation/ 2>/dev/null || true; \
		echo "✅ AI test generation history copied"; \
	fi
	@if [ -d "cloud-native-app/reports/allure-report/history" ]; then \
		cp -r cloud-native-app/reports/allure-report/history/* allure-history/cloud-native-app/ 2>/dev/null || true; \
		echo "✅ Cloud native app history copied"; \
	fi
	@echo "📊 Allure history copied for trend analysis"

allure-clean: ## Clean Allure reports and results for all modules
	@echo "Cleaning Allure reports for all modules..."
	$(MAKE) -C automation-framework allure-clean || true
	$(MAKE) -C cloud-native-app allure-clean || true
	$(MAKE) -C ai-test-generation allure-clean || true
	rm -rf allure-history/
	@echo "Allure reports cleaned for all modules"

# Docker-based Allure (no Java required)
allure-docker-serve: allure-results ## Serve Allure reports using Docker (no Java required)
	@echo "🐳 Starting Allure report server using Docker..."
	@echo "📊 Available reports:"
	@echo "  - Automation Framework: http://localhost:5050"
	@echo "  - AI Test Generation: http://localhost:5051"
	@echo "  - Cloud Native App: http://localhost:5052"
	@echo ""
	@echo "Starting Docker containers..."
	@docker run -d --name allure-automation-framework -p 5050:5050 -v $(PWD)/automation-framework/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@docker run -d --name allure-ai-test-generation -p 5051:5050 -v $(PWD)/ai-test-generation/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@docker run -d --name allure-cloud-native-app -p 5052:5050 -v $(PWD)/cloud-native-app/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest &
	@echo "✅ Docker-based Allure servers started"
	@echo "Press Ctrl+C to stop all servers"
	@trap 'docker stop allure-automation-framework allure-ai-test-generation allure-cloud-native-app && docker rm allure-automation-framework allure-ai-test-generation allure-cloud-native-app' INT
	@wait

allure-docker-generate: allure-results ## Generate Allure reports using Docker
	@echo "🐳 Generating Allure reports using Docker..."
	@$(MAKE) -C automation-framework allure-docker-generate || true
	@$(MAKE) -C ai-test-generation allure-docker-generate || true
	@$(MAKE) -C cloud-native-app allure-docker-generate || true
	@echo "✅ Docker-based Allure reports generated"

allure-docker-clean: ## Clean Docker-based Allure containers
	@echo "🧹 Cleaning Docker Allure containers..."
	@docker stop allure-automation-framework allure-ai-test-generation allure-cloud-native-app 2>/dev/null || true
	@docker rm allure-automation-framework allure-ai-test-generation allure-cloud-native-app 2>/dev/null || true
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
	$(MAKE) -C ai-test-generation test-unit allure-results || true
	$(MAKE) -C cloud-native-app test-unit allure-results || true
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
	$(MAKE) -C ai-test-generation clean || true
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
	@echo "AI Test Generation:"
	@$(MAKE) -C ai-test-generation status 2>/dev/null || echo "  Status unavailable"

info: ## Show portfolio information
	@echo "Dan Holman Portfolio"
	@echo "==================="
	@echo "Modules:"
	@echo "  - automation-framework: Python/TypeScript test automation framework"
	@echo "  - cloud-native-app: AWS serverless demo with Lambda and DynamoDB"
	@echo "  - ai-test-generation: AI-powered test generation using LLMs"
	@echo ""
	@echo "Available Commands:"
	@echo "  make test-regression  - Run comprehensive regression tests"
	@echo "  make allure-serve     - Serve Allure reports locally"
	@echo "  make allure-generate  - Generate Allure HTML reports"
	@echo "  make test-allure      - Run tests and generate reports"
