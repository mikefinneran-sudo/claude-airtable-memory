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
- `com.lifehub.dailynote.plist` - Daily note creation
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

**Last Updated:** 2025-11-02
**Reason:** Failed to find Perplexity automation for 45 minutes. Never again.
