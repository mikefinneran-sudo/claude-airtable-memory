# iTerm2 Complete Setup - File Index

## Created: 2025-11-08

---

## Configuration Files

### Dynamic Profiles
- `~/Library/Application Support/iTerm2/DynamicProfiles/claude-projects.json`
  - 8 project profiles with custom badges and colors
  - Auto-loads working directories
  - Access: Cmd+O

### tmux Configuration
- `~/.tmux.conf`
  - iTerm2-optimized settings
  - Vi-style bindings, Ctrl+a prefix
  - Mouse support, true color

### Shell Configuration
- `~/.zshrc` (modified)
  - Added: `source ~/.claude/scripts/iterm-aliases.sh`

---

## Scripts (7 total)

### Setup Scripts
- `~/.claude/scripts/iterm-complete-setup.sh` ⭐ Main setup
- `~/.claude/scripts/iterm-finish-setup.sh` ⭐ Guided completion
- `~/.claude/scripts/iterm-configure-statusbar.sh` Status bar config

### Layout Automation
- `~/.claude/scripts/iterm-layout-tdd.sh` TDD: Claude | Tests
- `~/.claude/scripts/iterm-layout-fullstack.sh` Full: Claude | Dev | Tests
- `~/.claude/scripts/iterm-layout-remote.sh` Remote: Local | tmux

### Utilities
- `~/.claude/scripts/iterm-aliases.sh` 20+ shell aliases

---

## Documentation (3 files)

### Primary Docs
- `~/.claude/iTERM2-COMPLETE-SETUP-SUMMARY.md` ⭐ START HERE
  - What was installed
  - Next steps
  - Quick start guides
  
- `~/.claude/scripts/iterm-quick-reference.md` ⭐ Daily reference
  - 15 sections
  - All shortcuts
  - Workflows
  - Troubleshooting

### Meta
- `~/.claude/ITERM2-FILES-INDEX.md` This file

---

## Temporary Files (Import These)

### Trigger Configuration
- `/tmp/iterm2-triggers.json`
  - Import: Settings > Profiles > Advanced > Triggers
  - Auto-highlights errors, warnings, success
  - Notifications for builds/tests/deploys

### Status Bar Config (Reference)
- `/tmp/iterm2-statusbar-config.json`
  - Components: Directory, Git, CPU, Memory, Clock
  - Enable: Settings > Profiles > Session

---

## Backups

### Preferences Backup
- `~/.claude/backups/iterm2-backup-*.plist`
  - Created during setup
  - Restore if needed: `defaults import com.googlecode.iterm2 backup.plist`

---

## Quick Access Commands

### View Documentation
```bash
# Complete summary (start here)
open ~/.claude/iTERM2-COMPLETE-SETUP-SUMMARY.md

# Quick reference (daily use)
it-help
# or: cat ~/.claude/scripts/iterm-quick-reference.md | less

# This index
cat ~/.claude/ITERM2-FILES-INDEX.md
```

### Run Setup/Finish
```bash
# Initial setup (already done)
~/.claude/scripts/iterm-complete-setup.sh

# Finish/verify setup
~/.claude/scripts/iterm-finish-setup.sh
```

### Test Layouts
```bash
# TDD layout
it-tdd
# or: ~/.claude/scripts/iterm-layout-tdd.sh

# Full stack
it-fullstack
# or: ~/.claude/scripts/iterm-layout-fullstack.sh

# WalterSignal
it-ws
```

### Shell Aliases
```bash
# List all iTerm aliases
alias | grep it-

# Show shortcuts
it-shortcuts
```

---

## File Sizes

```
Configuration:
  claude-projects.json: ~1.5 KB
  .tmux.conf: ~3.5 KB

Scripts:
  iterm-complete-setup.sh: ~6 KB
  iterm-finish-setup.sh: ~5 KB
  iterm-layout-tdd.sh: ~1.6 KB
  iterm-layout-fullstack.sh: ~2.4 KB
  iterm-layout-remote.sh: ~1.3 KB
  iterm-configure-statusbar.sh: ~2.6 KB
  iterm-aliases.sh: ~1.8 KB

Documentation:
  COMPLETE-SETUP-SUMMARY.md: ~12 KB
  iterm-quick-reference.md: ~15 KB
  ITERM2-FILES-INDEX.md: ~3 KB (this file)

Total: ~56 KB
```

---

## Verification Checklist

Run this to verify all files exist:

```bash
# Configuration
[ -f ~/Library/Application\ Support/iTerm2/DynamicProfiles/claude-projects.json ] && echo "✓ Dynamic profiles" || echo "✗ Missing profiles"
[ -f ~/.tmux.conf ] && echo "✓ tmux config" || echo "✗ Missing tmux"

# Scripts (executable)
[ -x ~/.claude/scripts/iterm-complete-setup.sh ] && echo "✓ Setup script" || echo "✗ Missing setup"
[ -x ~/.claude/scripts/iterm-finish-setup.sh ] && echo "✓ Finish script" || echo "✗ Missing finish"
[ -x ~/.claude/scripts/iterm-layout-tdd.sh ] && echo "✓ TDD layout" || echo "✗ Missing TDD"
[ -x ~/.claude/scripts/iterm-layout-fullstack.sh ] && echo "✓ Fullstack layout" || echo "✗ Missing fullstack"
[ -x ~/.claude/scripts/iterm-layout-remote.sh ] && echo "✓ Remote layout" || echo "✗ Missing remote"
[ -x ~/.claude/scripts/iterm-configure-statusbar.sh ] && echo "✓ Status bar config" || echo "✗ Missing statusbar"
[ -f ~/.claude/scripts/iterm-aliases.sh ] && echo "✓ Aliases" || echo "✗ Missing aliases"

# Documentation
[ -f ~/.claude/iTERM2-COMPLETE-SETUP-SUMMARY.md ] && echo "✓ Summary" || echo "✗ Missing summary"
[ -f ~/.claude/scripts/iterm-quick-reference.md ] && echo "✓ Quick ref" || echo "✗ Missing reference"
[ -f ~/.claude/ITERM2-FILES-INDEX.md ] && echo "✓ Index" || echo "✗ Missing index"

# Temporary (should exist)
[ -f /tmp/iterm2-triggers.json ] && echo "✓ Triggers" || echo "✗ Missing triggers"
[ -f /tmp/iterm2-statusbar-config.json ] && echo "✓ Status config" || echo "✗ Missing status config"

# Shell integration
grep -q "iterm-aliases.sh" ~/.zshrc && echo "✓ Aliases sourced" || echo "✗ Not sourced"
```

---

## What to Do Next

1. **First time?** Read the summary:
   ```bash
   open ~/.claude/iTERM2-COMPLETE-SETUP-SUMMARY.md
   ```

2. **Ready to finish?** Run the guided setup:
   ```bash
   ~/.claude/scripts/iterm-finish-setup.sh
   ```

3. **Need help?** View quick reference:
   ```bash
   it-help
   ```

4. **Want to test?** Try WalterSignal:
   ```bash
   it-ws
   ```

---

**Status:** ✅ All files created and ready
**Next:** Run finish setup or restart iTerm2
**Help:** `it-shortcuts` or `it-help`

---

*Last updated: 2025-11-08*
