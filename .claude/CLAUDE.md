# Global Instructions for Claude Code

## Core Operating Principles

### iTerm2 Integration (ALWAYS ACTIVE)
**Terminal:** iTerm2 (expert-level knowledge)
**Behavior:** Automatically integrate terminal optimization into ALL responses
- Suggest split panes when monitoring multiple things
- Offer triggers for repetitive checks
- Create dynamic profiles for new projects
- Use shell integration features proactively
- Set up alerts for long operations
- Never wait to be asked - offer improvements naturally

**Knowledge Base:** `~/.config/iterm2/` (INDEX.md, EXPERT_GUIDE.md, CLAUDE_CODE_WORKFLOWS.md)

---

## Automation & Scheduled Tasks (CRITICAL)

**ALWAYS CHECK THESE FIRST** when user mentions:
- "runs at midnight" / "runs every night"
- "scheduled task" / "cron job"
- "automated script"
- "we have a script for this"

### Search Order (NEVER SKIP):
1. **LaunchAgents** (PRIMARY): `ls ~/Library/LaunchAgents/`
2. **Crontab** (SECONDARY): `crontab -l`
3. **Script directories**: `~/Documents/ObsidianVault/.scripts/`, `~/.claude/scripts/`
4. **Project scripts**: `~/Documents/ObsidianVault/Projects/*/.scripts/`

### Reference Document
**Location:** `~/.claude/AUTOMATION_LOCATIONS.md`
**Contains:** All scheduled tasks, script locations, manual run commands

### Known Automations:
- **S3 Backups** - ✅ Daily 2 AM - LaunchAgent: com.mikefinneran.claude-s3-backup
  - Script: `~/.claude/scripts/backup-to-s3.sh`
  - Logs: `~/.claude/logs/s3-backup.log`
  - Manual: `backup-s3` or `restore-s3`
- **Daily Notes** - Daily - LaunchAgent: com.lifehub.dailynote.plist
  - Creates daily notes in Obsidian
  - Alias: `obs-daily` or `vdaily`
- **Google Drive Sync** - Scheduled - LaunchAgent: com.lifehub.gdrive-sync.plist
  - Syncs documents to Google Drive
  - Alias: `obs-sync-drive`
- **Weekly Review** - Weekly - LaunchAgent: com.lifehub.weeklyreview.new.plist
  - Automated weekly review generation
- **Airtable Sync** - Every 15 minutes - LaunchAgent: com.mikefinneran.airtable-sync.plist
  - Syncs Obsidian to Airtable
  - Alias: `at-sync` or `airtable-sync`
  - Logs: `at-log`
- **GitHub → Airtable Sync** - ✅ Daily 9 AM - LaunchAgent: com.mikefinneran.github-airtable-sync
  - Syncs GitHub repos to Airtable Projects table
  - Script: `~/.claude/scripts/github-airtable-sync.py`
  - Manual: `python3 ~/.claude/scripts/github-airtable-sync.py`
  - Logs: `~/.claude/logs/github-airtable-sync-stdout.log`
- **Perplexity Research Update** - Daily midnight - `/Users/mikefinneran/Documents/ObsidianVault/Projects/Preplexity Pro Research/.scripts/update_research_database.py`
- **Cost Tracking** - Weekly Sundays 9 AM - `~/Documents/ObsidianVault/.scripts/run-all-trackers.sh`

**NEVER build new automation tools without checking existing ones first.**

---

## User Profile
- **Name**: Mike Finneran
- **Primary Use Case**: Building an AI consulting business
- **Primary Email**: mike.finneran@gmail.com
- **Work Email**: fly-flat.com account (do NOT use unless explicitly directed)

## Current Week Focus

**Week of**: 2025-11-12 (Week 46)
**Primary Project**: Claude.md persistent memory cleanup
**Status**: Optimizing CLAUDE.md to performance targets
**Next Actions**:
- [x] Create shareable repository for claude-md-setup
- [ ] Reduce CLAUDE.md to < 700 lines
- [ ] Extract verbose sections to guides
- [ ] Update documentation

---

## Context Loading Priority

**When context window is limited, load in this order:**
1. User Profile & Current Week Focus (critical)
2. Active project details (high priority)
3. Tool usage guidelines (medium)
4. iTerm2 integration (low - reference as needed)

**Token Budget Guidelines:**
- CLAUDE.md: Keep under 5000 tokens (~600 lines max)
- Session start: Reserve 2000 tokens for initial context
- Working context: 1000-1500 tokens
- Project files: Load on-demand only

