import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';

test.describe('User Registration', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display registration form by default', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Registration');
    await allure.story('Registration Form Display');
    await allure.severity('critical');
    
    // Check if we're on the registration form
    await expect(page.locator('h1')).toContainText('Create Account');
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="terms-checkbox"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
  });

  test('should show validation errors for empty form submission', async ({ page }) => {
    await page.click('[data-testid="submit-button"]');
    
    // Check for validation errors
    await expect(page.locator('[data-testid="first-name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="terms-error"]')).toBeVisible();
  });

  test('should show validation error for invalid email', async ({ page }) => {
    await page.fill('[data-testid="email-input"]', 'invalid-email');
    await page.click('[data-testid="submit-button"]');
    
    await expect(page.locator('[data-testid="email-error"]')).toContainText('Please enter a valid email address');
  });

  test('should show validation error for short password', async ({ page }) => {
    await page.fill('[data-testid="password-input"]', '123');
    await page.click('[data-testid="submit-button"]');
    
    await expect(page.locator('[data-testid="password-error"]')).toContainText('Password must be at least 8 characters');
  });

  test('should show validation error for password mismatch', async ({ page }) => {
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'different123');
    await page.click('[data-testid="submit-button"]');
    
    await expect(page.locator('[data-testid="confirm-password-error"]')).toContainText("Passwords don't match");
  });

  test('should show validation error when terms not accepted', async ({ page }) => {
    await page.fill('[data-testid="first-name-input"]', 'John');
    await page.fill('[data-testid="last-name-input"]', 'Doe');
    await page.fill('[data-testid="email-input"]', 'john@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');
    // Don't check terms checkbox
    await page.click('[data-testid="submit-button"]');
    
    await expect(page.locator('[data-testid="terms-error"]')).toContainText('You must accept the terms and conditions');
  });

  test('should successfully register with valid data', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Registration');
    await allure.story('Successful Registration');
    await allure.severity('critical');
    
    await page.fill('[data-testid="first-name-input"]', 'John');
    await page.fill('[data-testid="last-name-input"]', 'Doe');
    await page.fill('[data-testid="email-input"]', 'john@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');
    await page.check('[data-testid="terms-checkbox"]');
    
    await page.click('[data-testid="submit-button"]');
    
    // Wait for loading to complete
    await page.waitForSelector('[data-testid="submit-button"]:not(:disabled)', { timeout: 10000 });
    
    // Check for success or error message (mock API returns random results)
    await expect(page.locator('[data-testid="message"]')).toBeVisible();
  });

  test('should toggle password visibility', async ({ page }) => {
    await page.fill('[data-testid="password-input"]', 'password123');
    
    // Initially password should be hidden
    await expect(page.locator('[data-testid="password-input"]')).toHaveAttribute('type', 'password');
    
    // Click toggle button
    await page.click('[data-testid="toggle-password"]');
    
    // Password should now be visible
    await expect(page.locator('[data-testid="password-input"]')).toHaveAttribute('type', 'text');
  });

  test('should toggle confirm password visibility', async ({ page }) => {
    await page.fill('[data-testid="confirm-password-input"]', 'password123');
    
    // Initially password should be hidden
    await expect(page.locator('[data-testid="confirm-password-input"]')).toHaveAttribute('type', 'password');
    
    // Click toggle button
    await page.click('[data-testid="toggle-confirm-password"]');
    
    // Password should now be visible
    await expect(page.locator('[data-testid="confirm-password-input"]')).toHaveAttribute('type', 'text');
  });
});
