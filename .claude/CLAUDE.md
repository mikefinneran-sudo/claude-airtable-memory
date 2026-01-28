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
4. **Project scripts**: `~/Documents/ObsidianVault/[1] WalterSignal/.scripts/`

### Reference Document
**Location:** `~/.claude/AUTOMATION_LOCATIONS.md`
**Contains:** All scheduled tasks, script locations, manual run commands

### Known Automations:
| Task | Schedule | Alias |
|------|----------|-------|
| S3 Vault Backup | Manual | `backup-s3` |
| Daily Notes | Daily | `vdaily` |
| GitHub → Airtable | Daily 9 AM | - |
| Perplexity Research | Daily midnight | - |

**Details:** `~/.claude/AUTOMATION_LOCATIONS.md`

**NEVER build new automation tools without checking existing ones first.**

---

## User Profile
- **Name**: Mike Finneran
- **Primary Use Case**: Building an AI consulting business
- **Primary Email**: mike.finneran@gmail.com
- **Work Email**: fly-flat.com account (do NOT use unless explicitly directed)

## Current Week Focus

**Week of**: 2026-01-22 (Week 4)
**Primary Focus**: System cleanup & organization
**Status**: Repository restructure complete
**Completed**:
- [x] Separated code from vault (2026-01-22)
- [x] Created vault purity checks
- [x] Added automated prevention (cron job every 6 hours)
**Next Actions**:
- [ ] Continue lead enrichment work
- [ ] Focus on active client projects

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

### CRITICAL: Code vs Documents Separation
**Code lives in:** `~/Code/` (organized by project)
**Documents live in:** `~/Documents/ObsidianVault/` (docs, media, notes)

**NEVER put code in the vault:**
- No `node_modules`, `venv`, `.next`, `__pycache__` in vault
- No `.claude` folders in vault (Claude Code creates these - delete if found)
- If you find code in the vault, move it to `~/Code/`

### Code Directory (`~/Code/`)
```
~/Code/
├── WalterSignal/     # Main business - crews, walterfetch, tools
├── BladeMafia/       # Knife group-buy Next.js app
├── FlyFlat/          # Client projects
└── Personal/         # Personal projects
```

### ObsidianVault (`~/Documents/ObsidianVault/`)
**For:** Documents, notes, research, media, comms - NOT code
- `[1] WalterSignal/` - Business docs, comms, research (no code)
- `Research/` - Research documents
- `Personal/` - Personal notes
- `Projects/` - Backlog, ideas, planning
- `Daily/` - Daily notes

### Other Storage
- **Airtable**: Client tracking, data tables
- **S3**: Cloud backup to `s3://mikefinneran-personal/obsidian-vault-backup/`

### Backup Strategy (3-Tier)
1. **Local**: ObsidianVault (`~/Documents/ObsidianVault/`) + git
2. **DGX External**: `rsync` to external drive on DGX (192.168.68.62)
3. **S3 Cloud**: `s3://mikefinneran-personal/obsidian-vault-backup/`

**Commands:**
- S3: `aws s3 sync ~/Documents/ObsidianVault/ s3://mikefinneran-personal/obsidian-vault-backup/`
- DGX: `rsync -avz ~/Documents/ObsidianVault/ mikefinneran@192.168.68.62:/mnt/external/obsidian-backup/`

## Command Auto-Approval

**Philosophy:** Keep work moving. Most commands are safe. Only pause for destructive/irreversible actions.

**Auto-approve:** Read-only (`ls`, `cat`, `grep`, `git status/diff/log`), dev (`npm *`, `pip *`, `python *`, `pytest`), git non-destructive (`add`, `commit`, `push` to non-main), system (`brew *`, `launchctl`), network (`ssh`, `scp`, `curl`, `ping`)

**NEVER auto-approve:** `sudo`, `rm -rf` without explicit path, `git push --force` to main, modifying `/etc`, `/usr`, `/System`, database DROP

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

### Quality Over Speed (CRITICAL - YOU MUST FOLLOW)
**STOP. STUDY. THEN EXECUTE.**
- When given a reference image: DESCRIBE what you see BEFORE writing code (colors, shapes, proportions)
- When recreating something: Break it into components, plan each one, THEN build
- First attempt MUST be close to correct - not garbage requiring 5+ iterations
- If unsure how to implement: ASK "how should I approach this?" instead of guessing
- After generating code/SVG/design: COMPARE to reference before showing user

**IMPORTANT:** One thoughtful attempt beats five rushed failures.

### Common Mistakes (LEARN FROM THESE)
| Mistake | Do This Instead |
|---------|-----------------|
| Writing SVG/code without studying reference | DESCRIBE the reference first, list components, then build |
| Guessing polygon coordinates | Use real measurements or trace in proper tool (Illustrator) |
| Multiple DALL-E attempts hoping for luck | Refine prompt once, if still wrong suggest alternative approach |
| Rushing to show something | Take 30 extra seconds to verify it matches requirements |
| Saying "let me try again" after failure | STOP, analyze why it failed, propose different approach |

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

**LLM Router:** `~/Code/WalterSignal/waltersignal-crews/llm-router/` - 25 model fleet (20 local FREE + 5 commercial)

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
- **"add to backlog"** / **"backlog: [topic]"** → Create project note in `~/Documents/ObsidianVault/Projects/` using Obsidian MCP
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

## Quick Reference

