# Warp Project Manager for Claude Code

**Created**: 2025-10-29
**Version**: 1.0
**Status**: Production Ready

---

## Overview

Automated project management system that integrates Warp terminal, Claude Code, and Perplexity Pro for efficient multi-project development workflows.

### What It Solves

1. **Context Pollution**: Each project opens in a separate Warp tab with isolated Claude Code context
2. **Token Limits**: Avoid hitting context limits by maintaining separate sessions per project
3. **Project Switching**: Switch between projects with one command
4. **Research Efficiency**: Automated documentation gathering with Perplexity Pro
5. **Setup Friction**: Initialize project environments instantly

---

## Architecture

### Components

```
Warp Terminal
    ↓
Launch Configurations (YAML) → Opens tab for each project
    ↓
Project Initialization Script → Sets up environment
    ↓
Claude Code Session → Isolated context per project
    ↓
Perplexity Pro Integration → Automated research
    ↓
Context Management → Prevents token bloat
```

### File Structure

```
~/.claude/
├── scripts/
│   ├── init-project-session.sh       # Main entry point
│   ├── research-project.sh            # Perplexity automation
│   ├── context-manager.sh             # Context utilities
│   ├── generate-warp-configs.sh       # Config generator
│   └── setup-aliases.sh               # Shell aliases
├── templates/
│   └── launch-config.yaml             # Warp config template
└── WARP-PROJECT-MANAGER.md            # This file

~/.warp/launch_configurations/
├── claude-granola.yaml
├── claude-lifehub-2.0.yaml
└── claude-persistent-memory.yaml

~/.claude/projects/
├── granola/
├── lifehub-2.0/
└── persistent-memory/
```

---

## Installation

### Step 1: Verify Installation

The system should already be installed. Verify:

```bash
ls -la ~/.claude/scripts/
ls -la ~/.warp/launch_configurations/
```

### Step 2: Load Shell Aliases

Add to your `~/.zshrc`:

```bash
# Claude Code Project Manager
source ~/.claude/scripts/setup-aliases.sh
```

Then reload:

```bash
source ~/.zshrc
```

### Step 3: Verify Warp Configurations

Open Warp and press `Cmd+P`, type "Launch", and verify you see configurations for your projects.

---

## Usage

### Open Project in New Warp Tab

**Interactive Menu:**
```bash
cproject
```

**Direct Access:**
```bash
cproject granola
cproject lifehub-2.0
cproject persistent-memory
```

**What happens:**
1. Opens new Warp tab in project directory
2. Updates WORKING-CONTEXT.md
3. Displays next steps
4. Ready for Claude Code

### Initialize Claude Code Session

After Warp tab opens:

```bash
claude
```

Then say:
```
Continue [project-name]
```

Claude will automatically:
- Load project README.md
- Load project STATUS.md
- Load project BACKLOG.md
- Set context to that project

### Research with Perplexity Pro

**Start Research:**
```bash
cresearch granola "meeting automation best practices"
cresearch lifehub-2.0 "React dashboard UI patterns"
```

**What happens:**
1. Creates `research/` directory in project
2. Generates research prompt
3. Copies prompt to clipboard
4. Creates placeholder file
5. You paste in Claude Code to complete

**List Research:**
```bash
cresearch granola --list
```

### Manage Context

**Check Status:**
```bash
ccontext status
```

**Switch Project:**
```bash
ccontext switch lifehub-2.0
```

**Archive Context:**
```bash
ccontext archive
```

**Reset Context (Weekly):**
```bash
ccontext reset
```

**Show Tips:**
```bash
ccontext tips
```

### Regenerate Warp Configs

If you add new projects:

```bash
cwarp
```

---

## Workflows

### Starting a Project Session

```bash
# Option 1: Interactive
cproject
# Select project from menu

# Option 2: Direct
cproject granola

# Wait for new Warp tab to open
# In new tab:
claude

# In Claude Code:
"Continue granola"
```

### Switching Between Projects

```bash
# Open second project in new tab
cproject lifehub-2.0

# In new tab:
claude
"Continue lifehub-2.0"

# Now you have:
# - Tab 1: Granola project with isolated context
# - Tab 2: LifeHub project with isolated context
```

### Research Workflow

