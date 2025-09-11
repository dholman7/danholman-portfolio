#!/bin/bash

# Ensure coverage reports are generated for Python modules
# This script runs unit tests to generate coverage even if other tests fail

echo "🔍 Checking if coverage reports exist..."

if [ ! -d "reports/coverage" ] || [ ! "$(ls -A reports/coverage)" ]; then
    echo "📊 Coverage directory missing or empty, generating from unit tests..."
    
    # Try to generate coverage from unit tests
    if [ -d "tests/unit" ]; then
        echo "Running unit tests to generate coverage..."
        pytest tests/unit/ --cov=src --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml -v || echo "Unit test coverage generation failed"
    elif [ -d "tests" ]; then
        echo "Running all tests to generate coverage..."
        pytest --cov=src --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml -v || echo "Test coverage generation failed"
    else
        echo "No tests directory found, creating placeholder coverage report..."
        mkdir -p reports/coverage
        echo "<!DOCTYPE html><html><head><title>Coverage Report</title></head><body><h1>Coverage Report</h1><p>No tests found to generate coverage.</p></body></html>" > reports/coverage/index.html
    fi
else
    echo "✅ Coverage reports already exist"
fi

echo "📁 Final coverage directory contents:"
ls -la reports/coverage/ || echo "No coverage directory found"

echo "📊 Coverage generation completed"
