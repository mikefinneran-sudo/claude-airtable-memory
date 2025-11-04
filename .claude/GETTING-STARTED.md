# Getting Started with Warp Project Manager

**You're all set up! Here's how to start using it.**

---

## Step 1: Reload Your Shell (30 seconds)

```bash
source ~/.zshrc
```

---

## Step 2: Try Opening a Project (1 minute)

**Interactive menu:**
```bash
cproject
```

**Or directly:**
```bash
cproject granola
```

A new Warp tab will open in your project directory!

---

## Step 3: Start Claude Code (1 minute)

In the new Warp tab:

```bash
claude
```

Then say:

```
Continue granola
```

Claude will automatically load your project context.

---

## Daily Workflow

### Morning
```bash
cproject [project-name]
# Wait for Warp tab
claude
"Continue [project-name]"
```

### During Work
- Use `/clear` between major tasks
- Watch context meter (bottom right)
- Use `/compact` at 70%

### End of Day
```bash
ccontext status
ccontext archive  # If needed
```

---

## Available Commands

```bash
cproject              # Open project
cresearch [name] ""   # Research with Perplexity
ccontext status       # Check context
ccontext tips         # Show tips
cwarp                 # Regenerate configs
```

---

## Documentation

- **This file**: Getting started basics
- **Quick Start**: `~/.claude/WARP-QUICKSTART.md`
- **Full Guide**: `~/.claude/WARP-PROJECT-MANAGER.md`
- **Implementation**: `~/.claude/WARP-IMPLEMENTATION-SUMMARY.md`

---

## Need Help?

**Show context tips:**
```bash
ccontext tips
```

**Read full documentation:**
```bash
cat ~/.claude/WARP-PROJECT-MANAGER.md
```

---

## What Was Built

1. **Warp Launch Configurations** - One tab per project
2. **Project Initialization** - Opens tabs with one command
3. **Perplexity Integration** - Automated research
4. **Context Management** - Prevent token limits
5. **Shell Aliases** - Easy-to-remember commands

---

## Next Steps

1. Reload your shell: `source ~/.zshrc`
2. Try opening a project: `cproject`
3. Start Claude Code in the new tab
4. Start working!

---

**Ready to go! Try `cproject` now.**
