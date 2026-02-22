# Automation Locations Reference

**ALWAYS CHECK THESE FIRST** when user mentions scheduled tasks, cron jobs, or "runs at midnight"

## Scheduled Task Locations

### macOS LaunchAgents (PRIMARY)
```bash
ls ~/Library/LaunchAgents/
```

**Active Automations:**
- `com.mikefinneran.research-update.plist` - Perplexity research database update (daily midnight)
- `com.lifehub.dailynote.plist` - Daily note with Calendar + Reminders (daily 7 AM)
- `com.mikefinneran.task-router.plist` - Route Inbox tasks by tag (every 15 min)
- `com.lifehub.weeklyreview.new.plist` - Weekly review
- `com.lifehub.gdrive-sync.plist` - Google Drive sync
- `com.flyflat.weeklyupdate.plist` - Fly Flat weekly update

- `com.mikefinneran.git-auto-push.plist` - Git auto-push WalterSignal monorepo (daily 11 PM)

**NAS Backup Automations (added 2026-02-12):**
- `com.mikefinneran.mount-nas.plist` - Mount NAS shares at login (RunAtLoad)
- `com.mikefinneran.backup-code-nas.plist` - Backup ~/Code/ to NAS (hourly)
- `com.mikefinneran.backup-vault-nas.plist` - Backup ObsidianVault to NAS (every 15 min)
- `com.mikefinneran.backup-claude-configs-nas.plist` - Backup ~/.claude/ to NAS (daily 2 AM)
- `com.mikefinneran.backup-desktop-nas.plist` - Backup ~/Desktop/ to NAS (daily 3 AM)
- `com.mikefinneran.sync-nas-to-s3.plist` - NAS → S3 offsite sync (weekly Sunday 4 AM)
- `com.mikefinneran.backup-health-alert.plist` - Backup health alert + log rotation (daily 8 AM)
- `com.mikefinneran.backup-dgx-nas.plist` - DGX Spark → NAS backup (weekly Wed 2 AM)

- `com.mikefinneran.context-check.plist` - Context files health check (weekly Sunday 3 AM)
- `com.waltersignal.campaign-health.plist` - Instantly campaign health monitor (daily 8 AM)
- `com.mikefinneran.slack-bot.plist` - Slack thread-export + action bot (KeepAlive, Socket Mode)

**Disabled:**
- `com.mikefinneran.airtable-sync.plist` - DISABLED (2026-02-07): data migrated to SQLite
- `com.mikefinneran.github-airtable-sync.plist` - DISABLED (2026-02-07): no longer syncing to Airtable
- `com.mikefinneran.claude-s3-backup.plist` - DISABLED (2026-02-16): replaced by NAS → S3 sync (was duplicate tar.gz path)

### Cron (SECONDARY)
```bash
crontab -l
```

Currently: No active crontab (uses LaunchAgents instead)

### Script Directories

**User Scripts:**
- `~/Documents/ObsidianVault/.scripts/` - Main automation scripts
- `~/.claude/scripts/` - Claude-specific scripts

**Project Scripts:**
- Pattern: `~/Documents/ObsidianVault/Projects/[PROJECT]/.scripts/`
- Example: `~/Documents/ObsidianVault/Projects/Preplexity Pro Research/.scripts/`

## Known Automation Scripts

### Perplexity Research Update
**Script:** `/Users/mikefinneran/Documents/ObsidianVault/Projects/Preplexity Pro Research/.scripts/update_research_database.py`

**Schedule:** Daily at midnight (LaunchAgent: com.mikefinneran.research-update.plist)

**Manual Run:**
```bash
python3 "/Users/mikefinneran/Documents/ObsidianVault/Projects/Preplexity Pro Research/.scripts/update_research_database.py"
```

**What it does:**
- Scans Perplexity research files
- Updates MASTER_RESEARCH_DATABASE.md
- Creates daily summary in Daily_Summaries/
- Tracks new/orphaned files

**Output:**
- Summary: `Projects/Preplexity Pro Research/Daily_Summaries/YYYY-MM-DD-research-update.md`
- Database: `Projects/Preplexity Pro Research/MASTER_RESEARCH_DATABASE.md`

### Daily Note with Calendar + Reminders
**Script:** `/Users/mikefinneran/Documents/ObsidianVault/.scripts/create_daily_note_enhanced.sh`

**Schedule:** Daily at 7 AM (LaunchAgent: com.lifehub.dailynote.plist)

