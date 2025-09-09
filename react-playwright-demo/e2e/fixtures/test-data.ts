/**
 * Test data fixtures for React Playwright Demo tests
 */

export const testUsers = {
  valid: {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    password: 'password123',
    confirmPassword: 'password123'
  },
  invalid: {
    shortPassword: {
      firstName: 'Jane',
      lastName: 'Smith',
      email: 'jane.smith@example.com',
      password: '123',
      confirmPassword: '123'
    },
    mismatchedPasswords: {
      firstName: 'Bob',
      lastName: 'Johnson',
      email: 'bob.johnson@example.com',
      password: 'password123',
      confirmPassword: 'different123'
    },
    invalidEmail: {
      firstName: 'Alice',
      lastName: 'Brown',
      email: 'invalid-email',
      password: 'password123',
      confirmPassword: 'password123'
    }
  }
};

export const testCredentials = {
  valid: {
    email: 'user@example.com',
    password: 'password123'
  },
  invalid: {
    email: 'invalid@example.com',
    password: 'wrongpassword'
  }
};

export const testSelectors = {
  form: {
    firstName: '[data-testid="first-name-input"]',
    lastName: '[data-testid="last-name-input"]',
    email: '[data-testid="email-input"]',
    password: '[data-testid="password-input"]',
    confirmPassword: '[data-testid="confirm-password-input"]',
    terms: '[data-testid="terms-checkbox"]',
    submit: '[data-testid="submit-button"]',
    toggleMode: '[data-testid="toggle-mode"]',
    togglePassword: '[data-testid="toggle-password"]',
    toggleConfirmPassword: '[data-testid="toggle-confirm-password"]'
  },
  messages: {
    general: '[data-testid="message"]',
    firstNameError: '[data-testid="first-name-error"]',
    lastNameError: '[data-testid="last-name-error"]',
    emailError: '[data-testid="email-error"]',
    passwordError: '[data-testid="password-error"]',
    confirmPasswordError: '[data-testid="confirm-password-error"]',
    termsError: '[data-testid="terms-error"]'
  },
  ui: {
    logo: '[data-testid="tech-logo"]',
    title: 'h1',
    subtitle: 'p'
  }
};

export const testUrls = {
  base: 'http://localhost:5173',
  registration: 'http://localhost:5173',
  login: 'http://localhost:5173'
};
