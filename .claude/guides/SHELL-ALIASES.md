# Shell Aliases Quick Reference

## Navigation
```bash
vault         # cd ~/Documents/ObsidianVault
work          # cd ~/Documents/Work
docs          # Google Drive Documents
gdocs         # Same as docs
```

## Obsidian Vault
```bash
# Daily Workflow
vdaily        # Create and open today's daily note
vmorning      # Run morning routine script
vevening      # Run evening routine script

# Vault Management
vopen         # Open Obsidian
vgit          # Git status in vault
vpush         # Git commit and push vault

# Sync & Integration
obs-sync-email # Sync Gmail to Obsidian
obs-sync-cal  # Sync calendar to Obsidian
obs-sync-all  # Sync both email and calendar
obs-sync-drive # Sync documents to Google Drive

# Utilities
obs-daily     # Create daily note
obs-metrics   # Update metrics
obs-open      # Open Obsidian Dashboard
vscreenshot   # Daily screenshot capture
vgranola      # Granola export script
```

## Airtable & GitHub Sync
```bash
at-sync       # Sync Obsidian to Airtable
airtable-sync # Full command
at-log        # View Obsidian→Airtable sync logs

# GitHub ↔ Airtable Sync
github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'
github-sync-logs='ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | xargs cat'
github-sync-status='launchctl list | grep github-airtable-sync'
```

## 1Password
```bash
1pass-guide   # Full security guide
1pass-quick   # Quick reference
1pass-summary # Migration summary
```

## Claude Code CLI
```bash
c='claude'                                    # Start new claude session
cp='claude -p'                                # Print mode (single query)
cc='claude -c'                                # Continue last session
yolo='claude --dangerously-skip-permissions'  # Skip prompts (use with caution)

# In-session commands
/init         # Create CLAUDE.md context file
/help         # List available commands
/exit         # Exit session
/config       # Runtime configuration
```

## iTerm2 Notifications Setup
```bash
# 1. iTerm2 → Settings → Profiles → Terminal
#    - Enable "Silence bell"
#    - Enable "Send escape sequence-generated alerts"
# 2. Configure claude:
claude config set preferredNotifChannel iterm2
```

**Documentation:** `~/.config/iterm2/CLAUDE_CODE_INTEGRATION.md`
