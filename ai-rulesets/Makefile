# AI Test Generation Makefile
# Common development and testing tasks

.PHONY: help install install-dev test test-unit test-component test-integration test-e2e clean lint format type-check coverage report-allure allure-results allure-generate allure-serve allure-open allure-history allure-clean allure-docker-serve allure-docker-generate report-comprehensive

# Read Python version from .python-version file
PYTHON_VERSION := $(shell cat .python-version 2>/dev/null || echo "3.13")

# Default target
help: ## Show this help message
	@echo "AI Test Generation - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Python version check
check-python: ## Check if correct Python version is active
	@echo "Checking Python version..."
	@python --version
	@echo "Expected Python version: $(PYTHON_VERSION)"
	@if ! python --version | grep -q "Python $(PYTHON_VERSION)"; then \
		echo "Warning: Python version mismatch. Expected $(PYTHON_VERSION)"; \
		echo "Please run: pyenv install $(PYTHON_VERSION) && pyenv local $(PYTHON_VERSION)"; \
	fi

# Installation
install: check-python ## Install production dependencies
	pyenv exec python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e .

install-dev: check-python ## Install development dependencies
	pyenv exec python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[dev]"

# Testing
test: ## Run all tests
	. .venv/bin/activate && pytest

test-unit: ## Run unit tests only
	. .venv/bin/activate && pytest tests/unit/ -v

test-component: ## Run component tests only
	. .venv/bin/activate && pytest tests/component/ -v

test-integration: ## Run integration tests only
	. .venv/bin/activate && pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests only
	. .venv/bin/activate && pytest tests/e2e/ -v

# Code Quality
lint: ## Run all linting tools
	@echo "Running Black (code formatting)..."
	black --check src/ tests/
	@echo "Running isort (import sorting)..."
	isort --check-only src/ tests/
	@echo "Running Ruff (fast linting)..."
	ruff check src/ tests/

format: ## Format code with Black and isort
	@echo "Formatting with Black..."
	black src/ tests/
	@echo "Sorting imports with isort..."
	isort src/ tests/

type-check: ## Run type checking with MyPy
	mypy src/

# Coverage
coverage: ## Run tests with coverage reporting
	. .venv/bin/activate && pytest --cov=ai_rulesets --cov-report=html --cov-report=xml --cov-report=term-missing

coverage-html: ## Generate HTML coverage report
	. .venv/bin/activate && pytest --cov=ai_rulesets --cov-report=html
	@echo "Coverage report generated in htmlcov/"

coverage-xml: ## Generate XML coverage report
	. .venv/bin/activate && pytest --cov=ai_rulesets --cov-report=xml

# Allure Reporting
allure-results: ## Generate Allure test results
	. .venv/bin/activate && pytest --alluredir=reports/allure-results
	@echo "Allure results generated in reports/allure-results/"

allure-generate: allure-results ## Generate Allure HTML report
	@if command -v allure >/dev/null 2>&1; then \
		allure generate reports/allure-results --clean -o reports/allure-report; \
		echo "Allure report generated in reports/allure-report/"; \
	else \
		echo "Allure command not found. Install with: npm install -g allure-commandline"; \
		echo "Or use Docker: docker run -v $(PWD)/reports/allure-results:/app/allure-results -v $(PWD)/reports/allure-report:/app/allure-report frankescobar/allure-docker-service:latest allure generate /app/allure-results /app/allure-report"; \
	fi

allure-serve: allure-results ## Serve Allure report locally
	@if command -v allure >/dev/null 2>&1; then \
		allure serve reports/allure-results; \
	else \
		echo "Allure command not found. Install with: npm install -g allure-commandline"; \
		echo "Or use Docker: docker run -p 5050:5050 -v $(PWD)/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest"; \
	fi

allure-open: ## Open Allure report in browser (requires allure-generate first)
	@if [ -d "reports/allure-report" ]; then \
		@if command -v allure >/dev/null 2>&1; then \
			allure open reports/allure-report; \
		else \
			echo "Opening report in browser..."; \
			python -m http.server 8000 -d reports/allure-report; \
		fi; \
	else \
		echo "Allure report not found. Run 'make allure-generate' first."; \
	fi

allure-history: ## Copy Allure history for trend analysis
	@if [ -d "reports/allure-report/history" ]; then \
		cp -r reports/allure-report/history/* reports/allure-results/history/ 2>/dev/null || true; \
		echo "Allure history copied for trend analysis"; \
	else \
		echo "No previous Allure history found"; \
	fi

allure-clean: ## Clean Allure reports and results
	rm -rf reports/allure-results/
	rm -rf reports/allure-report/
	@echo "Allure reports cleaned"

allure-docker-serve: allure-results ## Serve Allure report using Docker
	docker run -p 5050:5050 -v $(PWD)/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest

allure-docker-generate: allure-results ## Generate Allure report using Docker
	docker run -v $(PWD)/reports/allure-results:/app/allure-results -v $(PWD)/reports/allure-report:/app/allure-report frankescobar/allure-docker-service:latest allure generate /app/allure-results /app/allure-report

# Enhanced reporting with Allure
report-allure: allure-generate ## Generate comprehensive Allure report
	@echo "Allure report generated in reports/allure-report/"
	@echo "Run 'make allure-serve' to view the report locally"

report-comprehensive: ## Generate all types of reports (Coverage, Allure)
	. .venv/bin/activate && pytest --cov=ai_rulesets --cov-report=html --cov-report=xml --alluredir=reports/allure-results
	@if command -v allure >/dev/null 2>&1; then \
		allure generate reports/allure-results --clean -o reports/allure-report; \
		echo "Comprehensive reports generated:"; \
		echo "  - Coverage: htmlcov/"; \
		echo "  - Allure: reports/allure-report/"; \
	else \
		echo "Allure not available, but other reports generated"; \
	fi

# Cleanup
clean: ## Clean up generated files and caches
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf reports/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Development Workflow
dev-test: format lint type-check test ## Complete development test workflow

dev-full: clean install-dev format lint type-check test coverage ## Complete development workflow

# Quick Commands
quick-test: ## Quick test run
	. .venv/bin/activate && pytest -v

quick-lint: ## Quick linting check
	ruff check src/ tests/

quick-format: ## Quick code formatting
	black src/ tests/ && isort src/ tests/