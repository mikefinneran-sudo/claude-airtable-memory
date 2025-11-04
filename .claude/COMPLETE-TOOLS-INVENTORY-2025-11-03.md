# Complete Tools & Skills Inventory

**Date**: November 3, 2025
**Purpose**: Comprehensive audit of all available tools, integrations, and automation

---

## 1. MCP Servers (AI-Powered Tools)

### ✅ Active & Working
- **perplexity-research** - Web search and research via Perplexity Pro API
  - Location: `/Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research`
  - Status: ✓ Connected
  - **Use for**: Current events, market research, competitive analysis

- **memory** - Persistent knowledge graphs and entity tracking
  - Command: `npx -y @modelcontextprotocol/server-memory`
  - Status: ✓ Connected
  - **Use for**: Long-term project context, client preferences, technical patterns

- **puppeteer** - Browser automation, web scraping, screenshots
  - Command: `npx -y @modelcontextprotocol/server-puppeteer`
  - Status: ✓ Connected
  - **Use for**: Parse.bot-style scraping, dynamic content, visual testing

- **airtable** - Project management, backlog tracking, structured data
  - Command: `npx -y airtable-mcp-server`
  - Status: ✓ Connected
  - **Use for**: Project tracking, backlog management, WalterSignal ERP

- **gmail** - Email management (read, send, search, label)
  - Command: `npx -y @gongrzhe/server-gmail-autoauth-mcp`
  - Status: ✓ Connected
  - **Use for**: Proposals, follow-ups, client communication

### ⚠️ Failing (Needs Fix)
- **apple-notes** - Primary note-taking and knowledge management
  - Command: `uvx apple-notes-mcp`
  - Status: ✗ Failed to connect
  - **ACTION NEEDED**: Investigate and fix connection issue

### 📊 MCP Usage in CLAUDE.md
- ✅ All working MCPs documented in "Tools & Integrations"
- ❌ Apple Notes marked as available but actually broken
- ✅ Tool usage guidelines documented

---

## 2. LaunchAgents (Automated Tasks)

### ✅ Active Automations

**1. S3 Backups** (NEW - Nov 2)
- File: `com.mikefinneran.claude-s3-backup.plist`
- Schedule: Daily at 2:00 AM
- Script: `~/.claude/scripts/backup-to-s3.sh`
- Logs: `~/.claude/logs/s3-backup.log`
- Status: ✅ Working (tested Nov 2)

**2. Daily Notes**
- File: `com.lifehub.dailynote.plist`
- Purpose: Auto-create daily notes
- Status: ✅ Active

**3. Google Drive Sync**
- File: `com.lifehub.gdrive-sync.plist`
- Purpose: Sync documents to Google Drive
- Status: ✅ Active

**4. Weekly Review**
- File: `com.lifehub.weeklyreview.new.plist`
- Purpose: Weekly review automation
- Status: ✅ Active

**5. Airtable Sync**
- File: `com.mikefinneran.airtable-sync.plist`
- Purpose: Sync Obsidian to Airtable
- Status: ✅ Active

### 📊 LaunchAgents in CLAUDE.md
- ✅ S3 backup documented (just added)
- ✅ Listed in "Known Automations"
- ⚠️ Other LaunchAgents not documented (daily notes, gdrive-sync, weekly review, airtable-sync)
- **ACTION**: Add all LaunchAgents to CLAUDE.md

---

## 3. Shell Aliases & Functions

### Navigation Aliases
```bash
docs          # Google Drive Documents folder
gdocs         # Same as docs
vault         # cd ~/Documents/ObsidianVault
work          # cd ~/Documents/Work
```

### Obsidian Vault Aliases
```bash
obs-daily     # Create daily note
obs-metrics   # Update metrics
obs-open      # Open Obsidian Dashboard
obs-vault     # cd to vault and list
obs-sync-email # Sync Gmail to Obsidian
obs-sync-cal  # Sync calendar to Obsidian
obs-sync-all  # Sync both email and calendar
obs-sync-drive # Sync documents to Google Drive

vopen         # Open Obsidian
vdaily        # Create and open daily note
vmorning      # Morning routine script
vevening      # Evening routine script
vgranola      # Granola export script
vscreenshot   # Daily screenshot capture
vgit          # Git status in vault
vpush         # Git commit and push vault
```