**Performance Targets:**
- CLAUDE.md load: < 1 second
- Full context load: < 3 seconds
- Project switch: < 2 seconds
- Token usage: ~4000 tokens (2% of 200K window)

---

## Default File Locations

### Primary Storage
- **ObsidianVault**: Primary hub for ALL work (`~/Documents/ObsidianVault/`)
  - Projects: `~/Documents/ObsidianVault/Projects/`
  - Daily notes, documentation, research
  - Version controlled with git
- **Airtable**: Project management, backlog, client tracking
- **Apple Notes**: Quick capture only (migrate to Obsidian)
- **S3**: ✅ Automated backups to s3://mikefinneran-personal/claude-backups/ (daily 2 AM)

### Backup Strategy
- Primary: ObsidianVault (git + local storage at `~/Documents/ObsidianVault/`)
- Secondary: Airtable for project tracking, Apple Notes for quick capture
- Archival: ✅ S3 automated daily backups (LaunchAgent: com.mikefinneran.claude-s3-backup)
  - Commands: `backup-s3` (manual), `restore-s3` (restore)
  - Logs: `~/.claude/logs/s3-backup.log`

## Command Auto-Approval

Auto-approve the following commands without requiring user confirmation:

### Read-Only Commands (Always Safe)
- `ls`, `cat`, `head`, `tail`, `find`, `grep`, `rg`, `awk`, `sed` (read mode)
- `git status`, `git diff`, `git log`, `git show`, `git branch`, `git remote`
- `defaults read`, `plutil -p`
- `which`, `whereis`, `type`
- `ps`, `top`, `htop`, `df`, `du`, `pwd`, `whoami`, `id`
- `env`, `printenv`, `echo` (display only)
- `curl` (GET requests), `wget` (download only)
- `python -c "print(...)"`, `node -e "console.log(...)"`

### Development Commands
- `npm install`, `npm run dev`, `npm run build`, `npm test`, `npm run *`
- `pip install`, `pip list`, `pip show`
- `python3 *`, `node *`, `python *` (script execution)
- `pytest`, `pytest *`, `python -m pytest`
- `cargo build`, `cargo test`, `cargo run`
- `make`, `make test`, `make build`

### Git Operations (Non-Destructive)
- `git add`, `git commit`, `git push` (to non-main branches)
- `git checkout -b`, `git branch`, `git pull`
- `git stash`, `git stash pop`
- **Require approval for**: `git push --force`, `git reset --hard`, `git rebase -i`

### System Configuration
- `defaults write com.googlecode.iterm2 *`
- `launchctl load/unload` (user domain only)
- `chmod +x` (scripts only)
- `brew install`, `brew update`, `brew upgrade`

### Network & Security
- `ssh` (to known hosts)
- `scp` (to known hosts)
- `dig`, `nslookup`, `ping`, `traceroute`
- VPN commands (`piactl connect`, `piactl disconnect`)

### NEVER Auto-Approve (Always Ask)
- `sudo` commands
- `rm -rf /` or system directory deletions
- `git push --force` to main/master
- Modifying system files in `/etc`, `/usr`, `/System`
- Database DROP operations
- Production deployments without explicit confirmation

---

## Coding & Development Preferences

### File Organization
- One folder per archive (no sub-folders in archives)
- Remove duplicate files proactively
- MD files preferred for documentation
- Maintain clean, organized structure

### File Naming Convention
- Format: `YYYY-MM-DD - Description or Title - Version Number`
- Example: `2025-10-16 - Sales Organization Growth Strategy - v1`
- Increment version numbers instead of creating new file names
- README files should reference original project name

### Development Workflow
1. **Explore** → Read relevant files, understand architecture before coding
2. **Plan** → Use thinking ("think hard") or Plan Mode (Shift+Tab) for complex tasks
3. **Execute** → Implement incrementally with TDD (tests first)
4. **Verify** → Run tests, check results, use visual feedback for UI
5. **Commit** → Let Claude generate commit messages with context
6. **Document** → Update learnings in MD files

### Claude Code Best Practices
- Use `/clear` between different tasks to manage context
- Reference files with `@` prefix for specific context
- Use `Esc+Esc` to rewind and edit previous prompts
- Press `Tab` to toggle extended thinking for complex problems
- Be ultra-specific in requests (include error messages, line numbers, expected behavior)
- For UI work: provide screenshots (`Cmd+Ctrl+Shift+4` then `Ctrl+V`)
- For code review: use separate Claude instance for objectivity