```bash
# Start research
cresearch granola "Granola API integration methods"

# Prompt is copied to clipboard
# In Claude Code:
Cmd+V  # Paste research prompt

# Claude uses Perplexity to research and saves results
# Results saved to: ~/.claude/projects/granola/research/
```

### End of Day Cleanup

```bash
# Check context status
ccontext status

# If needed, archive
ccontext archive

# Close Warp tabs
# Context saved automatically
```

### Weekly Reset (Monday)

```bash
# Reset working context
ccontext reset

# Review projects
ls ~/.claude/projects/

# Clean up if needed
```

---

## Context Management Strategy

### The Problem

Claude Code has a 200K token context limit. Working on multiple projects or lengthy sessions causes:
- Context compaction at 95% (automatic summarization)
- Loss of detail
- Slower responses
- Need to re-explain things

### The Solution

**1. Separate Warp Tabs = Separate Contexts**

Each Warp tab maintains its own Claude Code session:
- Tab 1: Granola (0/200K tokens)
- Tab 2: LifeHub (0/200K tokens)
- Tab 3: Memory System (0/200K tokens)

**2. Use /clear Between Major Tasks**

Within a single project session:
```
# After completing feature A
/clear

# Start feature B with fresh context
"Continue working on feature B"
```

**3. Use /compact at 70%**

Check context meter (bottom right). At 70%:
```
/compact
```

**4. Project-Specific CLAUDE.md**

Create `.claude/CLAUDE.md` in project directories:
```markdown
# Project-Specific Context

## Architecture
- React + TypeScript
- Node.js backend

## Important Files
- Ignore: /node_modules, /dist
- Focus: /src, /tests

## Coding Standards
- Use functional components
- Jest for testing
```

---

## Perplexity Pro Integration

### How It Works

1. You run: `cresearch [project] "[query]"`
2. Script generates optimized Perplexity prompt
3. Prompt copied to clipboard
4. You paste in Claude Code
5. Claude uses Perplexity MCP server
6. Results saved to project research directory

### Research Types

**Documentation Research:**
```bash
cresearch granola "Granola official API documentation"
```

**Best Practices:**
```bash
cresearch lifehub-2.0 "React dashboard performance optimization"
```

**Competitive Analysis:**
```bash
cresearch granola "meeting automation tools comparison"
```

**Community Resources:**
```bash
cresearch persistent-memory "Claude Code context management strategies"
```

### Research Storage

```
~/.claude/projects/[project-name]/research/
├── 2025-10-29-api-documentation.md
├── 2025-10-29-best-practices.md
└── 2025-10-30-community-resources.md
```

---

## Advanced Features

### Custom Launch Configurations

Edit `~/.warp/launch_configurations/claude-[project].yaml`:

```yaml
---
name: My Project
windows:
  - tabs:
      - title: Project Name
        layout:
          cwd: /absolute/path
          commands:
            - exec: echo "Custom startup message"
            - exec: npm install  # Run on startup
        color: blue
```

### Multiple Tabs Per Project

Modify launch config:

```yaml
---
name: Full Stack Project
windows:
  - tabs:
      - title: Backend
        layout:
          cwd: /path/to/backend
        color: blue
      - title: Frontend
        layout:
          cwd: /path/to/frontend
        color: green
      - title: Database
        layout:
          cwd: /path/to/db
        color: magenta
```

### Split Panes

```yaml
---
name: Side by Side
windows:
  - tabs:
      - title: Code + Logs
        layout:
          split_direction: vertical
          panes:
            - cwd: /path/to/code
            - cwd: /path/to/logs
        color: blue
```

---

## Troubleshooting

### Warp Tab Doesn't Open

**Symptom:** `open warp://...` does nothing

**Solution:**
1. Ensure Warp is installed: `/Applications/Warp.app`
2. Try opening Warp first
3. Run command again

### Launch Configuration Not Showing

**Symptom:** Config not in Warp's Command Palette

**Solution:**
1. Check file location: `ls ~/.warp/launch_configurations/`
2. Verify YAML syntax (no tabs, proper indentation)
3. Ensure `cwd` is absolute path (not `~`)
4. Restart Warp

### Context Not Loading

**Symptom:** Claude doesn't remember project

**Solution:**
1. Check files exist: `ls ~/.claude/projects/[name]/`
2. Verify README.md, STATUS.md present
3. Try: `"Read the project README and STATUS files"`

