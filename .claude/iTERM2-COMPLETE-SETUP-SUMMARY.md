# iTerm2 Complete Setup - Summary

**Created:** 2025-11-08
**Status:** ✅ Production Ready

---

## What Was Installed

### 1. Dynamic Profiles (8 profiles)
**Location:** `~/Library/Application Support/iTerm2/DynamicProfiles/claude-projects.json`

- **WalterSignal** - Blue badge, auto-loads WS project
- **Claude Efficiency** - Purple badge, CE project
- **LifeHub** - Green badge, LH project
- **Ivy League AI** - Red badge, IVY project
- **ObsidianVault** - Purple badge, vault root
- **TDD Workflow** - Auto-split layout for testing
- **Full Stack** - 3-pane layout (Claude | Dev | Tests)
- **Research Mode** - Cyan badge, research tools ready

**How to use:** `Cmd+O`, then type profile name

### 2. Universal Triggers
**Location:** `/tmp/iterm2-triggers.json` (manual import required)

Auto-highlights and notifies:
- ❌ Errors (red)
- ⚠️ Warnings (orange)
- ✅ Success (green)
- 🔔 Build/Test/Deploy complete notifications

**Import:** Settings > Profiles > Advanced > Triggers > Edit

### 3. Smart Selection Rules
**Status:** ✅ Auto-configured

`Cmd+Click` now selects:
- URLs
- File paths
- File:line numbers (src/main.js:42)
- IP addresses
- Email addresses
- Git commit hashes

### 4. Layout Automation Scripts
**Location:** `~/.claude/scripts/`

- `iterm-layout-tdd.sh` - TDD layout (Claude | Tests)
- `iterm-layout-fullstack.sh` - Full stack (Claude | Dev | Tests)
- `iterm-layout-remote.sh` - Remote with tmux integration

**Aliases:** `it-tdd`, `it-fullstack`, `it-remote`

### 5. tmux Integration
**Location:** `~/.tmux.conf`

- Optimized for iTerm2 integration mode
- Vi-style key bindings
- Ctrl+a prefix
- Mouse support enabled
- Session persistence

**Usage:** `ssh user@host -t 'tmux -CC new -A -s dev'`

### 6. Status Bar Configuration
**Location:** `/tmp/iterm2-statusbar-config.json`

Components:
- Current Directory
- Git Branch
- CPU %
- Memory
- Clock

**Enable:** Settings > Profiles > Session > Status bar enabled

### 7. Shell Aliases (20+ shortcuts)
**Location:** `~/.claude/scripts/iterm-aliases.sh`
**Status:** ✅ Auto-loaded in .zshrc

Quick commands:
- `it-tdd [dir]` - Launch TDD layout
- `it-fullstack [dir]` - Launch full stack
- `it-ws` - Open WalterSignal
- `it-help` - Show quick reference
- `it-shortcuts` - List all shortcuts

---

## What's Next (Manual Steps)

### Step 1: Restart iTerm2 (Required)
```bash
osascript -e 'quit app "iTerm"'
open -a iTerm
```

### Step 2: Import Triggers (Recommended)
1. Open iTerm2 Settings (Cmd+,)
2. Profiles > Advanced > Triggers > Edit
3. Click "Import" and select `/tmp/iterm2-triggers.json`
4. Or manually add from the JSON file

### Step 3: Enable Status Bar (Optional)
1. View > Show Status Bar
2. Or: Settings > Profiles > Session > Check "Status bar enabled"
3. Click "Configure Status Bar" to customize

### Step 4: Test Dynamic Profiles
```bash
# Quick test
Cmd+O
# Type: "WalterSignal"
# Should load with blue "WS" badge
```

### Step 5: Test Layout Scripts
```bash
# Reload shell to get aliases
source ~/.zshrc

# Test TDD layout
it-tdd ~/Documents/ObsidianVault/Projects/WalterSignal

# Test full stack layout
it-fullstack ~/Documents/ObsidianVault/Projects/WalterSignal
```

---

## Quick Start Guide

### For WalterSignal Development
```bash
# Method 1: Profile
Cmd+O → "WalterSignal"

# Method 2: Alias
it-ws

# Method 3: Full command
it-fullstack ~/Documents/ObsidianVault/Projects/WalterSignal
```

### For TDD Workflow
```bash
# Current directory
it-tdd

# Specific project
it-tdd ~/path/to/project

# WalterSignal TDD
it-tdd ~/Documents/ObsidianVault/Projects/WalterSignal
```

### For Remote Work
```bash
# Basic
it-remote user@host

# DGX server example
it-remote nvidia@192.168.68.81

# EC2 example
it-remote ubuntu@98.89.88.138
```

---

## Essential Shortcuts (Memorize These)

**Shell Integration:**
- `Cmd+Shift+Up/Down` - Jump between commands
- `Cmd+Shift+A` - Select last command output
- `Cmd+Opt+A` - Alert when command completes

**Panes:**
- `Cmd+D` - Split vertical
- `Cmd+Shift+D` - Split horizontal
- `Cmd+[` / `Cmd+]` - Navigate panes

**Profiles:**
- `Cmd+O` - Open profile switcher
- `Cmd+I` - Edit current session

**Marks:**
- `Cmd+Shift+M` - Set mark/bookmark
- `Cmd+Shift+Up` - Jump to previous mark

---

## File Locations Reference

