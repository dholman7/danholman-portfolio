"""
TypeScript testing standards ruleset.
"""

from pathlib import Path
from typing import Optional
from ...core import Ruleset, RulesetMetadata, RulesetItem
from ...renderers import CursorRenderer, CopilotRenderer


class TestingRuleset:
    """TypeScript testing standards ruleset."""
    
    def __init__(self):
        self.metadata = RulesetMetadata(
            name="TypeScript Testing Standards",
            version="1.0.0",
            description="Organizational TypeScript testing guidelines and best practices",
            categories=["development", "typescript", "testing"],
            tags=["typescript", "testing", "jest", "coverage", "mocking"],
            author="Dan Holman",
            maintainer="engineering@company.com"
        )
        
        self.ruleset = Ruleset(metadata=self.metadata)
        self._load_rules()
    
    def _load_rules(self):
        """Load testing standards rules."""
        
        # Jest testing rule
        self.ruleset.add_rule(RulesetItem(
            name="Jest Testing",
            description="Jest testing framework best practices",
            content="""# Use Jest for all testing
# Write descriptive test names that explain behavior
# Use describe() and it() for test organization
# Aim for 80%+ test coverage
# Use proper mocking strategies
# Use snapshots for UI component testing

describe('UserService', () => {
  it('should create a user with valid data', () => {
    // Test implementation
  });

  it('should throw error when creating user with invalid data', () => {
    // Test implementation
  });
});""",
            tags=["jest", "testing", "coverage"],
            priority=1,
            category="testing"
        ))
        
        # Mocking rule
        self.ruleset.add_rule(RulesetItem(
            name="Mocking",
            description="Mocking and test isolation guidelines",
            content="""# Use Jest mocks for external dependencies
# Mock at the boundary of your system
# Use jest.fn() for function mocks
# Use jest.mock() for module mocks
# Verify mock calls when behavior matters

import { jest } from '@jest/globals';

// Mock a function
const mockFetch = jest.fn();
global.fetch = mockFetch;

// Mock a module
jest.mock('../api/client', () => ({
  getData: jest.fn(),
}));

// Verify mock calls
expect(mockFetch).toHaveBeenCalledWith('/api/users');
expect(mockFetch).toHaveBeenCalledTimes(1);""",
            tags=["mocking", "jest", "isolation"],
            priority=2,
            category="testing"
        ))
        
        # TypeScript testing rule
        self.ruleset.add_rule(RulesetItem(
            name="TypeScript Testing",
            description="TypeScript-specific testing patterns",
            content="""# Use proper TypeScript types in tests
# Test type safety and compile-time errors
# Use type assertions when necessary
# Test generic functions with different types
# Use utility types for test data

interface TestUser {
  id: number;
  name: string;
  email: string;
}

const createTestUser = (overrides: Partial<TestUser> = {}): TestUser => ({
  id: 1,
  name: 'Test User',
  email: 'test@example.com',
  ...overrides,
});

// Test generic function
function processData<T>(data: T[]): T[] {
  return data.filter(item => item !== null);
}

describe('processData', () => {
  it('should filter out null values', () => {
    const data = [1, null, 2, null, 3];
    const result = processData(data);
    expect(result).toEqual([1, 2, 3]);
  });
});""",
            tags=["typescript", "types", "generics"],
            priority=2,
            category="testing"
        ))
    
    def apply(self, output_dir: str = ".cursor/rules", format: str = "cursor"):
        """Apply the testing ruleset to the specified output directory."""
        output_path = Path(output_dir)
        
        if format == "cursor":
            renderer = CursorRenderer()
            filename = "typescript-testing-standards.mdc"
        elif format == "copilot":
            renderer = CopilotRenderer()
            filename = "typescript-testing-standards.instructions.md"
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        output_file = output_path / filename
        renderer.render_file(self.ruleset, output_file)
    
    def get_rules(self):
        """Get all rules in this ruleset."""
        return self.ruleset.rules
    
    def get_rules_by_category(self, category: str):
        """Get rules by category."""
        return self.ruleset.get_rules_by_category(category)
