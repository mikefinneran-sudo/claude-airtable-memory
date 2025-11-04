# Airtable ↔ GitHub Sync Analysis

**Date**: November 3, 2025
**Status**: ⚠️ NO GitHub sync exists

---

## Current State

### ✅ What's Working

**Airtable Base** (app6g0t0wtruwLA5I - "WalterFetch Intelligence"):
- 10 tables created and populated
- Projects table: 4 active projects
- Tasks table: 10+ tasks with status tracking
- Automated sync to local markdown every 15 minutes

**Airtable → Local Sync**:
- Script: `~/Documents/ObsidianVault/airtable-sync.py`
- LaunchAgent: com.mikefinneran.airtable-sync.plist
- Frequency: Every 15 minutes (900 seconds)
- Output: `~/Documents/Work/` (Tasks/, Projects/, CRM/)
- Status: ✅ Running and working

---

## ❌ What's Missing: GitHub Integration

### Problem 1: No GitHub Repos for WalterSignal Projects

**Airtable Projects** (no GitHub repos):
1. **WalterFetch v2.1**
   - Airtable: ✅ Tracked (85% complete)
   - GitHub Repo field: ❌ Empty
   - Actual GitHub repo: ❌ Doesn't exist

2. **SpecialAgentStanny**
   - Airtable: ✅ Tracked (45% complete)
   - GitHub Repo field: ❌ Empty
   - Actual GitHub repo: ❌ Doesn't exist

3. **WalterSignal PM System**
   - Airtable: ✅ Tracked (90% complete)
   - GitHub Repo field: ❌ Empty
   - Actual GitHub repo: ❌ Doesn't exist

4. **FlyFlat Data Enrichment**
   - Airtable: ✅ Tracked (10% complete)
   - GitHub Repo field: ❌ Empty
   - Actual GitHub repo: ❌ Doesn't exist

**GitHub Account Status**:
- gh CLI configured: ✅ Yes
- GitHub username: mikefinneran
- Public repos found: 1 (pdfjs_viewer-rails-va from 2023)
- WalterSignal repos: ❌ None found

**Local Git Repos** (in ~/Documents/ObsidianVault/Projects/):
- 10+ projects have `.git` directories
- But NO GitHub remotes configured
- These are local-only repos

---

### Problem 2: Airtable Has GitHub Fields But They're Empty

**Projects Table**:
- Field: "GitHub Repo" (URL type)
- Current value: Empty in all 4 projects

**Tasks Table**:
- Field: "GitHub Issue" (URL type)
- Field: "GitHub PR" (URL type)
- Current value: Empty in all 10 tasks

**Deployments Table**:
- Field: "GitHub Release" (URL type)
- Current value: Not checked (likely empty)

---

### Problem 3: No Automation Between Airtable ↔ GitHub

**Current sync direction**:
```
Airtable → Local Markdown Files
```

**Missing sync directions**:
```
❌ GitHub Issues → Airtable Tasks
❌ Airtable Tasks → GitHub Issues
❌ GitHub Repos → Airtable Projects
❌ Airtable Projects → GitHub Repos
❌ GitHub PRs → Airtable Tasks
❌ GitHub Releases → Airtable Deployments
```

**No automation exists for**:
- Creating GitHub issues from Airtable tasks
- Syncing GitHub issue status to Airtable
- Linking GitHub PRs to Airtable tasks
- Tracking GitHub releases in Airtable
- Updating Airtable when GitHub changes

---

## Security Issue Found

**Hardcoded API Token in Script**:
```python
# File: ~/Documents/ObsidianVault/airtable-sync.py
AIRTABLE_TOKEN = "REDACTED_AIRTABLE_TOKEN"
```

**Risk**: High
- API token exposed in plain text
- File synced to iCloud (potential exposure)
- Should use 1Password or environment variable

---

## What You Told Me

**Your request**: "we need to check and make sure airtable and our github are in sync"

**Reality**: They're not in sync because:
1. No GitHub repos exist for WalterSignal projects
2. No automation connects Airtable to GitHub
3. GitHub fields in Airtable are empty
4. Only sync is Airtable → Local markdown files

---

## Options to Fix This

### Option 1: Create GitHub Repos for WalterSignal Projects (Recommended)

**Step 1: Create repos**:
```bash
# Create repos for each project
gh repo create waltersignal/walterfetch --public --description "Zapier/n8n webhook integration for automated research"
gh repo create waltersignal/specialagentstanny --public --description "Multi-agent AI framework"
gh repo create waltersignal/pm-system --private --description "Airtable-based PM system"
gh repo create waltersignal/flyflat-enrichment --private --description "FlyFlat data enrichment"
```

**Step 2: Update Airtable with GitHub repo URLs**:
- Manually or via script
- Fill in "GitHub Repo" field for each project

**Step 3: Set up local Git repos to push to GitHub**:
```bash
cd ~/Documents/ObsidianVault/Projects/WalterSignal
git remote add origin https://github.com/waltersignal/walterfetch.git
git push -u origin main
```

**Pros**:
- Version control for code
- Track issues and PRs
- Professional project presence
- Enable GitHub Actions for CI/CD

**Cons**:
- Initial setup work
- Need to decide public vs private
- Need to create organization or use personal account

---

### Option 2: Set Up Airtable ↔ GitHub Sync Automation

**After repos exist**, set up two-way sync:

