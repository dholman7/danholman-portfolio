module.exports = {
  resultsDir: 'allure-results',
  reportDir: 'allure-report',
  categories: [
    {
      name: 'Failed tests',
      matchedStatuses: ['failed']
    },
    {
      name: 'Broken tests',
      matchedStatuses: ['broken']
    },
    {
      name: 'Skipped tests',
      matchedStatuses: ['skipped']
    },
    {
      name: 'Passed tests',
      matchedStatuses: ['passed']
    }
  ],
  executor: {
    name: 'Playwright',
    type: 'playwright',
    buildName: process.env.BUILD_NAME || 'local-build',
    buildUrl: process.env.BUILD_URL || 'http://localhost:5173'
  }
};
