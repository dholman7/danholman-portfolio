#!/bin/bash
# Setup script for local Allure testing with history support
# This script sets up Allure commandline and creates necessary directories

set -e

echo "🔧 Setting up local Allure testing environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   - macOS: brew install node"
    echo "   - Ubuntu: sudo apt-get install nodejs npm"
    echo "   - Windows: Download from https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

# Check if Java is installed (required for Allure)
if ! command -v java &> /dev/null; then
    echo "❌ Java is not installed. Allure requires Java 8 or higher."
    echo "Please install Java first:"
    echo "   - macOS: brew install openjdk@11"
    echo "   - Ubuntu: sudo apt-get install openjdk-11-jdk"
    echo "   - Windows: Download from https://adoptium.net/"
    echo ""
    echo "Alternatively, you can use Docker-based Allure:"
    echo "   - Use 'make allure-docker-serve' instead of 'make allure-serve-local'"
    echo "   - Use 'make allure-docker-generate' instead of 'make allure-generate'"
    exit 1
fi

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ "$JAVA_VERSION" -lt 8 ]; then
    echo "❌ Java version $JAVA_VERSION is too old. Allure requires Java 8 or higher."
    echo ""
    echo "Alternatively, you can use Docker-based Allure:"
    echo "   - Use 'make allure-docker-serve' instead of 'make allure-serve-local'"
    echo "   - Use 'make allure-docker-generate' instead of 'make allure-generate'"
    exit 1
fi

# Install Allure commandline globally
echo "📦 Installing Allure commandline..."
yarn global add allure-commandline

# Verify installation
if command -v allure &> /dev/null; then
    echo "✅ Allure commandline installed successfully"
    allure --version
else
    echo "❌ Failed to install Allure commandline"
    exit 1
fi

# Create directories for Allure history
echo "📁 Creating Allure directories..."
mkdir -p allure-history/automation-framework
mkdir -p allure-history/ai-rulesets
mkdir -p allure-history/cloud-native-app

# Create a global Allure configuration
cat > allure-config.yml << 'EOF'
# Global Allure configuration for local development
allure:
  results:
    - automation-framework/reports/allure-results
    - ai-rulesets/reports/allure-results
    - cloud-native-app/reports/allure-results
  report:
    - automation-framework/reports/allure-report
    - ai-rulesets/reports/allure-report
    - cloud-native-app/reports/allure-report
  history:
    - allure-history/automation-framework
    - allure-history/ai-rulesets
    - allure-history/cloud-native-app
EOF

echo "✅ Allure setup completed successfully!"
echo ""
echo "🚀 Next steps:"
echo "1. Run tests with Allure: make test-allure"
echo "2. Serve reports locally: make allure-serve-local"
echo "3. View individual module reports: make allure-serve-single MODULE=<module-name>"
echo ""
echo "📊 Available modules:"
echo "   - automation-framework"
echo "   - ai-rulesets" 
echo "   - cloud-native-app"
