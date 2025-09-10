# Allure Integration for AI Rulesets

## Overview

This document provides specific guidance for integrating Allure reporting with the AI Rulesets module. It covers setup, configuration, and advanced usage patterns specific to organizational standards and ruleset generation.

## Quick Start

### 1. Install Dependencies

```bash
cd ai-rulesets
pip install -e ".[dev]"
```

### 2. Generate Test Results

```bash
# Run tests with Allure results
make allure-results

# Or run specific test types
make test-unit
make test-component
make test-integration
```

### 3. View Reports

```bash
# Generate and serve report
make allure-serve

# Or generate static report
make allure-generate
make allure-open
```

## Configuration

### Pytest Configuration

The module is pre-configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = [
    "--alluredir=reports/allure-results",
    # ... other options
]
```

### Allure Properties

Configuration is in `allure.properties`:

```properties
allure.results.directory=reports/allure-results
allure.environment=ai-rulesets
allure.link.issue.pattern=https://github.com/danholman/danholman-portfolio/issues/{}
```

## Test Organization

### Epic and Feature Structure

```python
@allure.epic("AI Test Generation")
@allure.feature("Test Case Generation")
class TestCaseGeneration:
    pass

@allure.epic("AI Test Generation")
@allure.feature("Template Processing")
class TestTemplateProcessing:
    pass

@allure.epic("AI Test Generation")
@allure.feature("Prompt Engineering")
class TestPromptEngineering:
    pass
```

### Story Organization

```python
@allure.story("AI Model Integration")
@allure.story("Test Case Validation")
@allure.story("Template Rendering")
class TestAIIntegration:
    pass
```

## Advanced Patterns

### AI Model Integration

```python
import allure
from src.ai.generator import TestGenerator

@allure.epic("AI Test Generation")
@allure.feature("Test Case Generation")
class TestAIGeneration:
    
    @allure.story("Model Integration")
    @allure.title("Test AI model integration for test generation")
    def test_ai_model_integration(self, test_generator):
        """Test AI model integration for generating test cases."""
        
        with allure.step("Initialize AI model"):
            model_config = {
                "model_name": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            allure.attach(json.dumps(model_config, indent=2), 
                         "Model Configuration", allure.attachment_type.JSON)
        
        with allure.step("Generate test cases"):
            prompt = "Generate test cases for user authentication API"
            generated_tests = test_generator.generate_tests(prompt)
            allure.attach("\n".join(generated_tests), 
                         "Generated Tests", allure.attachment_type.TEXT)
        
        with allure.step("Validate generated tests"):
            assert len(generated_tests) > 0
            assert all("def test_" in test for test in generated_tests)
```

### Template Processing

```python
import allure
from src.templates.processor import TemplateProcessor

@allure.epic("AI Test Generation")
@allure.feature("Template Processing")
class TestTemplateProcessing:
    
    @allure.story("Template Rendering")
    @allure.title("Test template rendering with data")
    def test_template_rendering(self, template_processor):
        """Test template rendering with various data inputs."""
        
        with allure.step("Load template"):
            template = """
def test_&#123;&#123;test_name&#125;&#125;():
    \"\"\"&#123;&#123;test_description&#125;&#125;\"\"\"
    # Test implementation
    assert &#123;&#123;assertion&#125;&#125;
            """.strip()
            allure.attach(template, "Template", allure.attachment_type.TEXT)
        
        with allure.step("Prepare test data"):
            test_data = {
                "test_name": "user_login",
                "test_description": "Test user login functionality",
                "assertion": "user.is_authenticated"
            }
            allure.attach(json.dumps(test_data, indent=2), 
                         "Test Data", allure.attachment_type.JSON)
        
        with allure.step("Render template"):
            rendered_test = template_processor.render(template, test_data)
            allure.attach(rendered_test, "Rendered Test", allure.attachment_type.TEXT)
        
        with allure.step("Validate rendered test"):
            assert "def test_user_login" in rendered_test
            assert "Test user login functionality" in rendered_test
```

### YAML Configuration Processing

```python
import allure
from src.config.yaml_processor import YAMLProcessor

@allure.epic("AI Test Generation")
@allure.feature("Configuration Processing")
class TestYAMLProcessing:
    
    @allure.story("YAML Parsing")
    @allure.title("Test YAML configuration parsing")
    def test_yaml_parsing(self, yaml_processor):
        """Test YAML configuration parsing and validation."""
        
        with allure.step("Load YAML configuration"):
            yaml_config = """
test_suite:
  name: "API Tests"
  description: "Generated API test suite"
  tests:
    - name: "test_get_users"
      method: "GET"
      endpoint: "/api/users"
      expected_status: 200
            """.strip()
            allure.attach(yaml_config, "YAML Configuration", allure.attachment_type.YAML)
        
        with allure.step("Parse YAML"):
            parsed_config = yaml_processor.parse(yaml_config)
            allure.attach(json.dumps(parsed_config, indent=2), 
                         "Parsed Configuration", allure.attachment_type.JSON)
        
        with allure.step("Validate configuration"):
            assert "test_suite" in parsed_config
            assert parsed_config["test_suite"]["name"] == "API Tests"
```

### Prompt Engineering

```python
import allure
from src.prompts.engine import PromptEngine

@allure.epic("AI Test Generation")
@allure.feature("Prompt Engineering")
class TestPromptEngineering:
    
    @allure.story("Prompt Generation")
    @allure.title("Test prompt generation for different test types")
    def test_prompt_generation(self, prompt_engine):
        """Test prompt generation for various test scenarios."""
        
        with allure.step("Generate API test prompt"):
            api_prompt = prompt_engine.generate_api_prompt({
                "endpoint": "/api/users",
                "method": "POST",
                "description": "Create user account"
            })
            allure.attach(api_prompt, "API Test Prompt", allure.attachment_type.TEXT)
        
        with allure.step("Generate UI test prompt"):
            ui_prompt = prompt_engine.generate_ui_prompt({
                "page": "login",
                "action": "user authentication",
                "framework": "pytest"
            })
            allure.attach(ui_prompt, "UI Test Prompt", allure.attachment_type.TEXT)
        
        with allure.step("Validate prompts"):
            assert "API" in api_prompt
            assert "UI" in ui_prompt
            assert "pytest" in ui_prompt
```

## Error Handling and Debugging

### AI Model Errors

```python
import allure
import traceback

def test_ai_model_error_handling():
    """Test error handling for AI model failures."""
    try:
        # AI model operation
        result = ai_model.generate("invalid prompt")
    except Exception as e:
        with allure.step("Capture AI model error"):
            error_info = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "model_status": ai_model.get_status(),
                "traceback": traceback.format_exc()
            }
            allure.attach(json.dumps(error_info, indent=2), 
                         "AI Model Error", allure.attachment_type.JSON)
        raise
