#!/bin/bash

# Fully automated Google passkey fix with 1Password

echo "🔐 Checking 1Password authentication..."

# Check if 1Password CLI is authenticated
if ! op whoami &>/dev/null; then
    echo "❌ 1Password CLI not authenticated"
    echo "Run: op signin"
    exit 1
fi

echo "✅ 1Password authenticated"
echo "🚀 Running automated passkey fix..."
echo ""

node fix-google-passkeys-auto.js

echo ""
echo "✅ Done!"
