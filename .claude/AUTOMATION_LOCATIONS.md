# Automation Locations Reference

**ALWAYS CHECK THESE FIRST** when user mentions scheduled tasks, cron jobs, or "runs at midnight"

## Scheduled Task Locations

### macOS LaunchAgents (PRIMARY)
```bash
ls ~/Library/LaunchAgents/
```

**Active Automations:**
- `com.mikefinneran.research-update.plist` - Perplexity research database update (daily midnight)
- `com.mikefinneran.airtable-sync.plist` - Airtable sync
- `com.lifehub.dailynote.plist` - Daily note with Calendar + Reminders (daily 7 AM)
- `com.mikefinneran.task-router.plist` - Route Inbox tasks by tag (every 15 min)
- `com.lifehub.weeklyreview.new.plist` - Weekly review
- `com.lifehub.gdrive-sync.plist` - Google Drive sync
- `com.flyflat.weeklyupdate.plist` - Fly Flat weekly update

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

**Last Updated:** 2026-01-28
**Reason:** Added Apple Reminders task router and enhanced daily note with Calendar/Reminders injection.