```
Configuration:
  ~/Library/Application Support/iTerm2/DynamicProfiles/claude-projects.json
  ~/.tmux.conf
  ~/.zshrc (aliases sourced)

Scripts:
  ~/.claude/scripts/iterm-complete-setup.sh
  ~/.claude/scripts/iterm-layout-tdd.sh
  ~/.claude/scripts/iterm-layout-fullstack.sh
  ~/.claude/scripts/iterm-layout-remote.sh
  ~/.claude/scripts/iterm-configure-statusbar.sh
  ~/.claude/scripts/iterm-aliases.sh

Documentation:
  ~/.claude/scripts/iterm-quick-reference.md
  ~/.config/iterm2/EXPERT_GUIDE.md
  ~/.config/iterm2/CLAUDE_CODE_WORKFLOWS.md

Temporary:
  /tmp/iterm2-triggers.json (import this)
  /tmp/iterm2-statusbar-config.json (reference)

Backups:
  ~/.claude/backups/iterm2-backup-*.plist
```

---

## Troubleshooting

**Dynamic profiles not showing:**
```bash
# Verify file exists
ls -la ~/Library/Application\ Support/iTerm2/DynamicProfiles/

# Restart iTerm2
it-reload
```

**Shell integration not working:**
```bash
# Check if sourced
grep -q "iterm2_shell_integration" ~/.zshrc

# Reinstall if needed
curl -L https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh | bash
```

**Triggers not firing:**
1. Import triggers from `/tmp/iterm2-triggers.json`
2. Check: Settings > Profiles > Advanced > Triggers
3. Test with: `echo "ERROR: test"` (should highlight red)

**Aliases not working:**
```bash
# Reload shell
source ~/.zshrc

# Verify loaded
type it-tdd

# Should show: it-tdd is an alias for...
```

**tmux not connecting:**
```bash
# Check tmux installed
which tmux

# Install if needed
brew install tmux

# Test local
tmux -CC

# Test remote
ssh user@host 'which tmux'
```

---

## Performance Tips

**For heavy output (logs, builds):**
1. Reduce scrollback: Settings > Profiles > Terminal > Scrollback Lines (5000)
2. Use captured output: Cmd+Opt+B > Captured Output
3. Disable transparency: Settings > Profiles > Window > Transparency (0%)

**For maximum speed:**
1. Enable Metal: Settings > General > GPU Rendering
2. Disable blur: Settings > Profiles > Window > Blur (off)
3. Use solid colors instead of background images

**For long sessions:**
1. Use tmux for persistence
2. Enable session restoration: Settings > General > Startup
3. Save arrangements: Window > Save Window Arrangement

---

## Advanced Features (Next Level)

**Python API Automation:**
```python
# Auto-configure panes based on project type
# Location: ~/Library/Application Support/iTerm2/Scripts/AutoLaunch/
```

**Coprocesses:**
```bash
# Run background process that can interact with terminal
# Use for: auto-completion, context-aware commands
```

**Automatic Profile Switching:**
```bash
# Set badge based on SSH host
# Settings > Profiles > General > Badge
# Use: \(session.hostname)
```

**Custom Actions:**
```bash
# Right-click on selected text
# Settings > Pointer > Advanced > Smart Selection
# Add actions: "Search Google", "Open in IDE", etc.
```

---

## Resources

**Documentation:**
- Quick Reference: `~/.claude/scripts/iterm-quick-reference.md`
- Expert Guide: `~/.config/iterm2/EXPERT_GUIDE.md`
- Official Docs: https://iterm2.com/documentation.html

**Get Help:**
```bash
# Show all shortcuts
it-shortcuts

# View quick reference
it-help

# List aliases
alias | grep it-
```

**Community:**
- Forum: https://iterm2.com/forum
- Issues: https://gitlab.com/gnachman/iterm2/-/issues

---

## What Changed in Your System

**Files Created:**
- 8 dynamic profiles
- 5 shell scripts
- 1 tmux config
- 3 documentation files
- 2 configuration JSONs

**Files Modified:**
- ~/.zshrc (added alias sourcing)

**Settings Changed:**
- Shell integration enabled
- Smart selection configured
- Scrollback set to 10,000 lines
- Status bar enabled
- Metal rendering enabled
- Notifications configured

**Backups Created:**
- `~/.claude/backups/iterm2-backup-*.plist`

---

## Next Steps (Recommended)

1. ✅ **Restart iTerm2** (apply all changes)
2. ✅ **Import triggers** (enable auto-highlighting)
3. ✅ **Test a layout script** (`it-ws` or `it-tdd`)
4. ✅ **Enable status bar** (View > Show Status Bar)
5. ✅ **Memorize 3 shortcuts:**
   - `Cmd+Shift+A` - Select last output
   - `Cmd+Opt+A` - Alert on complete
   - `Cmd+D` - Split pane
6. ✅ **Save a window arrangement** for your main workflow
7. 📚 **Read quick reference** (`it-help`)

---

## Success Criteria

You'll know it's working when:
- `Cmd+O` shows your project profiles
- `echo "ERROR: test"` highlights in red
- `it-ws` opens WalterSignal in full stack layout
- `Cmd+Shift+A` selects command output
- Status bar shows git branch and system stats
- `it-shortcuts` displays your alias list

---

**Status:** ✅ Ready to use
**Next:** Restart iTerm2 and test!

**Questions?**
- Run: `it-help`
- Check: `~/.claude/scripts/iterm-quick-reference.md`
- Ask Claude: "How do I [task] in iTerm2?"

---

*Created by Claude Code - 2025-11-08*
