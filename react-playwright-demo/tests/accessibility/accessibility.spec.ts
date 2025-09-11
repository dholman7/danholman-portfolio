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

  test('Main page should be WCAG 2.1 AA compliant', async ({ page }) => {
    // Check accessibility compliance for the main page only
    await checkA11y(page, null, {
      detailedReport: false, // Reduced reporting for faster execution
      detailedReportOptions: {
        html: false,
      },
    });
  });

  test('Forms should have proper labels and ARIA attributes', async ({ page }) => {
    // Check specific form elements - critical for form accessibility
    const violations = await getViolations(page, {
      include: ['form', 'input', 'label', 'button', 'select', 'textarea']
    });
    
    expect(violations).toHaveLength(0);
  });

  test('Color contrast should meet WCAG standards', async ({ page }) => {
    // Check color contrast - critical for accessibility
    const violations = await getViolations(page, {
      rules: {
        'color-contrast': { enabled: true }
      }
    });
    
    expect(violations).toHaveLength(0);
  });
});