**Manual Run:**
```bash
/Users/mikefinneran/Documents/ObsidianVault/.scripts/create_daily_note_enhanced.sh
```

**What it does:**
- Creates daily note in `Daily/YYYY-MM-DD.md`
- Injects today's calendar events from Apple Calendar
- Injects due/overdue reminders from Apple Reminders
- Skips if note already exists

**Supporting Scripts:**
- `~/.claude/scripts/get-calendar-events.scpt` - Extracts calendar events
- `~/.claude/scripts/get-due-reminders.scpt` - Extracts due reminders

---

### Task Router (Inbox Triage)
**Script:** `/Users/mikefinneran/.claude/scripts/route-inbox-tasks.sh`

**Schedule:** Every 15 minutes (LaunchAgent: com.mikefinneran.task-router.plist)

**Manual Run:**
```bash
~/.claude/scripts/route-inbox-tasks.sh
```

**What it does:**
- Scans Apple Reminders "Inbox" list
- Routes tasks to destination lists based on tags in title:
  - `#ws` or `#work` → Work list
  - `#personal` → Personal list
  - `#grocery` or `#groceries` → Grocery list
  - No tag → Stays in Inbox for manual triage
- Removes tag from task title after routing

**Capture Methods:**
- Siri: "Hey Siri, remind me to #ws Review proposal"
- Shortcuts: Create "Quick Task" and "Work Task" shortcuts
- Claude Code: Use apple-reminders MCP

**Logs:** `~/.claude/logs/task-router.log`

---

### WalterSignal News Updater
**Script:** `/Users/mikefinneran/.claude/scripts/waltersignal-news-updater.py`

**Schedule:** Daily at 12:30 AM (LaunchAgent — check for plist)

**Manual Run:**
```bash
python3 ~/.claude/scripts/waltersignal-news-updater.py
```

**What it does:**
- Fetches top 5 AI/GTM news via Perplexity API
- Stores articles in SQLite (`~/Code/WalterSignal/walterfetch-v2/data/news.db`)
- Exports to JSON and deploys to Lightsail (`/var/www/html/api/news.json`)
- **Migrated from Airtable to SQLite on 2026-02-07**

---

### Cost Tracking Automations
**Script:** `/Users/mikefinneran/Documents/ObsidianVault/.scripts/run-all-trackers.sh`

**Schedule:** Weekly (Sundays 9 AM) - NOT CURRENTLY IN CRON

**Trackers:**
- Gmail subscription invoices
- GitHub Actions usage
- Anthropic API usage
- Perplexity API cost analysis

**Manual Run:**
```bash
cd ~/Documents/ObsidianVault/.scripts/
./run-all-trackers.sh
```

### Git Auto-Push (WalterSignal)
**Script:** `/Users/mikefinneran/.claude/scripts/git-auto-push.sh`

**Schedule:** Daily at 11 PM (LaunchAgent: com.mikefinneran.git-auto-push.plist)

**Manual Run:**
```bash
~/.claude/scripts/git-auto-push.sh
```

**What it does:**
- Checks for unpushed commits in `~/Code/WalterSignal/`
- Pushes to `origin main` if any exist
- Logs to `~/.claude/logs/git-auto-push.log`

**Related:**
- PostToolUse hook `git-push-reminder.sh` shows unpushed count after `git commit`
- Pre-commit hooks block `.env`, private keys, files >500KB

---

### NAS Backup System (UGREEN DH2300)
**NAS IP:** `192.168.68.70` | **Shares:** backups, archives, timemachine
**Mount Points:** `/Volumes/IronWolf-Backups`, `/Volumes/IronWolf-Archives`

| Script | Schedule | Source → Dest |
|--------|----------|---------------|
| `mount-nas.sh` | Login (RunAtLoad) | Mounts SMB shares |
| `backup-code-to-nas.sh` | Hourly | `~/Code/` → NAS backups/code/ |
| `backup-vault-to-nas.sh` | Every 15 min | `~/Documents/ObsidianVault/` → NAS backups/vault/ |
| `backup-claude-configs-to-nas.sh` | Daily 2 AM | `~/.claude/` → NAS backups/claude-configs/ |
| `backup-desktop-to-nas.sh` | Daily 3 AM | `~/Desktop/` → NAS backups/desktop/ |
| `sync-nas-to-s3.sh` | Weekly Sun 4 AM | Full NAS → S3: vault, configs, files, cloud-imports, desktop (STANDARD_IA) |
| `archive-project.sh` | Manual | `~/Code/<name>/` → NAS archives/projects/ |
| `archive-client-file.sh` | Manual | File → NAS archives/clients/ |
| `backup-dgx-to-nas.sh` | Weekly Wed 2 AM | DGX Spark → NAS backups/dgx/ (data + code, skip venvs/models) |
| `backup-status.sh` | Manual | Dashboard: all backup health (parses logs for errors) |
| `backup-health-alert.sh` | Daily 8 AM | Scans logs for persistent failures → macOS notification |
| `rotate-backup-logs.sh` | Daily 8 AM (with alerter) | Truncates logs to 500 lines |

