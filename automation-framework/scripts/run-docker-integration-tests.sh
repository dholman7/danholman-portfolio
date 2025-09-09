#!/bin/bash

# Docker Integration Test Runner Script
# This script runs integration tests in a Docker environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed and running
check_docker() {
    # Check if Docker is installed
    if ! command -v docker > /dev/null 2>&1; then
        print_error "Docker is not installed. Please install Docker first:"
        print_error "  macOS: brew install --cask docker"
        print_error "  Ubuntu/Debian: sudo apt-get install docker.io docker-compose"
        print_error "  Windows: Download Docker Desktop from https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        print_error "  macOS/Windows: Start Docker Desktop"
        print_error "  Linux: sudo systemctl start docker"
        exit 1
    fi
    print_success "Docker is installed and running"
}

# Function to check if docker compose is available
check_docker_compose() {
    if ! docker compose version > /dev/null 2>&1; then
        print_error "docker compose is not available. Please install Docker with Compose support and try again."
        print_error "  macOS: brew install --cask docker"
        print_error "  Ubuntu/Debian: sudo apt-get install docker.io docker-compose-plugin"
        print_error "  Windows: Download Docker Desktop from https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    print_success "docker compose is available"
}

# Function to start services
start_services() {
    print_status "Starting Docker services for integration tests..."
    docker compose up -d mock-api test-db test-redis
    
    print_status "Waiting for services to be ready..."
    sleep 15
    
    # Check if services are healthy
    print_status "Checking service health..."
    
    # Check Mock API
    if curl -f http://localhost:1080/status > /dev/null 2>&1; then
        print_success "Mock API is ready"
    else
        print_warning "Mock API may not be ready yet"
    fi
    
    # Check Database
    if docker compose exec -T test-db pg_isready -U test_user -d test_automation > /dev/null 2>&1; then
        print_success "Test database is ready"
    else
        print_warning "Test database may not be ready yet"
    fi
    
    # Check Redis
    if docker compose exec -T test-redis redis-cli ping > /dev/null 2>&1; then
        print_success "Redis is ready"
    else
        print_warning "Redis may not be ready yet"
    fi
}

# Function to run tests
run_tests() {
    print_status "Running integration tests in Docker..."
    
    # Use pytest-docker.ini configuration
    docker compose up --build test-runner
    
    # Check if tests passed
    if [ $? -eq 0 ]; then
        print_success "Integration tests completed successfully"
    else
        print_error "Integration tests failed"
        return 1
    fi
}

# Function to run tests in development mode
run_tests_dev() {
    print_status "Starting Docker development environment..."
    docker-compose up --build test-dev
}

# Function to stop services
stop_services() {
    print_status "Stopping Docker services..."
    docker-compose down
    print_success "Services stopped"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker environment..."
    docker-compose down -v
    docker system prune -f
    print_success "Cleanup completed"
}

# Function to show logs
show_logs() {
    print_status "Showing Docker integration test logs..."
    docker-compose logs -f test-runner
}

# Function to show service status
show_status() {
    print_status "Docker service status:"
    docker-compose ps
}

# Function to show help
show_help() {
    echo "Docker Integration Test Runner"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start Docker services for integration tests"
    echo "  test        Run integration tests in Docker"
    echo "  test-dev    Run integration tests in Docker with interactive shell"
    echo "  stop        Stop Docker services"
    echo "  restart     Restart Docker services"
    echo "  logs        Show test logs"
    echo "  status      Show service status"
    echo "  cleanup     Clean up Docker environment"
    echo "  full        Run full test cycle (start -> test -> stop)"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 full                    # Run complete test cycle"
    echo "  $0 start                   # Start services only"
    echo "  $0 test                    # Run tests (services must be running)"
    echo "  $0 test-dev                # Run tests in development mode"
    echo "  $0 logs                    # View test logs"
}

# Main script logic
case "${1:-help}" in
    start)
        check_docker
        check_docker_compose
        start_services
        ;;
    test)
        check_docker
        check_docker_compose
        run_tests
        ;;
    test-dev)
        check_docker
        check_docker_compose
        run_tests_dev
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 2
        start_services
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    cleanup)
        cleanup
        ;;
    full)
        check_docker
        check_docker_compose
        start_services
        run_tests
        stop_services
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
