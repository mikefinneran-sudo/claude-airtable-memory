#!/bin/bash
# iTerm2 Setup Verification Script

echo "=== iTerm2 Setup Verification ==="
echo ""

# Check iTerm2 installation
if [ -d "/Applications/iTerm.app" ]; then
    echo "✓ iTerm2 installed"
    ITERM_VERSION=$(defaults read /Applications/iTerm.app/Contents/Info.plist CFBundleShortVersionString)
    echo "  Version: $ITERM_VERSION"
else
    echo "✗ iTerm2 not found"
    exit 1
fi

# Check shell integration
if [ -f "$HOME/.iterm2_shell_integration.zsh" ]; then
    echo "✓ Shell integration downloaded"
else
    echo "✗ Shell integration missing"
fi

# Check if integration is sourced in .zshrc
if grep -q "iterm2_shell_integration" "$HOME/.zshrc"; then
    echo "✓ Shell integration configured in .zshrc"
else
    echo "✗ Shell integration not in .zshrc"
fi

# Check config directory
if [ -d "$HOME/.config/iterm2" ]; then
    echo "✓ Config directory exists"
    echo "  Location: $HOME/.config/iterm2"
else
    echo "✗ Config directory missing"
fi

# Check custom config
if defaults read com.googlecode.iterm2 LoadPrefsFromCustomFolder 2>/dev/null | grep -q 1; then
    echo "✓ Custom config folder enabled"
    PREFS_PATH=$(defaults read com.googlecode.iterm2 PrefsCustomFolder 2>/dev/null)
    echo "  Path: $PREFS_PATH"
else
    echo "⚠ Custom config folder not enabled (will use defaults)"
fi

# Check for Claude Code compatibility
if command -v claude &> /dev/null; then
    echo "✓ Claude Code CLI found"
else
    echo "⚠ Claude Code CLI not found (may need separate install)"
fi

echo ""
echo "=== Next Steps ==="
echo "1. Open iTerm2: open -a iTerm"
echo "2. Test shell integration: ls (should see command markers)"
echo "3. Try split panes: Cmd+D (vertical) or Cmd+Shift+D (horizontal)"
echo "4. View quick reference: cat ~/.config/iterm2/QUICK_REFERENCE.md"
echo ""
echo "=== Optional Warp Cleanup ==="
echo "To remove Warp (once you're happy with iTerm2):"
echo "  brew uninstall --cask warp"
echo "  rm -rf ~/.warp"
echo ""
