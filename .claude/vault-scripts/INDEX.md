# ObsidianVault Scripts - Quick Index

**Fast reference guide for all custom automation scripts**

---

## 🎯 Most Used Scripts

```bash
# Daily workflow
obs-daily              # Create today's note
obs-metrics            # Update revenue metrics
obs-open               # Open dashboard

# Integrations
python3 sync_to_notion.py              # Sync to Notion
python3 sync_calendar.py               # Sync calendar
./setup-integrations.sh                # Setup tools

# Utilities
./capture-screenshot.sh                # Screenshot → vault
./get-api-key.sh "Anthropic API"       # Get API key
```

---

## 📂 Browse by Category

### Daily Operations
- **Daily Notes** → `create_daily_note_enhanced.sh`
- **Weekly Reviews** → `create_weekly_review_enhanced.sh`
- **Metrics Tracking** → `update_metrics.py`
- **Daily Auto-Update** → `update_daily_note.py`

### Integrations
- **Notion Sync** → `sync_to_notion.py`
- **Gmail Sync** → `sync_gmail.py`
- **Calendar Sync** → `sync_calendar.py`
- **Google Drive Sync** → `sync-documents-to-gdrive.sh`

### Screenshots & Media
- **Screenshot Capture** → `capture-screenshot.sh`
- **Daily Screenshot** → `daily-screenshot.sh`
- **Project Screenshot** → `project-screenshot.sh`
- **OCR to Daily** → `ocr-to-daily.sh`

### Setup & Configuration
- **Master Setup** → `setup-integrations.sh`
- **Notion Setup** → `setup-notion-sync.sh`
- **Setup Wizard** → `setup_wizard.py`
- **OAuth Server** → `oauth_server.py`

### Utilities
- **Get API Key** → `get-api-key.sh`
- **Open Vault** → `open-vault.sh`

### Project Scripts
- **FlyFlat Updates** → `create_flyflat_update.sh`
- **WalterSignal Education** → `waltersignal_education.py`
- **Web Dev Education** → `web_dev_education.py`

### macOS Automation
- **Create VM** → `create-utm-vm.applescript`

---

## 📚 Documentation Files

- **README.md** - Complete script documentation (8,000+ words)
- **CONTRIBUTING.md** - Guidelines for adding new scripts
- **INDEX.md** - This file (quick reference)
- **Setup Guides:**
  - `QUICK-SETUP.md` - 5-minute quick start
  - `DAILY_NOTE_AUTOMATION_SETUP.md` - Daily note automation
  - `NOTION-SETUP-GUIDE.md` - Notion integration
  - `FLYFLAT-NOTION-SETUP.md` - FlyFlat Notion setup
  - `CALENDAR-SETUP-GUIDE.md` - Google Calendar
  - `GMAIL-SETUP-GUIDE.md` - Gmail integration
  - `SHELL-COMMANDS-SETUP-GUIDE.md` - Obsidian Shell Commands

---

## 🤖 Alfred Workflows

**Location:** `.integrations/alfred/workflows/`
**Documentation:** `.integrations/alfred/README.md`

| Keyword | Purpose |
|---------|---------|
| `obs` | Vault commands |
| `qn` | Quick note |
| `vs` | Search vault |
| `ss` | Screenshot |
| `api` | Get API keys |

---

## 🔧 MCP Servers

**Location:** `.mcp/`

### Perplexity Research
- **Server:** `.mcp/perplexity-research/server.py`
- **Setup:** `.mcp/perplexity-research/setup.sh`
- **Tools:** `perplexity_search`, `perplexity_deep_research`, `perplexity_compare`

---

## 🚀 Quick Actions

### First Time Setup
```bash
cd ~/Documents/ObsidianVault/.scripts
./setup-integrations.sh
```

### Daily Routine
```bash
# Morning
obs-daily && obs-calendar

# During day
obs-screenshot    # As needed
obs-notion        # Periodic sync

# Evening
obs-metrics       # Update numbers
```

### Add New Script
```bash
# 1. Create script
touch .scripts/my-script.sh
chmod +x .scripts/my-script.sh

# 2. Document in README.md

# 3. Test thoroughly
./scripts/my-script.sh

# 4. Commit
git add .scripts/my-script.sh .scripts/README.md
git commit -m "Add my-script.sh: brief description"
git push
```

---

## 📊 Script Statistics

| Category | Count |
|----------|-------|
| Shell Scripts (.sh) | 13 |
| Python Scripts (.py) | 9 |
| AppleScripts | 1 |
| Alfred Workflows | 6 |
| MCP Servers | 1 |
| Documentation Files | 10 |
| **Total** | **40** |

---

## 🔍 Find by Task

**I want to...**

- **Create a daily note** → `obs-daily` or `create_daily_note_enhanced.sh`
- **Track revenue** → `obs-metrics` or `update_metrics.py`
- **Sync to Notion** → `python3 sync_to_notion.py`
- **Take a screenshot** → `./capture-screenshot.sh` or `⌃⌥⌘S` (Alfred)
- **Get an API key** → `./get-api-key.sh "Key Name"` or `api` in Alfred
- **Search vault** → `vs [query]` in Alfred
- **Create quick note** → `qn` in Alfred or `⌃⌥⌘N`
- **Sync calendar** → `python3 sync_calendar.py`
- **Setup integrations** → `./setup-integrations.sh`
- **Open vault** → `obs-open` or `open-vault.sh`

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Script won't run | `chmod +x script.sh` |
| Command not found | Check PATH, try `source ~/.zshrc` |
| 1Password fails | Run `op signin`, enable CLI in 1Password app |
| Obsidian won't open | Verify vault name is "ObsidianVault" |
| Python import error | `pip3 install [package]` |
| Git push fails | Check remote: `git remote -v` |

---

## 📦 Dependencies

**Required:**
- Obsidian
- Python 3.8+
- Bash/Zsh
- Git

**Optional:**
- 1Password CLI (`brew install --cask 1password-cli`)
- CleanShot X (`https://cleanshot.com/`)
- Alfred Powerpack (`https://www.alfredapp.com/`)
- Notion account (for Notion sync)
- Google Workspace (for Calendar/Gmail)

**Python packages:**
```bash
pip3 install notion-client python-frontmatter google-auth-oauthlib google-api-python-client httpx mcp
```

---

## 🔗 External Links

- **GitHub Repository:** https://github.com/mikefinneran-sudo/obsidian-vault
- **Obsidian:** https://obsidian.md/
- **1Password CLI:** https://developer.1password.com/docs/cli/
- **Alfred:** https://www.alfredapp.com/
- **MCP Protocol:** https://github.com/anthropics/mcp

---

## 📧 Getting Help

1. **Check README.md** - Comprehensive documentation
2. **Check setup guides** - Step-by-step instructions
3. **Read script comments** - Inline documentation
4. **Test with --dry-run** - Available on many scripts
5. **Review CONTRIBUTING.md** - Best practices

---

**Last Updated:** 2025-10-28
**Version:** 2.0
**Author:** Mike Finneran
