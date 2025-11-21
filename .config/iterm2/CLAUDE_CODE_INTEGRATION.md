# Claude Code + iTerm2 Integration Guide

## Overview
This guide covers the complete integration of Claude Code CLI with iTerm2, including setup, configuration, MCP integration, and advanced workflows.

---

## Understanding the Ecosystem

### Three Integration Paths

**Path 1: CLI-Native (Recommended for Developers)**
- Uses `claude-code` CLI directly in iTerm2
- Most powerful and agentic approach
- Deep project context via CLAUDE.md files
- Best for: Complex coding tasks, TDD workflows, multi-file refactors

**Path 2: Desktop-Controlled**
- Claude Desktop app controls iTerm2 via MCP
- GUI interface executing terminal commands
- Best for: Users who prefer graphical interface

**Path 3: iTerm-Native AI Plugin**
- Built-in iTerm2 AI features (Cmd+Y)
- Quick, stateless command generation
- Best for: Fast, simple AI assistance

This guide focuses on **Path 1** (CLI-Native) as the primary workflow.

---

## Installation

### Prerequisites

**System Requirements:**
- macOS 10.15+ (12+ recommended)
- Homebrew installed
- Git installed

**Professional Node.js Setup:**

```bash
# Install nvm (Node Version Manager)
brew install nvm

# Configure .zshrc
echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.zshrc
echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.zshrc
echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.zshrc

# Reload shell
source ~/.zshrc

# Install Node.js LTS (v18+)
nvm install --lts
nvm use --lts
```

**Why nvm?** Avoids permission issues and the dangerous `sudo npm install -g` pattern.

### Anthropic API Setup

1. **Create Account:** Sign up at console.anthropic.com
2. **Generate API Key:** Profile Settings → API Keys → "+ Create Key"
3. **Enable Billing:** ⚠️ CRITICAL - API won't work without payment method
4. **Set Usage Limits:** Recommended $5/day to prevent unexpected charges

### Install Claude Code

```bash
# Via npm (recommended)
npm install -g @anthropic-ai/claude-code

# OR via curl installer
curl -fsSL https://claude.ai/install.sh | bash
```

### First-Run Authentication

```bash
# Start claude (opens browser for OAuth)
claude

# Verify installation
claude doctor

# Update in future
claude update
```

---

## Core Usage

### Invocation Modes

**Interactive (REPL) Mode:**
```bash
# Start new session
claude

# Start with initial prompt
claude "explain this project"
```

**Print Mode (Unix Philosophy):**
```bash
# Single query, exit
claude -p "review this code"

# Composable in pipelines
tail -f app.log | claude -p "Alert me if you see anomalies"
```

**Session Management:**
```bash
# Continue last conversation
claude -c

# Resume specific session
claude -r "session-id"
```

### Essential In-Session Commands

| Command | Description |
|---------|-------------|
| `/init` | Create CLAUDE.md context file |
| `/help` | List available commands |
| `/exit` | Exit session |
| `/terminal-setup` | Configure iTerm2 keybindings (⚠️ see warning below) |
| `/config` | Runtime configuration |
| `/agents` | Manage specialized sub-agents |

---

## The CLAUDE.md Context System

### Overview
**CLAUDE.md is the most important feature for "training" Claude Code.**

The `/init` command creates a CLAUDE.md file that Claude automatically reads when starting sessions in that directory. It's persistent "memory" for your project.

### Hierarchical Loading Strategy

```
~/.claude/CLAUDE.md              # Global defaults
repo_root/CLAUDE.md              # Project-specific (commit to Git)
repo_root/CLAUDE.local.md        # Local overrides (.gitignored)
```

Context inherits from parent and child directories - perfect for monorepos.

### What to Include in CLAUDE.md

**High Priority:**
- Common bash commands (e.g., `npm test`, `make build`)
- Core files and utility functions
- Code style guidelines
- Testing instructions
- Branch naming conventions
- Tech stack overview

**Example CLAUDE.md:**
```markdown
# Project Context

## Tech Stack
- Framework: Next.js 14
- Testing: Jest
- Database: PostgreSQL

## Commands
- Tests: `npm test`
- Dev server: `npm run dev`
- Build: `npm run build`

## Conventions
- Test files: `*.test.ts`
- Branch naming: `feature/description`
- No emojis in commit messages
```

