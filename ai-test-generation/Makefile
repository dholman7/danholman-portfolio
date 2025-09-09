.PHONY: install lint test test-unit test-component test-integration test-e2e fmt build clean

# Read Python version from .python-version file
PYTHON_VERSION := $(shell cat .python-version 2>/dev/null || echo "3.13.0")

install:
	@echo "Installing with Python $(PYTHON_VERSION)..."
	python$(PYTHON_VERSION) -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

install-dev:
	@echo "Installing development environment with Python $(PYTHON_VERSION)..."
	python$(PYTHON_VERSION) -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt && pip install -e .

lint:
	. .venv/bin/activate && ruff check .

fmt:
	. .venv/bin/activate && black .

test: ## Run all tests
	. .venv/bin/activate && pytest -q

test-unit: ## Run unit tests only
	. .venv/bin/activate && pytest tests/unit/ -v

test-component: ## Run component tests only
	. .venv/bin/activate && pytest tests/component/ -v

test-integration: ## Run integration tests only
	. .venv/bin/activate && pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests only
	. .venv/bin/activate && pytest tests/e2e/ -v

build:
	. .venv/bin/activate && python -m build

clean:
	rm -rf .venv
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Rule generation commands

.PHONY: generate-cursor generate-copilot generate-all list-rules

generate-cursor:
	. .venv/bin/activate && ai-test-gen generate cursor --output .cursor/rules

generate-cursor-python:
	. .venv/bin/activate && ai-test-gen generate cursor --type python --output .cursor/rules

generate-cursor-typescript:
	. .venv/bin/activate && ai-test-gen generate cursor --type typescript --output .cursor/rules

generate-cursor-api:
	. .venv/bin/activate && ai-test-gen generate cursor --type api --output .cursor/rules

generate-cursor-contract:
	. .venv/bin/activate && ai-test-gen generate cursor --type contract --output .cursor/rules

generate-copilot:
	. .venv/bin/activate && ai-test-gen generate copilot --output .github/instructions

generate-copilot-python:
	. .venv/bin/activate && ai-test-gen generate copilot --type python --output .github/instructions

generate-copilot-typescript:
	. .venv/bin/activate && ai-test-gen generate copilot --type typescript --output .github/instructions

generate-copilot-api:
	. .venv/bin/activate && ai-test-gen generate copilot --type api --output .github/instructions

generate-copilot-contract:
	. .venv/bin/activate && ai-test-gen generate copilot --type contract --output .github/instructions

generate-all: generate-cursor generate-copilot

list-rules:
	. .venv/bin/activate && ai-test-gen list-rules

# Development helpers

.PHONY: dev-setup examples check-python

check-python:
	@echo "Checking Python version..."
	@python --version
	@echo "Expected Python version: $(PYTHON_VERSION)"
	@if ! python --version | grep -q "Python $(PYTHON_VERSION)"; then \
		echo "Warning: Python version mismatch. Expected $(PYTHON_VERSION)"; \
		echo "Please run: pyenv install $(PYTHON_VERSION) && pyenv local $(PYTHON_VERSION)"; \
	fi

dev-setup: check-python install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make generate-all' to generate example rules"

examples: generate-all
	@echo "Generated example rules in .cursor/rules and .github/instructions"
	@echo "Check examples/ directory for usage instructions"

# Legacy commands (kept for compatibility)

.PHONY: redacted eval-run

redacted:
	@echo "Legacy redacted command - use 'make generate-all' instead"
	. .venv/bin/activate || true; python3 scripts/redact.py ../ai-private ./redacted

eval-run:
	@echo "Legacy eval-run command - use 'make test' instead"
	@echo "Simulating model output..." > evals/reports/output.txt
	python3 evals/scorers/contains_scoring.py evals/cases/summarize.jsonl evals/reports/output.txt > evals/reports/scores.jsonl
	@echo "Wrote evals/reports/scores.jsonl"