**Shell Aliases**: `~/.claude/guides/SHELL-ALIASES.md` - Most used: `vault`, `vdaily`, `c`, `cc`
**Alfred Snippets**: `~/.claude/ALFRED-SNIPPETS-GUIDE.md` - Quick access: `;ctx`, `;ws`, `;save`

---

## Active Projects

### WalterSignal (Primary)
- **Code**: `~/Code/WalterSignal/` - See `~/Code/WalterSignal/CLAUDE.md` for infrastructure details
- **Docs**: `~/Documents/ObsidianVault/[1] WalterSignal/` - Business docs, research, comms
- **Site**: waltersignal.io (Lightsail: 98.89.88.138)

### Other Projects
- **BladeMafia**: `~/Code/BladeMafia/` - Knife group-buy platform (Next.js 16, React 19, Supabase)
- **FlyFlat**: `~/Code/FlyFlat/` - Client work
- **Various**: `~/Code/[ProjectName]/` - See individual project CLAUDE.md files

---

## Custom Scripts Library

**Location**: `~/.claude/scripts/`
- Session: `start-session.sh`, `save-session-memory.sh`, `resume-work.sh`
- Backup: `backup-to-s3.sh`, `restore-from-s3.sh` (aliases: `backup-s3`, `restore-s3`)
- Airtable: `create-airtable-bases.py`, `log-activity-to-airtable.sh`

---

## iTerm2 Expertise

**Docs:** `~/.config/iterm2/` (EXPERT_GUIDE.md, CLAUDE_CODE_WORKFLOWS.md, QUICK_REFERENCE.md)
**Capabilities:** Shell integration, Python API, triggers, dynamic profiles, tmux, split panes
**Behavior:** Automatically suggest iTerm2 optimizations during development work

---

## Tools & Integrations

### Claude Code Plugins (✅ = Installed)
| Plugin | Purpose | Type |
|--------|---------|------|
| github | PR/issue management | manual |
| code-review | Structured reviews | manual |
| security-guidance | Security scanning | auto |
| playwright | Browser automation | manual |
| sentry | Error tracking | manual |
| hookify | Safety guardrails | auto |
| context7 | Library docs | semi-auto |
| frontend-design | UI/CSS guidance | manual |

**Install more:** `claude plugin install <name>`
**List available:** Check `~/.claude/plugins/marketplaces/`

### Hookify Rules (Active)
| Rule | Action | Triggers |
|------|--------|----------|
| block-dangerous-rm | BLOCK | `rm -rf /`, `~`, `/var`, `/etc` |
| warn-dgx-commands | warn | Commands to 192.168.68.62 |
| warn-production-lightsail | warn | Commands to 98.89.88.138 |
| warn-env-files | warn | Editing .env files |
| warn-hardcoded-secrets | warn | API keys in code |
| warn-database-drops | BLOCK | DROP, TRUNCATE, mass DELETE |

**Manage:** `ls ~/.claude/hookify.*.local.md`
**Disable:** Edit file, set `enabled: false`

### MCP Servers (✅ = Connected)
| Tool | Purpose | Status |
|------|---------|--------|
| perplexity | Web search, research | ✅ |
| airtable | Client data, tables | ✅ |
| gmail | Email (mike.finneran@gmail.com) | ⚠️ Not active |
| memory | Knowledge graphs | ✅ |
| playwright | Browser automation | ⚠️ Not active |
| apple-reminders | Task management | ✅ NEW |
| obsidian-vault | Vault notes access | ✅ |

**Other:** PIA VPN (IP rotation), claudish (multi-model CLI)

### Airtable API (CRITICAL)
**ALWAYS use `AirtableClient`** for any Airtable operations in Python scripts.
```python
from utils.airtable_client import AirtableClient
client = AirtableClient(base_id="appXXX", table_id="tblXXX")
records = client.fetch_records(filter_formula="{Status}='New'")
client.batch_update(updates)  # 10 records/call
client.batch_create(records)  # 10 records/call
```
**Location:** `~/Code/WalterSignal/walterfetch-v2/utils/airtable_client.py`
**Features:** Batching (90% fewer calls), rate limiting, retries, caching, stats

### Storage
- **ObsidianVault**: Primary (`~/Documents/ObsidianVault/`)
- **Obsidian Projects**: Backlog & feature tracking (`~/Documents/ObsidianVault/Projects/`)
- **S3**: Automated backups (s3://mikefinneran-personal/claude-backups/)

---

## Health Check & Security

**Quick checks:** `cat ~/.claude/CLAUDE.md | wc -l` (should be <600), `launchctl list | grep claude`

**Troubleshooting:** CLAUDE.md >700 lines → archive verbose sections | Backups failing → `tail ~/.claude/logs/s3-backup-error.log` | Context missing → `restore-s3`

**NEVER in CLAUDE.md:** API keys, passwords, client data, credentials
**Use 1Password:** `op item get "credential-name"` for all secrets

---

## Document Metadata

**Version:** 3.1 | **Last Updated:** 2025-01-21 | **Owner:** Mike Finneran

---

## Changelog

**v3.1** (2025-01-21): Separated code from vault - ~/Code/ for code, vault for docs only
**v3.0** (2025-12-16): Added Claude Code plugins section, hookify safety rules
**v2.9** (2025-12-15): Trimmed to <575 lines, condensed automations/tools sections
**Full history:** `~/.claude/CHANGELOG-ARCHIVE.md`

---
*Automatically loaded by Claude Code on every session*
