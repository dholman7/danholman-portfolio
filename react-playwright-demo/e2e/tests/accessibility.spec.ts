import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y, getViolations } from 'axe-playwright';

test.describe('Accessibility Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto('/');
    
    // Wait for the page to load completely
    await page.waitForLoadState('networkidle');
    
    // Inject Axe accessibility testing library
    await injectAxe(page);
  });

  test('Homepage should be WCAG 2.1 AA compliant', async ({ page }) => {
    // Check accessibility compliance
    await checkA11y(page, null, {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    });
  });

  test('Registration page should be accessible', async ({ page }) => {
    // Navigate to registration page
    await page.goto('/register');
    await page.waitForLoadState('networkidle');
    
    // Check accessibility compliance
    await checkA11y(page, null, {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    });
  });

  test('Login page should be accessible', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');
    await page.waitForLoadState('networkidle');
    
    // Check accessibility compliance
    await checkA11y(page, null, {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    });
  });

  test('Dashboard should be accessible', async ({ page }) => {
    // Navigate to dashboard (assuming user is logged in)
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    // Check accessibility compliance
    await checkA11y(page, null, {
      detailedReport: true,
      detailedReportOptions: {
        html: true,
      },
    });
  });

  test('Forms should have proper labels and ARIA attributes', async ({ page }) => {
    await page.goto('/register');
    await page.waitForLoadState('networkidle');
    
    // Check specific form elements
    const violations = await getViolations(page, {
      include: ['form', 'input', 'label', 'button', 'select', 'textarea']
    });
    
    expect(violations).toHaveLength(0);
  });

  test('Navigation should be keyboard accessible', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Check navigation elements
    const violations = await getViolations(page, {
      include: ['nav', 'a', 'button'],
      rules: {
        'keyboard-navigation': { enabled: true },
        'tabindex': { enabled: true }
      }
    });
    
    expect(violations).toHaveLength(0);
  });

  test('Images should have alt text', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Check image accessibility
    const violations = await getViolations(page, {
      include: ['img'],
      rules: {
        'image-alt': { enabled: true }
      }
    });
    
    expect(violations).toHaveLength(0);
  });

  test('Color contrast should meet WCAG standards', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Check color contrast
    const violations = await getViolations(page, {
      rules: {
        'color-contrast': { enabled: true }
      }
    });
    
    expect(violations).toHaveLength(0);
  });

  test('Page should have proper heading structure', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Check heading structure
    const violations = await getViolations(page, {
      include: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
      rules: {
        'heading-order': { enabled: true }
      }
    });
    
    expect(violations).toHaveLength(0);
  });

  test('Focus management should be proper', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Check focus management
    const violations = await getViolations(page, {
      rules: {
        'focus-order-semantics': { enabled: true },
        'focusable-no-name': { enabled: true }
      }
    });
    
    expect(violations).toHaveLength(0);
  });
});