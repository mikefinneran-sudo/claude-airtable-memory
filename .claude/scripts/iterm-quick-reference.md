# iTerm2 Complete Setup - Quick Reference

## Created: 2025-11-08
## Status: Production Ready

---

## 1. Dynamic Profiles (Cmd+O)

Profiles automatically load project context with custom colors and working directories.

**Available Profiles:**
- `WalterSignal` - Badge: WS (Blue)
- `Claude Efficiency` - Badge: CE (Purple)
- `LifeHub` - Badge: LH (Green)
- `Ivy League AI` - Badge: IVY (Red)
- `ObsidianVault` - Badge: VAULT (Purple)
- `TDD Workflow` - Badge: TDD (Auto-split for tests)
- `Full Stack` - Badge: STACK (3-pane layout)
- `Research Mode` - Badge: RESEARCH (Cyan)

**Usage:**
```bash
# Quick switch
Cmd+O, then type profile name

# From command line
open -a iTerm ~/Documents/ObsidianVault/Projects/WalterSignal
```

---

## 2. Shell Integration (CRITICAL)

These shortcuts are the foundation of productivity:

**Navigation:**
- `Cmd+Shift+Up` - Jump to previous command
- `Cmd+Shift+Down` - Jump to next command
- `Cmd+Opt+/` - Recent directories
- `Cmd+Shift+;` - Command history (autocomplete)

**Selection:**
- `Cmd+Shift+A` - Select last command output
- `Cmd+Click` - Smart selection (URLs, paths, IPs, emails)
- `Triple-click` - Select entire line

**Marks & Alerts:**
- `Cmd+Shift+M` - Set bookmark/mark
- `Cmd+Opt+A` - Alert when command completes
- `Cmd+Opt+Shift+A` - Alert on next mark

---

## 3. Split Panes & Layouts

**Manual Splits:**
- `Cmd+D` - Split vertically
- `Cmd+Shift+D` - Split horizontally
- `Cmd+[` / `Cmd+]` - Navigate panes
- `Cmd+Opt+Arrow` - Resize active pane

**Automated Layouts:**
```bash
# TDD: Claude | Tests
~/.claude/scripts/iterm-layout-tdd.sh ~/path/to/project

# Full Stack: Claude | Dev Server | Tests
~/.claude/scripts/iterm-layout-fullstack.sh ~/path/to/project

# Remote: Local Claude | Remote tmux
~/.claude/scripts/iterm-layout-remote.sh user@host
```

**Layout Tips:**
- Use `Cmd+Shift+Enter` to maximize current pane (toggle)
- Use `View > Show Session Name` to label panes
- Save arrangements: `Window > Save Window Arrangement`

---

## 4. Universal Triggers

Triggers automatically highlight and notify on patterns:

**Auto-Configured:**
- **Errors** → Red highlight (error, ERROR, failed, fatal)
- **Warnings** → Orange highlight (warning, WARN)
- **Success** → Green highlight (success, passed, ✓)
- **Build Complete** → Notification
- **Tests Complete** → Notification
- **Deploy Complete** → Notification

**Manual Addition:**
1. Settings > Profiles > Advanced > Triggers > Edit
2. Import from: `/tmp/iterm2-triggers.json`

---

## 5. Smart Selection

