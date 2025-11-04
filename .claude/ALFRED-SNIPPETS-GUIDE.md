# Alfred Snippets for Claude Code

**Created**: November 2, 2025
**Alfred Version**: Alfred 5
**Snippet File**: `~/Desktop/Claude-Code-Snippets.alfredsnippets`

---

## Installation (One-Time Setup)

### Step 1: Import Snippets into Alfred

1. **Open Alfred Preferences**
   - Press `Cmd + ,` while Alfred is focused
   - OR: Click Alfred icon in menu bar → Preferences

2. **Navigate to Snippets**
   - Click "Features" in the top bar
   - Click "Snippets" in the left sidebar

3. **Import the Collection**
   - Click the `+` button at the bottom left
   - Select "Import"
   - Navigate to Desktop
   - Select `Claude-Code-Snippets.alfredsnippets`
   - Click "Import"

4. **Verify Installation**
   - You should see a new collection: "Claude Code"
   - It should contain 12 snippets

### Step 2: Enable Auto-Expansion

1. In Alfred Preferences → Features → Snippets
2. Make sure "Automatically expand snippets by keyword" is checked
3. Set your preferred expansion key (default is usually fine)

---

## All Available Snippets

### 1. Session Start (Most Important) ⭐
**Keyword**: `;ctx`
**Expands to**: `Load context: What am I working on this week?`

**Use this**: Every time you start a Claude Code session

**What it does**:
- Loads WORKING-CONTEXT.md
- Shows current week focus
- Reviews recent progress
- Suggests next actions

---

### 2. Continue Project
**Keyword**: `;cont`
**Expands to**: `Continue {cursor} - show status, next actions, and recent progress`

**Usage**:
1. Type `;cont`
2. Cursor appears where you type project name
3. Type project name (e.g., "WalterSignal")
4. Press Enter

**Example**: `;cont` → `Continue WalterSignal - show status, next actions, and recent progress`

---

### 3. Deep Dive
**Keyword**: `;deep`
**Expands to**: `Load full context for {cursor} including all research, code, and documentation`

**Use when**: You need complete context for a project (not just status)

**Example**: `;deep` → `Load full context for WalterSignal including all research, code, and documentation`

---

### 4. Weekly Review
**Keyword**: `;weekly`
**Expands to**: `Review this week's progress across all projects and suggest priorities for next week`

**Use**: Monday mornings for weekly planning

---

### 5. Save Session
**Keyword**: `;save`
**Expands to**: `Update WORKING-CONTEXT.md with today's progress and completed tasks`

**Use**: End of session to save progress

---

### 6. Show Projects
**Keyword**: `;proj`
**Expands to**: `Show all active projects from PROJECT-REGISTRY.md with status`

**Use when**: You want to see all projects at a glance

---

### 7. Health Check
**Keyword**: `;health`
**Expands to**: `Run health check: verify CLAUDE.md, backups, and automations are working`

**Use**: Weekly to verify system health

---

### 8. Restore Backup
**Keyword**: `;restore`
**Expands to**:
```
restore-s3
# I need to restore from backup before {cursor}
```

**Use when**: Emergency - need to restore from S3 backup

---

### 9. WalterSignal Shortcut
**Keyword**: `;ws`
**Expands to**: `Continue WalterSignal - show dashboard project status and next actions`

**Use**: Quick shortcut for your primary project

---

### 10. Add to Backlog
**Keyword**: `;backlog`
**Expands to**: `Add to backlog: {cursor}`

**Use**: Quick capture of ideas/tasks to Airtable backlog

**Example**: `;backlog` → `Add to backlog: Research competitor pricing`

---

### 11. Yesterday's Work
**Keyword**: `;yesterday`
**Expands to**: `What did we accomplish yesterday? Show completed tasks and current blockers`

**Use**: Start of day to review what was done

---

### 12. Update Week Focus
**Keyword**: `;focus`
**Expands to**:
```
Update Current Week Focus in CLAUDE.md:
Week of: {date:YYYY-MM-DD}
Primary Project: {cursor}
Next Actions:
```

**Use**: Monday mornings to update weekly focus

---

## Daily Workflow with Snippets

### Morning Routine (5 minutes)

**1. Start Claude Code**

**2. Type**: `;ctx`
```
Load context: What am I working on this week?
```

**3. Review** what Claude shows you

**4. (Optional) Type**: `;yesterday`
```
What did we accomplish yesterday?
```

**5. Start working**

---

### During Work

**Switch projects**: `;cont` → type project name

**Add quick task**: `;backlog` → type task

**Deep dive**: `;deep` → type project name

---

### End of Day

**Save progress**: `;save`
```
Update WORKING-CONTEXT.md with today's progress
```

**Done!** (S3 backup runs automatically at 2 AM)

