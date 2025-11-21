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
alias -- ai-beast='ollama run llama3.1:70b'
alias -- ai-chat='ollama run llama3.1:8b'
alias -- ai-code='ollama run qwen2.5-coder:7b'
alias -- ai-deepseek='ollama run deepseek-r1:70b'
alias -- ai-dgx='ssh mikefinneran@192.168.68.88'
alias -- ai-list='ollama list'
alias -- ai-quick='ollama run llama3.2:1b'
alias -- ai-reason='ollama run qwen2.5:14b'
alias -- ai-vision='ollama run llava:13b'
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
alias -- dgx='ssh mikefinneran@192.168.68.88'
alias -- dgx-claude='ssh mikefinneran@192.168.68.88 -t "tmux -CC new -A -s dgx-claude"'
alias -- dgx-gpu='ssh mikefinneran@192.168.68.88 -t "watch -n 2 nvidia-smi"'
alias -- dgx-organize='ssh mikefinneran@192.168.68.88 "python3 ~/research-archive/dgx_organize_research.py"'
alias -- docs='cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents'
alias -- fix-google-passkey='cd /Users/mikefinneran/Documents/ObsidianVault/.scripts && ./run-passkey-fix.sh'
alias -- gdocs='cd ~/Library/CloudStorage/GoogleDrive-mike@fly-flat.com/My\ Drive/Documents'
alias -- github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'
alias -- github-sync-logs='ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | awk "{print \$NF}" | xargs cat'
alias -- github-sync-status='launchctl list | grep github-airtable-sync'
alias -- it-backup='defaults export com.googlecode.iterm2 ~/.claude/backups/iterm2-backup-$(date +%Y%m%d-%H%M%S).plist'
alias -- it-ce='it-tdd ~/Documents/ObsidianVault/Projects/claude-efficiency-system'
alias -- it-dgx='~/.claude/scripts/iterm-layout-dgx-claude.sh'
alias -- it-fullstack='~/.claude/scripts/iterm-layout-fullstack.sh'
alias -- it-help='cat ~/.claude/scripts/iterm-quick-reference.md | less'
alias -- it-ivy='it-tdd ~/Documents/ObsidianVault/Projects/ivy-league-ai-education'
alias -- it-lh='it-tdd ~/Documents/ObsidianVault/Projects/LifeHub'
alias -- it-profiles='ls -lh ~/Library/Application\ Support/iTerm2/DynamicProfiles/'
alias -- it-reload='osascript -e "quit app \"iTerm\"" && open -a iTerm'
alias -- it-remote='~/.claude/scripts/iterm-layout-remote.sh'
alias -- it-setup='~/.claude/scripts/iterm-complete-setup.sh'
alias -- it-shortcuts=$'echo "\niTerm2 Quick Shortcuts:\n  Cmd+Shift+Up/Down - Navigate commands\n  Cmd+Shift+A - Select last output\n  Cmd+Opt+A - Alert on complete\n  Cmd+D - Split vertical\n  Cmd+Shift+D - Split horizontal\n  Cmd+O - Switch profile\n\nLayout Commands:\n  it-tdd [dir] - TDD layout\n  it-fullstack [dir] - Full stack layout\n  it-remote user@host - Remote layout\n\nProject Shortcuts:\n  it-ws - WalterSignal\n  it-ce - Claude Efficiency\n  it-lh - LifeHub\n  it-ivy - Ivy League AI\n  it-dgx - DGX Spark (Claude + GPT-OSS)\n\nDGX Spark Commands:\n  dgx - SSH to DGX Spark\n  dgx-claude - tmux Claude session\n  dgx-gpu - Monitor GPU usage\n  it-dgx - Full layout (Claude + GPU monitor)\n"'
alias -- it-statusbar='~/.claude/scripts/iterm-configure-statusbar.sh'
alias -- it-tdd='~/.claude/scripts/iterm-layout-tdd.sh'
alias -- it-ws='it-fullstack ~/Documents/ObsidianVault/Projects/WalterSignal'
alias -- kill-puppeteer='pkill -f "mcp-server-puppeteer" && pkill -f "Google Chrome for Testing" && echo "Killed all Puppeteer processes"'
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
alias -- organize-research='python3 ~/crewai-specialists/crews/research_organizer/auto_organize_research.py'
alias -- research-download='scp mikefinneran@192.168.68.88:~/research-archive/organized-outputs/*.md ~/Downloads/'
alias -- research-status='ssh mikefinneran@192.168.68.88 "echo \"DGX Research Archive:\" && du -sh ~/research-archive/* && echo && echo \"File counts:\" && echo \"  Downloads: \$(ls ~/research-archive/downloads/*.md 2>/dev/null | wc -l) files\" && echo \"  Outputs: \$(ls ~/research-archive/organized-outputs/*.md 2>/dev/null | wc -l) documents\""'
alias -- research-upload='function _upload() { scp "$1" mikefinneran@192.168.68.88:~/research-archive/downloads/; }; _upload'
alias -- restore-s3='~/.claude/scripts/restore-from-s3.sh'
alias -- resume='~/.claude/scripts/resume-work.sh'
alias -- run-help=man
alias -- s3-setup='~/.claude/scripts/setup-s3-integration.sh'
alias -- save-session='~/.claude/scripts/save-session-memory.sh'
alias -- scan-scripts='~/.claude/scripts/scan-project-scripts.sh'
alias -- scrape='python3 ~/.claude/scripts/scrape-url.py'
alias -- scrape-js='python3 ~/.claude/scripts/scrape-url.py --js'
alias -- scrape-proxy='python3 ~/.claude/scripts/scrape-url.py --proxy'
alias -- session='cat ~/.claude/SESSION-MEMORY.md'
alias -- start-session='~/.claude/scripts/start-session.sh'
alias -- surf=windsurf
alias -- tm='tmux -CC'
alias -- tma='tmux -CC attach -t'
alias -- tms='tmux -CC new -A -s'
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
  alias rg='/Users/mikefinneran/.local/share/claude/versions/2.0.46 --ripgrep'
fi
export PATH=/Users/mikefinneran/.local/bin\:/opt/homebrew/bin\:/opt/homebrew/sbin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin\:/Applications/iTerm.app/Contents/Resources/utilities
