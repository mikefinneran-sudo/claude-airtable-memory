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
4. **Project scripts**: `~/Documents/ObsidianVault/Projects/*/. scripts/`

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

**Week of**: 2025-11-03 (Week 44)
**Primary Project**: System Recovery & Cleanup
**Status**: Restored ObsidianVault as primary hub, cleaned up duplicates
**Next Actions**:
- [x] Restore ObsidianVault from backup
- [x] Clean up 48k → 6.7k files (removed bloat)
- [x] Delete ADDB AeroDyne MASTER mess
- [x] Update CLAUDE.md to make Obsidian the hub

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

### Process Management
- `killall iTerm2`, `killall Claude`, `killall Terminal`
- `kill` (specific PIDs after user review)

### File Operations (Project Directories Only)
- `mkdir`, `touch`, `cp`, `mv` (within `/Users/mikefinneran/Documents/ObsidianVault/Projects/`)
- `rm` (require confirmation for bulk deletes or important files)

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

### Airtable & API Operations
- Any commands with `AIRTABLE_TOKEN` environment variable
- API calls to Perplexity, Anthropic (read operations)

### Specific Script Approvals
- `./deploy.sh`, `./test-integrations.sh`, `./lightsail-launch.sh`
- `~/.claude/ea-team/verify-setup.sh`
- `~/.config/iterm2/verify-setup.sh`
- `.scripts/*` (within ObsidianVault)

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

**When requesting work from AI (including yourself), use this structure:**

### Standard Prompt Template

```markdown
# [Task Type] Task

## Objective
[Clear, specific description of what needs to be accomplished]

## Context
- **Project:** [Relevant project or domain]
- **Audience:** [Who this is for]
- **Environment:** [Technical context, tools, constraints]
- **Background:** [Any relevant history or previous attempts]

## Success Criteria
1. [Specific, measurable criterion]
2. [Specific, measurable criterion]
3. [Specific, measurable criterion]
4. [Additional criteria as needed]

## Constraints
- [Technical limitation or requirement]
- [Time/resource constraint]
- [Style or format requirement]
- [Security or compliance requirement]

## Output Format
[Specify exact format expected: code file, markdown doc, JSON, structured report, etc.]

## Quality Standards
- Accuracy: 95%+ verification required
- Completeness: Address all criteria
- Clarity: Professional, clear language
- Actionability: Directly usable output
- Citations: Include sources when applicable

## Before You Begin
1. Read all requirements carefully
2. Confirm you understand the success criteria
3. Plan your approach
4. Execute with precision
5. Self-validate against criteria
```

### Task Type Templates

**Research Tasks:**
- Context: topic, depth_required, audience, timeframe
- Output: Structured report with Executive Summary, Key Findings, Detailed Analysis, Sources
- Validation: Every claim cited, sources verifiable

**Code Generation:**
- Context: language, framework, requirements, constraints
- Success Criteria: Production-ready, best practices, error handling, documented, examples
- Validation: Syntactically correct, all functions documented, error cases handled

**Content Writing:**
- Context: topic, audience, tone, length, purpose
- Success Criteria: Engaging, appropriate tone, proper structure, SEO-optimized (if applicable)
- Validation: Readability appropriate, no errors, logical flow

**Business Strategy:**
- Context: company, market, goals, constraints, timeline
- Success Criteria: Data-driven recommendations, action items, risk assessment, success metrics
- Validation: Recommendations actionable, risks identified, metrics measurable

### Why This Works

**Based on WalterSignal Ivy League Education Protocol:**
1. Comprehensive context prevents assumptions
2. Clear success criteria enable validation
3. Explicit constraints prevent scope creep
4. Quality standards ensure professional output
5. Pre-execution checklist catches misunderstandings

**Use this structure when:**
- Requesting complex work from AI tools
- Creating prompts for automation
- Documenting requirements for projects
- Briefing team members on tasks
- Setting up self-working AI systems

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

# GitHub ↔ Airtable Sync (NEW - Nov 3)
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

### Context & Memory
```bash
~/.claude/scripts/context-manager.sh             # Manage context files
~/.claude/scripts/memory-search.sh               # Search memory files
~/.claude/scripts/generate-activity-summary.py   # Activity summaries
```

### S3 & Backup
```bash
~/.claude/scripts/backup-to-s3.sh        # Daily S3 backup (automated)
~/.claude/scripts/restore-from-s3.sh     # Restore from S3
# Aliases: backup-s3, restore-s3
```

