import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';

test.describe('UI Components and Responsiveness', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display all UI elements correctly', async ({ page }) => {
    await allure.epic('UI/UX');
    await allure.feature('UI Components');
    await allure.story('Element Visibility');
    await allure.severity('high');
    
    // Ensure we're in registration mode (not login mode)
    const loginToggle = page.locator('[data-testid="login-toggle"]');
    if (await loginToggle.isVisible()) {
      await loginToggle.click();
    }
    
    // Wait for the form to be in registration mode
    await page.waitForSelector('h1:has-text("Get started with HolmanTech")', { timeout: 5000 });
    
    // Check main branding elements
    await expect(page.locator('h1:has-text("Get started with HolmanTech")')).toBeVisible();
    await expect(page.locator('text=Get started with HolmanTech')).toBeVisible();
    
    // Check logo
    await expect(page.locator('[data-testid="tech-logo"]')).toBeVisible();
    
    // Check form elements
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="terms-checkbox"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
    
    // Check toggle mode button
    await expect(page.locator('[data-testid="toggle-mode"]')).toBeVisible();
    
    // Check feature list on the left side
    await expect(page.locator('text=Secure and reliable platform')).toBeVisible();
    await expect(page.locator('text=24/7 customer support')).toBeVisible();
    await expect(page.locator('text=Advanced analytics dashboard')).toBeVisible();
  });

  test('should have proper form labels', async ({ page }) => {
    await expect(page.locator('[data-testid="first-name-label"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-label"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-label"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-label"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-label"]')).toBeVisible();
  });

  test('should have proper placeholders', async ({ page }) => {
    await expect(page.locator('[data-testid="first-name-input"]')).toHaveAttribute('placeholder', 'John');
    await expect(page.locator('[data-testid="last-name-input"]')).toHaveAttribute('placeholder', 'Doe');
    await expect(page.locator('[data-testid="email-input"]')).toHaveAttribute('placeholder', 'john@example.com');
    await expect(page.locator('[data-testid="password-input"]')).toHaveAttribute('placeholder', 'Enter your password');
    await expect(page.locator('[data-testid="confirm-password-input"]')).toHaveAttribute('placeholder', 'Confirm your password');
  });

  test('should display loading state during form submission', async ({ page }) => {
    // Fill form with valid data
    await page.fill('[data-testid="first-name-input"]', 'John');
    await page.fill('[data-testid="last-name-input"]', 'Doe');
    await page.fill('[data-testid="email-input"]', 'john@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');
    await page.check('[data-testid="terms-checkbox"]');
    
    // Submit form
    await page.click('[data-testid="submit-button"]');
    
    // Check loading state
    await expect(page.locator('[data-testid="submit-button"]')).toContainText('Please wait...');
    await expect(page.locator('[data-testid="submit-button"]')).toBeDisabled();
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Check if form is still visible and properly laid out
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
  });

  test('should have proper focus management', async ({ page }) => {
    // Test that form elements are focusable and interactive
    await page.click('[data-testid="first-name-input"]');
    await expect(page.locator('[data-testid="first-name-input"]')).toBeFocused();
    
    await page.click('[data-testid="last-name-input"]');
    await expect(page.locator('[data-testid="last-name-input"]')).toBeFocused();
    
    await page.click('[data-testid="email-input"]');
    await expect(page.locator('[data-testid="email-input"]')).toBeFocused();
    
    await page.click('[data-testid="password-input"]');
    await expect(page.locator('[data-testid="password-input"]')).toBeFocused();
    
    await page.click('[data-testid="confirm-password-input"]');
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeFocused();
    
    // Test checkbox interaction
    await page.click('[data-testid="terms-checkbox"]');
    await expect(page.locator('[data-testid="terms-checkbox"]')).toBeChecked();
    
    // Test submit button is clickable (don't test focus as buttons behave differently)
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeEnabled();
  });

  test('should handle basic keyboard navigation', async ({ page }) => {
    // Test basic keyboard navigation - focus and type
    await page.locator('[data-testid="first-name-input"]').focus();
    await page.keyboard.type('John');
    
    await page.locator('[data-testid="email-input"]').focus();
    await page.keyboard.type('john@example.com');
    
    // Verify form fields have the correct values
    await expect(page.locator('[data-testid="first-name-input"]')).toHaveValue('John');
    await expect(page.locator('[data-testid="email-input"]')).toHaveValue('john@example.com');
  });
});