### 1Password Aliases (NEW)
```bash
1pass-guide   # Full security guide
1pass-quick   # Quick reference
1pass-summary # Migration summary
```

### Airtable Aliases
```bash
airtable-sync # Sync to Airtable
at-sync       # Short version
at-log        # View sync logs
```

### 📊 Aliases in CLAUDE.md
- ❌ Shell aliases NOT documented in CLAUDE.md
- ❌ No quick reference for available shortcuts
- **ACTION**: Add alias quick reference section to CLAUDE.md

---

## 4. Custom Scripts in ~/.claude/scripts/

### Session Management
- **start-session.sh** - Initialize Claude session
- **save-session-memory.sh** - Save session progress
- **resume-work.sh** - Resume previous session
- **continue-enhanced.sh** - Enhanced continue command

### Context & Memory
- **context-manager.sh** - Manage context files
- **memory-search.sh** - Search memory files
- **generate-activity-summary.py** - Generate activity summaries

### S3 & Backup
- **backup-to-s3.sh** - Daily S3 backup script (NEW)
- **restore-from-s3.sh** - Restore from S3
- **setup-s3-integration.sh** - Setup S3 integration
- **setup-automated-s3-backups.sh** - Setup LaunchAgent

### 1Password Integration
- **1password-session.sh** - Manage 1Password sessions
- **check-1password-session.sh** - Check session status

### Project Management
- **init-project-session.sh** - Initialize project session
- **research-project.sh** - Research project helper
- **scan-project-scripts.sh** - Scan for project scripts

### Airtable Integration
- **create-airtable-bases.py** - Create Airtable bases
- **log-activity-to-airtable.sh** - Log activities to Airtable
- **setup-activity-tracking-airtable.py** - Setup activity tracking
- **track-api-usage.py** - Track API usage

### Utilities
- **setup-aliases.sh** - Setup shell aliases
- **open-in-editor.sh** - Open files in editor
- **archive-custom-script.sh** - Archive old scripts
- **generate-warp-configs.sh** - Generate Warp terminal configs

### 📊 Scripts in CLAUDE.md
- ❌ Custom scripts NOT documented in CLAUDE.md
- ❌ No quick reference for available scripts
- **ACTION**: Add scripts reference to CLAUDE.md

---

## 5. Obsidian Vault Scripts (~/.scripts/)

### Daily Workflow
- **create_daily_note_enhanced.sh** - Enhanced daily notes
- **create_weekly_review_enhanced.sh** - Weekly review generator
- **create_flyflat_update.sh** - FlyFlat status updates
- **morning-routine.sh** (referenced by alias)
- **evening-routine.sh** (referenced by alias)

### Sync & Integration
- **sync_gmail.py** - Gmail to Obsidian sync
- **sync_calendar.py** - Calendar to Obsidian sync
- **sync-documents-to-gdrive.sh** - Document sync to Google Drive
- **airtable-sync.py** - Main Airtable sync script

### Tracking & Metrics
- **anthropic-api-tracker.py** - Track Anthropic API usage
- **update_metrics.py** (referenced by alias)
- **run-all-trackers.sh** - Run all cost tracking scripts

### Automation
- **granola-export.sh** (referenced by alias)
- **daily-screenshot.sh** (referenced by alias)
- **capture-screenshot.sh** - Screenshot capture utility

### Craft Integration (NEW - Nov 2)
- **craft-full-auto.applescript** - Full Craft automation
- **craft-import-all.sh** - Import all to Craft
- **craft-import-files.applescript** - Import specific files
- **craft-setup-automation.applescript** - Setup Craft automation

### 📊 Obsidian Scripts in CLAUDE.md
- ❌ Obsidian scripts NOT documented
- ❌ Aliases documented but not linked to underlying scripts
- **ACTION**: Add Obsidian scripts section

---

## 6. iTerm2 Integration

