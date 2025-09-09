import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../src/App';

describe('Form Integration Tests', () => {
  beforeEach(() => {
    render(<App />);
  });

  describe('Registration Form Integration', () => {
    it('should complete full registration flow', async () => {
      // Fill out all registration fields
      await userEvent.type(screen.getByTestId('first-name-input'), 'John');
      await userEvent.type(screen.getByTestId('last-name-input'), 'Doe');
      await userEvent.type(screen.getByTestId('email-input'), 'john@example.com');
      await userEvent.type(screen.getByTestId('password-input'), 'password123');
      await userEvent.type(screen.getByTestId('confirm-password-input'), 'password123');
      await userEvent.click(screen.getByTestId('terms-checkbox'));

      // Verify all fields are filled
      expect(screen.getByTestId('first-name-input')).toHaveValue('John');
      expect(screen.getByTestId('last-name-input')).toHaveValue('Doe');
      expect(screen.getByTestId('email-input')).toHaveValue('john@example.com');
      expect(screen.getByTestId('password-input')).toHaveValue('password123');
      expect(screen.getByTestId('confirm-password-input')).toHaveValue('password123');
      expect(screen.getByTestId('terms-checkbox')).toBeChecked();

      // Submit the form
      await userEvent.click(screen.getByTestId('submit-button'));

      // The form should show loading state (button disabled)
      expect(screen.getByTestId('submit-button')).toBeDisabled();
    });

    it('should handle form validation errors', async () => {
      // Try to submit empty form
      await userEvent.click(screen.getByTestId('submit-button'));

      // Should show validation errors
      await waitFor(() => {
        expect(screen.getByTestId('first-name-error')).toBeInTheDocument();
        expect(screen.getByTestId('email-error')).toBeInTheDocument();
        expect(screen.getByTestId('password-error')).toBeInTheDocument();
        expect(screen.getByTestId('terms-error')).toBeInTheDocument();
      });
    });

    it('should clear form when switching between modes', async () => {
      // Fill out registration form
      await userEvent.type(screen.getByTestId('first-name-input'), 'John');
      await userEvent.type(screen.getByTestId('email-input'), 'john@example.com');

      // Switch to login mode
      await userEvent.click(screen.getByTestId('toggle-mode'));

      // Switch back to registration mode
      await userEvent.click(screen.getByTestId('toggle-mode'));

      // Form should be cleared
      expect(screen.getByTestId('first-name-input')).toHaveValue('');
      expect(screen.getByTestId('email-input')).toHaveValue('');
    });
  });

  describe('Login Form Integration', () => {
    beforeEach(async () => {
      // Switch to login mode
      await userEvent.click(screen.getByTestId('toggle-mode'));
    });

    it('should complete login flow', async () => {
      // Fill out login form
      await userEvent.type(screen.getByTestId('email-input'), 'john@example.com');
      await userEvent.type(screen.getByTestId('password-input'), 'password123');

      // Verify fields are filled
      expect(screen.getByTestId('email-input')).toHaveValue('john@example.com');
      expect(screen.getByTestId('password-input')).toHaveValue('password123');

      // Submit the form
      await userEvent.click(screen.getByTestId('submit-button'));

      // Form should be submitted (no validation errors should appear)
      expect(screen.queryByTestId('email-error')).not.toBeInTheDocument();
      expect(screen.queryByTestId('password-error')).not.toBeInTheDocument();
    });

    it('should handle login validation errors', async () => {
      // Try to submit empty login form
      await userEvent.click(screen.getByTestId('submit-button'));

      // Should show validation errors
      await waitFor(() => {
        expect(screen.getByTestId('email-error')).toBeInTheDocument();
        expect(screen.getByTestId('password-error')).toBeInTheDocument();
      });
    });
  });

  describe('Password Visibility Integration', () => {
    it('should toggle password visibility in registration mode', async () => {
      const passwordInput = screen.getByTestId('password-input');
      const confirmPasswordInput = screen.getByTestId('confirm-password-input');
      const togglePassword = screen.getByTestId('toggle-password');
      const toggleConfirmPassword = screen.getByTestId('toggle-confirm-password');

      // Type passwords
      await userEvent.type(passwordInput, 'password123');
      await userEvent.type(confirmPasswordInput, 'password123');

      // Initially hidden
      expect(passwordInput).toHaveAttribute('type', 'password');
      expect(confirmPasswordInput).toHaveAttribute('type', 'password');

      // Toggle password visibility
      await userEvent.click(togglePassword);
      expect(passwordInput).toHaveAttribute('type', 'text');
      expect(confirmPasswordInput).toHaveAttribute('type', 'password');

      // Toggle confirm password visibility
      await userEvent.click(toggleConfirmPassword);
      expect(passwordInput).toHaveAttribute('type', 'text');
      expect(confirmPasswordInput).toHaveAttribute('type', 'text');

      // Toggle back
      await userEvent.click(togglePassword);
      await userEvent.click(toggleConfirmPassword);
      expect(passwordInput).toHaveAttribute('type', 'password');
      expect(confirmPasswordInput).toHaveAttribute('type', 'password');
    });

    it('should toggle password visibility in login mode', async () => {
      // Switch to login mode
      await userEvent.click(screen.getByTestId('toggle-mode'));

      const passwordInput = screen.getByTestId('password-input');
      const togglePassword = screen.getByTestId('toggle-password');

      // Type password
      await userEvent.type(passwordInput, 'password123');

      // Initially hidden
      expect(passwordInput).toHaveAttribute('type', 'password');

      // Toggle visibility
      await userEvent.click(togglePassword);
      expect(passwordInput).toHaveAttribute('type', 'text');

      // Toggle back
      await userEvent.click(togglePassword);
      expect(passwordInput).toHaveAttribute('type', 'password');
    });
  });

  describe('Form State Management', () => {
    it('should maintain form state during interactions', async () => {
      // Fill out form partially
      await userEvent.type(screen.getByTestId('first-name-input'), 'John');
      await userEvent.type(screen.getByTestId('email-input'), 'john@example.com');

      // Toggle password visibility
      await userEvent.click(screen.getByTestId('toggle-password'));

      // Form state should be maintained
      expect(screen.getByTestId('first-name-input')).toHaveValue('John');
      expect(screen.getByTestId('email-input')).toHaveValue('john@example.com');
      expect(screen.getByTestId('password-input')).toHaveAttribute('type', 'text');
    });

    it('should reset form state when switching modes', async () => {
      // Fill out registration form
      await userEvent.type(screen.getByTestId('first-name-input'), 'John');
      await userEvent.type(screen.getByTestId('last-name-input'), 'Doe');
      await userEvent.type(screen.getByTestId('email-input'), 'john@example.com');
      await userEvent.type(screen.getByTestId('password-input'), 'password123');
      await userEvent.click(screen.getByTestId('terms-checkbox'));

      // Switch to login mode
      await userEvent.click(screen.getByTestId('toggle-mode'));

      // Login form should be empty
      expect(screen.getByTestId('email-input')).toHaveValue('');
      expect(screen.getByTestId('password-input')).toHaveValue('');

      // Switch back to registration mode
      await userEvent.click(screen.getByTestId('toggle-mode'));

      // Registration form should be empty
      expect(screen.getByTestId('first-name-input')).toHaveValue('');
      expect(screen.getByTestId('last-name-input')).toHaveValue('');
      expect(screen.getByTestId('email-input')).toHaveValue('');
      expect(screen.getByTestId('password-input')).toHaveValue('');
      expect(screen.getByTestId('terms-checkbox')).not.toBeChecked();
    });
  });
});
