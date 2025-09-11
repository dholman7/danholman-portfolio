import { render } from '@testing-library/react';
import { screen } from '@testing-library/dom';
import userEvent from '@testing-library/user-event';
import App from '../../src/App';

describe('App Component', () => {
  beforeEach(() => {
    render(<App />);
  });

  describe('Initial Render', () => {
    it('should display the logo', () => {
      const logo = screen.getByTestId('tech-logo');
      expect(logo).toBeInTheDocument();
    });

    it('should display registration form by default', () => {
      expect(screen.getByRole('heading', { name: 'Create your account' })).toBeInTheDocument();
      expect(screen.getByText('Get started with a free account')).toBeInTheDocument();
    });

    it('should display all registration form fields', () => {
      expect(screen.getByTestId('first-name-input')).toBeInTheDocument();
      expect(screen.getByTestId('last-name-input')).toBeInTheDocument();
      expect(screen.getByTestId('email-input')).toBeInTheDocument();
      expect(screen.getByTestId('password-input')).toBeInTheDocument();
      expect(screen.getByTestId('confirm-password-input')).toBeInTheDocument();
      expect(screen.getByTestId('terms-checkbox')).toBeInTheDocument();
      expect(screen.getByTestId('submit-button')).toBeInTheDocument();
    });
  });

  describe('Form Toggle', () => {
    it('should switch to login form when toggle is clicked', async () => {
      const toggleButton = screen.getByTestId('toggle-mode');
      await userEvent.click(toggleButton);

      expect(screen.getByRole('heading', { level: 2, name: 'Welcome back' })).toBeInTheDocument();
      expect(screen.getByText('Sign in to your account')).toBeInTheDocument();
    });

    it('should hide registration fields in login mode', async () => {
      const toggleButton = screen.getByTestId('toggle-mode');
      await userEvent.click(toggleButton);

      expect(screen.queryByTestId('first-name-input')).not.toBeInTheDocument();
      expect(screen.queryByTestId('last-name-input')).not.toBeInTheDocument();
      expect(screen.queryByTestId('confirm-password-input')).not.toBeInTheDocument();
      expect(screen.queryByTestId('terms-checkbox')).not.toBeInTheDocument();
    });
  });

  describe('Password Visibility Toggle', () => {
    it('should toggle password visibility', async () => {
      const passwordInput = screen.getByTestId('password-input');
      const toggleButton = screen.getByTestId('toggle-password');

      await userEvent.type(passwordInput, 'password123');
      
      expect(passwordInput).toHaveAttribute('type', 'password');
      
      await userEvent.click(toggleButton);
      expect(passwordInput).toHaveAttribute('type', 'text');
      
      await userEvent.click(toggleButton);
      expect(passwordInput).toHaveAttribute('type', 'password');
    });
  });

  describe('Form Interaction', () => {
    it('should allow typing in form fields', async () => {
      const firstNameInput = screen.getByTestId('first-name-input');
      const emailInput = screen.getByTestId('email-input');

      await userEvent.type(firstNameInput, 'John');
      await userEvent.type(emailInput, 'john@example.com');

      expect(firstNameInput).toHaveValue('John');
      expect(emailInput).toHaveValue('john@example.com');
    });

    it('should toggle terms checkbox', async () => {
      const termsCheckbox = screen.getByTestId('terms-checkbox');
      
      expect(termsCheckbox).not.toBeChecked();
      
      await userEvent.click(termsCheckbox);
      expect(termsCheckbox).toBeChecked();
      
      await userEvent.click(termsCheckbox);
      expect(termsCheckbox).not.toBeChecked();
    });
  });
});