### DGX Spark On-Box Backup
**Host:** `192.168.68.62` (SSH alias: `dgx`) | **External SSD:** `/mnt/models` (3.6TB)

| Script | Schedule | Source → Dest |
|--------|----------|---------------|
| `backup-to-ssd.sh` | Daily 3 AM (crontab) | DGX home → `/mnt/models/backups/` (data + code, skip venvs/models) |

**Log:** `/home/mikefinneran/backup-to-ssd.log` (self-rotating at 500 lines)
**Manual Run:** `ssh dgx /home/mikefinneran/backup-to-ssd.sh`

**SMB Tuning:** `/etc/nsmb.conf` — signing off, notify off, dir cache 1024, streams on.
**TCC:** `/bin/bash` + `/usr/bin/rsync` must have Full Disk Access (System Settings → Privacy).

**Manual Run:**
```bash
mount-nas              # Mount NAS shares
backup-status          # Show all backup health (with failure detection)
archive-project Foo    # Archive ~/Code/Foo/ to NAS
archive-client f.xlsx ClientName  # Archive deliverable
```

**Logs:** `~/.claude/logs/backup-{code,vault,claude-configs,desktop}-nas.log`, `mount-nas.log`, `sync-nas-to-s3.log`, `backup-health-alert.log`

**S3 Bucket Layout** (`s3://mikefinneran-personal/`) — red-teamed 2026-02-16:
| S3 Prefix | Size | Source | Notes |
|-----------|------|--------|-------|
| `obsidian-vault-backup/` | 78MB | NAS backups/vault/ | Weekly sync. Irreplaceable notes/research. |
| `claude-configs/` | 24MB | NAS backups/claude-configs/ | Weekly sync. Scripts, guides, frameworks. Excludes debug/, projects/tasks/, statsig/. |
| `nas-files/` | 4GB | NAS files/ | Weekly sync. Client deliverables, documents. |
| `walterfetch-backup/` | 74MB | Manual | leads.db snapshots. Enriched lead data. |

**NOT on S3 (by design):**
- `cloud-imports` — originals still in Google Drive/iCloud (triple-redundant)
- `desktop` — staging area; permanent files belong in nas-files
- `code` — all repos on GitHub
- DGX fine-tune data (ChromaDB, models) — re-embeddable/downloadable, too large for cloud

**Deleted 2026-02-16:** claude-backups (6GB legacy tar.gz), obsidian-vault-archive-2026-01-07 (1.6GB stale snapshot), nas-cloud-imports (13.7GB redundant), nas-desktop (40MB staging), agreements/dpa/scoping-logos (orphans)

---

### Context Files Health Check
**Script:** `/Users/mikefinneran/.claude/scripts/context-check.sh`

**Schedule:** Weekly Sunday 3 AM (LaunchAgent: com.mikefinneran.context-check.plist) + manual alias `context-check`

**Manual Run:**
```bash
context-check
```

**What it does:**
- Validates MEMORY.md (<200 lines) and CLAUDE.md (<600 lines)
- Checks topic files in `memory/` for line count limits
- Detects broken `memory/*.md` and `~/Code/*/CLAUDE.md` pointers
- Flags duplicate H2 headers across context files
- Warns on dated sections older than 90 days

**Exit code:** Number of issues found (0 = all clean)

---

## Search Protocol for "Runs at Midnight" Tasks

**ALWAYS follow this order:**

1. **Check LaunchAgents** (10 sec)
   ```bash
   ls ~/Library/LaunchAgents/ | grep -i [keyword]
   cat ~/Library/LaunchAgents/[found-file].plist
   ```

2. **Check Crontab** (5 sec)
   ```bash
   crontab -l
   ```

