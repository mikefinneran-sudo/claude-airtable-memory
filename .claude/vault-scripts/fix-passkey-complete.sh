#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Google Passkey Fix - Fully Automated with 1Password       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if 1Password CLI is authenticated
if ! op whoami &>/dev/null; then
    echo "🔐 1Password authentication required..."
    echo ""
    echo "Please authenticate with 1Password (Touch ID or password):"
    echo ""

    # Sign in to 1Password
    eval $(op signin)

    # Check if signin was successful
    if ! op whoami &>/dev/null; then
        echo ""
        echo "❌ 1Password authentication failed"
        echo "Please run 'op signin' manually and try again"
        exit 1
    fi
fi

echo "✅ 1Password authenticated as: $(op whoami)"
echo ""
echo "🚀 Running automated Google passkey fix..."
echo "   Account: mike.finneran@gmail.com"
echo ""
echo "This will:"
echo "  ✓ Log into your Google account automatically"
echo "  ✓ Disable 'Skip password when possible'"
echo "  ✓ Delete ALL passkeys"
echo "  ✓ Save verification screenshots"
echo ""
echo "Press ENTER to continue or Ctrl+C to cancel..."
read

# Run the automated fix
node fix-google-passkeys-auto.js

echo ""
echo "✅ Fix complete!"
echo ""
echo "Next steps:"
echo "  1. Check screenshots in: google-passkey-screenshots/"
echo "  2. Sign out of Google and sign back in to test"
echo "  3. Verify you can log in with password (not passkey)"
echo ""
