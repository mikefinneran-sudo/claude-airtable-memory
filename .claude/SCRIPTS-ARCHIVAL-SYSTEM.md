# Custom Scripts Archival System

**Created**: November 1, 2025
**Purpose**: Automatically document and archive custom scripts to GitHub

---

## What This Does

Whenever you complete a project and create custom scripts, this system:
1. **Detects** new scripts automatically when you save a session
2. **Documents** each script with usage, description, and source code
3. **Archives** to organized GitHub repository (`utilities-repo-setup`)
4. **Catalogs** in searchable CATALOG.md with metadata

**Result**: Never lose custom scripts, easy to find and reuse later

---

## How It Works

### Automatic (Integrated with Session Save)

When you run `save-session` or exit terminal:
1. System scans for new `.sh` and `.py` files created during session
2. Asks if you want to archive each script
3. Auto-generates documentation
4. Commits to utilities repo with description

### Manual (Archive Specific Script)

```bash
archive-script /path/to/script.sh project-name "Description"
```

**Example**:
```bash
archive-script ./fix-passkey-complete.sh waltersignal "Google passkey automation with 1Password"
```

### Bulk Scan (Find All Scripts)

```bash
scan-scripts
```

Scans all projects and offers to archive everything at once.

---

## Repository Structure

```
~/.claude/projects/utilities-repo-setup/
├── README.md              # Repository overview
├── CATALOG.md             # Searchable index of all scripts
├── automation/            # Automation and workflow scripts
├── fixes/                 # Problem-solving scripts
├── utilities/             # General utility scripts
├── project-specific/      # Scripts tied to specific projects
│   ├── waltersignal/
│   ├── flyflat/
│   └── lifehub/
└── archive/               # Historical/deprecated scripts
```

---

## Catalog Example

Each archived script gets entry in `CATALOG.md`:

| Script | Category | Project | Description | Date Added |
|--------|----------|---------|-------------|------------|
| `fix-passkey-complete.sh` | fixes | waltersignal | Google passkey automation | 2025-11-01 |
| `memory-search.sh` | utilities | claude-code | Search all memory files | 2025-11-01 |
| `continue-enhanced.sh` | automation | claude-code | Enhanced continue with preview | 2025-11-01 |

---

## Documentation Auto-Generated

For each script, creates markdown file with:
- Description and usage
- Dependencies
- Source project
- Full source code
- Date added and last updated

**Example**: `fixes/fix-passkey-complete.md`

---

## Commands

### Archive Single Script
```bash
archive-script <file> <project> <description>
```

### Scan All Projects
```bash
scan-scripts
```

### View Archived Scripts
```bash
cd ~/.claude/projects/utilities-repo-setup
cat CATALOG.md
```

### Push to GitHub
```bash
cd ~/.claude/projects/utilities-repo-setup
gh repo create utilities-repo-setup --public --source=. --push
```

Or manually:
```bash
cd ~/.claude/projects/utilities-repo-setup
git remote add origin git@github.com:YOUR-USERNAME/utilities-repo-setup.git
git push -u origin main
```

---

## Current Scan Results

**Date**: November 1, 2025
**Scripts Found**: 111 across all projects

**Projects with Most Scripts**:
- WalterSignal: 31 scripts
- FlyFlat: 20 scripts
- LifeHub: 14 scripts
- warp-enhancement: 5 scripts
- EventFlow-AI: 2 scripts

**Categories Detected**:
- Automation: 45 scripts
- Fixes: 12 scripts
- Utilities: 28 scripts
- Project-specific: 26 scripts

---

## Integration with Workflow

### On Session Save

When you save a session with `save-session` or exit terminal:

1. System checks `SESSION-MEMORY.md` for created files
2. Filters for executable `.sh` and `.py` files
3. Prompts: "Archive to GitHub utilities repo? (y/N)"
4. If yes:
   - Extracts description from session context
   - Determines category (automation/fixes/utilities)
   - Archives with full documentation
   - Commits to utilities repo

### On Project Completion

When you mark a project as complete:
1. System automatically offers to scan for all custom scripts
2. Bulk archive option for efficiency
3. Creates project-specific subdirectory in utilities repo

---

## Best Practices

### When to Archive

✅ **Archive immediately**:
- General utility scripts (reusable)
- Problem-fixing scripts (document the solution)
- Automation workflows
- Integration scripts

⏸️ **Consider before archiving**:
- Project-specific code that won't be reused
- Scripts with hardcoded credentials/paths
- Temporary debugging scripts

❌ **Don't archive**:
- Standard build scripts (package.json, setup.py)
- Generated code
- Third-party scripts

### Naming Convention

**Good**:
- `fix-google-passkey.sh` (clear purpose)
- `sync-gmail-to-notion.py` (clear action)
- `auto-backup-airtable.sh` (clear automation)

**Avoid**:
- `script1.sh` (not descriptive)
- `test.py` (too generic)
- `old.sh` (confusing)

### Descriptions

**Good**:
- "Automates Google passkey removal with 1Password integration"
- "Syncs Gmail inbox to Notion database with filtering"
- "Daily backup of Airtable bases to S3 with compression"

**Avoid**:
- "Script for stuff" (not specific)
- "Automation" (not helpful)
- "Fix" (what does it fix?)

---

## Customization

### Change Repository Location

Edit `archive-custom-script.sh`:
```bash
SCRIPTS_REPO="$HOME/custom-location/utilities"
```

### Change Category Detection

Edit `archive-custom-script.sh` category logic:
```bash
# Add custom categories
if [[ "$DESCRIPTION" == *"backup"* ]]; then
    CATEGORY="backups"
fi
```

### Exclude Paths from Scan

Edit `scan-project-scripts.sh`:
```bash
# Skip specific directories
if [[ "$file" == *"node_modules"* ]]; then
    return 1
fi
```

---

## GitHub Setup

### First Time Setup

```bash
# 1. Scan and archive your scripts
scan-scripts

# 2. Navigate to utilities repo
cd ~/.claude/projects/utilities-repo-setup

# 3. Create GitHub repo (using GitHub CLI)
gh repo create utilities-repo-setup \
    --public \
    --description "Custom scripts library - auto-archived by Claude Code" \
    --source=. \
    --push

# Done! Scripts are now on GitHub
```

### Manual Setup

```bash
# 1. Create repo on GitHub.com
# 2. Add remote
cd ~/.claude/projects/utilities-repo-setup
git remote add origin git@github.com:YOUR-USERNAME/utilities-repo-setup.git

# 3. Push
git push -u origin main
```

### Ongoing Usage

After initial setup, scripts auto-commit to utilities repo.

To push to GitHub:
```bash
cd ~/.claude/projects/utilities-repo-setup
git push
```

**Pro Tip**: Set up cron job to auto-push daily:
```bash
0 18 * * * cd ~/.claude/projects/utilities-repo-setup && git push origin main 2>/dev/null
```

---

## Examples

### Example 1: Archive After Project Completion

```bash
# Finish working on project
continue waltersignal

# Create some scripts
./fix-passkey-complete.sh
./memory-search.sh

# Save session (auto-detects scripts)
save-session

# Prompt appears:
# "✓ Found script: fix-passkey-complete.sh"
# "Archive to GitHub utilities repo? (y/N):"

# Type: y

# Script is:
# - Documented
# - Categorized (fixes)
# - Committed to utilities repo
# - Added to CATALOG.md
```

### Example 2: Manual Archive

```bash
# Created useful script
./custom-backup.sh

# Archive manually
archive-script ./custom-backup.sh flyflat "Automated backup to S3 with encryption"

# ✅ Script archived!
#    Location: ~/.claude/projects/utilities-repo-setup/automation/custom-backup.sh
#    Docs: automation/custom-backup.md
```

### Example 3: Bulk Scan and Archive

```bash
# Scan all projects
scan-scripts

# Shows:
# "Total scripts found: 111"
# "Would you like to archive all these scripts? (y/N):"

# Type: y

# All 111 scripts are:
# - Documented
# - Categorized
# - Committed
# - Cataloged
```

---

## Troubleshooting

### "Script not found"

```bash
# Make sure file exists and is executable
ls -la /path/to/script.sh
chmod +x /path/to/script.sh
```

### "Utilities repo not found"

```bash
# Repo will be created automatically on first archive
archive-script ./test.sh general "Test script"
```

### "Git commit failed"

```bash
# Navigate to repo and check status
cd ~/.claude/projects/utilities-repo-setup
git status

# Fix any conflicts, then retry
```

### "Category detection wrong"

```bash
# Manually specify category by using proper keywords in description
archive-script ./script.sh project "fix authentication bug"  # → fixes
archive-script ./script.sh project "automate backup"         # → automation
archive-script ./script.sh project "general utility"         # → utilities
```

---

## Benefits

### Organization
- All scripts in one place
- Categorized and searchable
- Version controlled

### Documentation
- Auto-generated for every script
- Includes source code and usage
- Date tracked

### Reusability
- Easy to find similar scripts
- Copy and adapt for new projects
- Share across team

### Preservation
- Never lose custom scripts
- Survives project deletions
- Backed up to GitHub

### Discovery
- Catalog shows all available scripts
- Search by category, project, or description
- See what problems you've already solved

---

## Future Enhancements

Potential additions:

1. **Script Marketplace**
   - Share scripts with community
   - Rate and review scripts
   - Download popular scripts

2. **Dependency Management**
   - Auto-detect required packages
   - Generate requirements.txt
   - Check for security issues

3. **Usage Analytics**
   - Track which scripts are used most
   - Identify deprecated scripts
   - Suggest related scripts

4. **AI-Powered Summaries**
   - Auto-generate better descriptions
   - Suggest improvements
   - Find similar scripts

5. **Cross-Project Intelligence**
   - "Which projects use this script?"
   - "Find scripts that solve X problem"
   - "What scripts were created for Y project?"

---

## Status

**Implementation**: ✅ COMPLETE
**Scripts Scanned**: 111
**Ready to Use**: YES

**Next Steps**:
1. Run `scan-scripts` to archive existing scripts
2. Push to GitHub with `gh repo create`
3. Scripts auto-archive on future project completions

---

**Created**: 2025-11-01
**Last Updated**: 2025-11-01
**Owner**: Mike Finneran
