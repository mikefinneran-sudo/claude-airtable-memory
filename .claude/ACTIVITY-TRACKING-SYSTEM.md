# Daily Activity Tracking System

**Created**: November 1, 2025
**Purpose**: Capture all session work in Airtable for on-demand summaries and analytics

---

## What This Does

Automatically logs every session's activity to Airtable, enabling you to:
- Generate weekly/monthly summaries on demand
- Track productivity across projects
- Identify blockers and patterns
- Query activity history with natural language
- Export to reports for clients

**Result**: Never lose track of what you've accomplished, always have data-driven insights

---

## Quick Start

### 1. Setup Airtable Table (One-Time)

```bash
# Get Airtable token from https://airtable.com/create/tokens
export AIRTABLE_TOKEN='your_token_here'

# Run setup script
~/.claude/scripts/setup-activity-tracking-airtable.py
```

Choose option:
- **Option 1**: Creates new "Claude Activity Tracking" base
- **Option 2**: Adds table to existing base

Script will auto-add `AIRTABLE_BASE_ID` to your `~/.zshrc`

### 2. Reload Shell

```bash
source ~/.zshrc
```

### 3. Use It

Activity logging is now **automatic** on every `save-session`:

```bash
# Work on project
continue waltersignal

# ... do work ...

# Save session (auto-logs to Airtable)
save-session
# or just exit terminal
```

### 4. Generate Summaries

```bash
# This week
weekly-summary

# This month
monthly-summary

# Custom timeframe
activity-summary day     # Today
activity-summary quarter # Last 90 days
```

---

## Airtable Schema

The "Daily Activity Log" table captures:

| Field | Type | Description |
|-------|------|-------------|
| Date | DateTime | Session timestamp |
| Project | Text | Project name |
| Session Start | Text | Session start time |
| Location | Text | Working directory |
| Completed Tasks | Number | Tasks finished |
| Task Details | Long Text | Task descriptions |
| Decisions Made | Long Text | Key decisions |
| Files Created | Number | New files count |
| Files Modified | Number | Modified files count |
| Blockers | Long Text | Current blockers |
| Session Type | Select | Development/Research/Planning/etc |
| Status | Select | Completed/In Progress/Blocked |
| Duration (mins) | Number | Session length |
| Tags | Multi-Select | High Priority/Quick Win/etc |

---

## Commands

### Activity Logging (Automatic)
```bash
save-session  # Auto-logs to Airtable on session save
```

### Generate Summaries
```bash
activity-summary        # Last week (default)
activity-summary day    # Today only
activity-summary week   # Last 7 days
activity-summary month  # Last 30 days
activity-summary quarter # Last 90 days

# Quick aliases
weekly-summary   # Same as "activity-summary week"
monthly-summary  # Same as "activity-summary month"
```

### Manual Logging (Rare)
```bash
~/.claude/scripts/log-activity-to-airtable.sh
```

---

## Summary Output Example

```
╔════════════════════════════════════════════════════════════════╗
║          Activity Summary - Last Week                          ║
╚════════════════════════════════════════════════════════════════╝

📊 Overall Statistics
   Total Sessions: 12
   Tasks Completed: 47
   Files Created: 23
   Files Modified: 89

📁 Projects Worked On
   WalterSignal: 6 sessions
   FlyFlat: 4 sessions
   LifeHub: 2 sessions

🏷️  Session Types
   Development: 8 sessions
   Bug Fix: 2 sessions
   Research: 2 sessions

⚠️  Active Blockers
   - API rate limiting on Perplexity
   - 1Password CLI authentication flow

💡 Key Decisions Made
   - Switched to Puppeteer v24 for stability
   - Implemented script archival to GitHub
   - Built activity tracking with Airtable

📝 Recent Sessions
   2025-11-01 | WalterSignal | 15 tasks | Completed
   2025-10-31 | FlyFlat | 8 tasks | Completed
   2025-10-30 | WalterSignal | 12 tasks | Completed
```