3. **Search script directories** (10 sec)
   ```bash
   find ~/Documents/ObsidianVault -name "*[keyword]*" -type f
   ```

4. **ONLY THEN** consider building new tool

## Common Mistakes to Avoid

❌ **DON'T:**
- Start with browser automation
- Build new tools without checking existing
- Ignore when user says "we already have this"
- Search random locations first

✅ **DO:**
- Check LaunchAgents first for scheduled tasks
- Read plist files to find script paths
- Run existing scripts before building new ones
- Listen when user mentions "runs every night"

## Quick Commands

**List all LaunchAgents:**
```bash
ls -la ~/Library/LaunchAgents/
```

**Find script in LaunchAgent:**
```bash
grep -A2 "ProgramArguments" ~/Library/LaunchAgents/[name].plist
```

**Check LaunchAgent status:**
```bash
launchctl list | grep [keyword]
```

**Run script from LaunchAgent manually:**
```bash
# Extract path from plist, then run directly
python3 "/path/from/plist"
```

---

### Instantly Campaign Health Monitor
**Script:** `/Users/mikefinneran/Code/WalterSignal/walterfetch-v2/scripts/campaign_health_monitor.py`

**Schedule:** Daily at 8 AM (LaunchAgent: com.waltersignal.campaign-health.plist)

**Manual Run:**
```bash
# Full run
~/Code/WalterSignal/walterfetch-v2/venv/bin/python3 ~/Code/WalterSignal/walterfetch-v2/scripts/campaign_health_monitor.py

# Preview only (no delivery)
~/Code/WalterSignal/walterfetch-v2/venv/bin/python3 ~/Code/WalterSignal/walterfetch-v2/scripts/campaign_health_monitor.py --dry-run

# Verbose preview
~/Code/WalterSignal/walterfetch-v2/venv/bin/python3 ~/Code/WalterSignal/walterfetch-v2/scripts/campaign_health_monitor.py --dry-run --verbose

# Basic report (no AI)
~/Code/WalterSignal/walterfetch-v2/venv/bin/python3 ~/Code/WalterSignal/walterfetch-v2/scripts/campaign_health_monitor.py --skip-ai
```

**What it does:**
- Pulls campaign + account analytics from Instantly API V2
- Evaluates against thresholds (bounce >2% critical, >1% warning, open <15%, etc.)
- Compares 3-day trends for bounce rate increases
- Stores history in SQLite (`data/campaign_health.db`)
- Generates AI summary via Claude Haiku (with `--skip-ai` fallback)
- Delivers report to Apple Notes (`[WalterSignal] Campaign Health - YYYY-MM-DD`)
- Sends macOS notification for CRITICAL alerts

**Logs:** `~/.claude/logs/campaign-health.log`, `campaign-health-error.log`

---

### File Consolidation & NAS Migration (2026-02-13)
**One-time scripts** — used to consolidate cloud storage to NAS.

| Script | Purpose | Manual Run |
|--------|---------|------------|
| `setup-nas-folders.sh` | Create cloud-imports/, files/, media/ on NAS | `~/.claude/scripts/setup-nas-folders.sh` |
| `import-cloud-to-nas.sh` | rsync Google Drive + iCloud → NAS (additive, idempotent) | `~/.claude/scripts/import-cloud-to-nas.sh` |
| `cleanup-downloads.sh` | Triage ~/Downloads (--audit or --execute) | `~/.claude/scripts/cleanup-downloads.sh --audit` |
| `verify-nas-migration.sh` | Verify file counts, Finder defaults, backup health | `~/.claude/scripts/verify-nas-migration.sh` |

**Logs:** `~/.claude/logs/cloud-import-nas.log`, `~/.claude/logs/downloads-cleanup.log`

**NAS folder layout:**
```
~/NAS/
├── backups/          (automated backups)
├── archives/         (manual project/client archives)
├── timemachine/      (Time Machine)
├── cloud-imports/    (Google Drive + iCloud imports)
│   ├── google-drive-personal/
│   ├── google-drive-flyflat/
│   └── icloud-unique/
├── files/            (default save target)
│   ├── documents/
│   └── downloads-kept/
└── media/            (3D models, large files)
```

**Shell aliases:** `nas-files` → open ~/NAS/files/, `nas-imports` → open ~/NAS/cloud-imports/

---

**Last Updated:** 2026-02-13
**Reason:** Added file consolidation & NAS migration scripts.
