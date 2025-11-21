# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
claude-edit () {
	if [ -f .claude/CLAUDE.md ]
	then
		${EDITOR:-nano} .claude/CLAUDE.md
	else
		echo "No .claude/CLAUDE.md found in current directory"
		echo "Run 'claude-init' to create one"
	fi
}
claude-init () {
	~/.claude/init-project-memory.sh "$@"
}
claude-show () {
	if [ -f .claude/CLAUDE.md ]
	then
		cat .claude/CLAUDE.md
	else
		echo "No .claude/CLAUDE.md found in current directory"
	fi
}
# Shell Options
setopt nohashdirs
setopt login
# Aliases
alias -- docs='cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents'
alias -- gdocs='cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents'
alias -- obs-daily='~/Documents/ObsidianVault/.scripts/create_daily_note.sh'
alias -- obs-metrics='python3 ~/Documents/ObsidianVault/.scripts/update_metrics.py'
alias -- obs-open='open -a Obsidian ~/Documents/ObsidianVault/Dashboard.md'
alias -- obs-sync-all='obs-sync-email && obs-sync-cal'
alias -- obs-sync-cal='python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py'
alias -- obs-sync-drive='~/Documents/ObsidianVault/.scripts/sync-documents-to-gdrive.sh'
alias -- obs-sync-email='python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py'
alias -- obs-vault='cd ~/Documents/ObsidianVault && ls -la'
alias -- run-help=man
alias -- which-command=whence
# Check for rg availability
if ! command -v rg >/dev/null 2>&1; then
  alias rg='/Users/mikefinneran/.local/share/claude/versions/2.0.26 --ripgrep'
fi
export PATH=/Users/mikefinneran/.local/bin\:/opt/homebrew/bin\:/opt/homebrew/sbin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin
