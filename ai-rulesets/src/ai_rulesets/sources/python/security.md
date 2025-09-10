# Python Security Standards

## Security Basics

- Never commit secrets or sensitive data
- Use environment variables for configuration
- Use secure random number generation
- Implement proper authentication and authorization
- Use HTTPS for all external communications
- Follow OWASP security guidelines

## Input Validation

- Validate all inputs at function boundaries
- Use type hints for input validation
- Sanitize user inputs before processing
- Use whitelist validation when possible
- Implement proper error handling for invalid inputs
- Use libraries like pydantic for data validation

```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
```

## Encryption

- Use encryption for sensitive data at rest
- Use secure hashing for passwords (bcrypt, scrypt)
- Use proper key management
- Implement proper session management
- Use secure random number generation
- Follow encryption best practices

```python
import bcrypt
import secrets

# Hash passwords
password = "user_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Generate secure random tokens
secure_token = secrets.token_urlsafe(32)
```

## Dependency Security

- Keep dependencies up to date
- Use security scanning tools (safety, bandit)
- Pin dependency versions
- Review dependency licenses
- Use virtual environments for isolation
- Monitor for security vulnerabilities

```bash
# Use safety to check for known vulnerabilities
pip install safety
safety check

# Use bandit for security linting
pip install bandit
bandit -r src/
```
