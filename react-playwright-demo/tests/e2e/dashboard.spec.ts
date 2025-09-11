import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';

test.describe('Dashboard Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    
    // Register a user to get to the dashboard
    await page.fill('[data-testid="first-name-input"]', 'John');
    await page.fill('[data-testid="last-name-input"]', 'Doe');
    await page.fill('[data-testid="email-input"]', 'john@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.fill('[data-testid="confirm-password-input"]', 'password123');
    await page.check('[data-testid="terms-checkbox"]');
    await page.click('[data-testid="submit-button"]');
    
    // Wait for dashboard to load (this will wait for the form to disappear and dashboard to appear)
    await page.waitForSelector('[data-testid="dashboard-title"]', { timeout: 15000 });
  });

  test('should display dashboard with all elements', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('Dashboard Display');
    await allure.severity('critical');
    
    // Check header elements
    await expect(page.locator('[data-testid="header-logo"]')).toBeVisible();
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="sign-out-button"]')).toBeVisible();
    
    // Check main dashboard content
    await expect(page.locator('[data-testid="dashboard-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="dashboard-description"]')).toBeVisible();
    
    // Check account status cards
    await expect(page.locator('[data-testid="account-status-card"]')).toBeVisible();
    await expect(page.locator('[data-testid="last-login-card"]')).toBeVisible();
    
    // Check quick actions section
    await expect(page.locator('[data-testid="view-profile-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="security-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="support-button"]')).toBeVisible();
    
    // Check demo information
    await expect(page.locator('text=Demo Information')).toBeVisible();
    await expect(page.locator('text=This is a portfolio demonstration of modern authentication flows using React, TypeScript, and Tailwind CSS.')).toBeVisible();
  });

  test('should allow user to sign out', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('Sign Out');
    await allure.severity('high');
    
    // Click sign out button
    await page.click('[data-testid="sign-out-button"]');
    
    // Should return to login/registration form
    await expect(page.locator('[data-testid="form-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    
    // Dashboard elements should not be visible
    await expect(page.locator('[data-testid="dashboard-title"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="welcome-message"]')).not.toBeVisible();
  });

  test('should persist authentication state on page refresh', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('Session Persistence');
    await allure.severity('high');
    
    // Refresh the page
    await page.reload();
    
    // Should still be on dashboard
    await expect(page.locator('[data-testid="dashboard-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="sign-out-button"]')).toBeVisible();
  });

  test('should display user information correctly', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('User Information Display');
    await allure.severity('medium');
    
    // Check that user's first name is displayed
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
    
    // Check that last login time is displayed (should be recent)
    const lastLoginText = await page.locator('[data-testid="last-login-card"]').textContent();
    expect(lastLoginText).toContain('Last Login');
  });

  test('should have interactive quick action buttons', async ({ page }) => {
    await allure.epic('UI/UX');
    await allure.feature('Dashboard');
    await allure.story('Interactive Elements');
    await allure.severity('medium');
    
    // Check that quick action buttons are clickable
    const viewProfileButton = page.locator('[data-testid="view-profile-button"]');
    const securityButton = page.locator('[data-testid="security-button"]');
    const supportButton = page.locator('[data-testid="support-button"]');
    
    await expect(viewProfileButton).toBeVisible();
    await expect(securityButton).toBeVisible();
    await expect(supportButton).toBeVisible();
    
    // Test hover effects (buttons should be interactive)
    await viewProfileButton.hover();
    await securityButton.hover();
    await supportButton.hover();
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    await allure.epic('UI/UX');
    await allure.feature('Dashboard');
    await allure.story('Mobile Responsiveness');
    await allure.severity('high');
    
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Dashboard should still be visible and properly laid out
    await expect(page.locator('[data-testid="dashboard-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="sign-out-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="view-profile-button"]')).toBeVisible();
  });

  test('should be responsive on tablet devices', async ({ page }) => {
    await allure.epic('UI/UX');
    await allure.feature('Dashboard');
    await allure.story('Tablet Responsiveness');
    await allure.severity('high');
    
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Dashboard should still be visible and properly laid out
    await expect(page.locator('[data-testid="dashboard-title"]')).toBeVisible();
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="sign-out-button"]')).toBeVisible();
    await expect(page.locator('[data-testid="view-profile-button"]')).toBeVisible();
  });
});