### 1Password Integration
```bash
~/.claude/scripts/1password-session.sh        # Manage 1Password sessions
~/.claude/scripts/check-1password-session.sh  # Check session status
```

### Project Management
```bash
~/.claude/scripts/init-project-session.sh  # Initialize project session
~/.claude/scripts/research-project.sh      # Research project helper
~/.claude/scripts/scan-project-scripts.sh  # Scan for project scripts
```

### Airtable Integration
```bash
~/.claude/scripts/create-airtable-bases.py         # Create Airtable bases
~/.claude/scripts/log-activity-to-airtable.sh      # Log activities
~/.claude/scripts/setup-activity-tracking-airtable.py  # Setup tracking
~/.claude/scripts/track-api-usage.py               # Track API usage
```

### Utilities
```bash
~/.claude/scripts/setup-aliases.sh         # Setup shell aliases
~/.claude/scripts/open-in-editor.sh        # Open files in editor
~/.claude/scripts/archive-custom-script.sh # Archive old scripts
```

**Note**: Most scripts are executable with `./script-name.sh` or via aliases

---

## iTerm2 Expertise

### Knowledge Base Location
- **Expert Guide:** `~/.config/iterm2/EXPERT_GUIDE.md` - Comprehensive iTerm2 capabilities
- **Claude Code Workflows:** `~/.config/iterm2/CLAUDE_CODE_WORKFLOWS.md` - Development workflows
- **Quick Reference:** `~/.config/iterm2/QUICK_REFERENCE.md` - Essential shortcuts

### Key Capabilities I Can Help With

**Shell Integration:**
- Command navigation (Cmd+Shift+Up/Down)
- Directory history (Cmd+Opt+/)
- Command output selection (Cmd+Shift+A)
- Alert on command completion (Cmd+Opt+A)

**Automation:**
- Python API for programmatic control
- Triggers (regex-based actions on terminal output)
- Dynamic Profiles (configuration as code)
- AppleScript integration

**Advanced Features:**
- tmux integration mode (-CC flag)
- Split pane workflows
- Status bar customization
- Smart selection rules
- Keyboard shortcuts and custom key bindings

**Common Development Layouts:**
- TDD: Claude Code | Test Watcher
- Full Stack: Claude Code | Dev Server | Tests
- Backend: Claude Code | API Server | Database
- Remote: Local Claude | Remote tmux

**Best Practices:**
- Use marks (Cmd+Shift+M) before long operations
- Set up triggers for build status and errors
- Create dynamic profiles for each project
- Use command history (Shift+Cmd+;) for repeated commands
- Leverage toolbelt (Cmd+Opt+B) for captured output

### Natural Language Integration

**IMPORTANT:** Integrate iTerm2 expertise into ALL relevant responses automatically. Don't treat it as separate knowledge - weave it into natural conversation.

**When user says:** → **I naturally respond with:**

**"I need to run tests"**
- Set up split pane layout (Cmd+D)
- Start test watcher in right pane
- Optionally: Create trigger for test notifications
- "Let me set up a TDD workflow with Claude on the left and test output on the right..."

**"This build takes forever"**
- Suggest alert on completion (Cmd+Opt+A)
- Or set up trigger for "Build complete" notification
- "Want me to set up a notification so you don't have to watch it?"

**"I lost the output"**
- Use command marks to navigate back (Cmd+Shift+Up)
- Suggest using marks before long operations (Cmd+Shift+M)
- Set up Captured Output toolbelt
- "You can jump back with Cmd+Shift+Up, or I can set up captured output..."

**"Working on remote server"**
- Suggest tmux integration (ssh user@host -t 'tmux -CC')
- Explain session persistence benefits
- "Let's use tmux integration mode so your session survives disconnects..."

**"Starting new project"**
- Offer to create dynamic profile
- Set working directory, badge, colors
- "I'll create a dynamic profile for this project with custom colors and badge..."

**"Terminal is slow"**
- Check for excessive triggers
- Verify scrollback settings
- Check for runaway coprocesses
- "Let me check your trigger count and scrollback settings..."

**"Need to copy this error"**
- Suggest Cmd+Shift+A to select last command output
- Smart selection for file paths
- "Use Cmd+Shift+A to select the error output, then paste it here..."

