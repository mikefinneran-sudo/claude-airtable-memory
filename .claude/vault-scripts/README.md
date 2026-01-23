# ObsidianVault Custom Scripts

**Complete automation toolkit for personal knowledge management and business operations**

This directory contains 22 custom scripts and 6 Alfred workflows that power automated daily notes, metrics tracking, integrations with Notion/Gmail/Calendar, screenshot management, and AI-powered research.

**Author:** Mike Finneran
**Last Updated:** 2025-10-28
**Vault:** ObsidianVault
**Git Repository:** https://github.com/mikefinneran-sudo/obsidian-vault

---

## 📋 Quick Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `create_daily_note_enhanced.sh` | Create/open daily notes | `obs-daily` or `./create_daily_note_enhanced.sh` |
| `update_metrics.py` | Update revenue/activity metrics | `obs-metrics` or `python3 update_metrics.py` |
| `setup-integrations.sh` | Setup 1Password, CleanShot X, Alfred | `./setup-integrations.sh` |
| `sync_to_notion.py` | Sync vault to Notion databases | `python3 sync_to_notion.py` |
| `capture-screenshot.sh` | Screenshot → vault with CleanShot X | `./capture-screenshot.sh` |
| `get-api-key.sh` | Retrieve API keys from 1Password | `./get-api-key.sh "Anthropic API"` |

---

## 📂 Script Categories

### 1. Daily & Weekly Automation

#### `create_daily_note_enhanced.sh`
**Purpose:** Creates comprehensive daily notes with structured templates
**Features:**
- Auto-generates date, day, week, month metadata
- Includes morning setup, priorities, tasks sections
- Business metrics tracking
- Habit tracker with 8 daily habits
- Time log and evening reflection
- Auto-opens in Obsidian with URL scheme

**Usage:**
```bash
obs-daily  # Shell alias
./create_daily_note_enhanced.sh
```

**Template includes:**
- Morning intention & top 3 priorities
- Energy/mood tracking
- Active projects check-in
- Revenue & customer activity
- Communications & meetings
- Time log (morning/afternoon/evening)
- Wins & learnings
- Evening reflection & gratitude

**Location:** `.scripts/create_daily_note_enhanced.sh:1`

---

#### `create_weekly_review_enhanced.sh`
**Purpose:** Generates weekly review notes for reflection and planning
**Features:**
- Week number and date range calculation
- Links to all daily notes in the week
- Weekly wins, challenges, learnings
- Metrics rollup
- Next week planning

**Usage:**
```bash
./create_weekly_review_enhanced.sh
```

**Location:** `.scripts/create_weekly_review_enhanced.sh:1`

---

#### `update_daily_note.py`
**Purpose:** Auto-updates daily notes with project priorities from external sources
**Features:**
- Fetches priorities from WalterSignal projects
- Smart detection of current project phase
- Updates revenue activities and tasks
- Can run on vault open or manual trigger

**Usage:**
```bash
python3 update_daily_note.py
```

**Setup Guide:** `.scripts/DAILY_NOTE_AUTOMATION_SETUP.md`
**Location:** `.scripts/update_daily_note.py:1`

---

### 2. Metrics & Analytics

#### `update_metrics.py`
**Purpose:** Interactive metrics tracking for revenue, customers, and activities
**Features:**
- Update revenue metrics (MRR, customers)
- Log outreach activity (leads, conversations)
- Auto-calculates daily averages
- Updates Dashboard.md progress bars
- Updates Revenue Goals tracking table

**Usage:**
```bash
obs-metrics  # Shell alias
python3 update_metrics.py
```

**Options:**
1. Update revenue metrics → MRR, customers, notes
2. Log outreach activity → Outreach messages sent
3. Log conversations → Customer conversations
4. Quick update → Manual MRR/customer entry

**Location:** `.scripts/update_metrics.py:1`

---

### 3. Integration Scripts

#### `sync_to_notion.py`
**Purpose:** Syncs Obsidian notes to Notion databases with intelligent mapping
**Features:**
- Syncs Projects, Clients, Daily notes to Notion
- Frontmatter → Notion property mapping
- Handles create/update detection
- Configurable folder-to-database mappings
- Dry-run mode for testing
- Comprehensive logging