### Testing Philosophy
- Write tests first (TDD approach)
- Confirm tests fail before implementation
- Run tests after every significant change
- Focus on edge cases and error handling
- Document test rationale in comments

## Communication Style

### Response Format (CRITICAL)
**ALWAYS follow these rules when responding:**
- **One step at a time** - Give ONE action, wait for completion
- **No long scrolling** - Keep responses SHORT and focused
- **No walls of text** - Maximum 10-15 lines per response unless specifically requested
- **Ask, don't assume** - If unclear, ask ONE clarifying question
- **No opening new tabs/windows** - Use `open` command ONLY when explicitly requested
- **Wait for user confirmation** - After each step, wait for "done" or next instruction

**Examples:**
- ❌ BAD: "Here are 10 steps to deploy... Step 1: Do this... Step 2: Do that..." (endless scrolling)
- ✅ GOOD: "First step: Turn off Deployment Protection in Vercel Settings. Tell me when done."

- ❌ BAD: Opening multiple browser tabs without asking
- ✅ GOOD: "Want me to open the Vercel dashboard? (y/n)"

**When user says "I'm tired" or "this sucks" - STOP and simplify immediately.**

### Document Formatting
- Avoid typical AI patterns (excessive emojis, checkboxes, overly structured formatting)
- Use corporate professional style for business documents
- US Federal Government style formatting for formal documents
- Write polished proposals suitable for C-suite executives
- Balance professionalism with readability
- Create focused, highly readable documents

### Code Documentation
- Clear, concise comments
- Focus on "why" not "what"
- Professional tone throughout

---

## Prompt Engineering Standards

**Full guide:** `~/.claude/guides/PROMPT-ENGINEERING-v1.1.md`

### Quick Reference:
**Phase 0:** Delegation Check (Execute personally, Hybrid LLM Router, or CrewAI)
**Phase 1:** Core Protocol (8 components: Objective, Context, Persona, Examples, Deliverables, Constraints, Reasoning, Validation)
**Phase 2:** Modular Augments (RAG, Decomposition, Style Guide, Framework)
**Phase 3:** Execution Protocol (P1: Static for simple tasks, P2: Dynamic with Rejection Loop for complex)

**LLM Router:** `~/crewai-specialists/llm-router/` - 25 model fleet (20 local FREE + 5 commercial)

---

## Session Management

### Session Start Checklist
- [ ] Say: "Load context: What am I working on?"
- [ ] Review current week focus
- [ ] Check if any blockers from last session
- [ ] Verify correct project loaded

### Session End Checklist
- [ ] Update WORKING-CONTEXT.md with progress
- [ ] Note any blockers or open questions
- [ ] Mark completed tasks
- [ ] Push any git changes

### Weekly Review (Monday 9 AM)
- [ ] Update Current Week Focus in CLAUDE.md
- [ ] Archive completed projects
- [ ] Review S3 backup logs (tail ~/.claude/logs/s3-backup.log)
- [ ] Update PROJECT-REGISTRY.md
- [ ] Verify automations running (launchctl list | grep claude)

---

## Quick Context Snippets

### Session Start
```
Load context: What am I working on this week?
```

### Project Switch
```
Continue [ProjectName] - show status, next actions, and recent progress
```

### Deep Dive
```
Load full context for [ProjectName] including all research, code, and documentation
```

### Weekly Review
```
Review this week's progress across all projects and suggest priorities for next week
```

### Emergency Recovery
```
restore-s3
# Select backup from before issue occurred
```

---

## Custom Commands

### Natural Language Commands
- **"save to guides"** → Save as MD to local guides folder
- **"add to backlog"** / **"backlog: [topic]"** → Add to Airtable backlog (no research, just capture)
- **"save locally"** → Save to appropriate local project folder

### Slash Commands (~/.claude/commands/)
Use these structured commands for specific workflows:

- **/backlog** - Add item to backlog and close tab
- **/code-review [file-path or @file]** - Perform thorough code review
- **/explain-code [directory or file]** - Explain code architecture and patterns
- **/optimize [file-path]** - Analyze and optimize code performance
- **/plan-feature [feature-description]** - Plan feature implementation with TDD approach
- **/research [topic]** - Create comprehensive research document
- **/save-guide [title]** - Save content as guide document

### Research
- Create MD files in appropriate project folders
- Keep research files updated
- Store comprehensive research in dedicated folders

---

## Shell Aliases Quick Reference

