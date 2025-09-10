# Pytest Automation Framework Makefile
# Common development and testing tasks

.PHONY: help install install-dev test test-unit test-component test-integration test-e2e test-api test-ui test-performance clean lint format type-check security-check coverage report docs check-python docker-integration-up docker-integration-down docker-integration-test docker-integration-test-dev docker-integration-logs docker-integration-clean docker-integration-status test-integration-docker test-integration-docker-dev test-integration-docker-clean

# Read Python version from .python-version file
PYTHON_VERSION := $(shell cat .python-version 2>/dev/null || echo "3.11")

# Default target
help: ## Show this help message
	@echo "Pytest Automation Framework - Available Commands:"
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
	pyenv exec python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

install-dev: check-python ## Install development dependencies
	pyenv exec python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[dev,test,api,web,performance]"

install-all: check-python ## Install all dependencies including optional extras
	pyenv exec python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -e ".[all]"

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

test-api: ## Run API tests only
	. .venv/bin/activate && pytest -m "api"

test-ui: ## Run UI tests only
	. .venv/bin/activate && pytest -m "ui"

test-performance: ## Run performance tests only
	. .venv/bin/activate && pytest -m "performance"

test-smoke: ## Run smoke tests only
	. .venv/bin/activate && pytest -m "smoke"

test-regression: ## Run regression tests only
	. .venv/bin/activate && pytest -m "regression"

test-parallel: ## Run tests in parallel (4 workers)
	. .venv/bin/activate && pytest -n 4

test-parallel-max: ## Run tests in parallel with maximum workers
	. .venv/bin/activate && pytest -n auto

test-chrome: ## Run tests with Chrome browser
	. .venv/bin/activate && pytest --browser=chrome

test-firefox: ## Run tests with Firefox browser
	. .venv/bin/activate && pytest --browser=firefox

test-headless: ## Run tests in headless mode
	. .venv/bin/activate && pytest --headless

test-slow: ## Run slow tests (requires --runslow flag)
	. .venv/bin/activate && pytest --runslow

test-flaky: ## Run flaky tests (requires --runflaky flag)
	. .venv/bin/activate && pytest --runflaky

# Test execution with different configurations
test-dev: ## Run tests against dev environment
	. .venv/bin/activate && TEST_ENVIRONMENT=dev pytest

test-staging: ## Run tests against staging environment
	. .venv/bin/activate && TEST_ENVIRONMENT=staging pytest

test-prod: ## Run tests against production environment
	. .venv/bin/activate && TEST_ENVIRONMENT=prod pytest

# Code Quality
lint: ## Run all linting tools
	@echo "Running Black (code formatting)..."
	black --check src/ tests/
	@echo "Running isort (import sorting)..."
	isort --check-only src/ tests/
	@echo "Running Flake8 (linting)..."
	flake8 src/ tests/
	@echo "Running Ruff (fast linting)..."
	ruff check src/ tests/

format: ## Format code with Black and isort
	@echo "Formatting with Black..."
	black src/ tests/
	@echo "Sorting imports with isort..."
	isort src/ tests/

type-check: ## Run type checking with MyPy
	mypy src/

security-check: ## Run security checks
	@echo "Running Bandit (security analysis)..."
	bandit -r src/ -f json -o bandit-report.json
	@echo "Running Safety (dependency security)..."
	safety check --json --output safety-report.json

# Coverage
coverage: ## Run tests with coverage reporting
	. .venv/bin/activate && pytest --cov=src --cov-report=html --cov-report=xml --cov-report=term-missing

coverage-html: ## Generate HTML coverage report
	. .venv/bin/activate && pytest --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/"

coverage-xml: ## Generate XML coverage report
	. .venv/bin/activate && pytest --cov=src --cov-report=xml

# Reporting
report: ## Generate comprehensive test reports
	. .venv/bin/activate && pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml --cov=src --cov-report=html

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

report-comprehensive: ## Generate all types of reports (HTML, JUnit, Coverage, Allure)
	. .venv/bin/activate && pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml --cov=src --cov-report=html --cov-report=xml --alluredir=reports/allure-results
	@if command -v allure >/dev/null 2>&1; then \
		allure generate reports/allure-results --clean -o reports/allure-report; \
		echo "Comprehensive reports generated:"; \
		echo "  - HTML: reports/report.html"; \
		echo "  - JUnit: reports/junit.xml"; \
		echo "  - Coverage: htmlcov/"; \
		echo "  - Allure: reports/allure-report/"; \
	else \
		echo "Allure not available, but other reports generated"; \
	fi

# Data Management
generate-test-data: ## Generate test data using factories
	python -c "from src.data.factories import TestDataManager; tdm = TestDataManager(); data = tdm.generate_test_dataset(100, 50, 200); print('Test data generated successfully')"

clean-test-data: ## Clean generated test data
	rm -rf test_data/generated/

# Database Operations
db-migrate: ## Run database migrations
	alembic upgrade head

db-rollback: ## Rollback database migrations
	alembic downgrade -1

db-reset: ## Reset database (WARNING: destructive)
	alembic downgrade base
	alembic upgrade head

