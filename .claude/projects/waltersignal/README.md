# WalterSignal Project Workspace

**Navigation Hub** for WalterSignal AI consulting business

**Last Updated**: November 1, 2025 (Migrated to Airtable infrastructure)

---

## Quick Reference

**Project Type**: AI Consulting Business (Stealth Mode)
**Data Location**: Airtable (app6g0t0wtruwLA5I)
**Code Location**: `~/ADDB/WalterSignal/Code/` (formerly `~/Documents/Code/`)
**Status**: MVP Development Phase
**Owner**: Mike Finneran

---

## NEW Infrastructure (As of Nov 1, 2025)

### Airtable - Source of Truth
**WalterSignal DB**: https://airtable.com/app6g0t0wtruwLA5I
- Tasks (backlogs migrated here)
- Projects
- Clients
- Research
- Documents
- Meetings
- Ideas
- Resources
- Templates
- Team

### Code Repositories (Git)
**Location**: `~/ADDB/WalterSignal/Code/`

- **SpecialAgentStanny**: `~/ADDB/WalterSignal/Code/SpecialAgentStanny/`
  - Python framework for AI automation
  - Git repo initialized

- **WalterFetch v2**: `~/ADDB/WalterSignal/Code/walterfetch-v2/`
  - Lead generation platform (Next.js)
  - Git repo initialized

### Business Data
**AeroDyne Master DB**: https://airtable.com/appLTPMWXOY9LKqEw
- Operating Companies (WalterSignal linked)
- Strategic Initiatives
- Consolidated Financials
- Company KPIs

---

## Legacy Archive (Read-Only)

**ObsidianVault** is now a read-only archive:
- Location: `~/Documents/ObsidianVault/`
- Status: Read-only (for historical reference)
- Backup: `~/Documents/AeroDyne_LLC/Archives/ObsidianVault-Archive-2025-11-01/`
- See: `ARCHIVE-NOTICE.md` in vault root

**Do not edit files in ObsidianVault.** Use Airtable and Code repos instead.

---

## Project Status

See `STATUS.md` in this directory for detailed feature matrix and current state.

---

## Backlog

**Migrated to Airtable**: WalterSignal Tasks table (10 items)
**View in Airtable**: https://airtable.com/app6g0t0wtruwLA5I

Local copy: See `BACKLOG.md` for reference (read-only).

---

## Session History

See `SESSIONS.md` for chronological log of all work sessions.

---

## How to Resume Work

### Start a Session
1. Type: `resume` (launches interactive memory system)
2. Select "WalterSignal" from project list
3. Claude loads full context from Airtable + Code repos
4. Check STATUS.md for current state
5. Review Tasks in Airtable for next priorities

### End a Session
1. Type: `save-session`
2. Summary automatically saved to `SESSIONS.md`
3. Updates synced to Airtable (future automation)

---

## Quick Commands

```bash
# Navigate to code (via symlink)
cd ~/WalterSignal/Code/SpecialAgentStanny
cd ~/WalterSignal/Code/walterfetch-v2

# Or use full path
cd ~/ADDB/WalterSignal/Code/SpecialAgentStanny
cd ~/ADDB/WalterSignal/Code/walterfetch-v2

# Open Airtable
open https://airtable.com/app6g0t0wtruwLA5I  # WalterSignal
open https://airtable.com/appLTPMWXOY9LKqEw  # AeroDyne Master

# View project workspace
cd ~/.claude/projects/waltersignal
cat README.md

# Check current status
cat ~/.claude/projects/waltersignal/STATUS.md

# See recent work
cat ~/.claude/projects/waltersignal/SESSIONS.md | tail -100

# View archive (read-only)
cd ~/Documents/ObsidianVault/Projects/WalterSignal
cat ~/Documents/ObsidianVault/ARCHIVE-NOTICE.md
```

---

## Links

### Active Locations
- **WalterSignal Airtable**: https://airtable.com/app6g0t0wtruwLA5I
- **AeroDyne Master**: https://airtable.com/appLTPMWXOY9LKqEw
- **Code Repos**: `~/Documents/Code/`
- **Memory System**: `~/.claude/SESSION-MEMORY.md`

### Archives (Read-Only)
- **ObsidianVault**: `~/Documents/ObsidianVault/Projects/WalterSignal` (deprecated)
- **Full Backup**: `~/Documents/AeroDyne_LLC/Archives/ObsidianVault-Archive-2025-11-01/`

### Documentation
- **Migration Report**: `~/Documents/AeroDyne_LLC/Archives/ObsidianVault-Archive-2025-11-01/MIGRATION-REPORT.md`
- **Airtable Setup**: `~/.claude/AIRTABLE-SETUP-COMPLETE.md`
- **Business Structure**: `~/.claude/BUSINESS-STRUCTURE.md`

---

## Database Hierarchy

```
Mike Finneran (Founder)
│
├── AeroDyne LLC (appLTPMWXOY9LKqEw)
│   ├── Operating Companies
│   │   └── WalterSignal → app6g0t0wtruwLA5I
│   ├── Strategic Initiatives
│   ├── Consolidated Financials
│   └── Company KPIs
│
├── WalterSignal (app6g0t0wtruwLA5I)
│   ├── Tasks (backlogs migrated)
│   ├── Projects
│   ├── Clients (FlyFlat)
│   └── [7 other tables]
│
└── Mike Personal (appXiUbIRnkmFDlfz)
    ├── Personal Projects
    ├── Goals & OKRs
    └── [4 other tables]
```

---

## Migration Summary (Nov 1, 2025)

**What Changed:**
- ✅ Backlogs → Airtable WalterSignal Tasks (10 items)
- ✅ Code → `~/Documents/Code/` (git repos)
- ✅ Business data → Airtable AeroDyne Master
- ✅ ObsidianVault → Read-only archive
- ✅ Complete backup (151MB tar.gz)

**What to Use Now:**
- **Tasks**: Airtable WalterSignal Tasks table
- **Code**: `~/Documents/Code/SpecialAgentStanny` and `walterfetch-v2`
- **Quick notes**: Apple Notes
- **Business tracking**: Airtable AeroDyne Master
- **Historical reference**: ObsidianVault (read-only)

---

**Created**: 2025-11-01
**Last Updated**: 2025-11-01 (Migration complete)
**Review**: Weekly on Fridays