---

## Export to Markdown

Summaries can be exported to markdown files:

```bash
activity-summary week
# Prompt: "Export to markdown? (y/N):"
# Type: y

# Output: ~/.claude/activity-summary-week-2025-11-01.md
```

Use these markdown files for:
- Client reports
- Weekly reviews
- Performance tracking
- Portfolio documentation

---

## Use Cases

### Weekly Reviews
```bash
# Friday afternoon
weekly-summary
# Review accomplishments
# Plan next week
```

### Client Reporting
```bash
# End of month
monthly-summary
# Export to markdown
# Send to client
```

### Performance Tracking
```bash
# Query Airtable directly
# Filter by project
# Group by session type
# Analyze productivity trends
```

### Retrospectives
```bash
# Quarter end
activity-summary quarter
# Identify patterns
# Optimize workflow
```

---

## Advanced: Query Airtable

Since data is in Airtable, you can:

1. **Create Views**
   - "This Week" (filtered by date)
   - "High Priority" (filtered by tags)
   - "Blockers" (filtered by status)

2. **Build Dashboards**
   - Charts showing tasks over time
   - Project distribution pie chart
   - Session type breakdown

3. **Connect to Apps**
   - Zapier: Auto-send weekly summaries
   - Slack: Post daily accomplishments
   - Notion: Sync to project pages

4. **API Access**
   - Build custom queries
   - Generate custom reports
   - Integrate with other tools

---

## Environment Variables

Required in your shell profile (`~/.zshrc`):

```bash
# Airtable Activity Tracking
export AIRTABLE_TOKEN='your_token_here'
export AIRTABLE_BASE_ID='your_base_id_here'
```

These are auto-added by the setup script.

---

## Files Created

1. `/Users/mikefinneran/.claude/scripts/log-activity-to-airtable.sh`
   - Logs session data to Airtable

2. `/Users/mikefinneran/.claude/scripts/setup-activity-tracking-airtable.py`
   - Creates Airtable table with proper schema

3. `/Users/mikefinneran/.claude/scripts/generate-activity-summary.py`
   - Queries Airtable and generates summaries

**Modified**:
- `save-session-memory.sh` - Added auto-logging after session save
- `setup-aliases.sh` - Added summary commands

---

## Benefits

### Automatic Capture
- Zero manual effort
- Never miss logging work
- Complete session history

### On-Demand Insights
- Generate summaries anytime
- Filter by timeframe
- Export to any format

### Data-Driven Decisions
- See where time goes
- Identify bottlenecks
- Optimize workflow

### Client Reporting
- Professional summaries
- Detailed task lists
- Export to markdown

### Long-Term Memory
- Query past decisions
- Reference old solutions
- Track project evolution

---

## Troubleshooting

### "AIRTABLE_TOKEN not set"
```bash
export AIRTABLE_TOKEN='your_token_here'
source ~/.zshrc
```

### "Failed to create table"
- Check token permissions (needs write access)
- Verify base ID is correct
- Try creating new base (option 1)

### "No activities found"
- Verify logging is working: check `save-session` output
- Check Airtable base manually
- Ensure `AIRTABLE_BASE_ID` is set

### Summary shows wrong data
- Verify date filters in Airtable
- Check timezone settings
- Try different timeframe

---

## Next Steps

1. ✅ Run setup: `~/.claude/scripts/setup-activity-tracking-airtable.py`
2. ✅ Reload shell: `source ~/.zshrc`
3. ✅ Work and save: Activity auto-logs
4. ✅ Generate summary: `weekly-summary`

---

**Status**: Production Ready
**Auto-Logs**: Every `save-session`
**Manual Summaries**: On demand anytime

---

**Quick Reference**:
- Setup: `~/.claude/scripts/setup-activity-tracking-airtable.py`
- Summary: `weekly-summary` or `monthly-summary`
- Export: Answer 'y' when prompted
