#!/bin/bash

# Setup script for 1Password CLI, CleanShot X, and Alfred integrations
# For ObsidianVault automation workflow
# Author: Mike Finneran
# Date: 2025-10-27

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Vault directory
VAULT_DIR="/Users/mikefinneran/Documents/ObsidianVault"
SCRIPTS_DIR="${VAULT_DIR}/.scripts"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   ObsidianVault Tools Integration Setup              ║${NC}"
echo -e "${BLUE}║   1Password CLI + CleanShot X + Alfred                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if app is installed
app_installed() {
    [ -d "/Applications/$1.app" ]
}

echo -e "${YELLOW}[1/3] Checking installations...${NC}"
echo ""

# Check 1Password CLI
echo -n "  1Password CLI: "
if command_exists op; then
    echo -e "${GREEN}✓ Installed${NC}"
    OP_VERSION=$(op --version)
    echo "    Version: ${OP_VERSION}"
    OP_INSTALLED=true
else
    echo -e "${RED}✗ Not installed${NC}"
    echo "    Install: brew install --cask 1password-cli"
    OP_INSTALLED=false
fi
echo ""

# Check 1Password App
echo -n "  1Password App: "
if app_installed "1Password"; then
    echo -e "${GREEN}✓ Installed${NC}"
    OP_APP_INSTALLED=true
else
    echo -e "${RED}✗ Not installed${NC}"
    echo "    Install: brew install --cask 1password"
    OP_APP_INSTALLED=false
fi
echo ""

# Check CleanShot X
echo -n "  CleanShot X: "
if app_installed "CleanShot X"; then
    echo -e "${GREEN}✓ Installed${NC}"
    CLEANSHOT_INSTALLED=true
else
    echo -e "${RED}✗ Not installed${NC}"
    echo "    Install: https://cleanshot.com/"
    CLEANSHOT_INSTALLED=false
fi
echo ""

# Check Alfred
echo -n "  Alfred: "
if app_installed "Alfred 5"; then
    echo -e "${GREEN}✓ Installed${NC}"
    ALFRED_INSTALLED=true
elif app_installed "Alfred 4"; then
    echo -e "${GREEN}✓ Installed (v4)${NC}"
    ALFRED_INSTALLED=true
else
    echo -e "${RED}✗ Not installed${NC}"
    echo "    Install: brew install --cask alfred"
    ALFRED_INSTALLED=false
fi
echo ""

# Create necessary directories
echo -e "${YELLOW}[2/3] Setting up directories...${NC}"
echo ""

mkdir -p "${VAULT_DIR}/Resources/Screenshots"
echo -e "  ${GREEN}✓${NC} Created Resources/Screenshots/"

mkdir -p "${VAULT_DIR}/Daily/attachments"
echo -e "  ${GREEN}✓${NC} Created Daily/attachments/"

mkdir -p "${VAULT_DIR}/.integrations/alfred"
echo -e "  ${GREEN}✓${NC} Created .integrations/alfred/"

mkdir -p "${VAULT_DIR}/.integrations/1password"
echo -e "  ${GREEN}✓${NC} Created .integrations/1password/"

echo ""

# Configure 1Password CLI
if [ "$OP_INSTALLED" = true ] && [ "$OP_APP_INSTALLED" = true ]; then
    echo -e "${YELLOW}[3/3] Configuring 1Password CLI...${NC}"
    echo ""

    # Check if already signed in
    if op account list >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} Already signed in to 1Password"
        ACCOUNT=$(op account list | tail -n 1 | awk '{print $2}')
        echo "    Account: ${ACCOUNT}"
    else
        echo "  Setting up 1Password CLI authentication..."
        echo ""
        echo "  ${BLUE}Action Required:${NC}"
        echo "  1. Open 1Password app"
        echo "  2. Go to Settings → Developer"
        echo "  3. Enable '1Password CLI'"
        echo "  4. Use Touch ID when prompted"
        echo ""
        read -p "  Press Enter when ready to sign in..."

        if op signin; then
            echo -e "  ${GREEN}✓${NC} Successfully signed in"
        else
            echo -e "  ${RED}✗${NC} Sign-in failed. Run 'op signin' manually."
        fi
    fi
    echo ""
else
    echo -e "${YELLOW}[3/3] Skipping 1Password configuration (not installed)${NC}"
    echo ""
