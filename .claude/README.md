# Claude Code Memory System

**Automated project context and universal instructions for Claude Code**

Last Updated: 2025-10-20

---

## Overview

This directory contains your Claude Code configuration, including global instructions and project automation scripts. Claude automatically loads these files to maintain context across sessions.

## File Structure

```
~/.claude/
├── CLAUDE.md                    # Global instructions (auto-loaded)
├── README.md                    # This file
├── init-project-memory.sh       # Project initialization script
├── shell-integration.sh         # Shell commands and aliases
├── settings.local.json          # Tool permissions & config
└── projects/                    # Project-specific profiles
```

---

## CLAUDE.md - Global Memory

**Location:** `~/.claude/CLAUDE.md`

This file is **automatically loaded** by Claude Code in every session. It contains:

- Your coding preferences and workflow
- File naming conventions
- Communication style preferences
- Default save locations
- Active projects and context
- Development best practices

**When to update:**
- New preferences emerge
- Workflow changes
- New projects start
- Tools or integrations added

**Edit with:**
```bash
code ~/.claude/CLAUDE.md
# or
nano ~/.claude/CLAUDE.md
```

---

## Project Memory System

### Commands

Three shell commands are available (loaded from `shell-integration.sh`):

#### `claude-init`
Initialize Claude memory for a project

**Usage:**
```bash
# In project directory
cd ~/my-project
claude-init

# Or specify path
claude-init ~/path/to/project
```

**What it does:**
1. Creates `.claude/` directory
2. Auto-detects project type (Python, Node.js, Rust, Go, Java)
3. Identifies tech stack (React, TypeScript, etc.)
4. Generates customized CLAUDE.md template
5. Includes git repository info

**Output:**
- Creates `.claude/CLAUDE.md` with pre-filled template
- Prompts before overwriting existing files

#### `claude-edit`
Quick-edit current project's memory

**Usage:**
```bash
cd ~/my-project
claude-edit
```

Opens `.claude/CLAUDE.md` in your default editor (`$EDITOR` or nano).

#### `claude-show`
Display current project's memory

**Usage:**
```bash
cd ~/my-project
claude-show
```

Prints the contents of `.claude/CLAUDE.md` to terminal.

---

## How It Works

### Automatic Context Loading

When you start Claude Code in any directory:

1. **Global context** loads from `~/.claude/CLAUDE.md`
2. **Project context** loads from `./claude/CLAUDE.md` (if it exists)
3. Both contexts remain available throughout the session

### Project Workflow

**One-time setup per project:**

```bash
# Navigate to project
cd ~/my-awesome-project

# Initialize
claude-init

# Customize
claude-edit
```

**Fill in the template:**
- Project overview and purpose
- Architecture and key files
- Coding standards
- Development commands
- Business context
- Current work/tasks

**Commit to git (recommended):**
```bash
git add .claude/CLAUDE.md
git commit -m "Add Claude project memory"
```

**Result:** Next time you work on this project, Claude automatically knows:
- Project architecture
- Coding conventions
- Key files and their purposes
- Common commands
- Current focus areas

---

## Project Template Structure

The generated `.claude/CLAUDE.md` includes:

```markdown
# Project: [auto-detected name]

## Overview
[What this project does]

## Project Type
- Type: [auto-detected: Python, Node.js, etc.]
- Tech Stack: [auto-detected: React, TypeScript, etc.]
- Repository: [auto-detected from git]

## Architecture
[Project structure, key directories, component interaction]

## Key Files & Directories
[Important files and their purposes]

## Coding Standards
[Project-specific conventions]

## Development Commands
[Common commands: build, test, run, deploy]

## Dependencies & Setup
[Special requirements]

## Business Context
[Domain knowledge, business logic]

## Current Work
[What you're working on now]
```

---

## Best Practices

### Global Memory (CLAUDE.md)
- Keep universal preferences only
- Update when workflows change
- Document tool integrations
- Track active projects

### Project Memory (.claude/CLAUDE.md)
- Be specific to the project
- Update as architecture evolves
- Document key decisions
- Track current focus
- Include team conventions

### Maintenance
- Review monthly
- Update after major changes
- Clean up stale information
- Keep current work section fresh

---

## Integration with Other Tools

### Obsidian Vault
Your Obsidian vault is at: `~/Documents/ObsidianVault`

**Resources folder:** `~/Documents/ObsidianVault/Resources/`
- Contains guides, goals, templates
- See `Resources/Claude Code Guide.md` for integration details

### Shell Aliases
Already configured in `~/.zshrc`:
```bash
obs-daily      # Create today's Obsidian note
obs-metrics    # Update metrics
obs-open       # Open Obsidian dashboard
obs-vault      # Navigate to vault

claude-init    # Initialize project memory
claude-edit    # Edit project memory
claude-show    # Show project memory
```

---

## Advanced: Auto-initialization (Optional)

To automatically prompt for initialization when entering new git repos, uncomment in `~/.zshrc`:

```bash
# Edit ~/.zshrc and uncomment:
auto_claude_init() {
    if [ -d .git ] && [ ! -f .claude/CLAUDE.md ]; then
        echo "📋 New git project detected. Initialize Claude memory? (y/N)"
        read -q && echo && claude-init
    fi
}

chpwd_functions+=(auto_claude_init)
```

Then reload: `source ~/.zshrc`

---

## Troubleshooting

**Commands not found:**
```bash
source ~/.zshrc
```

**CLAUDE.md not loading:**
- Check file exists: `ls -la ~/.claude/CLAUDE.md`
- Check file permissions: `chmod 644 ~/.claude/CLAUDE.md`
- Restart Claude Code session

**Project context not loading:**
- Check file exists: `ls -la .claude/CLAUDE.md`
- Ensure you're in correct directory: `pwd`
- Try `claude-show` to verify content

---

## Related Documentation

- **Obsidian Integration:** `~/Documents/ObsidianVault/Resources/Claude Code Guide.md`
- **Project Template:** Run `claude-init` in any directory to see example
- **Claude Code Docs:** https://docs.claude.com/claude-code

---

## Quick Reference Card

```bash
# Setup new project
claude-init

# Edit memories
code ~/.claude/CLAUDE.md          # Global
claude-edit                       # Current project

# View memories
cat ~/.claude/CLAUDE.md           # Global
claude-show                       # Current project

# Reload shell
source ~/.zshrc
```

---

**Questions?** Reference this file or ask Claude about the memory system.
