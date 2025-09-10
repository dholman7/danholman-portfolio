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
    
    // Check main branding elements
    await expect(page.locator('text=HolmanTech')).toBeVisible();
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
    await expect(page.locator('label').filter({ hasText: 'First Name' })).toBeVisible();
    await expect(page.locator('label').filter({ hasText: 'Last Name' })).toBeVisible();
    await expect(page.locator('label').filter({ hasText: 'Email Address' })).toBeVisible();
    await expect(page.locator('label').filter({ hasText: 'Password' })).toBeVisible();
    await expect(page.locator('label').filter({ hasText: 'Confirm Password' })).toBeVisible();
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
    await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
  });

  test('should be responsive on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Check if form is still visible and properly laid out
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
  });

  test('should have proper focus management', async ({ page }) => {
    // Tab through form elements
    await page.keyboard.press('Tab'); // First name
    await expect(page.locator('[data-testid="first-name-input"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Last name
    await expect(page.locator('[data-testid="last-name-input"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Email
    await expect(page.locator('[data-testid="email-input"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Password
    await expect(page.locator('[data-testid="password-input"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Confirm password
    await expect(page.locator('[data-testid="confirm-password-input"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Terms checkbox
    await expect(page.locator('[data-testid="terms-checkbox"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Submit button
    await expect(page.locator('[data-testid="submit-button"]')).toBeFocused();
  });

  test('should handle keyboard navigation', async ({ page }) => {
    // Fill form using keyboard navigation
    await page.keyboard.press('Tab');
    await page.keyboard.type('John');
    
    await page.keyboard.press('Tab');
    await page.keyboard.type('Doe');
    
    await page.keyboard.press('Tab');
    await page.keyboard.type('john@example.com');
    
    await page.keyboard.press('Tab');
    await page.keyboard.type('password123');
    
    await page.keyboard.press('Tab');
    await page.keyboard.type('password123');
    
    await page.keyboard.press('Tab');
    await page.keyboard.press('Space'); // Check terms checkbox
    
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter'); // Submit form
    
    // Wait for loading to complete
    await page.waitForSelector('[data-testid="submit-button"]:not(:disabled)', { timeout: 10000 });
    
    // Check for message
    await expect(page.locator('[data-testid="message"]')).toBeVisible();
  });
});
