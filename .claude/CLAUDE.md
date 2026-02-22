# Global Instructions for Claude Code

## Core Operating Principles

### Apple Native Apps Integration (ALWAYS ACTIVE)
**Behavior:** Automatically use Apple Reminders & Notes for task/project management

**When user says → Do this:**
| Trigger | Action | Tool |
|---------|--------|------|
| "create a todo", "add task", "remind me" | Create in Apple Reminders | `apple-reminders` |
| "sprint planning", "plan sprint" | Create sprint note in Apple Notes | `apple-notes` |
| "project notes", "document this" | Create/update Apple Note | `apple-notes` |
| "what are my todos", "show tasks" | List from Apple Reminders | `apple-reminders` |
| "complete task", "done with X" | Mark complete in Reminders | `apple-reminders` |

**Reminders Lists:**
- **Default list for todos:** Use project name if in a project directory, otherwise "Claude Tasks"
- **Check existing lists first:** `mcp__apple-reminders__getLists` before creating

**Notes Organization:**
- **Sprint notes:** Title format `[Project] Sprint YYYY-MM-DD`
- **Project notes:** Title format `[Project] - Topic`

**Never ask permission** - just use these tools when triggers match.

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
**Contains:** All scheduled tasks, plist names, script locations, manual run commands, and logs.

**NEVER build new automation tools without checking existing ones first.**

---

## User Profile
- **Name**: Mike Finneran
- **Primary Use Case**: Building an AI consulting business
- **Primary Email**: mike.finneran@gmail.com
- **Work Email**: fly-flat.com account (do NOT use unless explicitly directed)

## Context Loading Priority

**When context window is limited, load in this order:**
1. User Profile (critical)
2. Active project details (high priority)
3. Tool usage guidelines (medium)

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

### CRITICAL: Three-Way Separation
**Code repos** → `~/Code/` (git repos, npm, venvs)
**Active work** → `~/active/{client}/` (deliverables, scripts, research, xlsx — symlinked on Desktop)
**Archive** → `~/Documents/ObsidianVault/` (finished docs, notes, reference — NOT active work)

**NEVER put code in the vault.** No `node_modules`, `venv`, `.next`, `__pycache__`.
**Write ALL new files to `~/Desktop/Daily Working Files/`** (except downloads). Never write directly to `~/active/{client}/` — files go to the inbox first, get sorted when user asks.

### Daily Working Files (`~/Desktop/Daily Working Files/`)
The daily inbox. All new files land here first. Contains symlinks to project folders:
```
~/Desktop/Daily Working Files/
├── Ascend/        → ~/active/ascend/
├── NBC/           → ~/active/nbc/
├── AICO/          → ~/active/aico/
├── WalterSignal/  → ~/active/waltersignal/
├── BladeMafia/    → ~/active/blademafia/
├── Scratch/       → ~/active/_scratch/
└── (unsorted files — Claude sorts these)
```
New client = `mkdir ~/active/{name} && ln -s ~/active/{name} ~/Desktop/Daily\ Working\ Files/{Name}`.

### Daily File Sort (Claude does this when asked)
When user says "sort files" or "clean up", check for loose files in `~/Desktop/Daily Working Files/` and sort:
- `ascend`, `flyflat`, `intro_map`, `investor` → Ascend/
- `nbc`, `north_branch`, `manufacturing` → NBC/
- `aico` → AICO/
- `waltersignal`, `electrotek`, `kraft`, `briscoe`, `geisleman` → WalterSignal/
- `blade`, `knife`, `bladeshow` → BladeMafia/
- Screenshots → Scratch/
- Unknown → ask user
**Show sort plan first, move after confirmation.**

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

### Backup Strategy (3-2-1 Rule)
1. **NAS** (local hub): UGREEN DH2300 at `192.168.68.70` — automated rsync + Time Machine
   - `/Volumes/IronWolf-Backups` — code (hourly), vault (15 min), configs (daily), desktop (daily)
   - `/Volumes/IronWolf-Archives` — projects, clients, media, exports (manual)
   - Time Machine → `timemachine` share (hourly, automatic)
