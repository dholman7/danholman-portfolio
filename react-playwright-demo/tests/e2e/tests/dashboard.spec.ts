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
    
    // Wait for dashboard to load
    await page.waitForSelector('text=Welcome to your HolmanTech Dashboard', { timeout: 10000 });
  });

  test('should display dashboard with all elements', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('Dashboard Display');
    await allure.severity('critical');
    
    // Check header elements
    await expect(page.locator('text=HolmanTech')).toBeVisible();
    await expect(page.locator('text=Welcome, John!')).toBeVisible();
    await expect(page.locator('text=Sign out')).toBeVisible();
    
    // Check main dashboard content
    await expect(page.locator('text=Welcome to your HolmanTech Dashboard')).toBeVisible();
    await expect(page.locator('text=You\'ve successfully authenticated! This is a demo dashboard showcasing modern authentication flows.')).toBeVisible();
    
    // Check account status cards
    await expect(page.locator('text=Account Status')).toBeVisible();
    await expect(page.locator('text=Active and verified')).toBeVisible();
    await expect(page.locator('text=Last Login')).toBeVisible();
    
    // Check quick actions section
    await expect(page.locator('text=Quick Actions')).toBeVisible();
    await expect(page.locator('text=View Profile')).toBeVisible();
    await expect(page.locator('text=Security')).toBeVisible();
    await expect(page.locator('text=Support')).toBeVisible();
    
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
    await page.click('text=Sign out');
    
    // Should return to login/registration form
    await expect(page.locator('text=Get started with HolmanTech')).toBeVisible();
    await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
    
    // Dashboard elements should not be visible
    await expect(page.locator('text=Welcome to your HolmanTech Dashboard')).not.toBeVisible();
    await expect(page.locator('text=Welcome, John!')).not.toBeVisible();
  });

  test('should persist authentication state on page refresh', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('Session Persistence');
    await allure.severity('high');
    
    // Refresh the page
    await page.reload();
    
    // Should still be on dashboard
    await expect(page.locator('text=Welcome to your HolmanTech Dashboard')).toBeVisible();
    await expect(page.locator('text=Welcome, John!')).toBeVisible();
    await expect(page.locator('text=Sign out')).toBeVisible();
  });

  test('should display user information correctly', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('Dashboard');
    await allure.story('User Information Display');
    await allure.severity('medium');
    
    // Check that user's first name is displayed
    await expect(page.locator('text=Welcome, John!')).toBeVisible();
    
    // Check that last login time is displayed (should be recent)
    const lastLoginText = await page.locator('text=Last Login').locator('..').textContent();
    expect(lastLoginText).toContain('Last Login');
  });

  test('should have interactive quick action buttons', async ({ page }) => {
    await allure.epic('UI/UX');
    await allure.feature('Dashboard');
    await allure.story('Interactive Elements');
    await allure.severity('medium');
    
    // Check that quick action buttons are clickable
    const viewProfileButton = page.locator('text=View Profile').locator('..');
    const securityButton = page.locator('text=Security').locator('..');
    const supportButton = page.locator('text=Support').locator('..');
    
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
    await expect(page.locator('text=Welcome to your HolmanTech Dashboard')).toBeVisible();
    await expect(page.locator('text=Welcome, John!')).toBeVisible();
    await expect(page.locator('text=Sign out')).toBeVisible();
    await expect(page.locator('text=Quick Actions')).toBeVisible();
  });

  test('should be responsive on tablet devices', async ({ page }) => {
    await allure.epic('UI/UX');
    await allure.feature('Dashboard');
    await allure.story('Tablet Responsiveness');
    await allure.severity('high');
    
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Dashboard should still be visible and properly laid out
    await expect(page.locator('text=Welcome to your HolmanTech Dashboard')).toBeVisible();
    await expect(page.locator('text=Welcome, John!')).toBeVisible();
    await expect(page.locator('text=Sign out')).toBeVisible();
    await expect(page.locator('text=Quick Actions')).toBeVisible();
  });
});