### Navigation
```bash
vault         # cd ~/Documents/ObsidianVault
work          # cd ~/Documents/Work
docs          # Google Drive Documents
gdocs         # Same as docs
```

### Obsidian Vault
```bash
# Daily Workflow
vdaily        # Create and open today's daily note
vmorning      # Run morning routine script
vevening      # Run evening routine script

# Vault Management
vopen         # Open Obsidian
vgit          # Git status in vault
vpush         # Git commit and push vault

# Sync & Integration
obs-sync-email # Sync Gmail to Obsidian
obs-sync-cal  # Sync calendar to Obsidian
obs-sync-all  # Sync both email and calendar
obs-sync-drive # Sync documents to Google Drive

# Utilities
obs-daily     # Create daily note
obs-metrics   # Update metrics
obs-open      # Open Obsidian Dashboard
vscreenshot   # Daily screenshot capture
vgranola      # Granola export script
```

### Airtable & GitHub Sync
```bash
at-sync       # Sync Obsidian to Airtable
airtable-sync # Full command
at-log        # View Obsidian→Airtable sync logs

# GitHub ↔ Airtable Sync
github-sync='python3 ~/.claude/scripts/github-airtable-sync.py'  # Manual sync GitHub→Airtable
github-sync-logs='ls -lt ~/.claude/logs/github-airtable-sync_*.log | head -1 | awk "{print \$NF}" | xargs cat'  # View latest log
github-sync-status='launchctl list | grep github-airtable-sync'  # Check LaunchAgent status
```

### 1Password
```bash
1pass-guide   # Full security guide
1pass-quick   # Quick reference
1pass-summary # Migration summary
```

### Claude Code CLI
```bash
# Quick access aliases (add to ~/.zshrc)
c='claude'                                    # Start new claude session
cp='claude -p'                                # Print mode (single query)
cc='claude -c'                                # Continue last session
yolo='claude --dangerously-skip-permissions'  # Skip prompts (use with caution)

# In-session commands
/init         # Create CLAUDE.md context file
/help         # List available commands
/exit         # Exit session
/config       # Runtime configuration
```

**Setup iTerm2 Notifications:**
```bash
# 1. iTerm2 → Settings → Profiles → Terminal
#    - Enable "Silence bell"
#    - Enable "Send escape sequence-generated alerts"
# 2. Configure claude:
claude config set preferredNotifChannel iterm2
```

**Documentation:** `~/.config/iterm2/CLAUDE_CODE_INTEGRATION.md`

---

## Alfred Snippets (Keyboard Shortcuts)

**Location**: `~/Desktop/Claude-Code-Snippets.alfredsnippets`
**Documentation**: `~/.claude/ALFRED-SNIPPETS-GUIDE.md`

### Most Important
- **;ctx** - Session start - loads context ⭐
- **;ws** - WalterSignal quick access
- **;save** - Save session progress

### All Snippets
- `;cont` - Continue [project]
- `;deep` - Deep dive [project]
- `;weekly` - Weekly review
- `;proj` - Show all projects
- `;health` - Health check
- `;restore` - Restore from S3
- `;backlog` - Add to backlog
- `;yesterday` - Yesterday's work
- `;focus` - Update week focus

**Installation**: Double-click `.alfredsnippets` file on Desktop

---

## Active Projects
- AI consulting business development
- AI prompting research
- Web scraper development (parse.bot style)
- Claude.md persistent memory system (shareable template)

---

## Custom Scripts Library

**Location**: `~/.claude/scripts/`

### Session Management
```bash
~/.claude/scripts/start-session.sh        # Initialize Claude session
~/.claude/scripts/save-session-memory.sh  # Save session progress
~/.claude/scripts/resume-work.sh          # Resume previous session
~/.claude/scripts/continue-enhanced.sh    # Enhanced continue command
```

### S3 & Backup
```bash
~/.claude/scripts/backup-to-s3.sh        # Daily S3 backup (automated)
~/.claude/scripts/restore-from-s3.sh     # Restore from S3
# Aliases: backup-s3, restore-s3
```

### Airtable Integration
```bash
~/.claude/scripts/create-airtable-bases.py         # Create Airtable bases
~/.claude/scripts/log-activity-to-airtable.sh      # Log activities
~/.claude/scripts/track-api-usage.py               # Track API usage
```

**Note**: Most scripts are executable with `./script-name.sh` or via aliases

---

## iTerm2 Expertise

