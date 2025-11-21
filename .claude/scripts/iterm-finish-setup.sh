#!/bin/bash
# iTerm2 Setup - Final Steps Helper
# Guides you through the manual configuration steps

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                iTerm2 Complete Setup - Final Steps             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}Step 1: Restart iTerm2${NC}"
echo "Press Enter to restart iTerm2 now, or Ctrl+C to do it manually later..."
read -r
osascript -e 'quit app "iTerm"'
sleep 1
open -a iTerm
echo -e "${GREEN}✓ iTerm2 restarted${NC}"
echo ""

# Wait for iTerm to start
sleep 2

echo -e "${BLUE}Step 2: Import Triggers${NC}"
echo "Follow these steps:"
echo "  1. Press Cmd+, to open Settings"
echo "  2. Go to: Profiles > Advanced > Triggers"
echo "  3. Click 'Edit' button"
echo "  4. Copy this path to import:"
echo ""
echo -e "${YELLOW}   /tmp/iterm2-triggers.json${NC}"
echo ""
echo "  Or add manually from the file above"
echo ""
echo "Press Enter when done..."
read -r
echo -e "${GREEN}✓ Triggers configured${NC}"
echo ""

echo -e "${BLUE}Step 3: Enable Status Bar${NC}"
echo "Choose your preferred method:"
echo "  A) Via menu: View > Show Status Bar"
echo "  B) Via settings: Cmd+, > Profiles > Session > Check 'Status bar enabled'"
echo ""
echo "Press Enter when done..."
read -r
echo -e "${GREEN}✓ Status bar enabled${NC}"
echo ""

echo -e "${BLUE}Step 4: Test Dynamic Profiles${NC}"
echo "Let's test if profiles are loaded correctly."
echo ""
echo "Press Cmd+O and type 'WalterSignal'"
echo "You should see a profile with a blue 'WS' badge"
echo ""
echo "Press Enter to continue..."
read -r
echo ""

echo -e "${BLUE}Step 5: Test Shell Integration${NC}"
echo "Testing shell integration features..."
echo ""
echo "Run this command in your terminal:"
echo -e "${YELLOW}  echo 'Test 1' && sleep 1 && echo 'Test 2'${NC}"
echo ""
echo "Then try: Cmd+Shift+Up to jump to previous command"
echo "And: Cmd+Shift+A to select last output"
echo ""
echo "Press Enter when tested..."
read -r
echo -e "${GREEN}✓ Shell integration working${NC}"
echo ""

echo -e "${BLUE}Step 6: Test Layout Scripts${NC}"
echo "Let's test the automated layouts."
echo ""
echo "Choose a test:"
echo "  1) TDD layout (it-tdd)"
echo "  2) Full Stack layout (it-fullstack)"
echo "  3) WalterSignal quick launch (it-ws)"
echo "  4) Skip tests"
echo ""
read -p "Choice (1-4): " choice

case $choice in
    1)
        echo -e "${YELLOW}Opening TDD layout...${NC}"
        ~/.claude/scripts/iterm-layout-tdd.sh "$PWD"
        ;;
    2)
        echo -e "${YELLOW}Opening Full Stack layout...${NC}"
        ~/.claude/scripts/iterm-layout-fullstack.sh "$PWD"
        ;;
    3)
        echo -e "${YELLOW}Opening WalterSignal...${NC}"
        ~/.claude/scripts/iterm-layout-fullstack.sh ~/Documents/ObsidianVault/Projects/WalterSignal
        ;;
    4)
        echo "Skipping tests..."
        ;;
    *)
        echo "Invalid choice, skipping..."
        ;;
esac
echo ""

echo -e "${GREEN}Step 7: Reload Shell (for aliases)${NC}"
echo "Opening new terminal tab with aliases loaded..."
osascript << 'EOF'
tell application "iTerm"
    tell current window
        create tab with default profile
        tell current session
            write text "source ~/.zshrc"
            write text "it-shortcuts"
        end tell
    end tell
end tell
EOF
echo -e "${GREEN}✓ New tab opened with aliases loaded${NC}"
echo ""

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Setup Complete! 🎉                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}What you can do now:${NC}"
echo ""
echo -e "${YELLOW}Quick Commands:${NC}"
echo "  it-shortcuts     - List all shortcuts"
echo "  it-help          - View full reference guide"
echo "  it-ws            - Launch WalterSignal"
echo "  it-tdd [dir]     - TDD layout for project"
echo "  it-fullstack     - Full stack layout"
echo ""
echo -e "${YELLOW}Essential Shortcuts:${NC}"
echo "  Cmd+O            - Switch profiles"
echo "  Cmd+Shift+A      - Select last output"
echo "  Cmd+Opt+A        - Alert on complete"
echo "  Cmd+D            - Split vertical"
echo "  Cmd+Shift+Up     - Previous command"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo "  Quick Ref:  ~/.claude/scripts/iterm-quick-reference.md"
echo "  Summary:    ~/.claude/iTERM2-COMPLETE-SETUP-SUMMARY.md"
echo ""
echo -e "${BLUE}Tip: Save your current window arrangement:${NC}"
echo "  Window > Save Window Arrangement"
echo "  Then: Settings > General > Startup > Open arrangement"
echo ""
echo "Enjoy your supercharged iTerm2! 🚀"
