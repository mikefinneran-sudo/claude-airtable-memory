# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
check_session () {
	if [ -f "$SESSION_FILE" ]
	then
		if [ -f "$SESSION_TIMESTAMP_FILE" ]
		then
			TIMESTAMP=$(cat "$SESSION_TIMESTAMP_FILE") 
			NOW=$(date +%s) 
			AGE=$((NOW - TIMESTAMP)) 
			if [ $AGE -lt 86400 ]
			then
				export OP_SESSION_my=$(cat "$SESSION_FILE") 
				if op account get &> /dev/null
				then
					if [ "$1" = "-v" ]
					then
						HOURS=$((AGE / 3600)) 
						echo -e "${GREEN}✅ 1Password session active${NC} (${HOURS}h old)"
					fi
					return 0
				fi
			fi
		fi
	fi
	return 1
}
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
claude_cleanup () {
	if [ -f "$HOME/.claude/SESSION-MEMORY.md" ]
	then
		"$HOME/.claude/scripts/save-session-memory.sh" 2> /dev/null || true
	fi
}
clear_session () {
	rm -f "$SESSION_FILE" "$SESSION_TIMESTAMP_FILE"
	unset OP_SESSION_my
	echo -e "${YELLOW}🔓 Session cleared${NC}"
}
create_session () {
	echo -e "${BLUE}🔐 Creating 1Password session...${NC}"
	echo ""
	echo "This will require biometric authentication ONE TIME."
	echo "Session will last 24 hours."
	echo ""
	SESSION_TOKEN=$(op signin --raw 2>&1) 
	if [ $? -eq 0 ] && [ ! -z "$SESSION_TOKEN" ]
	then
		echo "$SESSION_TOKEN" > "$SESSION_FILE"
		chmod 600 "$SESSION_FILE"
		date +%s > "$SESSION_TIMESTAMP_FILE"
		export OP_SESSION_my="$SESSION_TOKEN" 
		echo -e "${GREEN}✅ Session created successfully${NC}"
		echo ""
		echo "Session expires: $(date -v+24H '+%Y-%m-%d %H:%M')"
		echo ""
		return 0
	else
		echo -e "${RED}❌ Failed to create session${NC}"
		echo ""
		echo "Error: $SESSION_TOKEN"
		echo ""
		echo "Make sure:"
		echo "  1. 1Password app is unlocked"
		echo "  2. CLI integration is enabled (Settings → Developer)"
		echo ""
		return 1
	fi
}
main () {
	case "$1" in
		(-v | --verbose) check_session -v || create_session ;;
		(clear) clear_session ;;
		(status) if check_session -v
			then
				echo ""
				echo "Session file: $SESSION_FILE"
				ACCOUNT=$(op account get --format json 2>/dev/null | jq -r '.name' 2>/dev/null) 
				echo "Account: $ACCOUNT"
			else
				echo -e "${YELLOW}⚠️  No active session${NC}"
				echo ""
				echo "Run without arguments to create a session:"
				echo "  source ~/.claude/scripts/1password-session.sh"
			fi ;;
		(help | --help | -h) echo "1Password CLI Session Management"
			echo ""
			echo "Usage:"
			echo "  source ~/.claude/scripts/1password-session.sh        # Check/create session"
			echo "  source ~/.claude/scripts/1password-session.sh -v     # Verbose output"
			echo "  bash ~/.claude/scripts/1password-session.sh status   # Check status"
			echo "  bash ~/.claude/scripts/1password-session.sh clear    # Clear session"
			echo ""
			echo "Add to ~/.zshrc:"
			echo "  source ~/.claude/scripts/1password-session.sh"
			echo "" ;;
		(*) if ! check_session
			then
				create_session
			fi ;;
	esac
}
# Shell Options
setopt nohashdirs
setopt login
# Aliases
alias -- 1pass-guide='cat ~/.claude/1PASSWORD_SECURITY_GUIDE.md'
alias -- 1pass-quick='cat ~/.claude/1PASSWORD_QUICK_REFERENCE.md'
alias -- 1pass-summary='cat ~/.claude/1PASSWORD_MIGRATION_SUMMARY.md'
alias -- activity-summary='~/.claude/scripts/generate-activity-summary.py'
alias -- ai-code=cursor
alias -- airtable-sync='python3 ~/Documents/ObsidianVault/airtable-sync.py'
alias -- archive-script='~/.claude/scripts/archive-custom-script.sh'
alias -- at-log='tail -f ~/Documents/Work/.airtable-sync/logs/launchd-stdout.log'
alias -- at-sync='python3 ~/Documents/ObsidianVault/airtable-sync.py'
alias -- backup-s3='~/.claude/scripts/backup-to-s3.sh'
alias -- boardroom='open http://localhost:8000/boardroom.html'
alias -- cc='~/.claude/command-center/launch.sh'
alias -- ccontext='~/.claude/scripts/context-manager.sh'
alias -- command-center='~/.claude/command-center/launch.sh'
alias -- context='cat ~/.claude/WORKING-CONTEXT.md'
alias -- continue='~/.claude/scripts/continue-enhanced.sh'
alias -- cproject='~/.claude/scripts/init-project-session.sh'
alias -- cresearch='~/.claude/scripts/research-project.sh'
alias -- cwarp='~/.claude/scripts/generate-warp-configs.sh'
alias -- docs='cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents'
alias -- fix-google-passkey='cd /Users/mikefinneran/Documents/ObsidianVault/.scripts && ./run-passkey-fix.sh'
alias -- gdocs='cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents'
alias -- github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'
alias -- github-sync-logs='ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | awk "{print \$NF}" | xargs cat'
alias -- github-sync-status='launchctl list | grep github-airtable-sync'
alias -- memory-search='~/.claude/scripts/memory-search.sh'
alias -- monthly-summary='~/.claude/scripts/generate-activity-summary.py month'
alias -- msearch='~/.claude/scripts/memory-search.sh'
alias -- obs-daily='~/Documents/ObsidianVault/.scripts/create_daily_note.sh'
alias -- obs-metrics='python3 ~/Documents/ObsidianVault/.scripts/update_metrics.py'
alias -- obs-open='open -a Obsidian ~/Documents/ObsidianVault/Dashboard.md'
alias -- obs-sync-all='obs-sync-email && obs-sync-cal'
alias -- obs-sync-cal='python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py'
alias -- obs-sync-drive='~/Documents/ObsidianVault/.scripts/sync-documents-to-gdrive.sh'
alias -- obs-sync-email='python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py'
alias -- obs-vault='cd ~/Documents/ObsidianVault && ls -la'
alias -- restore-s3='~/.claude/scripts/restore-from-s3.sh'
alias -- resume='~/.claude/scripts/resume-work.sh'
alias -- run-help=man
alias -- s3-setup='~/.claude/scripts/setup-s3-integration.sh'
alias -- save-session='~/.claude/scripts/save-session-memory.sh'
alias -- scan-scripts='~/.claude/scripts/scan-project-scripts.sh'
alias -- session='cat ~/.claude/SESSION-MEMORY.md'
alias -- start-session='~/.claude/scripts/start-session.sh'
alias -- surf=windsurf
alias -- vault='cd ~/Documents/ObsidianVault'
alias -- vdaily='python3 ~/Documents/ObsidianVault/.scripts/update_daily_note.py && open "obsidian://open?vault=ObsidianVault&file=Daily/$(date +%Y-%m-%d).md"'
alias -- vevening='~/Documents/ObsidianVault/.scripts/evening-routine.sh'
alias -- vgit='cd ~/Documents/ObsidianVault && git status'
alias -- vgranola='~/Documents/ObsidianVault/.scripts/granola-export.sh'
alias -- vmorning='~/Documents/ObsidianVault/.scripts/morning-routine.sh'
alias -- vopen='open -a Obsidian ~/Documents/ObsidianVault'
alias -- vpush='cd ~/Documents/ObsidianVault && git add . && git commit -m "Updates $(date +%Y-%m-%d)" && git push'
alias -- vs=code
alias -- vscode=code
alias -- vscreenshot='~/Documents/ObsidianVault/.scripts/daily-screenshot.sh'
alias -- weekly-summary='~/.claude/scripts/generate-activity-summary.py week'
alias -- which-command=whence
alias -- work='cd ~/Documents/Work'
# Check for rg availability
if ! command -v rg >/dev/null 2>&1; then
  alias rg='/Users/mikefinneran/.local/share/claude/versions/2.0.31 --ripgrep'
fi
export PATH=/Users/mikefinneran/.local/bin\:/opt/homebrew/bin\:/opt/homebrew/sbin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin\:/Applications/iTerm.app/Contents/Resources/utilities
