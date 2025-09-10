# React Playwright Demo

A modern React TypeScript demo application showcasing registration/sign-up functionality with comprehensive E2E testing using Playwright and Allure reporting.

## 🚀 CI/CD Pipeline

This application demonstrates production-ready CI/CD practices for frontend development:

### **Automated Testing Pipeline**
- **Node.js Testing**: Comprehensive testing with Node.js 20
- **Type Safety Validation**: Comprehensive TypeScript type checking
- **Code Quality Gates**: ESLint, Prettier, and automated formatting
- **E2E Testing**: Cross-browser testing with Playwright
- **Allure Reporting**: Comprehensive test reporting with history

### **Frontend Build Pipeline**
- **Vite Build**: Fast, optimized production builds
- **TypeScript Compilation**: Strict type checking and compilation
- **Asset Optimization**: CSS, JS, and image optimization
- **Bundle Analysis**: Build size and performance monitoring

### **Deployment Automation**
- **PR Preview Deployment**: Automatic preview deployments on pull requests
- **Environment Management**: Proper environment-specific configurations
- **Build Artifact Management**: Optimized build artifact distribution
- **Smoke Testing**: Post-deployment validation and health checks

### **CI/CD Features**
- **Path-based Triggers**: Efficient CI runs based on changed files
- **Artifact Management**: Build artifact collection and distribution
- **Environment Protection**: Proper environment-specific deployment controls
- **Monitoring Integration**: Test result aggregation and reporting

## 🚀 Features

### Core Functionality
- **User Registration**: Complete registration form with validation
- **User Login**: Secure login functionality
- **Form Validation**: Real-time validation using react-hook-form and Zod
- **Responsive Design**: Mobile-first responsive design with Tailwind CSS
- **Modern UI**: Clean, accessible interface with proper form states

### Technical Highlights
- **React 19**: Latest React features with TypeScript
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Form Management**: react-hook-form with Zod validation
- **E2E Testing**: Comprehensive Playwright test suite
- **Allure Reporting**: Detailed test reports with history

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │────│   Vite Dev       │────│   Playwright    │
│   (Frontend)    │    │   Server         │    │   (E2E Tests)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Tailwind CSS  │    │   TypeScript     │    │   Allure        │
│   (Styling)     │    │   (Type Safety)  │    │   (Reporting)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
react-playwright-demo/
├── src/                        # Source Code
│   ├── App.tsx                 # Main React component
│   ├── index.css               # Global styles with Tailwind
│   └── main.tsx                # React entry point
├── e2e/                        # E2E Test Suite
│   ├── tests/                  # Playwright test files
│   │   ├── registration.spec.ts
│   │   ├── login.spec.ts
│   │   └── ui.spec.ts
│   ├── fixtures/               # Test data and utilities
│   │   └── test-data.ts
│   └── utils/                  # Test helper functions
├── public/                     # Static Assets
│   └── tech_logo.png           # Application logo
├── .github/workflows/          # CI/CD Pipeline
│   └── react-playwright-demo.yml
├── package.json                # Dependencies and scripts
├── playwright.config.ts        # Playwright configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── vite.config.ts              # Vite configuration
├── .nvmrc                      # Node.js version specification
└── README.md                   # This file
```

## 🛠️ Tech Stack

### Frontend
- **React 19**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **react-hook-form**: Performant form management
- **Zod**: TypeScript-first schema validation

### Testing
- **Playwright**: Cross-browser E2E testing
- **Allure**: Comprehensive test reporting
- **Jest**: Unit testing (if needed)

### Development
- **ESLint**: Code linting and quality
- **Prettier**: Code formatting
- **GitHub Actions**: CI/CD pipeline

## 🚀 Quick Start

### Prerequisites
- Node.js 20.19+
- npm or yarn package manager
- Git

#### Installing Node.js with nvm
```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload your shell or run:
source ~/.bashrc
# or
source ~/.zshrc

# Install and use the exact Node.js version specified in .nvmrc
nvm install
nvm use
nvm alias default $(cat .nvmrc)

# Verify installation (npm comes bundled with Node.js)
node --version
npm --version
```

**Note**:
- This project includes a `.nvmrc` file specifying Node.js version 20.19.0
- npm comes bundled with Node.js, so no separate installation is needed
- After installing nvm, you can simply run `nvm use` in the project directory to automatically use the correct Node.js version

**Troubleshooting**: If you get "command not found" errors:
```bash
# Make sure nvm is loaded in your current shell
source ~/.bashrc
# or
source ~/.zshrc

# Verify nvm is working
nvm --version

# Reinstall Node.js if needed
nvm uninstall 20.19.0
nvm install 20.19.0
nvm use 20.19.0
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd danholman-portfolio/react-playwright-demo
   ```

2. **Use the correct Node.js version**
   ```bash
   # If using nvm, automatically use the version specified in .nvmrc
   nvm use
   ```

3. **Install dependencies**
   ```bash
   yarn install
   ```

4. **Start development server**
   ```bash
   yarn dev
   ```

5. **Open in browser**
   Navigate to `http://localhost:5173`