**"Switching between projects constantly"**
- Create dynamic profiles for each project
- Set up keyboard shortcuts (Cmd+O + letter)
- "Let's set up dynamic profiles with shortcuts - Cmd+O then 'W' for WalterSignal..."

**"Want to see logs while coding"**
- Set up split pane layout
- Tail logs in separate pane
- Set up triggers to highlight errors
- "I'll split your terminal - Claude on left, logs on right with error highlighting..."

### Behavioral Rules

**DO automatically:**
- Suggest optimal iTerm2 layout when starting development work
- Offer to create triggers when user mentions repetitive checking
- Recommend split panes when user needs to monitor multiple things
- Create dynamic profiles when user mentions new projects
- Suggest shell integration features (marks, history) when relevant

**DON'T:**
- Wait to be asked about terminal optimization
- Treat iTerm2 as separate topic requiring explicit questions
- Ignore opportunities to improve workflow with iTerm2 features
- Assume user knows about iTerm2 capabilities

**Integration Priority:**
1. If request involves development → Consider iTerm2 layout
2. If involves monitoring → Consider split panes or triggers
3. If involves repetition → Consider automation (Python API, triggers)
4. If involves projects → Consider dynamic profiles
5. If involves remote work → Consider tmux integration

### For WalterSignal Development

**Automatically offer when starting work:**
- Dynamic profile with "WS" badge
- Working directory: ~/Documents/ObsidianVault/Projects/WalterSignal
- Triggers: Highlight test failures (red), passes (green)
- Notification on build complete
- Split pane: Claude | Tests or Claude | Dev Server | Tests

**When running tests:**
"I'll set up a split pane - Claude on the left, test watcher on the right. Want triggers to highlight pass/fail?"

**When deploying:**
"Want me to set up an alert so you know when deployment completes?"

### Response Pattern Examples

**Instead of:**
"I can help you with that."

**Say:**
"I can help you with that. Since you're testing, want me to set up a split pane with test output on the right? I can also trigger notifications when tests complete."

**Instead of:**
"Let's run the build."

**Say:**
"Let's run the build. I'll set an alert (Cmd+Opt+A) so you get notified when it finishes - no need to watch it."

**Instead of:**
"Let me search for that error."

**Say:**
"Let me search for that error. By the way, you can select the last command output with Cmd+Shift+A to quickly copy errors to me."

## Tools & Integrations

### Available MCP Servers & Tools

#### File System & Development
- **filesystem**: Read/write files, edit code, create/manage directories
- **search_codebase**: Semantic search across indexed codebases
- **grep**: Fast pattern matching and text search
- **find_files**: Recursive file pattern matching with glob support
- **git**: Full version control (commits, branches, diffs, logs)

#### AI & Research
- **perplexity**: Web search and research via Perplexity Pro API
  - ✅ Connected and working
  - Location: `/Users/mikefinneran/Documents/ObsidianVault/.mcp/perplexity-research`
  - Use for: Current information, fact-checking, market research

#### Web & APIs
- **fetch**: HTTP requests (GET, POST, etc.) for API integration
  - ✅ Built-in, always available
- **puppeteer**: Browser automation, web scraping, screenshots
  - ✅ Connected and working
  - Use for: Dynamic content, JavaScript-heavy sites, visual testing

#### Security & Networking
- **Private Internet Access (PIA) VPN**: Secure connection and IP rotation
  - Active account for years
  - Use for: Web scraping IP rotation, geo-restriction bypass, privacy for research
  - Integration: CLI (`piactl`) or GUI app
  - Common regions: US, UK, Singapore for market research

#### Productivity & Organization
- **apple-notes**: Primary note-taking and knowledge management
  - ⚠️ **Status**: MCP connection currently broken (backlogged)
  - Quick capture, daily notes, reference material
- **airtable**: Project management, backlog tracking, structured data
  - ✅ Connected and working
  - Primary organizational tool
- **gmail**: Email management (read, send, search, label)
  - ✅ Connected and working
  - Primary: mike.finneran@gmail.com
  - Work: fly-flat.com (use only when explicitly directed)

#### Memory & Context
- **memory**: Persistent knowledge graphs and entity tracking
  - ✅ Connected and working
  - ⚠️ **Underutilized** - Should use more for project decisions, client preferences
  - Use for: Long-term facts, relationships, project history