2. **Git/GitHub**: `~/Code/` repos pushed to GitHub (daily auto-push + manual)
3. **S3 Cloud** (offsite): NAS → S3 weekly (vault + configs, STANDARD_IA)
   - `s3://mikefinneran-personal/obsidian-vault-backup/`
   - `s3://mikefinneran-personal/claude-backups/`

**Quick commands:** `mount-nas`, `backup-status`, `nas-space`, `archive-project`, `archive-client`
**Details:** `~/.claude/AUTOMATION_LOCATIONS.md`

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
Files live in `~/active/{client}/` so the folder IS the client context. No client prefix needed.

| Type | Pattern | Example |
|------|---------|---------|
| Deliverable | `{what}_v{n}_{date}.xlsx` | `intro_map_8plus_v3_2026-02-19.xlsx` |
| Build script | `build_{what}_v{n}.py` | `build_intro_map_v3.py` |
| Research | `{topic}_{date}.md` | `connector_research_2026-02-19.md` |
| Reference | `{description}.{ext}` | `investor_targets_reranked.xlsx` |

**Rules:**
- Increment version, don't create new filenames
- Date = delivery/creation date, `YYYY-MM-DD`
- Lowercase, underscores, no spaces
- Scratch files: anything goes — they're in `_scratch/`

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

---

## Session Management

**Full guide:** `~/.claude/SESSION-GUIDE.md`

**Quick start:** "Check WORKING-CONTEXT.md - what was I working on?"
**End session:** Update WORKING-CONTEXT.md or run `cc-save`

**Slash commands:** `/backlog`, `/code-review`, `/explain-code`, `/optimize`, `/plan-feature`, `/research`, `/save-guide`

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
| apple-reminders | Task management | ✅ |
| apple-notes | Sprint planning, project docs | ✅ |
| obsidian-vault | Vault notes access | ✅ |

**Other:** PIA VPN (IP rotation), claudish (multi-model CLI)

### Storage
- **ObsidianVault**: Primary (`~/Documents/ObsidianVault/`)
- **Obsidian Projects**: Backlog & feature tracking (`~/Documents/ObsidianVault/Projects/`)
- **S3 Vault Backup**: `s3://mikefinneran-personal/obsidian-vault-backup/` (documents/notes)
- **S3 Claude Backup**: `s3://mikefinneran-personal/claude-backups/` (configs/scripts)

---

## Health Check & Security

**Quick checks:** `cat ~/.claude/CLAUDE.md | wc -l` (should be <600), `launchctl list | grep claude`

**Troubleshooting:** CLAUDE.md >700 lines → archive verbose sections | Backups failing → `tail ~/.claude/logs/s3-backup-error.log` | Context missing → `restore-s3`

**NEVER in CLAUDE.md:** API keys, passwords, client data, credentials
**Use 1Password:** `op item get "credential-name"` for all secrets

---

## Document Metadata

**Version:** 3.6 | **Last Updated:** 2026-02-13 | **Owner:** Mike Finneran

---

## Changelog

**v3.6** (2026-02-13): Context audit — removed stale sections, deduped automation table, trimmed ~30 lines
**v3.5** (2026-02-12): NAS backup system (UGREEN DH2300) — 6 LaunchAgents, 3-2-1 backup strategy
**v3.4** (2026-01-28): Added Apple Native Apps Integration - auto-use Reminders for todos, Notes for sprints
**v3.3** (2026-01-27): Trimmed 441→374 lines - moved session/commands to SESSION-GUIDE.md
**v3.2** (2026-01-27): Audit cleanup - removed project-specific content, clarified S3 paths
**v3.1** (2026-01-21): Separated code from vault - ~/Code/ for code, vault for docs only

---
*Automatically loaded by Claude Code on every session*