---

### Monday Morning (Weekly Review)

**1. Weekly review**: `;weekly`
```
Review this week's progress and suggest priorities
```

**2. Update focus**: `;focus`
```
Update Current Week Focus in CLAUDE.md
```

**3. Health check**: `;health`
```
Verify everything is working
```

---

## Keyboard Shortcuts

**Alfred doesn't require you to press anything after typing the keyword!**

Just type:
- `;ctx` → Snippet expands automatically
- `;cont` → Snippet expands, cursor ready for project name
- `;ws` → Instant WalterSignal context

**No Enter key needed** (unless snippet has {cursor} placeholder)

---

## Advanced: Custom Snippets

### Add Your Own Project Shortcuts

**Create snippet for FlyFlat:**
1. Alfred Preferences → Features → Snippets
2. Click "Claude Code" collection
3. Click `+` at bottom
4. Name: "Claude: FlyFlat"
5. Keyword: `;ff`
6. Snippet: `Continue FlyFlat - show status and next actions`

**Create snippet for SpecialAgentStanny:**
- Keyword: `;sas`
- Snippet: `Continue SpecialAgentStanny - show production status`

---

## Troubleshooting

### Snippets Not Expanding

**Check:**
1. Alfred Preferences → Features → Snippets
2. "Automatically expand snippets by keyword" is checked
3. You're typing in a text field (not in terminal - use for Claude Code chat only)

### Can't Find Imported Snippets

1. Alfred Preferences → Features → Snippets
2. Look for "Claude Code" collection in left sidebar
3. If not there, re-import from Desktop

### Snippets Expand in Wrong Places

**Alfred Settings:**
1. Preferences → Features → Snippets
2. Click "Advanced"
3. Add apps to ignore list if needed

---

## Snippet File Location

**Desktop**: `~/Desktop/Claude-Code-Snippets.alfredsnippets`

**Backup**: Already in CLAUDE.md documentation

**To re-import**: Just double-click the `.alfredsnippets` file

---

## Pro Tips

### 1. Muscle Memory
Practice these 3 most important ones:
- `;ctx` - Session start (every time)
- `;cont` - Continue project
- `;save` - Save session

### 2. Create Project Shortcuts
For your main projects:
- `;ws` - WalterSignal (already included)
- `;ff` - FlyFlat (add custom)
- `;sas` - SpecialAgentStanny (add custom)

### 3. Chain Commands
Type multiple snippets in one go:
```
;ctx
[wait for Claude's response]
;ws
[start working]
```

### 4. Use in VS Code, Cursor, Any App
Alfred snippets work everywhere, not just Claude Code!
- Works in Slack (for team updates)
- Works in email (for status reports)
- Works in notes apps

---

## Comparison: Alfred vs Other Methods

### Alfred Snippets ✅ (Recommended)
- **Pros**: Works everywhere, fast, no special setup per app
- **Cons**: Requires Alfred Powerpack ($$$)
- **Speed**: Instant
- **Complexity**: Easy

### macOS Text Replacement
- **Pros**: Free, built-in
- **Cons**: Less reliable, limited features
- **Speed**: Fast
- **Complexity**: Easy

### Shell Aliases
- **Pros**: Free, works in terminal
- **Cons**: Terminal only, extra steps (copy/paste)
- **Speed**: Medium
- **Complexity**: Medium

### iTerm2 Bindings
- **Pros**: Free if you use iTerm2
- **Cons**: Only works in iTerm2
- **Speed**: Fast
- **Complexity**: Hard

**Winner**: Alfred (if you have Powerpack), otherwise macOS Text Replacement

---

## Next Steps

**Right now:**
1. Double-click `Claude-Code-Snippets.alfredsnippets` on Desktop
2. Import into Alfred
3. Try `;ctx` in Claude Code

**This week:**
- Use `;ctx` every session start
- Try `;ws` when working on WalterSignal
- Use `;save` at end of day

**Next Monday:**
- Use `;weekly` for weekly review
- Use `;focus` to update week focus
- Use `;health` to verify system

---

## Summary

**12 snippets ready to use:**
- `;ctx` - Session start (use every time) ⭐
- `;cont` - Continue project
- `;deep` - Deep dive
- `;weekly` - Weekly review
- `;save` - Save session
- `;proj` - Show projects
- `;health` - Health check
- `;restore` - Restore backup
- `;ws` - WalterSignal shortcut
- `;backlog` - Add to backlog
- `;yesterday` - Yesterday's work
- `;focus` - Update week focus

**Installation**: Double-click `.alfredsnippets` file on Desktop

**Daily use**: Just type `;ctx` to start each session!

---

**Created**: November 2, 2025
**For**: Mike Finneran
**Alfred Version**: 5
**Collection**: Claude Code
