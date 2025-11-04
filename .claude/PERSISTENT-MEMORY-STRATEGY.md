# Persistent Memory Strategy for Claude Code

**Optimal structure for Mike Finneran's workflow**

---

## Current Analysis

### What's Working Well ✅
- **CLAUDE.md**: Good user profile, preferences, file locations
- **Project workspaces**: LifeHub 2.0 has excellent structure
- **Clear separation**: Global vs project-specific content

### What Needs Improvement ⚠️
- Active projects list is static (gets outdated)
- No quick project registry
- No "current context" tracking
- Decision logs are scattered

---

## Optimal Structure

### Level 1: Global Memory (`~/.claude/CLAUDE.md`)

**Purpose**: Information that applies to ALL sessions and projects

**Keep**:
- ✅ User profile (name, email, use case)
- ✅ Communication preferences
- ✅ File naming conventions
- ✅ Development workflow principles
- ✅ Default file locations (Obsidian vault, Google Drive)

**Remove/Minimize**:
- ❌ Static "Active Projects" list (use PROJECT-REGISTRY instead)
- ❌ Tool-specific details (move to project files)
- ❌ Long workflow descriptions (reference only)

**Size Target**: Keep under 150 lines

---

### Level 2: Project Registry (`~/.claude/PROJECT-REGISTRY.md`)

**Purpose**: Quick reference of all active projects

**Format**:
```markdown
# Active Projects

| Project | Status | Priority | Location | Last Updated |
|---------|--------|----------|----------|--------------|
| LifeHub 2.0 | Active | Medium | ~/.claude/projects/lifehub-2.0 | 2025-10-27 |
| WalterFetch | Active | High | ~/Documents/ObsidianVault/Projects/ | 2025-10-XX |
| Granola | Research | Low | ~/.claude/projects/granola | 2025-10-27 |

## Quick Links
- LifeHub: `~/.claude/projects/lifehub-2.0/README.md`
- Vault: `/Users/mikefinneran/Documents/ObsidianVault/`
```

**Update Frequency**: Weekly or when starting/pausing projects

---

### Level 3: Project Workspaces (`~/.claude/projects/[project-name]/`)

**Purpose**: All context for a specific project

**Essential Files** (for every project):

1. **README.md** (200-400 lines)
   - Navigation hub
   - Quick commands
   - File locations
   - How to resume work

2. **PROJECT.md** (400-600 lines)
   - Overview and vision
   - Technical architecture
   - Key decisions
   - Resources

3. **STATUS.md** (300-500 lines)
   - Current state
   - Feature matrix
   - What's working/broken
   - Known issues

4. **BACKLOG.md** (400-800 lines)
   - Prioritized tasks
   - Dependencies
   - Effort estimates
   - Sprint planning

**Optional Files** (as needed):

5. **DECISIONS.md** - Major decisions and why
6. **NOTES.md** - Ongoing learnings
7. **QUICKREF.md** - One-page cheat sheet

**Size Target**: 1-3 MB per project max

---

### Level 4: Working Memory (`~/.claude/WORKING-CONTEXT.md`)

**Purpose**: What you're working on RIGHT NOW (resets weekly)

**Format**:
```markdown
# Current Working Context

**Week of**: 2025-10-27
**Primary Focus**: LifeHub 2.0 automation setup
**Secondary**: Granola research

## This Week's Goals
- [ ] LifeHub: Enable all automation features
- [ ] LifeHub: Create customer package
- [ ] LifeHub: Send to Omar

## Active Files
- /Users/mikefinneran/Documents/ObsidianVault/.scripts/
- /Users/mikefinneran/Desktop/LifeHub-v2.0.zip

## Context Notes
- Just fixed script encoding issues (CRLF → LF)
- Created LaunchAgents for daily/weekly automation
- Package ready for Omar review

## Next Session
- Follow up on Omar's feedback
- Test Notion integration
- Document learnings
```

**Update Frequency**: Every session

---

## What Goes Where?

### Global CLAUDE.md
✅ **DO include**:
- Your name, email, primary use case
- Communication style preferences
- File naming conventions
- Default save locations (vault, Google Drive)
- Workflow principles (TDD, documentation standards)

❌ **DON'T include**:
- Active project lists (they change)
- Specific project details
- Long procedures (reference instead)
- Tool versions (unless critical)

---

### Project Files
✅ **DO include**:
- Everything about THIS project
- Architecture decisions
- Current status and todos
- File locations and commands
- Learnings and context

❌ **DON'T include**:
- General preferences (those are global)
- Other project info
- Outdated/archived content (move to /Archive)

---

### Obsidian Vault
✅ **DO use for**:
- Business documents
- Research notes
- Project planning
- Client information
- Guides and documentation

❌ **DON'T use for**:
- Claude-specific memory
- Session state
- Development notes for code projects

---

## Memory Retrieval Strategy

### When Starting a Session:

1. **CLAUDE.md** loads automatically (always available)
2. **Check PROJECT-REGISTRY.md** → Find active projects
3. **Open project README.md** → Get oriented
4. **Check WORKING-CONTEXT.md** → See where you left off
5. **Review STATUS.md** → Understand current state
6. **Pick from BACKLOG.md** → Choose next task

### When Resuming Specific Work:

