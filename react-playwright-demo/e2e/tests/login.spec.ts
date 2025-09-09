import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';

test.describe('User Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Switch to login mode
    await page.click('[data-testid="toggle-mode"]');
  });

  test('should display login form', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Login');
    await allure.story('Login Form Display');
    await allure.severity('critical');
    
    // Check if we're on the login form
    await expect(page.locator('h1')).toContainText('Welcome Back');
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
    
    // Registration fields should not be visible
    await expect(page.locator('[data-testid="first-name-input"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="last-name-input"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-input"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="terms-checkbox"]')).not.toBeVisible();
  });

  test('should show validation errors for empty login form', async ({ page }) => {
    await page.click('[data-testid="submit-button"]');
    
    // Check for validation errors
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });

  test('should show validation error for invalid email format', async ({ page }) => {
    await page.fill('[data-testid="email-input"]', 'invalid-email');
    await page.click('[data-testid="submit-button"]');
    
    await expect(page.locator('[data-testid="email-error"]')).toContainText('Please enter a valid email address');
  });

  test('should show validation error for short password', async ({ page }) => {
    await page.fill('[data-testid="password-input"]', '123');
    await page.click('[data-testid="submit-button"]');
    
    await expect(page.locator('[data-testid="password-error"]')).toContainText('Password must be at least 8 characters');
  });

  test('should attempt login with valid credentials', async ({ page }) => {
    await page.fill('[data-testid="email-input"]', 'john@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    
    await page.click('[data-testid="submit-button"]');
    
    // Wait for loading to complete
    await page.waitForSelector('[data-testid="submit-button"]:not(:disabled)', { timeout: 10000 });
    
    // Check for success or error message (mock API returns random results)
    await expect(page.locator('[data-testid="message"]')).toBeVisible();
  });

  test('should toggle password visibility in login form', async ({ page }) => {
    await page.fill('[data-testid="password-input"]', 'password123');
    
    // Initially password should be hidden
    await expect(page.locator('[data-testid="password-input"]')).toHaveAttribute('type', 'password');
    
    // Click toggle button
    await page.click('[data-testid="toggle-password"]');
    
    // Password should now be visible
    await expect(page.locator('[data-testid="password-input"]')).toHaveAttribute('type', 'text');
  });

  test('should switch back to registration mode', async ({ page }) => {
    // Click toggle mode button
    await page.click('[data-testid="toggle-mode"]');
    
    // Should now be in registration mode
    await expect(page.locator('h1')).toContainText('Create Account');
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
  });
});