**Usage:**
```bash
python3 sync_to_notion.py              # Sync all
python3 sync_to_notion.py --folder Projects  # Sync one folder
python3 sync_to_notion.py --dry-run    # Test without syncing
```

**Configuration:**
- Token: `~/.lifehub-notion-token`
- Config: `.scripts/notion-sync-config.json`
- Log: `.scripts/notion-sync.log`

**Setup Guides:**
- `.scripts/NOTION-SETUP-GUIDE.md`
- `.scripts/FLYFLAT-NOTION-SETUP.md`
- `.scripts/FLYFLAT-NOTION-QUICK-SETUP.md`

**Location:** `.scripts/sync_to_notion.py:1`

---

#### `sync_calendar.py`
**Purpose:** Syncs Google Calendar events to Obsidian daily notes
**Features:**
- OAuth2 authentication with Google Calendar
- Fetches today's events
- Adds to daily note's Meetings section
- Handles time zones
- Token caching

**Setup Guide:** `.scripts/CALENDAR-SETUP-GUIDE.md`
**Location:** `.scripts/sync_calendar.py:1`

---

#### `sync_gmail.py`
**Purpose:** Syncs Gmail inbox to Obsidian for email tracking
**Features:**
- OAuth2 authentication with Gmail
- Fetches unread emails
- Creates email tracking notes
- Priority email identification
- Follow-up reminders

**Setup Guide:** `.scripts/GMAIL-SETUP-GUIDE.md`
**Location:** `.scripts/sync_gmail.py:1`

---

#### `setup-notion-sync.sh`
**Purpose:** Automated setup wizard for Notion integration
**Features:**
- Guides through Notion API token setup
- Creates config files
- Tests connection
- Validates database IDs

**Usage:**
```bash
./setup-notion-sync.sh
```

**Location:** `.scripts/setup-notion-sync.sh:1`

---

### 4. Screenshot & Media Management

#### `capture-screenshot.sh`
**Purpose:** Captures screenshots directly to vault with CleanShot X
**Features:**
- Integrates with CleanShot X
- Auto-saves to `Resources/Screenshots/`
- Timestamped filenames
- Returns file path for easy linking

**Usage:**
```bash
./capture-screenshot.sh
```

**Location:** `.scripts/capture-screenshot.sh:1`

---

#### `daily-screenshot.sh`
**Purpose:** Captures screenshots to daily note attachments
**Features:**
- Saves to `Daily/attachments/`
- Date-stamped filenames
- Auto-embeds in today's daily note

**Usage:**
```bash
./daily-screenshot.sh
```

**Location:** `.scripts/daily-screenshot.sh:1`

---

#### `project-screenshot.sh`
**Purpose:** Captures screenshots for specific projects
**Features:**
- Organized by project name
- Auto-links to project notes

**Usage:**
```bash
./project-screenshot.sh <project-name>
```

**Location:** `.scripts/project-screenshot.sh:1`

---

#### `ocr-to-daily.sh`
**Purpose:** OCR screenshots and append text to daily note
**Features:**
- Uses macOS OCR (Vision framework)
- Appends to Quick Notes section
- Preserves original screenshot

**Usage:**
```bash
./ocr-to-daily.sh <screenshot-path>
```

**Location:** `.scripts/ocr-to-daily.sh:1`

---

### 5. Setup & Utilities

#### `setup-integrations.sh`
**Purpose:** Master setup script for 1Password CLI, CleanShot X, and Alfred
**Features:**
- Checks installations (1Password CLI/App, CleanShot X, Alfred)
- Creates necessary directories
- Configures 1Password CLI authentication
- Creates helper scripts (capture-screenshot, get-api-key, open-vault)
- Provides setup instructions for each tool

**Usage:**
```bash
./setup-integrations.sh
```

**Output Scripts:**
- `capture-screenshot.sh`
- `get-api-key.sh`
- `open-vault.sh`

