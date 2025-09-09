.PHONY: install lint test test-coverage test-unit test-component test-integration test-e2e fmt build deploy deploy-stage clean type-check package

# Default target
all: install lint type-check test build

# Install dependencies
install:
	@echo "Installing dependencies..."
	@if command -v yarn >/dev/null 2>&1; then \
		yarn install; \
	else \
		echo "Yarn not found, using npm..."; \
		npm install; \
	fi
	@echo "Dependencies installed successfully."

# Lint code
lint:
	@echo "Linting code..."
	yarn lint
	@echo "Linting completed."

# Format code
fmt:
	@echo "Formatting code..."
	yarn format
	@echo "Code formatted successfully."

# Type check
type-check:
	@echo "Running type check..."
	yarn type-check
	@echo "Type check completed."

# Run tests
test:
	@echo "Running tests..."
	yarn test
	@echo "Tests completed."

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	yarn test:coverage
	@echo "Test coverage completed."

# Run unit tests
test-unit:
	@echo "Running unit tests..."
	yarn test tests/unit/
	@echo "Unit tests completed."

# Run component tests
test-component:
	@echo "Running component tests..."
	yarn test tests/component/
	@echo "Component tests completed."

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	yarn test tests/integration/
	@echo "Integration tests completed."

# Run E2E tests
test-e2e:
	@echo "Running E2E tests..."
	yarn test tests/e2e/
	@echo "E2E tests completed."

# Run regression tests
test-regression:
	@echo "Running regression tests..."
	python -m pytest tests/test_regression.py --alluredir=reports/allure-results -v
	@echo "Regression tests completed."

# Allure Reporting
allure-results: ## Generate Allure test results
	@echo "Generating Allure results..."
	mkdir -p reports/allure-results
	python -m pytest tests/test_regression.py --alluredir=reports/allure-results -v
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
		allure serve reports/allure-results --port 5051; \
	else \
		echo "Allure command not found. Install with: npm install -g allure-commandline"; \
		echo "Or use Docker: docker run -p 5051:5050 -v $(PWD)/reports/allure-results:/app/allure-results frankescobar/allure-docker-service:latest"; \
	fi

allure-clean: ## Clean Allure reports and results
	rm -rf reports/allure-results/
	rm -rf reports/allure-report/
	@echo "Allure reports cleaned"

# Build the project
build:
	@echo "Building project..."
	yarn build
	@echo "Build completed."

# Package Lambda functions
package:
	@echo "Packaging Lambda functions..."
	yarn package
	@echo "Packaging completed."

# Deploy to AWS
deploy:
	@echo "Deploying to AWS..."
	yarn deploy
	@echo "Deployment completed."

# Deploy specific stage
deploy-stage:
	@echo "Deploying to stage: $(STAGE)"
	STAGE=$(STAGE) yarn deploy
	@echo "Deployment to $(STAGE) completed."

# Synthesize CloudFormation template
synth:
	@echo "Synthesizing CloudFormation template..."
	yarn cdk:synth
	@echo "Synthesis completed."

# Show differences
diff:
	@echo "Showing differences..."
	yarn cdk:diff
	@echo "Diff completed."

# Destroy stack
destroy:
	@echo "Destroying stack..."
	yarn cdk:destroy
	@echo "Stack destroyed."

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	yarn clean
	@echo "Clean completed."

# Run all checks
check: install lint type-check test
	@echo "All checks completed successfully."

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	@echo "Development setup completed."

# Production build
prod-build: clean install lint type-check test build package
	@echo "Production build completed."

# Help
help:
	@echo "Available targets:"
	@echo "  install       - Install dependencies"
	@echo "  lint          - Lint code"
	@echo "  fmt           - Format code"
	@echo "  type-check    - Run TypeScript type check"
	@echo "  test          - Run tests"
	@echo "  test-coverage - Run tests with coverage"
	@echo "  test-unit     - Run unit tests"
	@echo "  test-component - Run component tests"
	@echo "  test-integration - Run integration tests"
	@echo "  test-e2e      - Run E2E tests"
	@echo "  build         - Build the project"
	@echo "  package       - Package Lambda functions"
	@echo "  deploy        - Deploy to AWS"
	@echo "  deploy-stage  - Deploy to specific stage (STAGE=dev|staging|prod)"
	@echo "  synth         - Synthesize CloudFormation template"
	@echo "  diff          - Show differences"
	@echo "  destroy       - Destroy stack"
	@echo "  clean         - Clean build artifacts"
	@echo "  check         - Run all checks"
	@echo "  dev-setup     - Set up development environment"
	@echo "  prod-build    - Production build"
	@echo "  help          - Show this help"
