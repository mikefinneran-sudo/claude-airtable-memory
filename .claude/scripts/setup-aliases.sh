#!/bin/bash
# Claude Code Project Manager - Shell Aliases
# Usage: source ~/.claude/scripts/setup-aliases.sh

# Session management
alias resume='~/.claude/scripts/resume-work.sh'
alias continue='~/.claude/scripts/continue-enhanced.sh'
alias save-session='~/.claude/scripts/save-session-memory.sh'
alias start-session='~/.claude/scripts/start-session.sh'
alias session='cat ~/.claude/SESSION-MEMORY.md'
alias context='cat ~/.claude/WORKING-CONTEXT.md'
alias msearch='~/.claude/scripts/memory-search.sh'

# Scripts & activity
alias archive-script='~/.claude/scripts/archive-custom-script.sh'
alias scan-scripts='~/.claude/scripts/scan-project-scripts.sh'
alias activity-summary='~/.claude/scripts/generate-activity-summary.py'

# S3 backups
alias backup-s3='~/.claude/scripts/backup-to-s3.sh'
alias restore-s3='~/.claude/scripts/restore-from-s3.sh'

# Editors
alias vs='code'
alias surf='windsurf'

echo "✅ Claude aliases loaded (resume, session, context, msearch, backup-s3)"