1. Say: "Continue with [project-name]"
2. I read: `~/.claude/projects/[project-name]/README.md`
3. I check: `STATUS.md` and `BACKLOG.md`
4. We pick up where you left off

---

## Size Guidelines

### Keep It Lean

**Global Memory**: 3-5 KB
- CLAUDE.md: ~150 lines
- PROJECT-REGISTRY.md: ~50 lines
- WORKING-CONTEXT.md: ~50 lines

**Per Project**: 50-200 KB
- README: 200-400 lines
- PROJECT: 400-600 lines
- STATUS: 300-500 lines
- BACKLOG: 400-800 lines

**Why?**
- Faster to read
- Easier to maintain
- Less noise
- More focused context

---

## Update Frequency

| File | Update When | Who Updates |
|------|-------------|-------------|
| CLAUDE.md | Preferences change | Manual (rare) |
| PROJECT-REGISTRY.md | Start/pause project | Manual (weekly) |
| WORKING-CONTEXT.md | Every session | Claude + You |
| Project README.md | Setup or major changes | Manual (monthly) |
| Project STATUS.md | Feature changes | Claude (every session) |
| Project BACKLOG.md | Tasks change | Claude (as needed) |

---

## Best Practices

### 1. Keep Global Memory Minimal
Only truly global information. Everything else goes in projects.

### 2. Use Project Workspaces Aggressively
Each significant effort gets a project folder, even if temporary.

### 3. Update STATUS.md Religiously
At end of session, I should update what changed.

### 4. Weekly Context Reset
Every Monday, review and update WORKING-CONTEXT.md

### 5. Archive Completed Projects
Move to `~/.claude/projects/archive/[project-name]/` when done

---

## Efficient Commands

### For You:
```bash
# See all projects
cat ~/.claude/PROJECT-REGISTRY.md

# Start working on project
cd ~/.claude/projects/lifehub-2.0
cat README.md

# Check what's active
cat ~/.claude/WORKING-CONTEXT.md

# See status
cat ~/.claude/projects/lifehub-2.0/STATUS.md
```

### For Me:
When you say "continue lifehub", I:
1. Read `~/.claude/projects/lifehub-2.0/README.md`
2. Check `STATUS.md` for current state
3. Review `BACKLOG.md` for next tasks
4. Update `WORKING-CONTEXT.md` with session notes

---

## Example: Perfect Session Start

**You**: "Continue LifeHub, let's test Notion integration"

**Me**:
1. Read `~/.claude/projects/lifehub-2.0/README.md` → Get context
2. Check `STATUS.md` → See Notion sync status
3. Review `BACKLOG.md` → Find LIFE-002 (Test Notion sync)
4. Execute the task
5. Update `STATUS.md` with results
6. Update `WORKING-CONTEXT.md` with progress

---

## Anti-Patterns (Don't Do This)

❌ **Don't**: Store everything in CLAUDE.md
- Gets too long
- Hard to find information
- Slows down context loading

❌ **Don't**: Create projects without structure
- No README = Can't resume later
- No STATUS = Don't know what works
- No BACKLOG = Don't know what's next

❌ **Don't**: Duplicate information
- Keep it in ONE place
- Reference, don't repeat

❌ **Don't**: Let files get stale
- Update STATUS after every session
- Review PROJECT-REGISTRY weekly
- Archive completed work

---

## Migration Plan (For You)

### Week 1: Foundation
- [ ] Update CLAUDE.md (remove active projects list)
- [ ] Create PROJECT-REGISTRY.md
- [ ] Create WORKING-CONTEXT.md
- [ ] Review LifeHub workspace (already good!)

### Week 2: Refinement
- [ ] Create workspaces for other active projects
- [ ] Move scattered notes to project folders
- [ ] Set up weekly review routine

### Week 3: Optimization
- [ ] Archive old/completed projects
- [ ] Tune file sizes
- [ ] Establish update cadence

---

## Recommended Structure

```
~/.claude/
├── CLAUDE.md                    # Global preferences (150 lines)
├── PROJECT-REGISTRY.md          # Active projects list (50 lines)
├── WORKING-CONTEXT.md           # Current focus (50 lines)
│
└── projects/
    ├── lifehub-2.0/
    │   ├── README.md            # Navigation (300 lines)
    │   ├── PROJECT.md           # Overview (500 lines)
    │   ├── STATUS.md            # Current state (400 lines)
    │   ├── BACKLOG.md           # Tasks (600 lines)
    │   └── QUICKREF.md          # Cheat sheet (200 lines)
    │
    ├── walterfetch/             # Create when actively working
    │   ├── README.md
    │   ├── PROJECT.md
    │   ├── STATUS.md
    │   └── BACKLOG.md
    │
    └── archive/                 # Completed projects
        └── old-project/
```

---

## Bottom Line

**Most Efficient Strategy**:

1. **Minimal global** (CLAUDE.md) - Only true preferences
2. **Active registry** (PROJECT-REGISTRY.md) - Quick project list
3. **Rich project workspaces** - All context for each effort
4. **Current focus** (WORKING-CONTEXT.md) - What's happening now
5. **Regular updates** - STATUS after sessions, review weekly

**Key Insight**: Keep global lean, make projects rich, track current work, update frequently.

---

**Created**: 2025-10-27
**Next Review**: Weekly
**Owner**: Mike Finneran
