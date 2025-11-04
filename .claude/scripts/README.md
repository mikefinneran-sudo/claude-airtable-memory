# Claude Code Warp Project Manager - Scripts

This directory contains automation scripts for managing Claude Code projects with Warp terminal.

---

## Quick Reference

### Commands

```bash
cproject              # Open project (interactive or direct)
cresearch [name] ""   # Research with Perplexity Pro
ccontext [command]    # Manage context
cwarp                 # Regenerate Warp configs
```

---

## Scripts

### 1. init-project-session.sh
Opens a project in a new Warp tab

**Usage:**
```bash
./init-project-session.sh                # Interactive menu
./init-project-session.sh granola        # Direct access
```

**Alias:** `cproject`

---

### 2. research-project.sh
Automates research using Perplexity Pro

**Usage:**
```bash
./research-project.sh granola "meeting automation tools"
./research-project.sh granola --list
```

**Alias:** `cresearch`

---

### 3. context-manager.sh
Context management utilities

**Usage:**
```bash
./context-manager.sh status    # Show status
./context-manager.sh archive   # Archive context
./context-manager.sh reset     # Reset weekly
./context-manager.sh switch    # Switch projects
./context-manager.sh tips      # Show tips
```

**Alias:** `ccontext`

---

### 4. generate-warp-configs.sh
Generates Warp launch configurations

**Usage:**
```bash
./generate-warp-configs.sh
```

**Alias:** `cwarp`

---

### 5. setup-aliases.sh
Loads shell aliases

**Usage:**
```bash
source ./setup-aliases.sh
```

**Auto-loaded from ~/.zshrc**

---

### 6. install.sh
Installation script

**Usage:**
```bash
./install.sh
```

**Run once to set up everything**

---

## Documentation

**Quick Start**: `~/.claude/WARP-QUICKSTART.md`

**Full Guide**: `~/.claude/WARP-PROJECT-MANAGER.md`

**Implementation**: `~/.claude/WARP-IMPLEMENTATION-SUMMARY.md`

---

## Directory Structure

```
~/.claude/scripts/
├── init-project-session.sh       # Project opener
├── research-project.sh            # Perplexity automation
├── context-manager.sh             # Context utilities
├── generate-warp-configs.sh       # Config generator
├── setup-aliases.sh               # Alias loader
├── install.sh                     # Installation
└── README.md                      # This file
```

---

## Getting Help

**List commands:**
```bash
cproject --help
cresearch --help
ccontext --help
```

**Read docs:**
```bash
cat ~/.claude/WARP-QUICKSTART.md
cat ~/.claude/WARP-PROJECT-MANAGER.md
```

---

## Version

**Version**: 1.0
**Date**: 2025-10-29
**Status**: Production Ready
