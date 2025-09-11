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
    
    // Ensure we're in registration mode (not login mode)
    const loginToggle = page.locator('[data-testid="login-toggle"]');
    if (await loginToggle.isVisible()) {
      await loginToggle.click();
    }
    
    // Wait for the form to be in registration mode
    await page.waitForSelector('h2:has-text("Create your account")', { timeout: 5000 });
    
    // Check if we're on the registration form - new UI uses h2 for form title
    await expect(page.locator('h2')).toContainText('Create your account');
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="terms-checkbox"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
    
    // Check for new branding elements
    await expect(page.locator('h1:has-text("Get started with HolmanTech")')).toBeVisible();
    await expect(page.locator('[data-testid="tech-logo"]')).toBeVisible();
  });

  test('should show validation errors for empty form submission', async ({ page }) => {
    await page.click('[data-testid="submit-button"]');
    
    // Wait for validation errors to appear
    await page.waitForSelector('[data-testid="first-name-error"]', { timeout: 5000 });
    await page.waitForSelector('[data-testid="last-name-error"]', { timeout: 5000 });
    await page.waitForSelector('[data-testid="email-error"]', { timeout: 5000 });
    await page.waitForSelector('[data-testid="password-error"]', { timeout: 5000 });
    await page.waitForSelector('[data-testid="confirm-password-error"]', { timeout: 5000 });
    await page.waitForSelector('[data-testid="terms-error"]', { timeout: 5000 });
    
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

  test('should successfully register with valid data and show dashboard', async ({ page }) => {
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
    
    // Wait for loading to complete and check for dashboard
    await page.waitForSelector('[data-testid="dashboard-title"]', { timeout: 15000 });
    
    // Check for dashboard elements
    await expect(page.locator('[data-testid="dashboard-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="account-status-card"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-login-card"]')).toBeVisible();
    await expect(page.locator('[data-testid="view-profile-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="sign-out-button"]')).toBeVisible();
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
