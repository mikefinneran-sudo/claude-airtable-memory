#!/bin/bash
# Setup Shell Aliases for Claude Code Project Manager
# Author: Claude Code
# Usage: source ~/.claude/scripts/setup-aliases.sh

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Define aliases
alias cproject='~/.claude/scripts/init-project-session.sh'
alias cresearch='~/.claude/scripts/research-project.sh'
alias ccontext='~/.claude/scripts/context-manager.sh'
alias cwarp='~/.claude/scripts/generate-warp-configs.sh'

# Memory management aliases
alias resume='~/.claude/scripts/resume-work.sh'
alias continue='~/.claude/scripts/continue-enhanced.sh'
alias save-session='~/.claude/scripts/save-session-memory.sh'
alias start-session='~/.claude/scripts/start-session.sh'
alias session='cat ~/.claude/SESSION-MEMORY.md'
alias context='cat ~/.claude/WORKING-CONTEXT.md'
alias memory-search='~/.claude/scripts/memory-search.sh'
alias msearch='~/.claude/scripts/memory-search.sh'

# Custom scripts archival
alias archive-script='~/.claude/scripts/archive-custom-script.sh'
alias scan-scripts='~/.claude/scripts/scan-project-scripts.sh'

# Activity tracking and summaries
alias activity-summary='~/.claude/scripts/generate-activity-summary.py'
alias weekly-summary='~/.claude/scripts/generate-activity-summary.py week'
alias monthly-summary='~/.claude/scripts/generate-activity-summary.py month'

# S3 backups and archival
alias backup-s3='~/.claude/scripts/backup-to-s3.sh'
alias restore-s3='~/.claude/scripts/restore-from-s3.sh'
alias s3-setup='~/.claude/scripts/setup-s3-integration.sh'

# Command Center
alias command-center='~/.claude/command-center/launch.sh'
alias cc='~/.claude/command-center/launch.sh'
alias boardroom='open http://localhost:8000/boardroom.html'

# Code Editors
alias vscode='code'
alias vs='code'
alias ai-code='cursor'  # AI-powered editor
alias surf='windsurf'   # Windsurf editor

echo -e "${GREEN}✅ Claude Code Project Manager aliases loaded!${NC}\n"
echo -e "${BLUE}Available commands:${NC}"
echo -e "  ${GREEN}resume${NC}         - Load memory & resume work"
echo -e "  ${GREEN}continue${NC}       - Enhanced continue with preview"
echo -e "  ${GREEN}start-session${NC}  - Start new project session"
echo -e "  ${GREEN}save-session${NC}   - Save current session"
echo -e "  ${GREEN}session${NC}        - View current session memory"
echo -e "  ${GREEN}context${NC}        - View working context"
echo -e "  ${GREEN}memory-search${NC}  - Search all memory files"
echo -e "  ${GREEN}msearch${NC}        - Alias for memory-search"
echo -e "  ${GREEN}archive-script${NC} - Archive custom script to GitHub"
echo -e "  ${GREEN}scan-scripts${NC}   - Scan all projects for scripts"
echo ""
echo -e "  ${GREEN}activity-summary${NC}  - Generate activity summary"
echo -e "  ${GREEN}weekly-summary${NC}    - Last week's activity"
echo -e "  ${GREEN}monthly-summary${NC}   - Last month's activity"
echo ""
echo -e "  ${GREEN}backup-s3${NC}      - Backup to S3 storage"
echo -e "  ${GREEN}restore-s3${NC}     - Restore from S3 backup"
echo -e "  ${GREEN}s3-setup${NC}       - Configure S3 integration"
echo ""
echo -e "  ${GREEN}command-center${NC} - Launch elite control dashboard"
echo -e "  ${GREEN}cc${NC}             - Alias for command-center"
echo -e "  ${GREEN}boardroom${NC}      - Open boardroom (agent teams chat)"
echo ""
echo -e "  ${GREEN}code${NC}       - VS Code editor"
echo -e "  ${GREEN}cursor${NC}     - AI-powered Cursor editor"
echo -e "  ${GREEN}windsurf${NC}   - Windsurf editor"
echo -e "  ${GREEN}ai-code${NC}    - Alias for Cursor"
echo ""
echo -e "  ${GREEN}cproject${NC}   - Open project in new Warp tab"
echo -e "  ${GREEN}cresearch${NC}  - Research with Perplexity Pro"
echo -e "  ${GREEN}ccontext${NC}   - Manage context and sessions"
echo -e "  ${GREEN}cwarp${NC}      - Regenerate Warp configs\n"
echo -e "${BLUE}Examples:${NC}"
echo -e "  ${YELLOW}resume${NC}                    # Interactive project selection"
echo -e "  ${YELLOW}resume waltersignal${NC}       # Resume specific project"
echo -e "  ${YELLOW}start-session flyflat${NC}    # Start new session"
echo -e "  ${YELLOW}save-session${NC}              # Save current work"
echo -e "  ${YELLOW}session${NC}                   # View what you're working on"
echo ""
echo -e "  ${YELLOW}cproject granola${NC}"
echo -e "  ${YELLOW}cresearch granola \"meeting automation tools\"${NC}"
echo -e "  ${YELLOW}ccontext status${NC}\n"
