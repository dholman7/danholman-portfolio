"""
TypeScript coding standards ruleset.
"""

from pathlib import Path
from typing import Optional
from ...core import Ruleset, RulesetMetadata, RulesetItem
from ...renderers import CursorRenderer, CopilotRenderer


class CodingRuleset:
    """TypeScript coding standards ruleset."""
    
    def __init__(self):
        self.metadata = RulesetMetadata(
            name="TypeScript Coding Standards",
            version="1.0.0",
            description="Organizational TypeScript coding standards and best practices",
            categories=["development", "typescript", "coding"],
            tags=["typescript", "coding", "eslint", "prettier", "es6"],
            author="Dan Holman",
            maintainer="engineering@company.com"
        )
        
        self.ruleset = Ruleset(metadata=self.metadata)
        self._load_rules()
    
    def _load_rules(self):
        """Load coding standards rules."""
        
        # Code style rule
        self.ruleset.add_rule(RulesetItem(
            name="Code Style",
            description="TypeScript code style guidelines",
            content="""# Use ESLint and Prettier for code formatting
# Follow Airbnb TypeScript style guide
# Use strict type checking and strict mode
# Leverage modern ES6+ features: arrow functions, destructuring, template literals
# Use meaningful variable and function names
# Implement proper interfaces and type definitions""",
            tags=["style", "formatting", "eslint"],
            priority=1,
            category="code-quality"
        ))
        
        # Type safety rule
        self.ruleset.add_rule(RulesetItem(
            name="Type Safety",
            description="TypeScript type safety best practices",
            content="""# Use strict type checking
# Define interfaces for object shapes
# Use union types and type guards
# Leverage generics for reusable components
# Use enums for constants and configuration
# Implement proper error handling with Result types

interface User {
  id: number;
  name: string;
  email: string;
}

type Result<T, E> = Success<T> | Error<E>;

class Success<T> {
  constructor(public value: T) {}
}

class Error<E> {
  constructor(public error: E) {}
}""",
            tags=["types", "interfaces", "generics"],
            priority=1,
            category="type-safety"
        ))
        
        # Modern ES6+ rule
        self.ruleset.add_rule(RulesetItem(
            name="Modern ES6+",
            description="Modern JavaScript/TypeScript patterns",
            content="""# Use const for immutable values, let for mutable values
# Prefer arrow functions for short functions
# Use template literals for string interpolation
# Implement proper destructuring for objects and arrays
# Use spread operator for array/object operations
# Use async/await instead of Promises chains

// Arrow functions
const add = (a: number, b: number): number => a + b;

// Template literals
const message = `Hello, ${user.name}!`;

// Destructuring
const { id, name, email } = user;

// Spread operator
const newArray = [...oldArray, newItem];
const newObject = { ...oldObject, newProperty: value };

// Async/await
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}""",
            tags=["es6", "modern", "async"],
            priority=2,
            category="modern-patterns"
        ))
    
    def apply(self, output_dir: str = ".cursor/rules", format: str = "cursor"):
        """Apply the coding ruleset to the specified output directory."""
        output_path = Path(output_dir)
        
        if format == "cursor":
            renderer = CursorRenderer()
            filename = "typescript-coding-standards.mdc"
        elif format == "copilot":
            renderer = CopilotRenderer()
            filename = "typescript-coding-standards.instructions.md"
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