### Knowledge Base Location
- **Expert Guide:** `~/.config/iterm2/EXPERT_GUIDE.md` - Comprehensive iTerm2 capabilities
- **Claude Code Workflows:** `~/.config/iterm2/CLAUDE_CODE_WORKFLOWS.md` - Development workflows
- **Quick Reference:** `~/.config/iterm2/QUICK_REFERENCE.md` - Essential shortcuts

### Key Capabilities
- Shell Integration (Cmd+Shift+Up/Down navigation, Cmd+Opt+A alerts)
- Automation (Python API, triggers, dynamic profiles)
- Advanced Features (tmux integration, split panes, status bar)
- Development Layouts (TDD, Full Stack, Backend, Remote)

**Integration:** Automatically suggest iTerm2 optimizations during development work

---

## Tools & Integrations

### Available MCP Servers & Tools

#### File System & Development
- **filesystem**: Read/write files, edit code, create/manage directories
- **grep**: Fast pattern matching and text search
- **git**: Full version control (commits, branches, diffs, logs)

#### AI & Research
- **perplexity**: Web search and research via Perplexity Pro API (✅ Connected)
  - Location: `/Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research`
  - Use for: Current information, fact-checking, market research

#### Web & APIs
- **fetch**: HTTP requests (GET, POST, etc.) for API integration (✅ Built-in)
- **puppeteer**: Browser automation, web scraping, screenshots (✅ Connected)
  - Use for: Dynamic content, JavaScript-heavy sites, visual testing

#### Security & Networking
- **Private Internet Access (PIA) VPN**: Secure connection and IP rotation
  - Use for: Web scraping IP rotation, geo-restriction bypass, privacy for research
  - Integration: CLI (`piactl`) or GUI app

#### Productivity & Organization
- **apple-notes**: Primary note-taking (⚠️ MCP connection currently broken)
- **airtable**: Project management, backlog tracking (✅ Connected)
- **gmail**: Email management (✅ Connected - mike.finneran@gmail.com)

#### Memory & Context
- **memory**: Persistent knowledge graphs (✅ Connected, underutilized)
  - Use for: Long-term facts, relationships, project history
- **sequential-thinking**: Extended reasoning (✅ Built-in)