# Docker Operations
docker-build: ## Build Docker image
	docker build -t pytest-automation-framework .

docker-run: ## Run tests in Docker container
	docker run --rm -v $(PWD)/reports:/app/reports pytest-automation-framework

docker-shell: ## Open shell in Docker container
	docker run --rm -it pytest-automation-framework /bin/bash

# Docker Integration Tests
docker-integration-up: ## Start Docker services for integration tests
	docker compose up -d mock-api test-db test-redis
	@echo "Waiting for services to be ready..."
	@sleep 10
	@echo "Services are ready! Run 'make docker-integration-test' to run tests."

docker-integration-down: ## Stop Docker services for integration tests
	docker compose down

docker-integration-test: ## Run integration tests in Docker environment
	docker compose up --build test-runner

docker-integration-test-dev: ## Run integration tests in Docker with interactive shell
	docker compose up --build test-dev

docker-integration-logs: ## View logs from Docker integration tests
	docker compose logs -f test-runner

docker-integration-clean: ## Clean up Docker integration test environment
	docker compose down -v
	docker system prune -f

docker-integration-status: ## Check status of Docker integration services
	docker compose ps

# Integration Test Commands (Docker-based)
test-integration-docker: docker-integration-up docker-integration-test docker-integration-down ## Run integration tests using Docker (recommended)

test-integration-docker-dev: docker-integration-up docker-integration-test-dev ## Run integration tests in Docker with interactive shell

test-integration-docker-clean: docker-integration-clean ## Clean up Docker integration test environment

# Environment Setup
setup-env: ## Set up environment files
	cp .env.example .env
	@echo "Environment file created. Please edit .env with your configuration."

setup-pre-commit: ## Set up pre-commit hooks
	pre-commit install

setup-dev: install-dev setup-env setup-pre-commit ## Complete development setup

# Cleanup
clean: ## Clean up generated files and caches
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf reports/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf junit.xml
	rm -rf bandit-report.json
	rm -rf safety-report.json
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean clean-test-data ## Clean everything including test data

# Documentation
# Documentation is now located in .cursor/rules/ directory

# Performance Analysis
profile: ## Run performance profiling
	. .venv/bin/activate && pytest --profile --profile-svg

benchmark: ## Run benchmark tests
	. .venv/bin/activate && pytest --benchmark-only --benchmark-sort=mean

# Test Data Generation
data-users: ## Generate user test data
	python -c "from src.data.factories import UserFactory; users = UserFactory.create_users(100); print(f'Generated {len(users)} users')"

data-products: ## Generate product test data
	python -c "from src.data.factories import ProductFactory; products = ProductFactory.create_products(50); print(f'Generated {len(products)} products')"

data-orders: ## Generate order test data
	python -c "from src.data.factories import OrderFactory, UserFactory; users = UserFactory.create_users(10); orders = OrderFactory.create_orders([u.email for u in users]); print(f'Generated {len(orders)} orders')"

# Monitoring and Observability
monitor: ## Start monitoring dashboard
	@echo "Starting monitoring dashboard..."
	@echo "Access at http://localhost:3000"

logs: ## View test logs
	tail -f logs/tests.log

# CI/CD Helpers
ci-test: ## Run tests for CI environment
	. .venv/bin/activate && pytest --html=reports/ci-report.html --self-contained-html --junitxml=reports/ci-junit.xml --cov=src --cov-report=xml

ci-lint: ## Run linting for CI environment
	black --check src/ tests/
	isort --check-only src/ tests/
	flake8 src/ tests/
	ruff check src/ tests/
	mypy src/

# Release Management
version: ## Show current version
	python -c "import src; print(src.__version__)"

bump-version: ## Bump version (usage: make bump-version VERSION=1.1.0)
	@if [ -z "$(VERSION)" ]; then echo "Usage: make bump-version VERSION=1.1.0"; exit 1; fi
	sed -i "s/version = \".*\"/version = \"$(VERSION)\"/" pyproject.toml
	sed -i "s/__version__ = \".*\"/__version__ = \"$(VERSION)\"/" src/__init__.py

# Help and Information
info: ## Show framework information
	@echo "Pytest Automation Framework"
	@echo "Version: $(shell python -c 'import src; print(src.__version__)')"
	@echo "Python: $(shell python --version)"
	@echo "Pytest: $(shell pytest --version)"
	@echo "Selenium: $(shell python -c 'import selenium; print(selenium.__version__)')"

status: ## Show test status and statistics
	@echo "Test Statistics:"
	@. .venv/bin/activate && pytest --collect-only -q | grep -c "test session starts" || true
	@echo "Coverage Status:"
	@if [ -f .coverage ]; then coverage report --show-missing; else echo "No coverage data found. Run 'make coverage' first."; fi

# Development Workflow
dev-test: format lint type-check test ## Complete development test workflow

dev-full: clean install-dev format lint type-check security-check test coverage ## Complete development workflow

# Quick Commands
quick-test: ## Quick test run (smoke tests only)
	. .venv/bin/activate && pytest -m "smoke" -v

quick-lint: ## Quick linting check
	ruff check src/ tests/

quick-format: ## Quick code formatting
	black src/ tests/ && isort src/ tests/