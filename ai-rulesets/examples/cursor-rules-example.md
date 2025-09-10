# Cursor Rules Example

This example shows how to use the AI Test Generation package to generate Cursor rules for your project.

## Installation

```bash
pip install ai-rulesets
```

## Generate Cursor Rules

```bash
# Generate all rule sets for Cursor
ai-test-gen generate cursor --output .cursor/rules

# Generate specific test type rules
ai-test-gen generate cursor --type python --type api --output .cursor/rules
```

## Generated Files

After running the command, you'll have files like:
- `.cursor/rules/python-pytest-testing-rules.mdc`
- `.cursor/rules/typescript-jest-testing-rules.mdc`
- `.cursor/rules/rest-api-testing-rules.mdc`
- `.cursor/rules/pact-contract-testing-rules.mdc`

## Using in Cursor

1. Open Cursor in your project directory
2. The rules will be automatically loaded from `.cursor/rules/`
3. Ask Cursor to generate tests following the rules:

### Example Prompts

- "Generate unit tests for this Python function using pytest"
- "Create integration tests for this API endpoint"
- "Write end-to-end tests for this user flow using Playwright"
- "Generate contract tests for this service using Pact"

## Customizing Rules

You can customize the generated rules by:
1. Editing the generated `.mdc` files directly
2. Modifying the source rule sets in the package
3. Creating your own rule sets

## Example Generated Rule

Here's what a generated Cursor rule might look like:

```markdown
# Python pytest Testing Rules

Comprehensive rules for generating pytest-based tests with modern Python testing practices

## Languages
- python

## Frameworks
- pytest

## Categories
- unit
- integration

---

## Test Structure and Naming

Define proper test file and function structure with descriptive naming

```python
# Test files should be named test_*.py or *_test.py
# Test functions should start with test_
# Use descriptive test names that explain the expected behavior
# Group related tests in classes when appropriate

def test_user_can_login_with_valid_credentials():
    """Test that user can login with valid credentials."""
    pass

def test_user_cannot_login_with_invalid_credentials():
    """Test that user cannot login with invalid credentials."""
    pass

class TestUserService:
    """Test class for UserService functionality."""
    
    def test_create_user_with_valid_data(self):
        """Test creating user with valid data."""
        pass
```

**Tags:** structure, naming, organization

---
```

This rule will help Cursor understand how to generate proper pytest tests for your Python code.
