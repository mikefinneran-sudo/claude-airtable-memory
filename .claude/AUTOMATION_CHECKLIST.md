# Automation Discovery Checklist

**USE THIS CHECKLIST** when user mentions scheduled tasks or "we already have this"

## Keywords That Trigger This Checklist:
- "runs at midnight"
- "runs every night"
- "scheduled"
- "cron"
- "automated"
- "we have a script"
- "already built this"

## Step-by-Step Discovery (DO NOT SKIP STEPS)

### Step 1: Check LaunchAgents (10 seconds)
```bash
ls ~/Library/LaunchAgents/ | grep -i [keyword]
```

**If found:**
```bash
cat ~/Library/LaunchAgents/[found-file].plist
# Extract ProgramArguments path
# Run that script directly
```

### Step 2: Check Crontab (5 seconds)
```bash
crontab -l
```

### Step 3: Search Script Directories (15 seconds)
```bash
# Main scripts
ls ~/Documents/ObsidianVault/.scripts/ | grep -i [keyword]

# Project scripts
find ~/Documents/ObsidianVault/Projects -name "*.py" -o -name "*.sh" | grep -i [keyword]

# Claude scripts
ls ~/.claude/scripts/ | grep -i [keyword]
```

### Step 4: Git History (10 seconds)
```bash
cd ~/Documents/ObsidianVault
git log --all --oneline | grep -i [keyword]
```

### Step 5: Content Search (15 seconds)
```bash
# Search file contents for keywords
grep -r "[keyword]" ~/Documents/ObsidianVault/.scripts/
grep -r "[keyword]" ~/.claude/scripts/
```

## STOP BEFORE BUILDING

**Before creating ANY new automation tool, ask yourself:**

1. ✅ Did I check ALL LaunchAgents?
2. ✅ Did I check crontab?
3. ✅ Did I search script directories?
4. ✅ Did I search git history?
5. ✅ Did I search file contents?

**If answered YES to all 5, THEN and ONLY THEN consider building new tool.**

## Common Mistakes (NEVER DO THIS)

❌ Start with browser automation
❌ Build puppeteer scripts
❌ Create new tools without searching
❌ Ignore when user says "we already have this"
❌ Skip straight to Task tool
❌ Assume automation doesn't exist

## Time Budget

**Discovery should take MAX 60 seconds:**
- LaunchAgents: 10 sec
- Crontab: 5 sec
- Script dirs: 15 sec
- Git history: 10 sec
- Content search: 15 sec
- Running found script: 5 sec

**If spending more than 2 minutes, you're doing it wrong.**

## Known Locations Reference

See: `~/.claude/AUTOMATION_LOCATIONS.md` for complete list.

Quick paths:
- LaunchAgents: `~/Library/LaunchAgents/`
- Scripts: `~/Documents/ObsidianVault/.scripts/`
- Project scripts: `~/Documents/ObsidianVault/Projects/*/. scripts/`
- Claude scripts: `~/.claude/scripts/`

---

**Created:** 2025-11-02
**Reason:** Wasted 45 minutes failing to find existing Perplexity automation
**Grade:** F - Never repeat this mistake
