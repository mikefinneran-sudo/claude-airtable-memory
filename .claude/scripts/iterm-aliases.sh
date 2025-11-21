#!/bin/bash
# iTerm2 Quick Access Aliases
# Add to ~/.zshrc: source ~/.claude/scripts/iterm-aliases.sh

# Layout shortcuts
alias it-tdd='~/.claude/scripts/iterm-layout-tdd.sh'
alias it-fullstack='~/.claude/scripts/iterm-layout-fullstack.sh'
alias it-remote='~/.claude/scripts/iterm-layout-remote.sh'

# Project quick launch
alias it-ws='it-fullstack ~/Documents/ObsidianVault/Projects/WalterSignal'
alias it-ce='it-tdd ~/Documents/ObsidianVault/Projects/claude-efficiency-system'
alias it-lh='it-tdd ~/Documents/ObsidianVault/Projects/LifeHub'
alias it-ivy='it-tdd ~/Documents/ObsidianVault/Projects/ivy-league-ai-education'

# DGX Spark (GPU server with Claude Code + GPT-OSS)
alias dgx='ssh mikefinneran@192.168.68.88'
alias dgx-claude='ssh mikefinneran@192.168.68.88 -t "tmux -CC new -A -s dgx-claude"'
alias dgx-gpu='ssh mikefinneran@192.168.68.88 -t "watch -n 2 nvidia-smi"'
alias it-dgx='~/.claude/scripts/iterm-layout-dgx-claude.sh'

# Configuration
alias it-setup='~/.claude/scripts/iterm-complete-setup.sh'
alias it-statusbar='~/.claude/scripts/iterm-configure-statusbar.sh'
alias it-help='cat ~/.claude/scripts/iterm-quick-reference.md | less'

# Utilities
alias it-reload='osascript -e "quit app \"iTerm\"" && open -a iTerm'
alias it-backup='defaults export com.googlecode.iterm2 ~/.claude/backups/iterm2-backup-$(date +%Y%m%d-%H%M%S).plist'
alias it-profiles='ls -lh ~/Library/Application\ Support/iTerm2/DynamicProfiles/'

# tmux integration
alias tm='tmux -CC'
alias tma='tmux -CC attach -t'
alias tms='tmux -CC new -A -s'

# Quick reference
alias it-shortcuts='echo "
iTerm2 Quick Shortcuts:
  Cmd+Shift+Up/Down - Navigate commands
  Cmd+Shift+A - Select last output
  Cmd+Opt+A - Alert on complete
  Cmd+D - Split vertical
  Cmd+Shift+D - Split horizontal
  Cmd+O - Switch profile

Layout Commands:
  it-tdd [dir] - TDD layout
  it-fullstack [dir] - Full stack layout
  it-remote user@host - Remote layout

Project Shortcuts:
  it-ws - WalterSignal
  it-ce - Claude Efficiency
  it-lh - LifeHub
  it-ivy - Ivy League AI
  it-dgx - DGX Spark (Claude + GPT-OSS)

DGX Spark Commands:
  dgx - SSH to DGX Spark
  dgx-claude - tmux Claude session
  dgx-gpu - Monitor GPU usage
  it-dgx - Full layout (Claude + GPU monitor)
"'

echo "iTerm2 aliases loaded. Type 'it-shortcuts' for quick reference."
