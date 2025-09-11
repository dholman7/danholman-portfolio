# Python Makefile Rules

## Virtual Environment Management

### ❌ WRONG - Don't repeat .venv/bin/activate in every command
```makefile
# BAD - This is not normal practice
test:
	. .venv/bin/activate && pytest

lint:
	. .venv/bin/activate && ruff check .

coverage:
	. .venv/bin/activate && pytest --cov
```

### ✅ CORRECT - Use proper virtual environment setup
```makefile
# GOOD - Set up virtual environment once
.PHONY: venv
venv:
	python -m venv .venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -e ".[dev]"

# GOOD - Use virtual environment Python directly
test: venv
	.venv/bin/pytest

lint: venv
	.venv/bin/ruff check .

coverage: venv
	.venv/bin/pytest --cov

# GOOD - Or use a shell with activated environment
test-with-shell:
	@bash -c "source .venv/bin/activate && pytest"

# GOOD - For CI/CD, use system Python directly
test-ci:
	pytest --alluredir=reports/allure-results
```

## Best Practices

1. **Setup Once**: Create virtual environment in a dedicated target
2. **Use Direct Paths**: Use `.venv/bin/python` or `.venv/bin/pytest` directly
3. **CI/CD Exception**: In GitHub Actions, use system Python directly
4. **Shell Activation**: Only use shell activation for interactive commands
5. **Dependencies**: Always install dependencies in the venv target

## Makefile Structure

```makefile
# Virtual environment setup
.PHONY: venv install install-dev
venv:
	python -m venv .venv

install: venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -e .

install-dev: venv
	.venv/bin/pip install -U pip
	.venv/bin/pip install -e ".[dev]"

# Testing (use direct paths)
.PHONY: test test-unit test-coverage
test: install-dev
	.venv/bin/pytest

test-unit: install-dev
	.venv/bin/pytest tests/unit/

test-coverage: install-dev
	.venv/bin/pytest --cov=src --cov-report=html

# Linting (use direct paths)
.PHONY: lint format
lint: install-dev
	.venv/bin/ruff check src/ tests/
	.venv/bin/black --check src/ tests/

format: install-dev
	.venv/bin/black src/ tests/
	.venv/bin/isort src/ tests/

# CI/CD targets (use system Python)
.PHONY: test-ci
test-ci:
	pytest --alluredir=reports/allure-results -v
```

## GitHub Actions Integration

```yaml
# In GitHub Actions, use system Python directly
- name: Install dependencies
  run: |
    pip install -e ".[dev]"
    pip install allure-pytest allure-python-commons

- name: Run tests
  run: pytest --alluredir=reports/allure-results -v
```

## Tags
- makefile
- virtual-environment
- python
- best-practices
- ci-cd
