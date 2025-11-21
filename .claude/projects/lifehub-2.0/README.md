# LifeHub 2.0 - Claude Code Project Workspace

This is the Claude Code project workspace for LifeHub 2.0 development.

---

## Quick Start

**New to this project?** Read these in order:

1. **PROJECT.md** - Complete project overview, context, and vision (15 min)
2. **STATUS.md** - Current implementation status and feature matrix (10 min)
3. **BACKLOG.md** - Prioritized development backlog (10 min)

**Resuming work?** Check STATUS.md first, then pick a task from BACKLOG.md.

---

## File Structure

```
lifehub-2.0/
├── README.md           # This file (project navigation)
├── PROJECT.md          # Project overview and context
├── STATUS.md           # Current implementation status
├── BACKLOG.md          # Prioritized task backlog
└── NOTES.md            # Development notes and learnings (create as needed)
```

---

## Key Resources

### LifeHub Project Files
- **Main Location**: `/Users/mikefinneran/Documents/ObsidianVault/Projects/LifeHub/`
- **Scripts**: `/Users/mikefinneran/Documents/ObsidianVault/.scripts/`
- **LaunchAgents**: `~/Library/LaunchAgents/`

### Important Documents
- **Project README**: `Projects/LifeHub/README.md` (navigation hub)
- **Overview**: `Projects/LifeHub/lifehub-overview.md` (product vision)
- **Enhancement Summary**: `Projects/LifeHub/2025-10-20-LifeHub-Enhancement-Summary.md`
- **Comparison**: Google Drive `PERSONAL-VS-COMMERCIAL-LIFEHUB.md`

### Templates & Dashboard
- **Dashboard**: `Projects/LifeHub/Enhanced/00-LifeHub-Dashboard.md`
- **Templates**: `Projects/LifeHub/Enhanced/Templates/`
- **Guides**: `Projects/LifeHub/Enhanced/` (various guides)

### Distribution Packages
- **Pro Templates**: `Projects/LifeHub/Packages/LifeHub-Pro-Templates-v1.0/`
- **Automation Suite**: `Projects/LifeHub/Packages/LifeHub-Automation-Suite-v1.0/`

---

## Current Sprint

**Week of Oct 27 - Nov 3**
**Goal**: Enable personal automation and test core features

**Priority Tasks**:
1. [ ] Enable daily note auto-population (LIFE-001)
2. [ ] Create weekly review automation (LIFE-004)
3. [ ] Use LifeHub for 1 week (LIFE-003)
4. [ ] Test Notion sync (LIFE-002)

**Success Metric**: Using 90%+ of LifeHub features daily

---

## Quick Commands

### Open Key Files
```bash
# Project workspace
cd ~/.claude/projects/lifehub-2.0

# LifeHub files
cd ~/Documents/ObsidianVault/Projects/LifeHub

# Scripts
cd ~/Documents/ObsidianVault/.scripts

# Open Obsidian vault
obs-open
```

### Check Status
```bash
# Active LaunchAgents
launchctl list | grep lifehub

# Recent daily notes
ls -lt ~/Documents/ObsidianVault/Daily/ | head -10

# Script logs
ls -lt ~/.scripts/*.log
```

### Run Tools
```bash
# Create/open today's daily note
obs-daily

# Update revenue metrics
obs-metrics

# Sync to Notion (when configured)
python3 ~/.scripts/sync_to_notion.py --dry-run
```

---

## Development Workflow

### Starting a New Session

1. **Review context**: Read PROJECT.md and STATUS.md
2. **Check backlog**: Pick next priority task from BACKLOG.md
3. **Update status**: Mark task as "In Progress" in BACKLOG.md
4. **Do the work**: Implement, test, document
5. **Update files**: Update STATUS.md with results
6. **Mark complete**: Update BACKLOG.md when done

### Making Changes

1. **Scripts**: Edit in `/Users/mikefinneran/Documents/ObsidianVault/.scripts/`
2. **Templates**: Edit in `Projects/LifeHub/Enhanced/Templates/`
3. **Documentation**: Edit in `Projects/LifeHub/` or `Projects/LifeHub/Enhanced/`
4. **Test**: Use for real to verify it works
5. **Document**: Update STATUS.md with findings

### Testing Changes

1. **Local test**: Use in personal vault
2. **Document issues**: Create backlog items for bugs
3. **Clean test**: Test on fresh install (VM or test Mac)
4. **User test**: (Future) Beta testers

---

## Key Decisions

### What's In Scope for v2.0
- ✅ Enhanced templates (Done)
- ✅ Auto-updating dashboard (Done)
- ✅ Daily note creation automation (Done)
- ⚠️ Daily note auto-population (In progress)
- ⚠️ Weekly review automation (To do)
- ⚠️ Notion integration (To validate)

### What's Out of Scope for v2.0
- ❌ Native mobile apps (Phase 3+)
- ❌ Team collaboration (Phase 3+)
- ❌ AWS Lambda backend (Phase 3+)
- ❌ White label version (Future)

