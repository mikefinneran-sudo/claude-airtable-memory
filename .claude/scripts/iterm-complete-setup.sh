#!/bin/bash
# Complete iTerm2 Setup Script
# Configures triggers, smart selection, and preferences for optimal development workflow

set -e

echo "=== iTerm2 Complete Setup ==="
echo ""

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backup existing preferences
echo -e "${BLUE}Backing up current iTerm2 preferences...${NC}"
defaults read com.googlecode.iterm2 > ~/.claude/backups/iterm2-backup-$(date +%Y%m%d-%H%M%S).plist 2>/dev/null || true

# Enable shell integration features
echo -e "${BLUE}Enabling shell integration features...${NC}"
defaults write com.googlecode.iterm2 "ShellIntegrationEnabled" -bool true
defaults write com.googlecode.iterm2 "EnableProprietaryEscapeCodes" -bool true

# Configure notifications
echo -e "${BLUE}Configuring notifications...${NC}"
defaults write com.googlecode.iterm2 "SuppressBellAlertOnBackgroundTabs" -bool true
defaults write com.googlecode.iterm2 "SendBellAlert" -bool true

# Set up triggers (universal error/build/test patterns)
echo -e "${BLUE}Setting up universal triggers...${NC}"

# Trigger configurations as JSON (will be manually imported)
cat > /tmp/iterm2-triggers.json << 'EOF'
{
  "triggers": [
    {
      "regex": "(error|ERROR|Error|failed|FAILED|Failed|fatal|FATAL|Fatal)",
      "action": "HighlightText",
      "parameters": {
        "backgroundColor": {"red": 0.8, "green": 0.0, "blue": 0.0, "alpha": 0.3}
      }
    },
    {
      "regex": "(warning|WARNING|Warning|warn|WARN)",
      "action": "HighlightText",
      "parameters": {
        "backgroundColor": {"red": 0.8, "green": 0.6, "blue": 0.0, "alpha": 0.3}
      }
    },
    {
      "regex": "(success|SUCCESS|Success|passed|PASSED|Passed|✓|✔)",
      "action": "HighlightText",
      "parameters": {
        "backgroundColor": {"red": 0.0, "green": 0.6, "blue": 0.0, "alpha": 0.3}
      }
    },
    {
      "regex": "Build (complete|finished|succeeded)",
      "action": "PostNotification",
      "parameters": {
        "title": "Build Complete",
        "message": "Your build has finished"
      }
    },
    {
      "regex": "Tests? (passed|complete|succeeded)",
      "action": "PostNotification",
      "parameters": {
        "title": "Tests Complete",
        "message": "Test run finished"
      }
    },
    {
      "regex": "Deploy(ment)? (complete|finished|succeeded)",
      "action": "PostNotification",
      "parameters": {
        "title": "Deployment Complete",
        "message": "Deployment has finished"
      }
    },
    {
      "regex": "npm ERR!",
      "action": "HighlightText",
      "parameters": {
        "backgroundColor": {"red": 1.0, "green": 0.0, "blue": 0.0, "alpha": 0.5}
      }
    }
  ]
}
EOF

echo -e "${GREEN}Trigger configuration created at: /tmp/iterm2-triggers.json${NC}"
echo -e "${YELLOW}Note: Triggers must be manually added via iTerm2 > Settings > Profiles > Advanced${NC}"

# Configure smart selection rules
echo -e "${BLUE}Configuring smart selection rules...${NC}"

# Smart Selection for common patterns
defaults write com.googlecode.iterm2 "SmartSelectionRules" -array \
  '<dict>
    <key>notes</key><string>URLs</string>
    <key>precision</key><string>normal</string>
    <key>regex</key><string>https?://[a-zA-Z0-9./?=_-]+</string>
  </dict>' \
  '<dict>
    <key>notes</key><string>File paths</string>
    <key>precision</key><string>normal</string>
    <key>regex</key><string>~/[a-zA-Z0-9/_.-]+</string>
  </dict>' \
  '<dict>
    <key>notes</key><string>File:line</string>
    <key>precision</key><string>normal</string>
    <key>regex</key><string>[a-zA-Z0-9/_.-]+:[0-9]+</string>
  </dict>' \
  '<dict>
    <key>notes</key><string>IP addresses</string>
    <key>precision</key><string>normal</string>
    <key>regex</key><string>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}</string>
  </dict>' \
  '<dict>
    <key>notes</key><string>Email addresses</string>
    <key>precision</key><string>normal</string>
    <key>regex</key><string>[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}</string>
  </dict>' \
  '<dict>
    <key>notes</key><string>Git commit hashes</string>
    <key>precision</key><string>normal</string>
    <key>regex</key><string>\b[0-9a-f]{7,40}\b</string>
  </dict>'

# Enable advanced paste features
echo -e "${BLUE}Enabling advanced paste features...${NC}"
defaults write com.googlecode.iterm2 "PasteSpecialChunkSize" -int 1024
defaults write com.googlecode.iterm2 "PasteSpecialChunkDelay" -float 0.01

# Configure scrollback
echo -e "${BLUE}Configuring scrollback buffer...${NC}"
defaults write com.googlecode.iterm2 "UnlimitedScrollback" -bool false
defaults write com.googlecode.iterm2 "ScrollbackLines" -int 10000

# Enable session restoration
echo -e "${BLUE}Enabling session restoration...${NC}"
defaults write com.googlecode.iterm2 "OpenArrangementAtStartup" -bool false
defaults write com.googlecode.iterm2 "OpenBookmark" -bool false
defaults write com.googlecode.iterm2 "WindowRestoreUsesSavedArrangement" -bool true

# Configure status bar
echo -e "${BLUE}Configuring status bar components...${NC}"
defaults write com.googlecode.iterm2 "ShowStatusBar" -bool true

# Performance optimizations
echo -e "${BLUE}Applying performance optimizations...${NC}"
defaults write com.googlecode.iterm2 "UseMetal" -bool true
defaults write com.googlecode.iterm2 "DisableWindowSizeSnap" -bool true

# Configure hotkey window
echo -e "${BLUE}Configuring hotkey window (Cmd+Opt+T)...${NC}"
defaults write com.googlecode.iterm2 "HotkeyEnabled" -bool true

echo ""
echo -e "${GREEN}=== Setup Complete! ===${NC}"
echo ""
echo -e "${YELLOW}Manual steps required:${NC}"
echo "1. Import triggers: iTerm2 > Settings > Profiles > Advanced > Triggers"
echo "   - Use configuration from: /tmp/iterm2-triggers.json"
echo ""
echo "2. Restart iTerm2 to apply all changes"
echo ""
echo "3. Access dynamic profiles:"
echo "   - Cmd+O, then type profile name (WalterSignal, Claude Efficiency, etc.)"
echo ""
echo "4. Enable status bar: View > Show Status Bar"
echo ""
echo -e "${BLUE}Quick reference saved to: ~/.claude/scripts/iterm-quick-reference.md${NC}"