fi

# Create helper scripts
echo -e "${YELLOW}Creating helper scripts...${NC}"
echo ""

# 1. Screenshot to vault script
cat > "${SCRIPTS_DIR}/capture-screenshot.sh" << 'EOF'
#!/bin/bash
# Capture screenshot to vault with CleanShot X

DATE=$(date +%Y-%m-%d_%H-%M-%S)
SCREENSHOT_DIR="$HOME/Documents/ObsidianVault/Resources/Screenshots"

# Ensure directory exists
mkdir -p "$SCREENSHOT_DIR"

# Trigger CleanShot X area capture
open "cleanshot://capture-area?filepath=${SCREENSHOT_DIR}/screenshot-${DATE}.png"

echo "Screenshot will be saved to: ${SCREENSHOT_DIR}/screenshot-${DATE}.png"
EOF
chmod +x "${SCRIPTS_DIR}/capture-screenshot.sh"
echo -e "  ${GREEN}✓${NC} Created capture-screenshot.sh"

# 2. Get API key from 1Password
cat > "${SCRIPTS_DIR}/get-api-key.sh" << 'EOF'
#!/bin/bash
# Retrieve API key from 1Password CLI

if [ -z "$1" ]; then
    echo "Usage: $0 <item-name>"
    echo "Example: $0 'Anthropic API'"
    exit 1
fi

ITEM_NAME="$1"

if command -v op >/dev/null 2>&1; then
    # Try to read the credential
    if op read "op://Private/${ITEM_NAME}/credential" 2>/dev/null; then
        :
    else
        echo "Error: Could not find item '${ITEM_NAME}' in 1Password vault 'Private'" >&2
        echo "Available vaults:" >&2
        op vault list 2>/dev/null || echo "  (Not signed in)" >&2
        exit 1
    fi
else
    echo "Error: 1Password CLI not installed" >&2
    exit 1
fi
EOF
chmod +x "${SCRIPTS_DIR}/get-api-key.sh"
echo -e "  ${GREEN}✓${NC} Created get-api-key.sh"

# 3. Open vault in Obsidian
cat > "${SCRIPTS_DIR}/open-vault.sh" << 'EOF'
#!/bin/bash
# Open ObsidianVault in Obsidian app

VAULT_PATH="$HOME/Documents/ObsidianVault"

if [ -d "/Applications/Obsidian.app" ]; then
    open -a "Obsidian" "$VAULT_PATH"
else
    echo "Error: Obsidian not installed"
    exit 1
fi
EOF
chmod +x "${SCRIPTS_DIR}/open-vault.sh"
echo -e "  ${GREEN}✓${NC} Created open-vault.sh"

echo ""

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Setup Complete!                                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${GREEN}Helper Scripts Created:${NC}"
echo "  • capture-screenshot.sh - Capture to vault with CleanShot X"
echo "  • get-api-key.sh - Retrieve credentials from 1Password"
echo "  • open-vault.sh - Open vault in Obsidian"
echo ""

echo -e "${GREEN}Next Steps:${NC}"
if [ "$CLEANSHOT_INSTALLED" = true ]; then
    echo "  1. CleanShot X: Set default save location to:"
    echo "     ${VAULT_DIR}/Resources/Screenshots/"
fi

if [ "$OP_INSTALLED" = true ]; then
    echo "  2. 1Password: Store your API keys in 'Private' vault:"
    echo "     - Anthropic API"
    echo "     - Perplexity API"
    echo "     - GitHub Token"
fi

if [ "$ALFRED_INSTALLED" = true ]; then
    echo "  3. Alfred: Import workflows from:"
    echo "     ${VAULT_DIR}/.integrations/alfred/"
fi

echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "  • 1Password Setup: .integrations/1password/SETUP.md"
echo "  • Alfred Workflows: .integrations/alfred/README.md"
echo "  • CleanShot Guide: .integrations/CLEANSHOT-GUIDE.md"
echo ""

echo -e "${YELLOW}Run individual scripts:${NC}"
echo "  ${SCRIPTS_DIR}/capture-screenshot.sh"
echo "  ${SCRIPTS_DIR}/get-api-key.sh 'Anthropic API'"
echo "  ${SCRIPTS_DIR}/open-vault.sh"
echo ""