Auto-configured patterns (Cmd+Click):
- URLs (https://...)
- File paths (~/Documents/...)
- File:line numbers (src/main.js:42)
- IP addresses (192.168.1.1)
- Email addresses
- Git commit hashes

**Custom Actions:**
1. Settings > Profiles > Advanced > Smart Selection
2. Add actions: "Open with Sublime", "Search in Google", etc.

---

## 6. tmux Integration

**Local tmux:**
```bash
# Start integration mode
tmux -CC

# Attach to existing session
tmux -CC attach -t session-name
```

**Remote tmux:**
```bash
# Connect with integration mode
ssh user@host -t 'tmux -CC new -A -s dev'

# Or use the script
~/.claude/scripts/iterm-layout-remote.sh user@host
```

**Benefits:**
- Session survives disconnects
- Native iTerm2 tabs/panes
- Better clipboard integration
- Full mouse support

**tmux Key Bindings (Prefix: Ctrl+a):**
- `Ctrl+a |` - Split vertical
- `Ctrl+a -` - Split horizontal
- `Ctrl+a r` - Reload config
- `Ctrl+a c` - New window
- `Ctrl+a d` - Detach session

---

## 7. Status Bar

**Enable:**
1. Settings > Profiles > Session
2. Check "Status bar enabled"
3. Click "Configure Status Bar"

**Recommended Components:**
- Current Directory (left)
- Git Branch (left)
- CPU % (right)
- Memory (right)
- Clock (right)

**Quick Toggle:**
```bash
# Show/hide status bar
Cmd+Shift+B (custom binding)

# Or: View > Show Status Bar
```

---

## 8. Keyboard Shortcuts (Essential)

**Tabs:**
- `Cmd+T` - New tab
- `Cmd+W` - Close tab
- `Cmd+1-9` - Switch to tab 1-9
- `Cmd+Left/Right` - Previous/next tab

**Search:**
- `Cmd+F` - Find
- `Cmd+G` - Find next
- `Cmd+Shift+G` - Find previous

**Clipboard:**
- `Cmd+Shift+H` - Paste history
- `Cmd+Opt+;` - Command history

**Window Management:**
- `Cmd+N` - New window
- `Cmd+Opt+B` - Show toolbelt (captured output)
- `Cmd+Shift+Enter` - Maximize pane

**Instant Replay:**
- `Cmd+Opt+B` - Enable toolbelt
- Click "Captured Output" to see command outputs

---

## 9. Quick Setup Commands

**Run Complete Setup:**
```bash
# Make scripts executable
chmod +x ~/.claude/scripts/iterm-*.sh

# Run complete setup
~/.claude/scripts/iterm-complete-setup.sh

# Configure status bar
~/.claude/scripts/iterm-configure-statusbar.sh

# Restart iTerm2
osascript -e 'quit app "iTerm"'
open -a iTerm
```

**Individual Setups:**
```bash
# TDD layout for current project
~/.claude/scripts/iterm-layout-tdd.sh

# Full stack layout
~/.claude/scripts/iterm-layout-fullstack.sh

# Remote development
~/.claude/scripts/iterm-layout-remote.sh user@host
```

---

## 10. Development Workflows

### TDD Workflow
1. `Cmd+O` → Type "TDD"
2. Or run: `~/.claude/scripts/iterm-layout-tdd.sh`
3. Left pane: Claude Code
4. Right pane: Test watcher (auto-starts)

### Full Stack Workflow
1. Run: `~/.claude/scripts/iterm-layout-fullstack.sh`
2. Left pane: Claude Code
3. Top right: Dev server
4. Bottom right: Test watcher

### Remote Development
1. Run: `~/.claude/scripts/iterm-layout-remote.sh user@host`
2. Left pane: Local Claude
3. Right pane: Remote tmux session

### WalterSignal Specific
```bash
# Quick start
Cmd+O → "WalterSignal"

# Or automated
cd ~/Documents/ObsidianVault/Projects/WalterSignal
~/.claude/scripts/iterm-layout-fullstack.sh
```

---

## 11. Python API (Advanced Automation)

iTerm2 has a powerful Python API for automation.

**Example: Auto-split on project open**
```python
#!/usr/bin/env python3
import iterm2

async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window
    if window is not None:
        await window.async_create_tab()
        tab = window.current_tab
        # Split and configure
        left = tab.current_session
        right = await left.async_split_pane(vertical=True)
        await left.async_send_text('claude\n')
        await right.async_send_text('npm run test:watch\n')

iterm2.run_until_complete(main)
```

**Location:** `~/Library/ApplicationSupport/iTerm2/Scripts/`

---

## 12. Tips & Tricks

**Paste without newlines:**
- Edit > Paste Special > Advanced Paste
- Set up hotkey: Settings > Keys > Key Bindings

**Copy mode:**
- Hold Option while selecting text with mouse
- Allows rectangular selection

**Badge:**
- Settings > Profiles > General > Badge
- Use `\(user)@\(session.hostname)` for SSH sessions

**Notifications:**
- Enable for long builds: `Cmd+Opt+A` before running
- Configure: Settings > Profiles > Terminal > Notifications

**Performance:**
- Reduce scrollback for heavy output (Settings > Profiles > Terminal)
- Enable Metal renderer (Settings > General > GPU Rendering)
- Disable blur/transparency for better performance

**Session logs:**
- Toolbelt > Captured Output (Cmd+Opt+B)
- Or enable automatic logging: Settings > Profiles > Session > Logging

---

## 13. Troubleshooting

**Shell integration not working:**
```bash
# Reinstall integration
curl -L https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh | bash

# Or manually source
echo 'source ~/.iterm2_shell_integration.zsh' >> ~/.zshrc
```

**Dynamic profiles not showing:**
```bash
# Check file exists
ls -la ~/Library/Application\ Support/iTerm2/DynamicProfiles/

# Restart iTerm2
osascript -e 'quit app "iTerm"' && open -a iTerm
```

**Triggers not firing:**
1. Check regex: Settings > Profiles > Advanced > Triggers
2. Test with: `echo "ERROR: test"` (should highlight)
3. Ensure instant trigger is checked

**Status bar not visible:**
1. View > Show Status Bar
2. Settings > Profiles > Session > Enable status bar

---

## 14. Backup & Sync

**Export preferences:**
```bash
# Export all settings
defaults export com.googlecode.iterm2 ~/iterm2-backup.plist

# Backup dynamic profiles
cp -r ~/Library/Application\ Support/iTerm2/DynamicProfiles \
     ~/.claude/backups/iterm2-profiles-$(date +%Y%m%d)
```

**Sync between machines:**
1. Settings > General > Preferences
2. Check "Load preferences from a custom folder or URL"
3. Set to: `~/Dropbox/iTerm2` or iCloud path
4. Check "Save changes to folder when iTerm2 quits"

---

## 15. Resources

**Documentation:**
- Official: https://iterm2.com/documentation.html
- Python API: https://iterm2.com/python-api/
- Shell Integration: https://iterm2.com/documentation-shell-integration.html

**Local Guides:**
- Expert Guide: `~/.config/iterm2/EXPERT_GUIDE.md`
- Claude Workflows: `~/.config/iterm2/CLAUDE_CODE_WORKFLOWS.md`
- Quick Ref: `~/.config/iterm2/QUICK_REFERENCE.md`

**Support:**
- Issues: https://gitlab.com/gnachman/iterm2/-/issues
- Forum: https://iterm2.com/forum

---

## Quick Command Summary

```bash
# Setup
~/.claude/scripts/iterm-complete-setup.sh

# Layouts
~/.claude/scripts/iterm-layout-tdd.sh [project-dir]
~/.claude/scripts/iterm-layout-fullstack.sh [project-dir]
~/.claude/scripts/iterm-layout-remote.sh user@host

# Configuration
~/.claude/scripts/iterm-configure-statusbar.sh

# Status bar toggle
Cmd+Shift+B (or View > Show Status Bar)

# Profile switch
Cmd+O, then type name

# Shell integration
Cmd+Shift+Up/Down (navigate commands)
Cmd+Shift+A (select output)
Cmd+Opt+A (alert on complete)
```

---

**Last Updated:** 2025-11-08
**Version:** 1.0
**Status:** Production Ready
