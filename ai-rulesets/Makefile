# AI Test Generation Makefile
# Common development and testing tasks

.PHONY: help venv install install-dev test test-unit test-component test-integration test-e2e clean lint format type-check coverage report-allure allure-results allure-generate allure-serve allure-open allure-history allure-clean allure-docker-serve allure-docker-generate report-comprehensive quality-check quality-readmes quality-workflows quality-tests test-ci

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

# Virtual environment setup
venv: check-python ## Create virtual environment
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		python -m venv .venv; \
		.venv/bin/pip install -U pip; \
	else \
		echo "Virtual environment already exists"; \
	fi

# Installation
install: venv ## Install production dependencies
	.venv/bin/pip install -e .

install-dev: venv ## Install development dependencies
	.venv/bin/pip install -e ".[dev]"

# Testing (local development - uses virtual environment)
test: install-dev ## Run all tests
	.venv/bin/pytest

test-unit: install-dev ## Run unit tests only
	.venv/bin/pytest tests/unit/ -v

test-component: install-dev ## Run component tests only
	.venv/bin/pytest tests/component/ -v

test-integration: install-dev ## Run integration tests only
	.venv/bin/pytest tests/integration/ -v

test-e2e: install-dev ## Run end-to-end tests only
	.venv/bin/pytest tests/e2e/ -v

# CI/CD testing (uses system Python directly)
test-ci: ## Run tests for CI/CD (uses system Python)
	pytest --alluredir=reports/allure-results -v

test-ci-unit: ## Run unit tests for CI/CD
	pytest tests/unit/ -v --alluredir=reports/allure-results

test-ci-component: ## Run component tests for CI/CD
	pytest tests/component/ -v --alluredir=reports/allure-results

test-ci-integration: ## Run integration tests for CI/CD
	pytest tests/integration/ -v --alluredir=reports/allure-results

test-ci-e2e: ## Run e2e tests for CI/CD
	pytest tests/e2e/ -v --alluredir=reports/allure-results

# Code Quality
lint: install-dev ## Run all linting tools
	@echo "Running Black (code formatting)..."
	.venv/bin/black --check src/ tests/
	@echo "Running isort (import sorting)..."
	.venv/bin/isort --check-only src/ tests/
	@echo "Running Ruff (fast linting)..."
	.venv/bin/ruff check src/ tests/

format: install-dev ## Format code with Black and isort
	@echo "Formatting with Black..."
	.venv/bin/black src/ tests/
	@echo "Sorting imports with isort..."
	.venv/bin/isort src/ tests/

type-check: install-dev ## Run type checking with MyPy
	.venv/bin/mypy src/

# Coverage
coverage: install-dev ## Run tests with coverage reporting
	.venv/bin/pytest --cov=ai_rulesets --cov-report=html --cov-report=xml --cov-report=term-missing

coverage-html: install-dev ## Generate HTML coverage report
	.venv/bin/pytest --cov=ai_rulesets --cov-report=html
	@echo "Coverage report generated in htmlcov/"

coverage-xml: install-dev ## Generate XML coverage report
	.venv/bin/pytest --cov=ai_rulesets --cov-report=xml

# Allure Reporting (local development)
allure-results: install-dev ## Generate Allure test results
	.venv/bin/pytest --alluredir=reports/allure-results
	@echo "Allure results generated in reports/allure-results/"

allure-generate: allure-results ## Generate Allure HTML report
	@if command -v allure >/dev/null 2>&1; then \
		allure generate reports/allure-results --clean -o reports/allure-report; \
		echo "Allure report generated in reports/allure-report/"; \
	else \
		echo "Allure command not found. Install with: yarn global add allure-commandline"; \
		echo "Or use Docker: docker run -v $(PWD)/reports/allure-results:/app/allure-results -v $(PWD)/reports/allure-report:/app/allure-report frankescobar/allure-docker-service:latest allure generate /app/allure-results /app/allure-report"; \
	fi

allure-serve: allure-results ## Serve Allure report locally
	@if command -v allure >/dev/null 2>&1; then \
		allure serve reports/allure-results; \
	else \
		echo "Allure command not found. Install with: yarn global add allure-commandline"; \
		echo "Or use Docker: docker run -p 5050:5050 -v $(PWD)/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest"; \
	fi

allure-open: ## Open Allure report in browser (requires allure-generate first)
	@if [ -d "reports/allure-report" ]; then \
		if command -v allure >/dev/null 2>&1; then \
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

report-comprehensive: install-dev ## Generate all types of reports (Coverage, Allure)
	.venv/bin/pytest --cov=ai_rulesets --cov-report=html --cov-report=xml --alluredir=reports/allure-results
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
quick-test: install-dev ## Quick test run
	.venv/bin/pytest -v

quick-lint: install-dev ## Quick linting check
	.venv/bin/ruff check src/ tests/

quick-format: install-dev ## Quick code formatting
	.venv/bin/black src/ tests/ && .venv/bin/isort src/ tests/

# Quality Checks (local development)
quality-check: install-dev ## Run comprehensive code quality checks
	@echo "🔍 Running code quality checks..."
	.venv/bin/python -m ai_rulesets quality check --project-root . --fail-on-error

quality-readmes: install-dev ## Check README files for accuracy
	@echo "📚 Checking README files..."
	.venv/bin/python -m ai_rulesets quality readmes --project-root .

quality-workflows: install-dev ## Check GitHub workflow files
	@echo "⚙️ Checking workflow files..."
	.venv/bin/python -m ai_rulesets quality workflows --project-root .

quality-tests: install-dev ## Check test execution and reporting
	@echo "🧪 Checking test execution..."
	.venv/bin/python -m ai_rulesets quality tests --project-root .