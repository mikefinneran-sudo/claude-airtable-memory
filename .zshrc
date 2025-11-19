export PATH="$HOME/.local/bin:$PATH"

# iTerm2 Shell Integration
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# Claude Code Integration
source ~/.claude/shell-integration.sh

# Google Drive Documents shortcut
alias docs="cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents"
alias gdocs="cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents"

# Obsidian Life Hub Shortcuts
alias obs-daily="~/Documents/ObsidianVault/.scripts/create_daily_note.sh"
alias obs-metrics="python3 ~/Documents/ObsidianVault/.scripts/update_metrics.py"
alias obs-open="open -a Obsidian ~/Documents/ObsidianVault/Dashboard.md"
alias obs-vault="cd ~/Documents/ObsidianVault && ls -la"

# Email & Calendar Sync
alias obs-sync-email="python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py"
alias obs-sync-cal="python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py"
alias obs-sync-all="obs-sync-email && obs-sync-cal"

# 1Password CLI Session Management (authenticate once per day)
source ~/.claude/scripts/1password-session.sh 2>/dev/null

# Perplexity API Key (managed by 1Password)
export PERPLEXITY_API_KEY="$(op read 'op://API_Keys/Perplexity Pro API/credential' 2>/dev/null)"

# Google Drive sync alias
alias obs-sync-drive='~/Documents/ObsidianVault/.scripts/sync-documents-to-gdrive.sh'

# Claude Code Project Manager
source ~/.claude/scripts/setup-aliases.sh

# 1Password Security Docs
alias 1pass-guide="cat ~/.claude/1PASSWORD_SECURITY_GUIDE.md"
alias 1pass-quick="cat ~/.claude/1PASSWORD_QUICK_REFERENCE.md"
alias 1pass-summary="cat ~/.claude/1PASSWORD_MIGRATION_SUMMARY.md"

# ObsidianVault aliases
alias vault='cd ~/Documents/ObsidianVault'
alias vopen='open -a Obsidian ~/Documents/ObsidianVault'
alias vdaily='python3 ~/Documents/ObsidianVault/.scripts/update_daily_note.py && open "obsidian://open?vault=ObsidianVault&file=Daily/$(date +%Y-%m-%d).md"'
alias vmorning='~/Documents/ObsidianVault/.scripts/morning-routine.sh'
alias vevening='~/Documents/ObsidianVault/.scripts/evening-routine.sh'
alias vgranola='~/Documents/ObsidianVault/.scripts/granola-export.sh'
alias vscreenshot='~/Documents/ObsidianVault/.scripts/daily-screenshot.sh'
alias vgit='cd ~/Documents/ObsidianVault && git status'
alias vpush='cd ~/Documents/ObsidianVault && git add . && git commit -m "Updates $(date +%Y-%m-%d)" && git push'

# DGX Ollama - Use models from DGX Spark storage
export OLLAMA_HOST=http://192.168.68.88:11434

# AI Model Aliases (all run on DGX with GPU)
alias ai-code='ollama run qwen2.5-coder:7b'
alias ai-chat='ollama run llama3.1:8b'
alias ai-quick='ollama run llama3.2:1b'
alias ai-vision='ollama run llava:13b'
alias ai-reason='ollama run qwen2.5:14b'
alias ai-beast='ollama run llama3.1:70b'
alias ai-deepseek='ollama run deepseek-r1:70b'
alias ai-list='ollama list'
alias ai-dgx='ssh mikefinneran@192.168.68.88'


# Airtable Sync
alias airtable-sync='python3 ~/Documents/ObsidianVault/airtable-sync.py'
alias at-sync='python3 ~/Documents/ObsidianVault/airtable-sync.py'
alias at-log='tail -f ~/Documents/Work/.airtable-sync/logs/launchd-stdout.log'
alias work='cd ~/Documents/Work'

# Google Passkey Fix
source ~/.bash_profile_passkey_fix

# Auto-save Claude Code session memory on shell exit
claude_cleanup() {
  if [ -f "$HOME/.claude/SESSION-MEMORY.md" ]; then
    "$HOME/.claude/scripts/save-session-memory.sh" 2>/dev/null || true
  fi
}
trap claude_cleanup EXIT

# 1Password CLI - Enable biometric unlock (no session needed)
export OP_BIOMETRIC_UNLOCK_ENABLED=true
export S3_BACKUP_BUCKET="mikefinneran-personal"

# GitHub ↔ Airtable Sync (added 2025-11-03)
alias github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'
alias github-sync-logs='ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | awk "{print \$NF}" | xargs cat'
alias github-sync-status='launchctl list | grep github-airtable-sync'
alias organize-research='python3 ~/crewai-specialists/crews/research_organizer/auto_organize_research.py'

# DGX Research Organization
alias dgx-organize='ssh mikefinneran@192.168.68.88 "python3 ~/research-archive/dgx_organize_research.py"'
alias research-download='scp mikefinneran@192.168.68.88:~/research-archive/organized-outputs/*.md ~/Downloads/'
alias research-upload='function _upload() { scp "$1" mikefinneran@192.168.68.88:~/research-archive/downloads/; }; _upload'
alias research-status='ssh mikefinneran@192.168.68.88 "echo \"DGX Research Archive:\" && du -sh ~/research-archive/* && echo && echo \"File counts:\" && echo \"  Downloads: \$(ls ~/research-archive/downloads/*.md 2>/dev/null | wc -l) files\" && echo \"  Outputs: \$(ls ~/research-archive/organized-outputs/*.md 2>/dev/null | wc -l) documents\""'

# Puppeteer Cleanup (prevent session crashes)
alias kill-puppeteer='pkill -f "mcp-server-puppeteer" && pkill -f "Google Chrome for Testing" && echo "Killed all Puppeteer processes"'

source ~/.claude/scripts/iterm-aliases.sh