### Documentation Available
- **EXPERT_GUIDE.md** (21KB) - Comprehensive iTerm2 capabilities
- **CLAUDE_CODE_WORKFLOWS.md** (16KB) - Development workflows
- **INDEX.md** (8.7KB) - Overview and navigation
- **QUICK_REFERENCE.md** (4.9KB) - Essential shortcuts
- **PERSISTENT_MEMORY_INTEGRATION.md** (8.4KB) - Memory integration
- **AUTOLAUNCH_SETUP.md** (4.9KB) - Auto-launch configuration

### Key Features Available
- Shell integration (command marks, navigation)
- Split pane workflows
- Triggers (regex-based automation)
- Dynamic profiles (per-project configuration)
- Python API for programmatic control
- tmux integration mode
- Status bar customization

### 📊 iTerm2 in CLAUDE.md
- ✅ Fully documented with behavioral rules
- ✅ Natural language integration guidelines
- ✅ Response patterns and examples
- ✅ Knowledge base location referenced

---

## 7. Custom Slash Commands (~/.claude/commands/)

### Available Commands
1. **/backlog** - Add item to backlog and close tab
2. **/code-review** - Perform thorough code review
3. **/explain-code** - Explain code architecture and patterns
4. **/optimize** - Analyze and optimize code performance
5. **/plan-feature** - Plan feature implementation with TDD
6. **/research** - Create comprehensive research document
7. **/save-guide** - Save content as guide document

### 📊 Slash Commands in CLAUDE.md
- ❌ Slash commands NOT documented in CLAUDE.md
- ❌ Users may not know these exist
- **ACTION**: Add slash commands reference

---

## 8. Alfred Snippets (NEW - Nov 2)

### Available Snippets
- `;ctx` - Session start - load context
- `;cont` - Continue project
- `;deep` - Deep dive into project
- `;weekly` - Weekly review
- `;save` - Save session
- `;proj` - Show all projects
- `;health` - Health check
- `;restore` - Restore from S3
- `;ws` - WalterSignal shortcut
- `;backlog` - Add to backlog
- `;yesterday` - Yesterday's work
- `;focus` - Update week focus

### 📊 Alfred Snippets in CLAUDE.md
- ❌ Alfred snippets NOT documented in CLAUDE.md
- ✅ Documentation exists: `ALFRED-SNIPPETS-GUIDE.md`
- **ACTION**: Add Alfred snippets section to CLAUDE.md

---

## 9. Project-Specific Tools

