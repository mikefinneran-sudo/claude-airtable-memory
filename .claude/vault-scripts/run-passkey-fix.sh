#!/bin/bash

# Quick launcher for Google Passkey Fix
# Simply run: ./run-passkey-fix.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$SCRIPT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         Google Passkey Disabler - Ready to Run                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "This script will:"
echo "  1. Open a browser for you to log in"
echo "  2. Disable 'Skip password when possible'"
echo "  3. Delete all passkeys"
echo "  4. Save verification screenshots"
echo ""
echo "⚠️  Have your Google password ready!"
echo ""
echo "Press ENTER to start or Ctrl+C to cancel..."
read

node fix-google-passkeys.js

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                     Fix Complete!                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Screenshots saved to: $SCRIPT_DIR/google-passkey-screenshots"
echo ""
