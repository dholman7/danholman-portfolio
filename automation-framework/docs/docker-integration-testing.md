# Docker Integration Testing

This document describes how to run integration tests using Docker containers for the automation framework.

## Overview

The Docker integration testing setup provides a complete isolated environment for running integration tests, including:

- **Mock API Server**: MockServer for API endpoint mocking
- **Test Database**: PostgreSQL database for data persistence testing
- **Redis Cache**: Redis for caching and session testing
- **Test Runner**: Containerized test execution environment

## Quick Start

### Prerequisites

- **Docker and Docker Compose** (required)
  ```bash
  # macOS
  brew install --cask docker
  
  # Ubuntu/Debian
  sudo apt-get update
  sudo apt-get install docker.io docker-compose
  
  # Windows
  # Download Docker Desktop from https://www.docker.com/products/docker-desktop
  
  # Verify installation
  docker --version
  docker-compose --version
  ```
- **Python 3.13** (for local development)

### Running Integration Tests

```bash
# Run complete test cycle (recommended)
make test-integration-docker

# Or use the script directly
./scripts/run-docker-integration-tests.sh full
```

### Development Mode

```bash
# Start services and get interactive shell
make test-integration-docker-dev

# Or use the script
./scripts/run-docker-integration-tests.sh test-dev
```

## Available Commands

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make docker-integration-up` | Start Docker services |
| `make docker-integration-down` | Stop Docker services |
| `make docker-integration-test` | Run integration tests |
| `make docker-integration-test-dev` | Run tests in development mode |
| `make docker-integration-logs` | View test logs |
| `make docker-integration-clean` | Clean up environment |
| `make docker-integration-status` | Check service status |

### Script Commands

```bash
./scripts/run-docker-integration-tests.sh [COMMAND]
```

| Command | Description |
|---------|-------------|
| `start` | Start Docker services |
| `test` | Run integration tests |
| `test-dev` | Run tests in development mode |
| `stop` | Stop Docker services |
| `restart` | Restart services |
| `logs` | Show test logs |
| `status` | Show service status |
| `cleanup` | Clean up environment |
| `full` | Complete test cycle |
| `help` | Show help |

## Service Configuration

### Mock API Server
- **Port**: 1080
- **URL**: http://localhost:1080
- **Purpose**: Mock REST API and GraphQL endpoints
- **Expectations**: Located in `test_data/mock-expectations/`

### Test Database
- **Port**: 5433
- **Database**: test_automation
- **User**: test_user
- **Password**: test_password
- **Purpose**: Data persistence testing

### Redis Cache
- **Port**: 6380
- **Purpose**: Caching and session testing

## Test Configuration

### Environment Variables

The Docker environment sets the following variables:

```bash
TEST_ENVIRONMENT=docker
API_BASE_URL=http://mock-api:1080
DATABASE_URL=postgresql://test_user:test_password@test-db:5432/test_automation
REDIS_URL=redis://test-redis:6379
BROWSER=chrome
HEADLESS=true
PYTEST_TIMEOUT=300
PYTEST_MAX_FAIL=5
```

### Pytest Configuration

Docker integration tests use `pytest-docker.ini` which includes:

- Timeout settings for containerized execution
- Docker-specific markers
- Enhanced logging and reporting
- Service health checks

## Mock API Setup

### REST API Endpoints

The MockServer provides the following endpoints:

- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
- `GET /api/products` - List products
- `POST /api/products` - Create product
- `GET /api/products/{id}` - Get product by ID
- `PATCH /api/products/{id}` - Update product
- `POST /api/orders` - Create order
- `GET /api/users/{id}/orders` - Get user orders
- `PATCH /api/orders/{id}` - Update order status

### GraphQL Endpoints

- `POST /graphql` - GraphQL queries and mutations

### Mock Expectations

Mock expectations are defined in JSON files:

- `test_data/mock-expectations/users.json` - User API mocks
- `test_data/mock-expectations/products.json` - Product API mocks
- `test_data/mock-expectations/orders.json` - Order API mocks
- `test_data/mock-expectations/graphql.json` - GraphQL mocks

## Database Schema

The test database includes the following tables:

- `users` - User information
- `products` - Product catalog
- `orders` - Order management

Sample data is automatically loaded during database initialization.

## Test Execution

### Running Specific Tests

```bash
# Run only API tests
docker-compose exec test-runner pytest -m "api" -v

# Run only smoke tests
docker-compose exec test-runner pytest -m "smoke" -v

# Run specific test file
docker-compose exec test-runner pytest tests/integration/test_api_examples.py -v
```

### Debugging Tests

```bash
# Start development environment
make test-integration-docker-dev

# Inside the container, run tests with debugging
pytest tests/integration/test_api_examples.py::TestUserAPI::test_create_user -v -s --tb=long
```

## Troubleshooting

### Common Issues

1. **Docker not installed or not running**
   ```bash
   # Check if Docker is installed
   docker --version
   
   # Check if Docker is running
   docker info
   
   # Start Docker Desktop (macOS/Windows)
   # Or start Docker service (Linux)
   sudo systemctl start docker
   ```

2. **Services not starting**
   ```bash
   # Check Docker status
   docker-compose ps
   
   # View service logs
   docker-compose logs mock-api
   docker-compose logs test-db
   docker-compose logs test-redis
   ```

2. **Tests failing to connect to services**
   ```bash
   # Check service health
   curl http://localhost:1080/status
   
   # Check database connection
   docker-compose exec test-db pg_isready -U test_user -d test_automation
   
   # Check Redis connection
   docker-compose exec test-redis redis-cli ping
   ```

3. **Port conflicts**
   ```bash
   # Check if ports are in use
   lsof -i :1080
   lsof -i :5433
   lsof -i :6380
   
   # Stop conflicting services or change ports in docker-compose.yml
   ```

### Cleanup

```bash
# Clean up everything
make docker-integration-clean

# Or manually
docker-compose down -v
docker system prune -f
```

## Best Practices

1. **Always use Docker for integration tests** - This ensures consistent, isolated test environments
2. **Use the provided scripts** - They handle service health checks and proper sequencing
3. **Clean up after testing** - Run cleanup commands to free up resources
4. **Check service status** - Use status commands to verify services are running
5. **Use development mode for debugging** - Interactive shell access for troubleshooting

## Integration with CI/CD

The Docker integration tests can be easily integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Integration Tests
  run: |
    make test-integration-docker
```

## Performance Considerations

- Docker containers add overhead but provide isolation
- Services are started once and reused across test runs
- Use `docker-compose up -d` to run services in background
- Consider resource limits for CI environments

## Security Notes

- Test database uses weak credentials (acceptable for testing)
- Mock API is publicly accessible on localhost
- No production data should be used in test containers
- Clean up containers and volumes after testing