### WalterSignal
- **launch_dashboard.sh** - Launch dashboard
- **build_airtable_pm_system.py** - Build PM system
- **email-campaign-config.py** - Email campaign configuration
- **Products/DocuFlow/** - NDA generation and document workflows

### FlyFlat
- **/.scripts/** directory exists (need to explore)

### LifeHub
- Multiple archived versions with scripts
- Active: **Projects/notion-life-hub/.scripts/**

### 📊 Project Tools in CLAUDE.md
- ❌ Project-specific tools NOT documented
- ❌ No quick access to project utilities
- **ACTION**: Add project tools reference

---

## 10. Security & Credentials

### 1Password Integration
- ✅ CLI installed and working
- ✅ Scripts for session management
- ✅ Documentation:
  - `1PASSWORD_SECURITY_GUIDE.md`
  - `1PASSWORD_QUICK_REFERENCE.md`
  - `1PASSWORD_MIGRATION_SUMMARY.md`

### Environment Variables
- `S3_BACKUP_BUCKET=mikefinneran-personal`
- `AIRTABLE_TOKEN` (via 1Password)
- AWS credentials configured

### 📊 Security in CLAUDE.md
- ✅ Security best practices documented
- ✅ 1Password referenced for credential management
- ✅ What never to include in CLAUDE.md

---

## Summary: What's Missing from CLAUDE.md

### ❌ NOT Documented (Should Be)

1. **Shell Aliases Quick Reference**
   - 25+ aliases available but not listed
   - Users typing full commands when shortcuts exist

2. **Custom Scripts in ~/.claude/scripts/**
   - 30+ scripts available
   - No quick reference or usage guide

3. **Obsidian Vault Scripts**
   - 100+ scripts in vault
   - Aliases reference scripts but scripts not documented

4. **Slash Commands**
   - 7 custom commands available
   - Not documented in CLAUDE.md (users may not know they exist)

5. **Alfred Snippets** (NEW)
   - 12 snippets just created
   - Not yet added to CLAUDE.md

6. **LaunchAgents (Full List)**
   - 5 LaunchAgents active
   - Only S3 backup documented
   - Missing: daily notes, gdrive-sync, weekly review, airtable-sync

7. **Project-Specific Tools**
   - WalterSignal has launch scripts
   - FlyFlat has .scripts directory
   - No documentation of project utilities

8. **MCP Server Health**
   - apple-notes MCP is failing
   - No health check for this in CLAUDE.md

---

## Recommendations

### 🔴 Critical (Do Now)

1. **Fix Apple Notes MCP**
   - Currently failing to connect
   - Primary note-taking tool unavailable

2. **Add Aliases to CLAUDE.md**
   - Users retyping long commands
   - Add "Quick Access Aliases" section

3. **Document Slash Commands**
   - 7 commands available but hidden
   - Add to CLAUDE.md "Custom Commands" section

### 🟡 Important (This Week)

4. **Add All LaunchAgents to CLAUDE.md**
   - Only 1 of 5 documented
   - Users don't know what's automated

5. **Add Alfred Snippets Section**
   - Just created, not documented in CLAUDE.md
   - Reference installation and usage

6. **Document ~/.claude/scripts/**
   - 30+ scripts available
   - Create quick reference section

### 🟢 Nice to Have (This Month)

7. **Document Obsidian Scripts**
   - Link aliases to underlying scripts
   - Show what each automation does

8. **Add Project Tools Section**
   - WalterSignal launch scripts
   - FlyFlat utilities
   - Quick project access

9. **Create Tools Health Check Command**
   - Verify all MCPs connected
   - Check all LaunchAgents running
   - Validate all scripts executable

---

## Tools We Should Use More

### Underutilized

1. **Memory MCP** - Connected but rarely used
   - Should track: client preferences, project decisions, patterns
   - Use for: Long-term context that doesn't fit in CLAUDE.md

2. **Puppeteer MCP** - Available but not in active use
   - Great for: Web scraping, visual testing, screenshots
   - Could use for: WalterSignal competitive research

3. **Slash Commands** - Exist but unknown
   - `/research` could replace manual research prompts
   - `/plan-feature` for structured feature planning
   - `/code-review` for systematic code reviews

4. **Custom Scripts in ~/.claude/scripts/**
   - Many scripts created but not used
   - Example: `research-project.sh`, `init-project-session.sh`

5. **iTerm2 Triggers**
   - Available but not set up for projects
   - Could automate: Test notifications, build alerts, error highlighting

### Missing Integration Opportunities

1. **Alfred + Slash Commands**
   - Could create Alfred snippets for slash commands
   - Example: `;research` → `/research [topic]`

2. **Memory MCP + Project Context**
   - Store project decisions in memory graph
   - Query for "why did we choose X?"

3. **Airtable + Daily Workflow**
   - Auto-log completed tasks to Airtable
   - Use `log-activity-to-airtable.sh` more

4. **Puppeteer + WalterSignal**
   - Automate competitor research
   - Monitor pricing changes
   - Screenshot dashboard states

---

## Next Actions

**Immediate (Today):**
1. Fix apple-notes MCP connection
2. Add aliases section to CLAUDE.md
3. Add slash commands to CLAUDE.md
4. Add Alfred snippets reference

**This Week:**
5. Document all 5 LaunchAgents in CLAUDE.md
6. Create scripts quick reference
7. Test and document Memory MCP usage

**This Month:**
8. Set up iTerm2 triggers for WalterSignal
9. Create project tools documentation
10. Build tools health check command

---

**Created**: November 3, 2025
**Status**: Complete audit ready for review
**Next Review**: Weekly (Mondays)