**Location:** `.scripts/setup-integrations.sh:1`

---

#### `get-api-key.sh`
**Purpose:** Securely retrieves API keys from 1Password vault
**Features:**
- Uses 1Password CLI
- Reads from Private vault
- Touch ID authentication
- Returns credential value to stdout

**Usage:**
```bash
./get-api-key.sh "Anthropic API"
./get-api-key.sh "Perplexity API"
export ANTHROPIC_API_KEY=$(./get-api-key.sh "Anthropic API")
```

**Location:** `.scripts/get-api-key.sh:1`

---

#### `open-vault.sh`
**Purpose:** Opens ObsidianVault in Obsidian app
**Usage:**
```bash
./open-vault.sh
```

**Location:** `.scripts/open-vault.sh:1`

---

#### `setup_wizard.py`
**Purpose:** Interactive Python setup wizard for integrations
**Features:**
- Step-by-step configuration
- Validates credentials
- Creates config files
- Tests connections

**Usage:**
```bash
python3 setup_wizard.py
```

**Location:** `.scripts/setup_wizard.py:1`

---

#### `oauth_server.py`
**Purpose:** Local OAuth callback server for Google API authentication
**Features:**
- Handles OAuth redirects
- Exchanges auth codes for tokens
- Saves credentials securely

**Usage:**
```bash
python3 oauth_server.py
```

**Location:** `.scripts/oauth_server.py:1`

---

### 6. Document Syncing

#### `sync-documents-to-gdrive.sh`
**Purpose:** Syncs vault documents to Google Drive backup
**Features:**
- Rsync-based synchronization
- Preserves timestamps
- Excludes .git and node_modules
- Logs sync activity

**Usage:**
```bash
./sync-documents-to-gdrive.sh
```

**Location:** `.scripts/sync-documents-to-gdrive.sh:1`

---

### 7. Project-Specific Scripts

#### `create_flyflat_update.sh`
**Purpose:** Creates FlyFlat project update notes
**Features:**
- Generates weekly FlyFlat status updates
- Links to Notion databases
- Structured update template

**Usage:**
```bash
./create_flyflat_update.sh
```

**Location:** `.scripts/create_flyflat_update.sh:1`

---

#### `waltersignal_education.py`
**Purpose:** Education content automation for WalterSignal project
**Location:** `.scripts/waltersignal_education.py:1`

---

#### `web_dev_education.py`
**Purpose:** Web development education content generation
**Location:** `.scripts/web_dev_education.py:1`

---

### 8. macOS Automation

#### `create-utm-vm.applescript`
**Purpose:** AppleScript for creating UTM virtual machines
**Features:**
- Automates UTM VM creation
- Configures VM settings

**Usage:**
```bash
osascript create-utm-vm.applescript
```

**Location:** `.scripts/create-utm-vm.applescript:1`

---

## 🎯 Alfred Workflows

Located in `.integrations/alfred/workflows/`

### 1. `vault-commands.sh`
**Purpose:** Main Alfred workflow entry point for vault commands
**Keywords:** `obs`, `vault`
**Actions:**
- Quick note creation
- Vault search
- Open specific notes
- Run scripts

---

### 2. `quick-note.sh`
**Purpose:** Create quick capture notes via Alfred
**Keyword:** `qn` or `quick`
**Features:**
- Instant note creation
- Auto-dated filename
- Opens in Obsidian

---

### 3. `search-vault-filter.sh` & `search-vault-action.sh`
**Purpose:** Fast full-text search across vault
**Keyword:** `vs` or `search`
**Features:**
- Full-text search
- Recent files
- Quick open in Obsidian

---

### 4. `screenshot-to-vault.sh`
**Purpose:** Alfred integration for screenshot capture
**Keyword:** `ss` or `screenshot`
**Features:**
- Capture and save to vault
- Auto-link to current note

---

### 5. `get-api-keys-filter.sh` & `get-api-keys-action.sh`
**Purpose:** Quickly retrieve API keys from 1Password
**Keyword:** `api` or `key`
**Features:**
- List available API keys
- Copy to clipboard
- Touch ID authentication