### Open Questions
1. Are Gmail/Calendar sync required for MVP?
2. Is Notion integration core or optional?
3. What's the right pricing model?
4. How much support is sustainable for solo founder?

---

## Success Metrics

### Product Metrics
- **Feature Completeness**: 70% → Goal: 90%
- **Personal Usage**: 50% → Goal: 90%
- **Documentation**: 95% → Goal: 98%

### Business Metrics
- **Customers**: 0 → Goal: 10 beta users
- **Revenue**: $0 → Goal: $50-100/month
- **Landing Page**: No → Goal: Yes

### Quality Metrics
- **Bugs Found**: Track in BACKLOG.md
- **Time Savings**: Document actual vs claimed
- **User Satisfaction**: Gather feedback

---

## Common Tasks

### Enable Daily Note Auto-population

```bash
# Edit LaunchAgent to include update script
vim ~/Library/LaunchAgents/com.obsidian.lifehub.dailynote.plist

# Add call to update_daily_note.py after creation

# Reload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.obsidian.lifehub.dailynote.plist
launchctl load ~/Library/LaunchAgents/com.obsidian.lifehub.dailynote.plist
```

### Test Notion Integration

```bash
# Set up Notion integration
cd ~/Documents/ObsidianVault/.scripts
./setup-notion-sync.sh

# Test sync (dry run first)
python3 sync_to_notion.py --dry-run

# Run actual sync
python3 sync_to_notion.py
```

### Create New Template

```bash
# Copy existing template
cd ~/Documents/ObsidianVault/Projects/LifeHub/Enhanced/Templates
cp Daily-Note-Enhanced.md My-New-Template.md

# Edit with Obsidian or vim
vim My-New-Template.md

# Test in Obsidian with Templater
```

---

## Troubleshooting

### LaunchAgent Not Running

```bash
# Check if loaded
launchctl list | grep lifehub

# Check logs
log show --predicate 'subsystem contains "com.obsidian.lifehub"' --last 1h

# Reload
launchctl unload ~/Library/LaunchAgents/com.obsidian.lifehub.*.plist
launchctl load ~/Library/LaunchAgents/com.obsidian.lifehub.*.plist
```

### Script Errors

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check dependencies
pip3 list

# Run script manually with debug
python3 -m pdb ~/Documents/ObsidianVault/.scripts/script_name.py
```

### Obsidian Plugin Issues

1. Open Obsidian Settings
2. Community Plugins → Manage
3. Disable and re-enable plugin
4. Check console (Cmd+Opt+I) for errors

---

## Project Context

### Why LifeHub Exists

**Problem**: Existing productivity systems are either:
- Too simple (to-do lists)
- Too complex (enterprise project management)
- Too fragmented (many tools)
- Too cloud-dependent (no local control)

**Solution**: LifeHub combines:
- **Obsidian**: Powerful, local-first, extensible
- **Automation**: Reduce manual work
- **Integration**: Connect external services
- **Templates**: Best practices built-in
- **Flexibility**: Customize to your needs

### Target Customer

**Primary**: Solo founders and consultants who:
- Manage multiple projects and clients
- Need revenue tracking
- Want automation but keep control
- Prefer desktop but need mobile access
- Value their time highly

**Secondary**: Knowledge workers, freelancers, agency owners

### Competitive Advantage

- **Local-first**: You own your data
- **Obsidian-based**: Powerful plugin ecosystem
- **Hybrid approach**: Desktop power + mobile access
- **Automation included**: Unlike other Obsidian templates
- **Revenue focus**: Built for business, not just tasks

---

## Next Steps

**After initialization, the priorities are:**

1. **This Week**: Dogfood the product
   - Enable all automation
   - Use it daily
   - Document issues

2. **Next Week**: Validate core features
   - Test Notion sync
   - Define MVP scope
   - Simplify installation

3. **Week 3**: Prepare for launch
   - Landing page
   - Demo video
   - Support docs

4. **Week 4**: Beta launch
   - 10 free users
   - Gather feedback
   - Iterate

---

## Notes

- **Priority**: Medium (after WalterFetch)
- **Time Commitment**: ~3 hours/week
- **Revenue Target**: $500/month by end of Q1 2026
- **Customer Target**: 50 paying customers by mid-2026

---

## Links

### External Resources
- **Obsidian**: https://obsidian.md
- **Dataview Docs**: https://blacksmithgu.github.io/obsidian-dataview/
- **Templater Docs**: https://silentvoid13.github.io/Templater/
- **Notion API**: https://developers.notion.com/

### Communities
- **Obsidian Forum**: https://forum.obsidian.md/
- **Obsidian Discord**: https://discord.gg/obsidianmd
- **Indie Hackers**: https://www.indiehackers.com/

---

**Last Updated**: October 27, 2025
**Status**: Project initialized, ready for development
**Next Action**: Start with LIFE-001 from BACKLOG.md

---

*This workspace created by Claude Code for Mike Finneran*
*For questions or updates, edit these markdown files directly*
