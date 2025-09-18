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
    await allure.title('Display login form');
    await allure.description('Verify that the login form displays correctly with all required fields');
    await allure.tag('e2e', 'login', 'form-display');
    
    await allure.step('Step 1: Navigate to login form', async () => {
      await page.goto('/');
      await page.click('[data-testid="toggle-mode"]');
      allure.attachment(await page.screenshot(), 'Login Form Page', 'image/png');
    });
    
    await allure.step('Step 2: Verify login form elements are visible', async () => {
      // Check if we're on the login form - new UI uses h2 for form title
      await expect(page.locator('h2')).toContainText('Welcome back');
      await expect(page.locator('[data-testid="email-input"]')).toBeVisible();
      await expect(page.locator('[data-testid="password-input"]')).toBeVisible();
      await expect(page.locator('[data-testid="submit-button"]')).toBeVisible();
      allure.attachment('Login form elements verified', 'Form Elements Check', 'text/plain');
    });
    
    await allure.step('Step 3: Verify registration fields are hidden', async () => {
      // Registration fields should not be visible
      await expect(page.locator('[data-testid="first-name-input"]')).not.toBeVisible();
      await expect(page.locator('[data-testid="last-name-input"]')).not.toBeVisible();
      await expect(page.locator('[data-testid="confirm-password-input"]')).not.toBeVisible();
      await expect(page.locator('[data-testid="terms-checkbox"]')).not.toBeVisible();
      allure.attachment('Registration fields properly hidden', 'Hidden Fields Check', 'text/plain');
    });
  });

  test('should show validation errors for empty login form', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Login');
    await allure.story('Form Validation');
    await allure.severity('normal');
    await allure.title('Show validation errors for empty login form');
    await allure.description('Verify that validation errors are displayed when submitting empty login form');
    await allure.tag('e2e', 'login', 'validation');
    
    await allure.step('Step 1: Submit empty login form', async () => {
      await page.click('[data-testid="submit-button"]');
      allure.attachment('Empty form submitted', 'Form Submission', 'text/plain');
    });
    
    await allure.step('Step 2: Wait for validation errors to appear', async () => {
      await page.waitForSelector('[data-testid="email-error"]', { timeout: 5000 });
      await page.waitForSelector('[data-testid="password-error"]', { timeout: 5000 });
      allure.attachment('Validation errors appeared', 'Error Display', 'text/plain');
    });
    
    await allure.step('Step 3: Verify validation errors are visible', async () => {
      // Check for validation errors
      await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
      await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
      allure.attachment(await page.screenshot(), 'Validation Errors Displayed', 'image/png');
    });
  });

  test('should show validation error for invalid email format', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Login');
    await allure.story('Form Validation');
    await allure.severity('normal');
    await allure.title('Show validation error for invalid email format');
    await allure.description('Verify that email format validation works correctly');
    await allure.tag('e2e', 'login', 'email-validation');
    
    await allure.step('Step 1: Enter invalid email format', async () => {
      await page.fill('[data-testid="email-input"]', 'invalid-email');
      allure.attachment('Invalid email entered: invalid-email', 'Email Input', 'text/plain');
    });
    
    await allure.step('Step 2: Submit form with invalid email', async () => {
      await page.click('[data-testid="submit-button"]');
      allure.attachment('Form submitted with invalid email', 'Form Submission', 'text/plain');
    });
    
    await allure.step('Step 3: Verify email validation error appears', async () => {
      // Wait for validation error to appear
      await page.waitForSelector('[data-testid="email-error"]', { timeout: 5000 });
      await expect(page.locator('[data-testid="email-error"]')).toContainText('Please enter a valid email address');
      allure.attachment(await page.screenshot(), 'Email Validation Error', 'image/png');
    });
  });

  test('should show validation error for short password', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Login');
    await allure.story('Form Validation');
    await allure.severity('normal');
    await allure.title('Show validation error for short password');
    await allure.description('Verify that password length validation works correctly');
    await allure.tag('e2e', 'login', 'password-validation');
    
    await allure.step('Step 1: Enter short password', async () => {
      await page.fill('[data-testid="password-input"]', '123');
      allure.attachment('Short password entered: 123', 'Password Input', 'text/plain');
    });
    
    await allure.step('Step 2: Submit form with short password', async () => {
      await page.click('[data-testid="submit-button"]');
      allure.attachment('Form submitted with short password', 'Form Submission', 'text/plain');
    });
    
    await allure.step('Step 3: Verify password validation error appears', async () => {
      await expect(page.locator('[data-testid="password-error"]')).toContainText('Password must be at least 8 characters');
      allure.attachment(await page.screenshot(), 'Password Validation Error', 'image/png');
    });
  });

  test('should successfully login with valid credentials and show dashboard', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Login');
    await allure.story('Successful Login');
    await allure.severity('critical');
    await allure.title('Successfully login with valid credentials and show dashboard');
    await allure.description('Verify that users can successfully login and access the dashboard');
    await allure.tag('e2e', 'login', 'successful-login');
    
    await allure.step('Step 1: Enter valid login credentials', async () => {
      await page.fill('[data-testid="email-input"]', 'john@example.com');
      await page.fill('[data-testid="password-input"]', 'password123');
      allure.attachment('Valid credentials entered: john@example.com / password123', 'Login Credentials', 'text/plain');
    });
    
    await allure.step('Step 2: Submit login form', async () => {
      await page.click('[data-testid="submit-button"]');
      allure.attachment('Login form submitted', 'Form Submission', 'text/plain');
    });
    
    await allure.step('Step 3: Wait for dashboard to load', async () => {
      // Wait for loading to complete and check for dashboard
      await page.waitForSelector('[data-testid="dashboard-title"]', { timeout: 10000 });
      allure.attachment('Dashboard loaded successfully', 'Dashboard Load', 'text/plain');
    });
    
    await allure.step('Step 4: Verify dashboard elements are visible', async () => {
      // Check for dashboard elements
      await expect(page.locator('[data-testid="dashboard-title"]')).toBeVisible();
      await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
      await expect(page.locator('[data-testid="account-status-card"]')).toBeVisible();
      await expect(page.locator('[data-testid="last-login-card"]')).toBeVisible();
      await expect(page.locator('[data-testid="view-profile-button"]')).toBeVisible();
      await expect(page.locator('[data-testid="sign-out-button"]')).toBeVisible();
      allure.attachment(await page.screenshot(), 'Dashboard Successfully Displayed', 'image/png');
    });
  });

  test('should switch back to registration mode', async ({ page }) => {
    await allure.epic('User Management');
    await allure.feature('User Login');
    await allure.story('Mode Switching');
    await allure.severity('normal');
    await allure.title('Switch back to registration mode');
    await allure.description('Verify that users can switch between login and registration modes');
    await allure.tag('e2e', 'login', 'mode-switching');
    
    await allure.step('Step 1: Click toggle mode button', async () => {
      // Click toggle mode button
      await page.click('[data-testid="toggle-mode"]');
      allure.attachment('Mode toggle button clicked', 'Mode Toggle', 'text/plain');
    });
    
    await allure.step('Step 2: Verify registration mode is active', async () => {
      // Should now be in registration mode - new UI uses h2 for form title
      await expect(page.locator('h2')).toContainText('Create your account');
      await expect(page.locator('[data-testid="first-name-input"]')).toBeVisible();
      await expect(page.locator('[data-testid="last-name-input"]')).toBeVisible();
      allure.attachment(await page.screenshot(), 'Registration Mode Active', 'image/png');
    });
  });
});