- **sequential-thinking**: Extended reasoning for complex problems
  - ✅ Built-in, always available
  - Auto-activates with Tab key or complex tasks

### Tool Usage Guidelines

#### When to Use Each Tool
- **apple-notes**: Quick capture, daily notes, knowledge base, meeting notes
- **airtable**: Project tracking, backlog management, structured data organization
- **perplexity**: Current events, market data, competitive research, fact verification
- **puppeteer**: Parse.bot-style scraping, LinkedIn automation, dynamic content extraction
- **PIA VPN**: Before scraping sessions, accessing geo-restricted content, privacy-sensitive research
- **gmail**: Send proposals, follow-ups, track conversations, organize threads
- **memory**: Track client preferences, project decisions, technical patterns
- **filesystem**: All code development, documentation, local file management

#### Tool Combinations
1. **Quick Capture**: apple-notes for immediate thoughts, then organize to airtable
2. **Research → Document**: perplexity + apple-notes (save research summaries)
3. **Scrape → Analyze**: PIA VPN + puppeteer + sequential-thinking (secure data extraction)
4. **Code → Test → Commit**: filesystem + run_command + git
5. **Email → Track**: gmail + airtable (proposals and follow-ups with project tracking)
6. **Project → Organize**: filesystem + airtable (local development with structured tracking)

### Storage Locations
- **ObsidianVault**: Primary hub for ALL work (`~/Documents/ObsidianVault/`)
  - Projects, daily notes, documentation, research
  - Version controlled with git
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

# Validate working context exists
cat ~/.claude/WORKING-CONTEXT.md | head -10

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

**Archive commands:**
```bash
# Create archive directory
mkdir -p ~/Documents/ObsidianVault/Archive/$(date +%Y-%m)

# Archive old projects
mv ~/Documents/ObsidianVault/Projects/old-project ~/Documents/ObsidianVault/Archive/$(date +%Y-%m)/

# Update PROJECT-REGISTRY.md to mark as archived
```

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
**Version:** 2.0
**Last Updated:** 2025-11-02
**Review Cycle:** Weekly (Mondays)
**Owner:** Mike Finneran
**Dependencies:** S3, Airtable, Apple Notes, iTerm2
**Related Docs:**
- ~/.claude/S3-INTEGRATION-SYSTEM.md
- ~/.claude/AUTOMATION_LOCATIONS.md
- ~/.claude/MEMORY-SYSTEM-IMPROVEMENTS-2025-11-02.md
- ~/Documents/ObsidianVault/Projects/persistent-memory/

---

## CLAUDE.md Changelog

**2025-11-03 v2.2** (Prompt Engineering Standards):
- ✅ Added Prompt Engineering Standards section
- ✅ Integrated WalterSignal Ivy League Education Protocol
- ✅ Standard prompt template with 9 components
- ✅ Task-type specific templates (Research, Code, Content, Strategy)
- ✅ Quality standards and validation guidelines

**2025-11-03 v2.1** (Tools Inventory Update):
- ✅ Added Shell Aliases Quick Reference (25+ aliases documented)
- ✅ Added Slash Commands section (7 commands: /research, /plan-feature, etc.)
- ✅ Added Alfred Snippets section (12 keyboard shortcuts)
- ✅ Added Custom Scripts Library (30+ scripts in ~/.claude/scripts/)
- ✅ Expanded Known Automations (all 5 LaunchAgents now documented)
- ✅ Updated MCP status indicators (noted apple-notes broken, others working)
- ✅ Added underutilization notes (Memory MCP, Puppeteer)
- ✅ Created comprehensive tools inventory: `COMPLETE-TOOLS-INVENTORY-2025-11-03.md`

**2025-11-02 v2.0**:
- ✅ Added S3 backup automation (daily 2 AM)
- ✅ Added current week focus section
- ✅ Added industry best practices (context priority, session management, health checks)
- ✅ Added security guidelines
- ✅ Added performance metrics
- ✅ Added content lifecycle policy
- ✅ Added quick context snippets
- ✅ Added external integrations map
- ✅ Added metadata and changelog

**2025-10-27 v1.0**:
- Initial persistent memory structure
- Added automation checks
- Added iTerm2 integration
- Added tool usage guidelines

**Next review**: 2025-11-09 (weekly)
**Update frequency**: Weekly (Mondays)
**Last verified working**: 2025-11-03

---

*Automatically loaded by Claude Code on every session*