```

### Template Processing Errors

```python
import allure

def test_template_error_handling():
    """Test error handling for template processing failures."""
    try:
        # Template processing
        result = template_processor.render("&#123;&#123;invalid_template", {})
    except Exception as e:
        with allure.step("Capture template error"):
            error_info = {
                "error_type": type(e).__name__,
                "error_message": str(e),
                "template": "&#123;&#123;invalid_template",
                "data": {}
            }
            allure.attach(json.dumps(error_info, indent=2), 
                         "Template Error", allure.attachment_type.JSON)
        raise
```

## Performance Monitoring

### Generation Performance

```python
import allure
import time
import psutil

def test_generation_performance():
    """Test performance of AI test generation."""
    
    with allure.step("Measure generation time"):
        start_time = time.time()
        
        # AI generation
        generated_tests = ai_generator.generate_tests("Generate API tests")
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        allure.attach(f"Generation time: {generation_time:.3f} seconds", 
                     "Performance Metrics", allure.attachment_type.TEXT)
    
    with allure.step("Measure memory usage"):
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        allure.attach(f"Memory usage: {memory_usage:.2f} MB", 
                     "Memory Metrics", allure.attachment_type.TEXT)
    
    with allure.step("Validate performance requirements"):
        assert generation_time < 10.0  # Should complete within 10 seconds
        assert memory_usage < 200  # Should use less than 200 MB
```

### Template Processing Performance

```python
import allure
import time

def test_template_performance():
    """Test performance of template processing."""
    
    with allure.step("Measure template processing time"):
        start_time = time.time()
        
        # Template processing
        rendered_tests = template_processor.process_batch(templates, test_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        allure.attach(f"Processing time: {processing_time:.3f} seconds", 
                     "Performance Metrics", allure.attachment_type.TEXT)
    
    with allure.step("Validate performance requirements"):
        assert processing_time < 5.0  # Should complete within 5 seconds
```

## CI/CD Integration

### GitHub Actions

The module automatically generates Allure results in CI:

```yaml
- name: Generate Allure Results
  if: always()
  run: |
    if [ -d tests ] || ls -1 *.py >/dev/null 2>&1; then 
      pytest --alluredir=reports/allure-results || true
    fi

- name: Upload Allure Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: ai-rulesets-allure-results
    path: reports/allure-results/
    retention-days: 30
```

### Local Development

```bash
# Run tests with Allure results
make test

# Generate and view report
make allure-serve

# Clean up
make allure-clean
```

## Best Practices

### 1. AI-Specific Test Organization

- Organize tests by AI functionality (generation, validation, processing)
- Use clear, descriptive test names for AI operations
- Assign appropriate severity levels for AI failures
- Use meaningful tags for AI-specific features

### 2. Data Attachment

- Attach AI model configurations
- Include generated test cases
- Show template processing results
- Provide prompt engineering examples

### 3. Error Handling

- Capture AI model errors with context
- Include template processing failures
- Show validation error details
- Provide debugging information

### 4. Performance Monitoring

- Monitor AI generation times
- Track memory usage during processing
- Validate performance requirements
- Include scalability metrics

### 5. Integration Testing

- Test full AI pipeline
- Validate end-to-end generation
- Include regression testing
- Monitor quality metrics

## Troubleshooting

### Common Issues

1. **AI Model Errors**: Check model configuration and connectivity
2. **Template Processing**: Verify template syntax and data format
3. **YAML Parsing**: Check YAML syntax and structure
4. **Performance Issues**: Monitor resource usage and timeouts

### Debug Commands

```bash
# Check Allure installation
allure --version

# Generate with verbose output
allure generate reports/allure-results --clean -o reports/allure-report --verbose

# Serve with debug information
allure serve reports/allure-results --debug
```

## Examples

See `automation-framework/tests/test_allure_example.py` for comprehensive examples of Allure integration with the automation framework.

## Conclusion

Allure reporting provides powerful visualization and analysis capabilities for the AI test generation module. By following the patterns and practices outlined in this document, you can create comprehensive, informative test reports that help identify issues quickly and provide valuable insights into AI test generation processes.