---

## 🤖 MCP Servers

Located in `.mcp/`

### Perplexity Research MCP Server

**Directory:** `.mcp/perplexity-research/`

#### `server.py`
**Purpose:** MCP server providing Perplexity Pro AI research capabilities
**Features:**
- `perplexity_search` - Quick AI search with citations
- `perplexity_deep_research` - Iterative deep-dive analysis
- `perplexity_compare` - Structured entity comparison

**Use Cases:**
- Market research and sizing
- Competitive analysis
- Company background research
- Industry trend analysis

**Location:** `.mcp/perplexity-research/server.py:1`

---

#### `setup.sh`
**Purpose:** Setup script for Perplexity MCP server
**Features:**
- Installs Python dependencies
- Configures API key
- Sets up MCP configuration
- Tests connection

**Usage:**
```bash
cd .mcp/perplexity-research
./setup.sh
```

**Location:** `.mcp/perplexity-research/setup.sh:1`

---

## 🔧 Shell Aliases

These aliases are configured in `~/.zshrc` or `~/.bash_profile`:

```bash
# Daily workflow
alias obs-daily='~/Documents/ObsidianVault/.scripts/create_daily_note_enhanced.sh'
alias obs-metrics='python3 ~/Documents/ObsidianVault/.scripts/update_metrics.py'
alias obs-open='open -a Obsidian ~/Documents/ObsidianVault/Dashboard.md'
alias obs-vault='cd ~/Documents/ObsidianVault && ls -la'

# Integrations
alias obs-notion='python3 ~/Documents/ObsidianVault/.scripts/sync_to_notion.py'
alias obs-calendar='python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py'
alias obs-gmail='python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py'

# Screenshots
alias obs-screenshot='~/Documents/ObsidianVault/.scripts/capture-screenshot.sh'
alias obs-daily-screenshot='~/Documents/ObsidianVault/.scripts/daily-screenshot.sh'

# Utilities
alias obs-api='~/Documents/ObsidianVault/.scripts/get-api-key.sh'
alias obs-setup='~/Documents/ObsidianVault/.scripts/setup-integrations.sh'
```

---

## 📝 Setup Guides

Comprehensive setup documentation is available:

| Guide | Description |
|-------|-------------|
| `QUICK-SETUP.md` | Fast 5-minute setup for core features |
| `DAILY_NOTE_AUTOMATION_SETUP.md` | Daily note automation with Shell Commands plugin |
| `NOTION-SETUP-GUIDE.md` | Notion integration setup |
| `FLYFLAT-NOTION-SETUP.md` | FlyFlat-specific Notion setup |
| `FLYFLAT-NOTION-QUICK-SETUP.md` | Quick FlyFlat Notion integration |
| `CALENDAR-SETUP-GUIDE.md` | Google Calendar integration |
| `GMAIL-SETUP-GUIDE.md` | Gmail integration |
| `SHELL-COMMANDS-SETUP-GUIDE.md` | Obsidian Shell Commands plugin config |

---

## 🛠️ Dependencies

### Required Tools
- **Obsidian** - Note-taking app
- **Python 3.8+** - For Python scripts
- **Bash/Zsh** - For shell scripts
- **Git** - Version control

### Optional Tools
- **1Password CLI** - Secure credential management
- **CleanShot X** - Screenshot capture
- **Alfred** - macOS launcher (workflows)
- **Notion** - For Notion sync
- **Google Workspace** - For Calendar/Gmail sync

### Python Dependencies
```bash
pip3 install notion-client python-frontmatter google-auth-oauthlib google-api-python-client httpx mcp
```

---

## 🚀 Quick Start

### 1. Initial Setup
```bash
cd ~/Documents/ObsidianVault/.scripts
./setup-integrations.sh
```

### 2. Configure Shell Aliases
Add to `~/.zshrc`:
```bash
# ObsidianVault aliases
alias obs-daily='~/Documents/ObsidianVault/.scripts/create_daily_note_enhanced.sh'
alias obs-metrics='python3 ~/Documents/ObsidianVault/.scripts/update_metrics.py'
alias obs-open='open -a Obsidian ~/Documents/ObsidianVault/Dashboard.md'
alias obs-vault='cd ~/Documents/ObsidianVault && ls -la'
```

