# GitHub ↔ Airtable Automated Sync

**Created**: November 3, 2025
**Status**: ✅ Ready to use

---

## What This Does

Automatically syncs your GitHub repositories to Airtable Projects table:

**Every day at 9 AM**, it will:
1. Fetch all repos from `mikefinneran-sudo` GitHub account
2. Match repos to existing Airtable projects
3. Update projects with GitHub URLs (if empty)
4. Create new projects for repos not in Airtable
5. Update last commit dates
6. Log all changes

---

## Files Created

### 1. Sync Script
**Location**: `~/.claude/scripts/github-airtable-sync.py`

**What it does**:
- Fetches GitHub repos using `gh` CLI
- Fetches Airtable projects using API
- Matches repos to projects intelligently
- Updates or creates projects as needed
- Uses 1Password for credentials (secure!)
- Comprehensive logging

### 2. LaunchAgent
**Location**: `~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist`

**Schedule**: Daily at 9:00 AM
**Logs**: `~/.claude/logs/github-airtable-sync-stdout.log`

### 3. Logs Directory
**Location**: `~/.claude/logs/`
- Timestamped log for each sync run
- stdout and stderr logs from LaunchAgent

---

## Prerequisites (Already Set Up)

✅ **1Password CLI**: Installed and authenticated
✅ **GitHub CLI (gh)**: Installed and authenticated
✅ **Credentials in 1Password**:
  - "Airtable WalterSignal" (with `credential` field)
  - Optional: "GitHub mikefinneran-sudo" (for API rate limits)

---

## Installation & Setup

### Step 1: Verify 1Password Credentials

Check that credentials exist:
```bash
op item get "Airtable WalterSignal" --fields credential
```

Should return your Airtable API token.

### Step 2: Test Manual Run

Run sync manually to test:
```bash
python3 ~/.claude/scripts/github-airtable-sync.py
```

You should see output like:
```
🔄 Starting GitHub → Airtable Sync
==================================================
✅ Retrieved Airtable token from 1Password
ℹ️  No GitHub token in 1Password, using gh CLI default auth

📦 Fetching GitHub repositories...
✅ Found 24 GitHub repositories

📋 Fetching Airtable projects...
✅ Found 4 Airtable projects

🔗 Matching repos to projects...
  ✅ Updated 'WalterFetch v2.1' with GitHub URL
  ✅ Created project 'Waltersignal Ai'
  ...

==================================================
✅ Sync Complete!

📊 Statistics:
   GitHub repos checked: 24
   Projects updated: 4
   Projects created: 8
   Errors: 0
```

### Step 3: Load LaunchAgent

Start the daily automation:
```bash
launchctl load ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
```

Verify it's loaded:
```bash
launchctl list | grep github-airtable-sync
```

You should see:
```
-	0	com.mikefinneran.github-airtable-sync
```

---

## Usage

### Manual Sync (Anytime)

Run sync manually:
```bash
python3 ~/.claude/scripts/github-airtable-sync.py
```

Or create an alias (add to ~/.zshrc):
```bash
alias github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'
```

Then just run:
```bash
github-sync
```

### View Logs

**Latest manual run**:
```bash
ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | awk '{print $NF}' | xargs cat
```

**LaunchAgent logs** (stdout):
```bash
tail -50 ~/.claude/logs/github-airtable-sync-stdout.log
```

**LaunchAgent logs** (errors):
```bash
tail -50 ~/.claude/logs/github-airtable-sync-stderr.log
```

### Check LaunchAgent Status

```bash
launchctl list | grep github-airtable-sync
```

### Stop/Start LaunchAgent

**Stop** (disable daily sync):
```bash
launchctl unload ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
```

**Start** (enable daily sync):
```bash
launchctl load ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
```

---

## How It Works

### Matching Logic

The script matches GitHub repos to Airtable projects using:

1. **Exact URL match**: If project already has GitHub URL
2. **Name similarity**: If repo name appears in project name
3. **No match**: Creates new project

### Creating New Projects

When creating a project from a GitHub repo, it:

**Sets Status** based on last commit:
- Pushed within 7 days → "In Progress" (High priority)
- Pushed within 30 days → "In Progress" (Medium priority)
- Older than 30 days → "Paused" (Low priority)

**Determines Product Line** from repo name:
- Contains "walter" or "fetch" → WalterFetch
- Contains "stanny" → SpecialAgentStanny
- Contains "life" or "obsidian" → LifeHub
- Otherwise → Infrastructure

**Adds Tags** intelligently:
- "AI" if mentions: ai, claude, agent
- "Automation" if mentions: automat, sync, script
- "Client Work" if mentions: client, flyflat
- "Research" if mentions: research, study
- "Internal" if mentions: internal, utility, tool

**Sets Fields**:
- Project Name: Repo name formatted as Title Case
- Description: Repo description from GitHub
- Owner: "Mike Finneran"
- GitHub Repo: Full GitHub URL
- Notes: Auto-created timestamp and last pushed date

### Updating Existing Projects

For projects that exist but have empty "GitHub Repo" field:
- Adds GitHub URL
- Adds notes with link timestamp and last commit date
- Does NOT overwrite existing data

---

## Configuration

### Change Sync Schedule

Edit LaunchAgent:
```bash
nano ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
```

Change the hour (currently 9 AM):
```xml
<key>Hour</key>
<integer>9</integer>  <!-- Change to desired hour (0-23) -->
```

Reload LaunchAgent after changes:
```bash
launchctl unload ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
launchctl load ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
```

### Add Environment Variables