**A. GitHub Issues → Airtable Tasks** (via GitHub Actions):
```yaml
# .github/workflows/sync-to-airtable.yml
on:
  issues:
    types: [opened, edited, closed, labeled]
  pull_request:
    types: [opened, edited, closed]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Sync to Airtable
        uses: actions/airtable-sync@v1
        with:
          airtable_token: ${{ secrets.AIRTABLE_TOKEN }}
          base_id: app6g0t0wtruwLA5I
```

**B. Airtable Tasks → GitHub Issues** (via Airtable Automation):
- Airtable Automation: When Task created with "Create GitHub Issue" checkbox
- Run script to create GitHub issue via API
- Update "GitHub Issue" field with URL

**Pros**:
- Keeps everything in sync
- Single source of truth
- Automated updates

**Cons**:
- Complex setup
- Potential for sync conflicts
- Requires maintenance

---

### Option 3: Manual Sync (Current Workaround)

**Keep current system**:
- Track projects in Airtable
- Use local Git repos (no GitHub)
- Manually add GitHub links when needed

**Pros**:
- No setup needed
- No external dependencies
- Privacy (no public repos)

**Cons**:
- No backup on GitHub
- No collaboration features
- GitHub fields remain empty
- Not really "in sync"

---

## Recommended Path Forward

### Phase 1: Set Up GitHub Repos (1 hour)

1. **Create GitHub organization**: `waltersignal`
   ```bash
   gh org create waltersignal
   ```

2. **Create repos for each project**:
   ```bash
   gh repo create waltersignal/walterfetch --public
   gh repo create waltersignal/specialagentstanny --public
   gh repo create waltersignal/pm-system --private
   gh repo create waltersignal/flyflat-enrichment --private
   ```

3. **Link local repos to GitHub**:
   ```bash
   # For each project with code
   cd ~/Documents/ObsidianVault/Projects/[ProjectName]
   git remote add origin https://github.com/waltersignal/[repo].git
   git push -u origin main
   ```

4. **Update Airtable Projects** with GitHub repo URLs:
   - Add URLs to "GitHub Repo" field
   - Can do manually or via script

---

### Phase 2: Basic GitHub → Airtable Sync (2 hours)

**Create sync script**: `~/.claude/scripts/github-to-airtable-sync.sh`

**Functionality**:
- Fetch open issues from GitHub repos
- Create/update tasks in Airtable
- Link GitHub issue URL to Airtable task
- Run via LaunchAgent (daily or on-demand)

**Script outline**:
```bash
#!/bin/bash
# Fetch GitHub issues and sync to Airtable

for repo in walterfetch specialagentstanny pm-system flyflat-enrichment; do
  gh issue list --repo waltersignal/$repo --json number,title,state,labels \
    | jq -r '.[] | [.number, .title, .state] | @tsv' \
    | while read number title state; do
        # Call Airtable API to create/update task
        # Link GitHub issue URL
    done
done
```

---

### Phase 3: Advanced Two-Way Sync (Optional, 4+ hours)

**If needed later**:
- Airtable → GitHub issue creation
- PR tracking in Airtable
- Release tracking in Airtable
- Webhook-based real-time sync

---

## Security Fix Needed First

**Before any GitHub integration**, fix the exposed API token:

1. **Move token to 1Password**:
   ```bash
   op item create --category="API Credential" --title="Airtable WalterFetch" \
     --vault="Personal" token="REDACTED_AIRTABLE_TOKEN.."
   ```

2. **Update script to use 1Password**:
   ```python
   import subprocess
   AIRTABLE_TOKEN = subprocess.check_output(
       ["op", "item", "get", "Airtable WalterFetch", "--fields", "token"],
       text=True
   ).strip()
   ```

3. **Or use environment variable**:
   ```bash
   # In ~/.zshrc
   export AIRTABLE_TOKEN=$(op item get "Airtable WalterFetch" --fields token)
   ```

---

## Quick Decision Matrix

**Do you want to**:

| Action | Time | Benefit |
|--------|------|---------|
| Create GitHub repos | 1 hour | Version control, backup, professional presence |
| Set up basic GitHub → Airtable sync | 2 hours | Auto-populate Airtable from GitHub issues |
| Set up two-way sync | 4+ hours | Full automation, single source of truth |
| Keep current system (no GitHub) | 0 hours | No change, but no version control |

**My recommendation**: Start with Phase 1 (create repos) + Security fix. Then evaluate if you need automated sync based on usage.

---

## Next Steps (Your Choice)

**Option A: Create GitHub repos now**
- I can create repos via gh CLI
- Link local projects
- Update Airtable with URLs
- Takes ~30 minutes

**Option B: Fix security issue only**
- Move Airtable token to 1Password
- Update sync script
- Keep current workflow
- Takes ~15 minutes

**Option C: Full sync automation**
- Create repos
- Set up GitHub → Airtable sync script
- Add LaunchAgent for daily sync
- Takes ~2-3 hours

**Option D: Do nothing**
- Accept that Airtable and GitHub are not in sync
- Continue current workflow (Airtable → Local only)

---

## Summary

**Current State**:
- ✅ Airtable: Working, 4 projects tracked
- ✅ Airtable → Local sync: Working every 15 min
- ❌ GitHub repos: Don't exist for WalterSignal projects
- ❌ Airtable ↔ GitHub sync: Doesn't exist
- ⚠️ Security: API token hardcoded in script

**Bottom Line**: Your Airtable and GitHub are **not in sync** because there are no GitHub repos for your WalterSignal projects and no automation connecting the two systems.

**What do you want to do?**

---

**Created**: November 3, 2025
**Analysis Complete**: Ready for your decision