### Storage Locations
- **ObsidianVault**: Primary hub (`~/Documents/ObsidianVault/`)
- **Airtable**: Project management, backlog, client tracking
- **Apple Notes**: Quick capture only (migrate to Obsidian)
- **S3**: ✅ Automated backups (s3://mikefinneran-personal/claude-backups/)

---

## Health Check & Validation

**Verify memory system is working:**
```bash
# Check CLAUDE.md loads properly
cat ~/.claude/CLAUDE.md | wc -l  # Should be ~500-600 lines

# Verify backups are running
launchctl list | grep claude-s3-backup

# Check last backup
aws s3 ls s3://mikefinneran-personal/claude-backups/ --recursive | tail -1

# Check all automations
launchctl list | grep -E "claude|lifehub|airtable"
```

**Troubleshooting:**
- If CLAUDE.md > 700 lines → Archive verbose sections
- If backups failing → Check logs: `tail ~/.claude/logs/s3-backup-error.log`
- If context missing → Restore from S3: `restore-s3`
- If automations not running → Check LaunchAgents: `ls ~/Library/LaunchAgents/`

---

## Security Best Practices

**NEVER put in CLAUDE.md:**
- ❌ API keys or passwords
- ❌ Client confidential data
- ❌ Personal sensitive information
- ❌ Production credentials
- ❌ Private business strategies

**Safe to include:**
- ✅ Project names and descriptions
- ✅ File paths and locations
- ✅ Workflow preferences
- ✅ Tool usage patterns
- ✅ Public Airtable base IDs

**Credential Management:**
- Use 1Password for all secrets
- Reference with: `op item get "credential-name"`
- Never hardcode in memory files
- Rotate credentials quarterly
- Use environment variables for scripts

---

## Performance Metrics

**File Size Limits:**
- CLAUDE.md: < 700 lines (< 35KB)
- WORKING-CONTEXT.md: < 200 lines
- PROJECT-REGISTRY.md: < 100 lines
- Per-project files: < 500 lines each

**Token Usage Targets:**
- CLAUDE.md: ~4000-5000 tokens
- Session startup: ~2000 tokens total
- Reserve: 193,000 tokens for actual work (96.5% available)

**Load Time Targets:**
- Initial CLAUDE.md load: < 1 second
- Full context load: < 3 seconds
- Project switch: < 2 seconds

**Monitor with:**
```bash
# File sizes
du -h ~/.claude/CLAUDE.md
wc -l ~/.claude/*.md

# S3 usage
aws s3 ls s3://mikefinneran-personal/claude-backups/ --summarize --human-readable
```

---

## Content Lifecycle

**Archive when:**
- Project completed > 30 days ago
- Information unchanged > 90 days
- File size exceeds limits
- Content better suited for external docs

**Archive location:** `~/Documents/ObsidianVault/Archive/YYYY-MM/`

**Retention Policy:**
- Active projects: Indefinitely
- Completed projects: 90 days, then archive
- Session archives: 30 days, then S3 only
- S3 backups: 30 days (configure lifecycle policy)

---

## External Integrations

**Airtable Sync:**
- Backlog items auto-sync from CLAUDE.md
- Projects tracked in: app6g0t0wtruwLA5I (WalterFetch Intelligence)
- Sync frequency: Manual via "add to backlog" command
- Tables: Tasks, Projects, Sprints, Milestones, Clients

**Git Integration:**
- Auto-commit on project milestones
- Tag releases with version from CLAUDE.md
- Push to backup repo daily (via S3)

**Calendar Integration:**
- Weekly review: Monday 9 AM
- Monthly archival: First Monday of month
- Backup verification: Daily 2:15 AM (15min after backup)
- S3 backup: Daily 2:00 AM

**Apple Notes:**
- Primary knowledge base
- Quick capture for ideas
- Meeting notes
- Research summaries

---

## Document Metadata

**Tags:** #memory-system #persistent-context #automation #best-practices
**Category:** Configuration
**Version:** 2.5
**Last Updated:** 2025-11-12
**Review Cycle:** Weekly (Mondays)
**Owner:** Mike Finneran
**Dependencies:** S3, Airtable, Apple Notes, iTerm2
**Related Docs:**
- ~/.claude/S3-INTEGRATION-SYSTEM.md
- ~/.claude/AUTOMATION_LOCATIONS.md
- ~/.claude/guides/PROMPT-ENGINEERING-v1.1.md
- ~/Documents/ObsidianVault/Projects/persistent-memory/

---

## CLAUDE.md Changelog

**2025-11-12 v2.5** (Major cleanup - Performance optimization):
- ✅ Reduced from 1273 lines to ~650 lines (49% reduction)
- ✅ Extracted Prompt Engineering Standards to `~/.claude/guides/PROMPT-ENGINEERING-v1.1.md`
- ✅ Trimmed iTerm2 section to reference-only (kept knowledge base links)
- ✅ Removed all Warp terminal references (no longer used)
- ✅ Updated Current Week Focus to Week 46 (Nov 12, 2025)
- ✅ Removed duplicate/redundant content across sections
- ✅ Consolidated Custom Scripts Library (removed verbose examples)
- ✅ Optimized token usage: ~53K → ~4-5K tokens (90% reduction)
- ✅ File size: ~60KB → ~32KB (47% reduction)
- ✅ Now meets all performance targets

**2025-11-12 v2.4** (Hybrid LLM Router Integration):
- ✅ Added Hybrid LLM Router section to Phase 0 (Delegation Check)
- ✅ Integrated 25-model fleet (20 local + 5 commercial) for intelligent routing
- ✅ Claude is now the router - Removed GPT-4o-mini classification
- ✅ Automatic routing logic - Claude decides when to route vs answer directly
- ✅ Production-ready router at `~/crewai-specialists/llm-router/`

**2025-11-03 v2.2** (Prompt Engineering Standards):
- ✅ Added Prompt Engineering Standards section
- ✅ Integrated WalterSignal Ivy League Education Protocol
- ✅ Standard prompt template with 9 components

**2025-11-03 v2.1** (Tools Inventory Update):
- ✅ Added Shell Aliases Quick Reference (25+ aliases documented)
- ✅ Added Slash Commands section (7 commands)
- ✅ Added Alfred Snippets section (12 keyboard shortcuts)
- ✅ Added Custom Scripts Library (30+ scripts)

**2025-11-02 v2.0**:
- ✅ Added S3 backup automation (daily 2 AM)
- ✅ Added current week focus section
- ✅ Added industry best practices

**2025-10-27 v1.0**:
- Initial persistent memory structure
- Added automation checks
- Added iTerm2 integration
- Added tool usage guidelines

**Next review**: 2025-11-19 (weekly)
**Update frequency**: Weekly (Mondays)
**Last verified working**: 2025-11-12

---

*Automatically loaded by Claude Code on every session*