### Perplexity Not Working

**Symptom:** Research prompt fails

**Solution:**
1. Verify MCP server: Check Claude Code settings
2. Check API key: `echo $PERPLEXITY_API_KEY`
3. Restart Claude Code
4. Check Perplexity API status

### Scripts Not Found

**Symptom:** `cproject: command not found`

**Solution:**
```bash
# Reload shell config
source ~/.zshrc

# Or manually source
source ~/.claude/scripts/setup-aliases.sh

# Verify scripts exist
ls -la ~/.claude/scripts/
```

---

## Tips & Best Practices

### Context Hygiene

1. **Start Clean**: Use `cproject` for new sessions
2. **Clear Often**: Run `/clear` between major tasks
3. **Compact Early**: Don't wait until 95%, compact at 70%
4. **Weekly Reset**: Run `ccontext reset` every Monday
5. **Archive Old**: Archive context monthly

### Project Organization

1. **Small Projects**: Keep project docs under 50KB each
2. **Update STATUS**: Claude updates STATUS.md automatically
3. **Clear BACKLOG**: Remove completed tasks weekly
4. **Document Decisions**: Use DECISIONS.md for major choices

### Research Efficiency

1. **Specific Queries**: Be precise in research questions
2. **Cache Results**: Don't research the same thing twice
3. **Check First**: Run `cresearch [project] --list` before researching
4. **Link in README**: Reference research docs in project README

### Warp Configuration

1. **Color Code**: Use consistent colors per project type
2. **Descriptive Names**: Clear project titles in configs
3. **Startup Commands**: Add useful startup commands
4. **Test Configs**: Open manually first to verify

---

## Maintenance

### Daily

- Archive context if needed: `ccontext archive`
- Close unused Warp tabs
- Let Claude update STATUS.md

### Weekly (Monday)

```bash
# Reset context for new week
ccontext reset

# Check project status
ccontext status

# Review active projects
ls ~/.claude/projects/
```

### Monthly

```bash
# Archive completed projects
mkdir ~/.claude/projects/archive
mv ~/.claude/projects/old-project ~/.claude/projects/archive/

# Regenerate Warp configs
cwarp

# Clean up research files
# Keep only recent/relevant research
```

---

## Integration with Existing System

### Works With

- **Persistent Memory System**: Reads PROJECT-REGISTRY.md
- **CLAUDE.md**: Uses global preferences
- **WORKING-CONTEXT.md**: Updates on project switch
- **Project Structure**: Uses existing README, STATUS, BACKLOG
- **Perplexity MCP**: Integrates with existing server

### Doesn't Conflict With

- Existing Claude Code workflows
- Manual project navigation
- Git operations
- Other terminal usage

---

## Future Enhancements

### Planned

- [ ] Alfred workflow for quick project access
- [ ] Raycast extension integration
- [ ] Automatic context monitoring
- [ ] Project templates for new projects
- [ ] Batch research for multiple queries
- [ ] Integration with PROJECT-REGISTRY.md automation
- [ ] Session analytics (time per project)

### Not Planned

- Multi-user support (single-user system)
- Cloud sync (local-first design)
- Web interface (CLI-focused)

---

## Commands Quick Reference

```bash
# Project Management
cproject                    # Interactive menu
cproject [name]             # Open specific project

# Research
cresearch [name] "[query]"  # Start research
cresearch [name] --list     # List research files

# Context Management
ccontext status             # Show current status
ccontext switch [name]      # Switch projects
ccontext archive            # Archive context
ccontext reset              # Reset context
ccontext tips               # Show tips

# Configuration
cwarp                       # Regenerate Warp configs
```

---

## Support

**Issues**: Check troubleshooting section above

**Logs**: Check `~/.claude/archive/` for context backups

**Reset**: Delete `~/.warp/launch_configurations/` and run `cwarp`

**Documentation**: This file and individual script `--help`

---

## Credits

**Created by**: Claude Code
**For**: Mike Finneran
**Date**: 2025-10-29
**Version**: 1.0

**Built with**:
- Warp Terminal (Launch Configurations)
- Claude Code (AI pair programming)
- Perplexity Pro (AI research)
- Bash scripting

---

**Status**: Production Ready ✅
**Last Updated**: 2025-10-29
**Maintained By**: Mike Finneran