### Development

1. **Run type checking**
   ```bash
   yarn type-check
   ```

2. **Run linting**
   ```bash
   yarn lint
   ```

3. **Run tests**
   ```bash
   yarn test
   ```

4. **Build the project**
   ```bash
   yarn build
   ```

## 🧪 Testing

### E2E Tests with Playwright
```bash
# Run all E2E tests
yarn test

# Run tests with UI mode
yarn test:ui

# Run tests in headed mode (see browser)
yarn test:headed

# Debug tests
yarn test:debug
```

### Allure Reporting
```bash
# Run tests and generate Allure report
yarn test:allure

# Generate Allure report only
yarn test:allure:generate

# Open Allure report
yarn test:allure:open
```

### Test Structure
- **Registration Tests**: Form validation, user creation flow
- **Login Tests**: Authentication flow, error handling
- **UI Tests**: Component visibility, responsiveness, accessibility

### Test Coverage
```bash
# Run tests with coverage
yarn test:coverage
```

### Test Types
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows
- **Visual Regression**: Test UI consistency
- **Accessibility**: Test WCAG compliance

## 🚀 Deployment

### GitHub Actions PR Preview
The application automatically deploys to a preview environment on every pull request:

1. **Create a Pull Request**
2. **GitHub Actions** will build and deploy the app
3. **Preview URL** will be available in the PR comments
4. **E2E Tests** will run against the preview environment

### Manual Deployment
```bash
# Build the application
yarn build

# Preview the build locally
yarn preview

# Deploy to your hosting platform
# (e.g., Vercel, Netlify, AWS S3, etc.)
```

## 📚 API Documentation

### Mock API Endpoints
The application uses mock API functions for demonstration:

#### Registration
```typescript
POST /api/register
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "password": "password123",
  "confirmPassword": "password123",
  "terms": true
}
```

#### Login
```typescript
POST /api/login
{
  "email": "john@example.com",
  "password": "password123"
}
```

### Form Validation
- **Email**: Valid email format required
- **Password**: Minimum 8 characters, mixed case, numbers
- **Name**: Required, minimum 2 characters
- **Terms**: Must be accepted

## 🧪 Testing Strategy

### Test Types
- **E2E Tests**: Full user journey testing with Playwright
- **Component Tests**: Individual component testing (if added)
- **Visual Regression**: UI consistency testing
- **Accessibility**: WCAG compliance testing

### Test Data
- **Fixtures**: Centralized test data in `e2e/fixtures/`
- **Mock APIs**: Simulated backend responses
- **Test Users**: Predefined user accounts for testing

### Reporting
- **Allure Reports**: Comprehensive test reporting
- **Screenshots**: Automatic screenshots on failure
- **Videos**: Test execution recordings
- **Traces**: Detailed execution traces

## 🔧 Configuration

### Environment Variables
No environment variables required for local development.

### Playwright Configuration
- **Browsers**: Chrome, Firefox, Safari
- **Viewports**: Mobile, tablet, desktop
- **Base URL**: `http://localhost:5173`
- **Timeout**: 30 seconds default

### Tailwind Configuration
- **Custom Colors**: Primary, secondary, accent colors
- **Responsive**: Mobile-first breakpoints
- **Dark Mode**: Ready for dark mode implementation

## 📊 Monitoring

### Test Metrics
- **Test Execution Time**: Track test performance
- **Pass Rate**: Monitor test stability
- **Flaky Tests**: Identify unstable tests
- **Coverage**: Track test coverage

### CI/CD Metrics
- **Build Time**: Track build performance
- **Deployment Time**: Monitor deployment speed
- **Success Rate**: Track deployment success

## 🔒 Security

### Form Security
- **Input Validation**: Client and server-side validation
- **XSS Protection**: React's built-in XSS protection
- **CSRF Protection**: Ready for CSRF tokens

### Testing Security
- **Test Data**: No sensitive data in tests
- **Mock APIs**: Secure mock implementations
- **Environment Isolation**: Separate test environments

## 🚀 Performance

### Frontend Performance
- **Vite**: Fast build and HMR
- **Code Splitting**: Automatic code splitting
- **Tree Shaking**: Dead code elimination
- **Minification**: Production builds optimized

### Test Performance
- **Parallel Execution**: Tests run in parallel
- **Browser Reuse**: Efficient browser management
- **Selective Testing**: Run only changed tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Development Guidelines
- Follow React best practices
- Write comprehensive tests
- Update documentation
- Follow conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 👨‍💻 Author

**Dan Holman**
- Email: danxholman@gmail.com
- LinkedIn: [linkedin.com/in/danxholman](https://linkedin.com/in/danxholman)
- GitHub: [github.com/dholman7](https://github.com/dholman7)

## 🙏 Acknowledgments

- React team for the excellent frontend framework
- Playwright team for the comprehensive testing tool
- Tailwind CSS team for the utility-first CSS framework
- All open source contributors who made this project possible