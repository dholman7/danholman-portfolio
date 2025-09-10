# Python Coding Standards

## Code Style

- Use Black for code formatting with 88-character line limit
- Use Ruff for linting and code analysis
- Follow PEP 8 with organizational modifications
- Use type hints extensively for better IDE support
- Use meaningful variable and function names
- Group imports: standard library, third-party, local imports

## Error Handling

- Use context managers for resource cleanup
- Implement custom exception classes for domain-specific errors
- Use try/except/else/finally blocks appropriately
- Log exceptions with full stack traces
- Implement proper error recovery strategies
- Use assertions for debugging and development

## Performance

- Use appropriate data structures for the use case
- Implement proper caching strategies
- Use generators for large datasets
- Optimize database queries and connections
- Implement proper connection pooling
- Use profiling tools to identify bottlenecks

## Code Organization

- Use meaningful module and package names
- Keep functions small and focused on a single responsibility
- Use classes when you have data and behavior together
- Prefer composition over inheritance
- Use dataclasses for simple data containers
- Implement proper `__str__` and `__repr__` methods
