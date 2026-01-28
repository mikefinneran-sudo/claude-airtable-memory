# Session Management Guide

## Session Start Checklist
- [ ] Say: "Check WORKING-CONTEXT.md - what was I working on?"
- [ ] Review current week focus
- [ ] Check if any blockers from last session
- [ ] Verify correct project loaded

## Session End Checklist
- [ ] Update WORKING-CONTEXT.md with progress
- [ ] Note any blockers or open questions
- [ ] Mark completed tasks
- [ ] Push any git changes
- [ ] Run `cc-save` to archive session

## Weekly Review (Monday 9 AM)
- [ ] Update Current Week Focus in CLAUDE.md
- [ ] Archive completed projects
- [ ] Review S3 backup logs: `tail ~/.claude/logs/s3-backup.log`
- [ ] Update PROJECT-REGISTRY.md
- [ ] Verify automations: `launchctl list | grep claude`

---

## Quick Context Snippets

### Session Start
```
Check WORKING-CONTEXT.md - what was I working on?
```

### Project Switch
```
Continue [ProjectName] - show status, next actions, and recent progress
```

### Deep Dive
```
Load full context for [ProjectName] including all research, code, and documentation
```

### Weekly Review
```
Review this week's progress across all projects and suggest priorities for next week
```

### Check Memory
```
What do you remember about [ProjectName]?
```

### Emergency Recovery
```
restore-s3
# Select backup from before issue occurred
```

---

## Custom Commands

### Natural Language
- **"save to guides"** → Save as MD to local guides folder
- **"add to backlog"** / **"backlog: [topic]"** → Create project note in vault
- **"save locally"** → Save to appropriate local project folder
- **"remember this"** → Save to Memory MCP

### Slash Commands (~/.claude/commands/)
- **/backlog** - Add item to backlog
- **/code-review** - Thorough code review
- **/explain-code** - Explain architecture
- **/optimize** - Analyze performance
- **/plan-feature** - Plan with TDD
- **/research** - Create research doc
- **/save-guide** - Save as guide
