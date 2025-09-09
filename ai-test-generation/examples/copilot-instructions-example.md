# GitHub Copilot Instructions Example

This example shows how to use the AI Test Generation package to generate GitHub Copilot instructions for your project.

## Installation

```bash
pip install ai-test-generation
```

## Generate GitHub Copilot Instructions

```bash
# Generate all rule sets for GitHub Copilot
ai-test-gen generate copilot --output .github/instructions

# Generate specific test type instructions
ai-test-gen generate copilot --type typescript --type contract --output .github/instructions
```

## Generated Files

After running the command, you'll have files like:
- `.github/instructions/python-pytest-testing-rules.instructions.md`
- `.github/instructions/typescript-jest-testing-rules.instructions.md`
- `.github/instructions/rest-api-testing-rules.instructions.md`
- `.github/instructions/pact-contract-testing-rules.instructions.md`

## Using with GitHub Copilot

1. Place the generated files in `.github/instructions/` in your repository
2. GitHub Copilot will automatically use these instructions when generating code
3. The instructions will guide Copilot to generate tests following best practices

## Example Generated Instruction

Here's what a generated GitHub Copilot instruction might look like:

```markdown
# TypeScript Jest Testing Rules - GitHub Copilot Instructions

Comprehensive rules for generating Jest-based tests with TypeScript

## Supported Languages
- typescript
- javascript

## Supported Frameworks
- jest

## Test Categories
- unit
- integration

---

## Testing Rules and Guidelines

### Test Structure and Organization

Define proper test file structure and organization with TypeScript

```typescript
// Test files should be named *.test.ts or *.spec.ts
// Use describe() blocks to group related tests
// Use it() or test() for individual test cases
// Use TypeScript interfaces for test data types

interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

interface TestData {
  validUser: User;
  invalidUser: Partial<User>;
}

describe('UserService', () => {
  let userService: UserService;
  let testData: TestData;
  
  beforeEach(() => {
    userService = new UserService();
    testData = {
      validUser: { id: 1, name: 'Test User', email: 'test@example.com', role: 'user' },
      invalidUser: { name: '', email: 'invalid' }
    };
  });
  
  describe('createUser', () => {
    it('should create a user with valid data', () => {
      const result = userService.createUser(testData.validUser);
      expect(result).toBeDefined();
      expect(result.id).toBe(1);
      expect(result.name).toBe('Test User');
    });
    
    it('should throw error when creating user with invalid data', () => {
      expect(() => {
        userService.createUser(testData.invalidUser as User);
      }).toThrow('Invalid user data');
    });
  });
});
```

**Related concepts:** structure, organization, typescript, interfaces

---

## Usage Instructions

When generating tests, please follow these rules and guidelines:

1. **Structure**: Follow the test structure patterns defined above
2. **Naming**: Use descriptive test names that explain the expected behavior
3. **Coverage**: Ensure comprehensive test coverage including edge cases
4. **Maintainability**: Write tests that are easy to read, understand, and maintain
5. **Best Practices**: Follow the specific best practices for the chosen framework

## Example Prompts

- "Generate unit tests for this Python function using pytest"
- "Create integration tests for this API endpoint"
- "Write end-to-end tests for this user flow using Playwright"
- "Generate contract tests for this service using Pact"

Remember to adapt these rules to the specific context and requirements of your project.
```

## Benefits

Using these instructions with GitHub Copilot provides:

1. **Consistency**: All generated tests follow the same patterns and conventions
2. **Best Practices**: Tests are generated with industry best practices built-in
3. **Type Safety**: TypeScript tests include proper type definitions
4. **Comprehensive Coverage**: Rules ensure tests cover various scenarios
5. **Maintainability**: Generated tests are easy to read and maintain

## Customization

You can customize the generated instructions by:
1. Editing the generated `.instructions.md` files directly
2. Modifying the source rule sets in the package
3. Creating your own rule sets for specific frameworks or patterns

## Integration with CI/CD

These instructions work well with CI/CD pipelines:
1. Generate instructions as part of your build process
2. Commit the generated files to your repository
3. Use them consistently across your team
4. Update them when your testing patterns evolve