### Live Updates
Press `#` during a session to have Claude save an instruction to CLAUDE.md.

---

## iTerm2 Configuration

### Keybinding Configuration

**⚠️ CRITICAL WARNING: Do NOT run `/terminal-setup`**

The `/terminal-setup` command creates a global iTerm2 keybinding that **breaks Shift+Enter in Neovim, Vim, yazi, helix, and other TUI apps.**

**Recommended Solution: Manual Option+Enter Setup**

1. Open iTerm2 → Settings → Profiles → Keys
2. Under "General" section:
   - Set "Left Option Key" to: **Esc+**
   - Set "Right Option Key" to: **Esc+**
3. Use **Option+Enter** for multi-line input in Claude Code

This avoids the global binding conflict.

### Notification Setup

Get macOS notifications when long Claude tasks complete:

**1. Configure iTerm2:**
- Settings → Profiles → Terminal
- Enable: "Silence bell"
- Enable: "Send escape sequence-generated alerts" (Filter Alerts section)

**2. Configure Claude Code:**
```bash
claude config set preferredNotifChannel iterm2
```

### Shell Aliases for Rapid Workflows

Add to `~/.zshrc`:

```bash
# Start new claude session
alias c='claude'

# Single-shot print mode
alias cp='claude -p'

# Continue last session
alias cc='claude -c'

# YOLO mode: skip permission prompts (use with caution)
alias yolo='claude --dangerously-skip-permissions'
```

Reload: `source ~/.zshrc`

---

## MCP Integration (Advanced)

### Path 2A: Claude Desktop Controls iTerm2

**Method 1: Smithery (Easiest)**
```bash
npx -y @smithery/cli install iterm-mcp --client claude
```

**Method 2: Manual Config**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iterm-mcp": {
      "command": "npx",
      "args": ["-y", "iterm-mcp"]
    }
  }
}
```

**Method 3: Desktop Extensions (New)**
- Open Claude Desktop
- Settings → Extensions
- Install "iTerm2" extension

### Path 2B: Claude Code CLI Controls iTerm2

**Advanced technique** - Claude Code CLI can also act as MCP host:

```bash
claude mcp add-json "iterm-mcp" '{"command":"npx","args":["-y","iterm-mcp"]}'
```

### 🚨 CRITICAL: macOS Permissions

**This is the #1 failure point for MCP integration.**

iterm-mcp uses AppleScript to control iTerm2. Without permissions, it fails silently.

**Required Steps:**

1. **Automation Permissions:**
   - macOS Settings → Privacy & Security → Automation
   - Find "Claude" (Desktop) or "iTerm.app" (CLI)
   - Enable checkbox for: **iTerm.app**

2. **Accessibility Permissions:**
   - Privacy & Security → Accessibility
   - Add your host application (Claude/iTerm)

3. **Restart & Verify:**
   - Quit and restart host application completely
   - Ask: "What tools do you have?"
   - Should list: `write_to_terminal`, `read_terminal_output`

---

## TDD Workflow Example

Complete Test-Driven Development session using CLAUDE.md:

```bash
# Step 1: Initialize context
cd my-project
claude
> /init

# Step 2: Edit CLAUDE.md
# Add: "This project uses Jest. Test files: *.test.js. Run: npm test"

# Step 3: Start TDD loop
> Write a failing test for /api/user endpoint returning {id, name}

# Step 4: Confirm failure (in separate terminal)
npm test  # Should fail

# Step 5: Write implementation
claude -c
> The test fails as expected. Write minimal implementation to pass.

# Step 6: Confirm success
npm test  # Should pass

# Step 7: Refactor
> Refactor the new code for clarity and efficiency
```

---

## Global Configuration

### View/Modify Settings

```bash
# List all settings
claude config list

# Change setting
claude config set <key> <value>