If needed, add to LaunchAgent plist:
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>AIRTABLE_TOKEN</key>
    <string>your_token_here</string>
</dict>
```

But using 1Password is recommended for security.

---

## Troubleshooting

### Error: "No Airtable token found"

**Check 1Password item exists**:
```bash
op item get "Airtable WalterSignal"
```

**Check field name**:
```bash
op item get "Airtable WalterSignal" --fields credential
```

**Fallback**: Set environment variable:
```bash
export AIRTABLE_TOKEN="your_token_here"
python3 ~/.claude/scripts/github-airtable-sync.py
```

### Error: "gh: command not found"

Install GitHub CLI:
```bash
brew install gh
gh auth login
```

### LaunchAgent Not Running

**Check if loaded**:
```bash
launchctl list | grep github-airtable-sync
```

**Check logs for errors**:
```bash
cat ~/.claude/logs/github-airtable-sync-stderr.log
```

**Reload LaunchAgent**:
```bash
launchctl unload ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
launchctl load ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
```

### Projects Not Being Created

**Check API response in logs**:
```bash
tail -100 ~/.claude/logs/github-airtable-sync_*.log | grep "Failed to create"
```

**Check Airtable permissions**:
- Token must have write access to Projects table
- Base ID must be correct: app6g0t0wtruwLA5I

### Duplicate Projects Created

The script uses intelligent matching to avoid duplicates:
- Checks GitHub URL field
- Checks name similarity
- If it creates duplicates, manually merge in Airtable and re-run

---

## What Gets Synced

### GitHub → Airtable

**Synced**:
- ✅ Repository name → Project Name
- ✅ Repository URL → GitHub Repo field
- ✅ Description → Description field
- ✅ Last pushed date → Notes field
- ✅ Auto-determined Status, Priority, Product Line, Tags

**Not Synced** (future enhancements):
- ❌ GitHub Issues → Airtable Tasks
- ❌ GitHub PRs → Airtable Tasks
- ❌ GitHub Releases → Airtable Deployments
- ❌ Commit activity → Progress %

### Airtable → GitHub

**Not synced** (this is one-way: GitHub → Airtable only)
- To create GitHub issues from Airtable, see "Future Enhancements" below

---

## Aliases for Quick Access

Add to `~/.zshrc`:

```bash
# GitHub ↔ Airtable Sync
alias github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'
alias github-sync-logs='ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | awk "{print \$NF}" | xargs cat'
alias github-sync-status='launchctl list | grep github-airtable-sync'
```

Then reload:
```bash
source ~/.zshrc
```

Usage:
```bash
github-sync              # Run sync manually
github-sync-logs         # View latest log
github-sync-status       # Check if LaunchAgent is running
```

---

## Security

### ✅ Credentials Stored in 1Password

- Airtable token: Stored in "Airtable WalterSignal" item
- GitHub token: Optional, stored in "GitHub mikefinneran-sudo" item
- Script retrieves credentials at runtime
- Never stored in plain text

### ✅ Log Files Don't Contain Credentials

- Logs show "✅ Retrieved token from 1Password"
- Never log actual token values
- Safe to share logs for debugging

### ⚠️ GitHub Tokens in Git Remotes

**Found issue**: Some git remotes have embedded tokens:
```bash
https://REDACTED_GITHUB_TOKEN@github.com/...
```

**Should fix**: Use SSH or credential helper instead:
```bash
cd ~/Documents/ObsidianVault/Projects/[project]
git remote set-url origin git@github.com:mikefinneran-sudo/[repo].git
```

---

## Future Enhancements

### Phase 2: GitHub Issues → Airtable Tasks

**Script**: `github-issues-to-airtable.py`
**What it would do**:
- Fetch open issues from all repos
- Create/update tasks in Airtable
- Link GitHub Issue URL to task
- Sync issue status with task status

### Phase 3: Two-Way Sync

**Airtable → GitHub**:
- Create GitHub issue when task has "Create GitHub Issue" checkbox
- Update issue when task status changes
- Close issue when task marked "Done"

### Phase 4: Advanced Syncing

- Sync commit activity to Progress %
- Sync GitHub milestones to Airtable Milestones
- Sync GitHub releases to Airtable Deployments
- Track PR status in Airtable

---

## Summary

### ✅ What You Now Have

**Automated Sync**:
- Runs daily at 9 AM
- Syncs 24+ GitHub repos to Airtable
- Creates new projects automatically
- Updates GitHub URLs in existing projects
- Secure credential management via 1Password
- Comprehensive logging

**Manual Control**:
- Run anytime: `python3 ~/.claude/scripts/github-airtable-sync.py`
- View logs anytime
- Stop/start LaunchAgent as needed

**Smart Matching**:
- Avoids duplicate projects
- Determines status from commit activity
- Auto-assigns product lines and tags
- Preserves existing Airtable data

### 📝 Quick Start

1. **Test it now**:
   ```bash
   python3 ~/.claude/scripts/github-airtable-sync.py
   ```

2. **Enable daily sync**:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.mikefinneran.github-airtable-sync.plist
   ```

3. **Check tomorrow at 9 AM** - it will run automatically!

---

## Questions?

**Check logs**:
```bash
tail -50 ~/.claude/logs/github-airtable-sync-stdout.log
```

**Run manually to debug**:
```bash
python3 ~/.claude/scripts/github-airtable-sync.py
```

**Check if LaunchAgent is running**:
```bash
launchctl list | grep github-airtable-sync
```

---

**Created**: November 3, 2025
**Ready to use**: Yes ✅
**Next run**: Tomorrow 9:00 AM (or run manually now)
