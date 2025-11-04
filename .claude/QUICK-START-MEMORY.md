# Quick Start - Memory System

**One command to rule them all**: `resume`

---

## When You Open a New Claude Code Session

### Option 1: Interactive (Recommended)
Just type:
```bash
resume
```

**What you'll see**:
- 📅 Current week focus
- 📊 Recent activity (last 3 sessions)
- 🎯 Active projects
- ✅ This week's goals
- ⚠️ Current blockers
- Interactive project selection menu

**Then**:
1. Pick a project (1-6)
2. Session starts automatically
3. Context loads
4. Ready to work!

### Option 2: Direct Project Load
If you know which project:
```bash
resume waltersignal
# or
resume flyflat
# or
resume specialagentstanny
```

Instantly starts that project's session.

---

## During Your Session

### View Current Session
```bash
session
# Shows: SESSION-MEMORY.md (what you're working on NOW)
```

### View Overall Context
```bash
context
# Shows: WORKING-CONTEXT.md (recent activity, blockers, goals)
```

### Save Your Work
```bash
save-session
# Auto-saves to project's SESSIONS.md
# Updates WORKING-CONTEXT
# Archives session
```

---

## Complete Workflow Example

### Morning - Start Work
```bash
# Open terminal
resume

# Interactive menu appears:
# [Shows your week, goals, blockers, recent work]
#
# Select project:
#   1) WalterSignal  ← Pick this
#   2) FlyFlat
#   ...

# Session starts for WalterSignal
# ✅ Loads README, STATUS, BACKLOG, recent SESSIONS
```

### During - Check Progress
```bash
# What am I working on?
session

# What's my overall context?
context
```

### Evening - Save Work
```bash
# Save the session
save-session

# ✅ Summary saved to ~/.claude/projects/waltersignal/SESSIONS.md
# ✅ WORKING-CONTEXT updated
# ✅ Session archived
```

### Next Day - Resume
```bash
resume

# Shows yesterday's work in "Recent Activity"
# Pick same or different project
# Knows exactly where you left off
```

---

## All Available Commands

| Command | What It Does |
|---------|--------------|
| `resume` | Load memory + start work (MAIN COMMAND) |
| `resume [project]` | Jump directly to a project |
| `start-session [project]` | Start fresh session for project |
| `save-session` | Save current session to history |
| `session` | View current session memory |
| `context` | View working context |

---

## Quick Tips

**✅ DO**:
- Run `resume` at start of every session
- Run `save-session` at end of every session
- Use `session` to check what you're working on
- Trust the system - it remembers everything

**❌ DON'T**:
- Forget to save-session (you'll lose work history)
- Skip resume (Claude won't have context)
- Manually edit SESSION-MEMORY.md during work

---

## Troubleshooting

### "resume command not found"
```bash
# Reload shell config
source ~/.zshrc

# Or restart terminal
```

### "Can't remember what I was doing"
```bash
# Check last session
cat ~/.claude/projects/waltersignal/SESSIONS.md | tail -50

# Check overall context
context
```

### "Lost my session"
```bash
# Check archive
ls -lt ~/.claude/session-archive/

# View archived session
cat ~/.claude/session-archive/session-20251101-*.md
```

---

## Integration with Claude Code

### Start New Claude Code Session
1. Open Claude Code
2. Type: `resume`
3. Pick project
4. Tell Claude: "Continue [project]"
5. Claude loads full context

### During Conversation
Claude automatically:
- References SESSION-MEMORY.md
- Checks project STATUS
- Suggests tasks from BACKLOG
- Remembers decisions

### End Conversation
Before closing:
```bash
save-session
```

---

## What Makes This Powerful

### Instant Context
`resume` shows you EVERYTHING:
- What you worked on recently
- Current blockers
- This week's goals
- Active projects

### Smart Continuity
Each project maintains:
- README (navigation)
- STATUS (current state)
- BACKLOG (next tasks)
- SESSIONS (history)

### No Lost Work
Every session automatically saved to:
- Project's SESSIONS.md
- WORKING-CONTEXT
- Session archive

---

## Aliases Reference

These are loaded automatically when you open terminal:

```bash
resume              # Main command
start-session      # Start new session
save-session       # Save current session
session            # View session memory
context            # View working context

# Also available (from before):
cproject           # Open project in Warp
cresearch          # Research with Perplexity
ccontext           # Manage context
```

---

## Examples

### Example 1: Start Fresh Day
```bash
$ resume

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                   CLAUDE CODE - RESUME WORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Current Week Focus:
   **Week of**: 2025-11-01 (Week 44)
   **Primary Project**: WalterSignal

📊 Recent Activity (Last 3 Sessions):
   → 2025-11-01 14:31 - WalterSignal
   → 2025-10-31 14:42 - WalterSignal
   → 2025-10-30 14:40 - FlyFlat

🎯 Active Projects:
   | WalterSignal | 🟢 Active | ~/.claude/projects/waltersignal/
   | FlyFlat | 🟡 Maintenance | Obsidian vault

✅ This Week's Goals:
   - [x] Fix persistent memory system
   - [ ] Finalize WalterFetch tech stack

Select a project to continue:
  1) WalterSignal
  2) FlyFlat
  ...
```

### Example 2: Direct Load
```bash
$ resume waltersignal

▶ Loading project: waltersignal
✅ Session started: WalterSignal
📝 Session memory: ~/.claude/SESSION-MEMORY.md

Quick reference:
  - Project workspace: ~/.claude/projects/waltersignal
  - Recent sessions: cat ~/.claude/projects/waltersignal/SESSIONS.md
```

### Example 3: Check Session
```bash
$ session

# Current Session Memory

**Session Started**: 2025-11-01 14:31
**Project**: WalterSignal
**Location**: /Users/mikefinneran/Documents/ObsidianVault/Projects/WalterSignal

## Actions Taken This Session
✅ Fixed memory system
✅ Created resume command
...
```

---

## That's It!

**Main command**: `resume`
**End command**: `save-session`
**Check work**: `session`

The system handles the rest.

---

**Created**: 2025-11-01
**For**: Mike Finneran
**Status**: Production Ready ✅

*Just type `resume` and start working.*
