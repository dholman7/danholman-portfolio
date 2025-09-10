# GitHub Actions Workflows

This directory contains GitHub Actions workflows for the React Playwright Demo module.

## Workflows

### `ci-cd.yml`
Comprehensive CI/CD pipeline that includes:

- **Linting & Type Checking**: ESLint and TypeScript validation
- **Unit Tests**: Jest tests with coverage reporting
- **Integration Tests**: Component integration tests
- **E2E Tests**: Playwright end-to-end tests
- **Build & Package**: Vite build and artifact generation
- **Deploy to GitHub Pages**: Automatic deployment of the built application
- **Allure Reporting**: Test report generation and deployment
- **Cleanup**: Artifact cleanup after deployment

## Triggers

- **Push**: Runs on pushes to `main` and `develop` branches
- **Pull Request**: Runs on PRs targeting `main` and `develop` branches
- **Manual Dispatch**: Can be triggered manually with module selection

## Outputs

- **Application**: Deployed to GitHub Pages at `/react-playwright-demo/`
- **Allure Reports**: Available at `/react-playwright-demo/` (Allure reports)
- **Playwright Reports**: Available as downloadable artifacts

## Integration

This module is also integrated with the main portfolio test suite workflow (`portfolio-test-suite.yml`) and the centralized Allure reports deployment workflow (`deploy-allure-reports.yml`).
