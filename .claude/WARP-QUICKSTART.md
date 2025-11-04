# Warp Project Manager - Quick Start

**5-minute setup guide**

---

## Step 1: Load Shell Aliases (30 seconds)

Add to `~/.zshrc`:

```bash
# Claude Code Project Manager
source ~/.claude/scripts/setup-aliases.sh
```

Reload:
```bash
source ~/.zshrc
```

---

## Step 2: Verify Installation (30 seconds)

```bash
# Check aliases work
ccontext status

# Check Warp configs exist
ls ~/.warp/launch_configurations/
```

You should see:
- `claude-granola.yaml`
- `claude-lifehub-2.0.yaml`
- `claude-persistent-memory.yaml`

---

## Step 3: Open Your First Project (1 minute)

```bash
# Option A: Interactive menu
cproject

# Option B: Direct
cproject granola
```

A new Warp tab will open in the project directory.

---

## Step 4: Start Claude Code (1 minute)

In the new Warp tab:

```bash
claude
```

When Claude starts, say:

```
Continue granola
```

Claude will load:
- Project README
- Current STATUS
- Task BACKLOG

You're ready to work!

---

## Step 5: Try Research (2 minutes)

In a terminal:

```bash
cresearch granola "Granola meeting notes automation"
```

The research prompt is copied to your clipboard.

In Claude Code:
```
Cmd+V
```

Claude will use Perplexity Pro to research and save results.

---

## Daily Workflow

### Morning
```bash
# Start project
cproject [name]

# In new tab
claude
"Continue [name]"
```

### During Work
- Use `/clear` between major tasks
- Watch context meter (bottom right)
- Use `/compact` at 70%

### End of Day
```bash
# Check status
ccontext status

# Archive if needed
ccontext archive
```

---

## Working on Multiple Projects

```bash
# Tab 1: Open first project
cproject granola

# Tab 2: Open second project
cproject lifehub-2.0

# Tab 3: Open third project
cproject persistent-memory
```

Each tab has isolated Claude Code context!

---

## Common Commands

```bash
cproject              # Open project
cresearch [name] ""   # Research
ccontext status       # Check context
ccontext tips         # Show tips
cwarp                 # Regenerate configs
```

---

## Getting Help

**Full docs**: `~/.claude/WARP-PROJECT-MANAGER.md`

**Context tips**: `ccontext tips`

**Troubleshooting**: See main docs

---

## Next Steps

1. Open a project: `cproject`
2. Start Claude: `claude`
3. Load context: `"Continue [project]"`
4. Start coding!

---

**That's it! You're ready to go.**

For detailed documentation, see `WARP-PROJECT-MANAGER.md`