# Examples
claude config set theme dark
claude config set autoUpdates false
```

Settings stored in: `~/.claude/settings.json`

---

## Advanced: Local Models (Path 1 + Ollama)

### The "Holy Grail" Setup
Combine Claude Code's superior agentic interface with free, local models.

**Requirements:**
- Ollama installed
- Anthropic-to-Ollama proxy (e.g., claude-code-ollama-proxy)

**Setup:**

```bash
# 1. Install Ollama
brew install ollama
ollama pull llama3

# 2. Set up proxy (see: github.com/mattlqx/claude-code-ollama-proxy)
# Follow proxy setup instructions

# 3. Configure environment
export ANTHROPIC_API_KEY="your_proxy_api_key"
export ANTHROPIC_API_URL="http://localhost:8008/v1"

# 4. Run claude
claude "My prompt for the local model"
```

**Result:** Full Claude Code features (CLAUDE.md, agents, stateful sessions) with local, private inference.

---

## Troubleshooting

### Common Issues

**1. MCP Fails to Run**
- **Cause:** macOS Automation permissions not granted
- **Fix:** System Settings → Privacy & Security → Automation
- Enable host app to control iTerm.app

**2. Shift+Enter Breaks Neovim/Vim**
- **Cause:** Ran `/terminal-setup` command
- **Fix:** Manually remove global keybinding from iTerm2 settings
- Use Option+Enter instead (see Keybinding Configuration above)

**3. API Key Fails**
- **Cause:** Billing not enabled in Anthropic Console
- **Fix:** console.anthropic.com → Billing → Add payment method

**4. Python `pip` Error: externally-managed-environment**
- **Cause:** Violating PEP 668 (system Python protection)
- **Fix:** Use `pipx` for tools, `venv` for projects (never `pip install` globally)

---

## Best Practices

### Session Management
- Use `/init` in every project
- Update CLAUDE.md as project evolves
- Use `claude -c` to continue instead of starting fresh
- Keep CLAUDE.md under 500 lines (use links for longer docs)

### Performance
- Use `-p` (print mode) for scripting/pipelines
- Run `claude doctor` if experiencing issues
- Update regularly with `claude update`

### Security
- Set daily usage limits in Anthropic Console
- Never commit API keys to Git
- Use CLAUDE.local.md for sensitive/local overrides
- Review `--dangerously-skip-permissions` carefully before use

### Workflow Integration
- Create iTerm2 triggers for build status
- Use shell aliases for rapid access
- Set up notifications for long tasks
- Leverage shell integration (Cmd+Shift+A for output selection)

---

## Comparison with Alternatives

### Claude Code vs GitHub Copilot CLI
- **Claude Code:** Agentic, repository-aware, multi-file refactors, planning
- **Copilot CLI:** Lower latency, GitHub integration, PR/security features

### Claude Code vs Warp
- **Claude Code:** Runs in iTerm2, composable, scriptable, uses CLAUDE.md
- **Warp:** Complete terminal replacement, built-in AI, block-based UI

**Strategic Choice:** Claude Code + iTerm2 = power + composability + configurability

---

## Quick Reference

### Common Commands
```bash
claude                          # Start new session
claude "initial prompt"         # Start with prompt
claude -p "query"              # Print mode (single query)
claude -c                      # Continue last session
claude -r "id" "prompt"        # Resume specific session
claude doctor                  # Health check
claude update                  # Update to latest
claude config list             # View settings
claude mcp                     # Manage MCP servers
```

### Essential In-Session
```
/init          # Create CLAUDE.md
/help          # List commands
/exit          # Exit session
/config        # Configure session
/agents        # Manage sub-agents
#              # Save instruction to CLAUDE.md
```

### iTerm2 Shortcuts
```
Cmd+Shift+Up/Down    # Navigate between commands
Cmd+Shift+A          # Select last command output
Cmd+Opt+A            # Alert on next command completion
Shift+Cmd+;          # Command history popup
Cmd+Opt+/            # Recent directories
```

---

## Resources

- [Official Claude Code Docs](https://docs.claude.com/en/docs/claude-code/)
- [Claude Code CLI Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)
- [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [iTerm2 AI Plugin](https://iterm2.com/ai-plugin.html)

---

*Last Updated: 2025-11-08*
*Based on: "The Definitive Guide: Integrating and Mastering Claude in the iTerm2 Terminal"*