Then reload: `source ~/.zshrc`

### 3. Daily Workflow
```bash
# Morning
obs-daily          # Create today's note
obs-calendar       # Sync today's meetings
obs-open           # Open dashboard

# During day
obs-screenshot     # Capture screenshots
obs-notion         # Sync to Notion

# Evening
obs-metrics        # Update revenue metrics
```

---

## 📊 Script Statistics

- **Total Scripts:** 22
- **Shell Scripts:** 13
- **Python Scripts:** 9
- **AppleScripts:** 1
- **Alfred Workflows:** 6
- **MCP Servers:** 1
- **Documentation Files:** 8
- **Total Lines of Code:** ~3,500+

---

## 🔐 Security Notes

**API Keys & Credentials:**
- Never commit API keys to git (added to `.gitignore`)
- Use 1Password CLI for secure storage
- Token files stored in home directory (`~/.lifehub-notion-token`)
- OAuth tokens cached securely with encryption

**Git Safety:**
- `.env` files excluded
- Token files excluded
- OAuth credential files excluded
- Personal database IDs sanitized in examples

---

## 📦 Git Repository

**Repository:** https://github.com/mikefinneran-sudo/obsidian-vault
**Branch:** main
**Private:** Yes (contains personal data)

### Commit Guidelines
```bash
# Add new scripts
git add .scripts/

# Commit with descriptive message
git commit -m "Add [script-name]: [brief description]"

# Push to remote
git push origin main
```

---

## 🧪 Testing

### Test Script Execution
```bash
# Test daily note creation
./create_daily_note_enhanced.sh

# Test metrics update (dry run)
python3 update_metrics.py

# Test Notion sync (dry run)
python3 sync_to_notion.py --dry-run

# Test API key retrieval
./get-api-key.sh "Anthropic API"
```

### Verify Integrations
```bash
# Check 1Password
op account list

# Check CleanShot X
ls "/Applications/CleanShot X.app"

# Check Obsidian
ls "/Applications/Obsidian.app"
```

---

## 🐛 Troubleshooting

### Common Issues

**Daily note not opening:**
- Verify Obsidian is installed
- Check vault name matches "ObsidianVault"
- Try manual open: `open "obsidian://open?vault=ObsidianVault&file=Daily/2025-10-28"`

**Metrics not updating:**
- Check file paths in `update_metrics.py:12-14`
- Verify Dashboard.md exists
- Check Python 3 is installed: `python3 --version`

**Notion sync failing:**
- Verify token exists: `cat ~/.lifehub-notion-token`
- Check config: `.scripts/notion-sync-config.json`
- Test connection: `python3 sync_to_notion.py --dry-run`
- Review logs: `cat .scripts/notion-sync.log`

**1Password CLI not working:**
- Sign in: `op signin`
- Enable CLI in 1Password app: Settings → Developer
- Check authentication: `op account list`

---

## 📚 Additional Resources

- [Obsidian Documentation](https://help.obsidian.md/)
- [Notion API Documentation](https://developers.notion.com/)
- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
- [MCP Protocol Documentation](https://github.com/anthropics/mcp)
- [CleanShot X Documentation](https://cleanshot.com/help)

---

## 📧 Support

For issues or questions:
- Check documentation files in `.scripts/`
- Review setup guides
- Check script comments for inline documentation
- Test with dry-run flags when available

---

## 📅 Version History

**v2.0** - 2025-10-28
- Added comprehensive documentation
- Reorganized scripts by category
- Added MCP server documentation
- Enhanced setup guides

**v1.5** - 2025-10-27
- Added FlyFlat project scripts
- Enhanced Alfred workflows
- Improved error handling

**v1.0** - 2025-10-20
- Initial script collection
- Basic automation setup
- Core daily note functionality

---

**Last Updated:** 2025-10-28
**Maintained By:** Mike Finneran
**License:** Private Use
