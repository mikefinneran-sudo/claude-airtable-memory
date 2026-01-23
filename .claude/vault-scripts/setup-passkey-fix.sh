#!/bin/bash

# Setup script for Google Passkey Disabler
# Installs dependencies and prepares the script to run

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🔧 Setting up Google Passkey Disabler..."
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "📥 Install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check for npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

echo "✅ npm version: $(npm --version)"
echo ""

# Install puppeteer
echo "📦 Installing Puppeteer..."
cd "$SCRIPT_DIR"

# Create package.json if it doesn't exist
if [ ! -f "package.json" ]; then
    cat > package.json <<EOF
{
  "name": "google-passkey-fix",
  "version": "1.0.0",
  "description": "Automated script to disable Google passkey requirement",
  "main": "fix-google-passkeys.js",
  "dependencies": {
    "puppeteer": "^21.5.0"
  }
}
EOF
fi

npm install

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the script:"
echo "   cd $SCRIPT_DIR"
echo "   node fix-google-passkeys.js"
echo ""
echo "📋 What the script will do:"
echo "   1. Open a browser window for you to log in"
echo "   2. Disable 'Skip password when possible' setting"
echo "   3. Delete all passkeys from your account"
echo "   4. Save screenshots of each step"
echo ""
echo "⚠️  IMPORTANT: Have your Google password ready!"
echo ""
