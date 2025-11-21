# LifeHub 2.0 - Quick Reference Card

One-page reference for common LifeHub development tasks.

---

## File Locations

```
Obsidian Vault:    /Users/mikefinneran/Documents/ObsidianVault/
LifeHub Project:   /Users/mikefinneran/Documents/ObsidianVault/Projects/LifeHub/
Scripts:           /Users/mikefinneran/Documents/ObsidianVault/.scripts/
LaunchAgents:      ~/Library/LaunchAgents/
Claude Workspace:  ~/.claude/projects/lifehub-2.0/
```

---

## Key Commands

### Daily Usage
```bash
obs-open            # Open Obsidian vault
obs-daily           # Open today's daily note
obs-metrics         # Update revenue metrics
obs-vault           # Navigate to vault directory
```

### Development
```bash
# Check running automation
launchctl list | grep lifehub

# View logs
tail -f ~/Documents/ObsidianVault/.scripts/*.log

# Test Notion sync
cd ~/Documents/ObsidianVault/.scripts
python3 sync_to_notion.py --dry-run

# Edit LaunchAgent
vim ~/Library/LaunchAgents/com.obsidian.lifehub.dailynote.plist

# Reload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.obsidian.lifehub.*.plist
launchctl load ~/Library/LaunchAgents/com.obsidian.lifehub.*.plist
```

---

## Priority Tasks (Next 2 Weeks)

**This Week**:
- [ ] Enable daily note auto-population (30 min)
- [ ] Create weekly review automation (1 hour)
- [ ] Use LifeHub daily for 7 days (ongoing)
- [ ] Test Notion sync (2 hours)

**Next Week**:
- [ ] Define MVP feature set (2 hours)
- [ ] Simplify installation (3 hours)
- [ ] Test on clean Mac (2 hours)
- [ ] Create onboarding checklist (1 hour)

---

## Scripts Overview

| Script | Purpose | Status | Location |
|--------|---------|--------|----------|
| `create_daily_note.sh` | Create daily note at 7 AM | ✅ Running | `.scripts/` |
| `update_daily_note.py` | Auto-populate with tasks | ⚠️ Not integrated | `.scripts/` |
| `update_metrics.py` | Interactive revenue tracking | ✅ Working | `.scripts/` |
| `sync_gmail.py` | Gmail → Obsidian | ⚠️ Needs OAuth | `.scripts/` |
| `sync_calendar.py` | Calendar → Obsidian | ⚠️ Needs OAuth | `.scripts/` |
| `sync_to_notion.py` | Obsidian ↔ Notion | ⚠️ Needs testing | `.scripts/` |
| `setup-notion-sync.sh` | Notion setup wizard | ⚠️ Ready | `.scripts/` |

---

## LaunchAgents

| Agent | Schedule | Status | Purpose |
|-------|----------|--------|---------|
| `com.obsidian.lifehub.dailynote.plist` | Daily 7 AM | ✅ Running | Create daily note |
| `com.lifehub.dailynote-enhanced.plist` | Daily 7:01 AM | ⚠️ Not active | Auto-populate note |
| `com.lifehub.weeklyreview.plist` | Sunday 6 PM | ⚠️ Not active | Weekly review |

---

## Templates

Location: `Projects/LifeHub/Enhanced/Templates/`

- `Daily-Note-Enhanced.md` - Daily planning & reflection
- `Project-Template-Enhanced.md` - Project management
- `Client-Template-Enhanced.md` - CRM & client tracking
- `Weekly-Review-Template.md` - Weekly planning

---

## Dashboard

Location: `Projects/LifeHub/Enhanced/00-LifeHub-Dashboard.md`

**Features**:
- Auto-updating task counts
- Real-time revenue metrics
- Active project status
- Today's tasks (due, overdue, priority)
- Weekly goals
- Habit tracking
- Quick actions

**Usage**: Open every morning, pin to sidebar

---

## Documentation

Location: `Projects/LifeHub/`

**Main Index**: `README.md` (navigation hub)
**Product Overview**: `lifehub-overview.md`
**Quick Start**: `Enhanced/QUICK-START.md`
**Full Guide**: `Enhanced/LifeHub-Enhancement-Guide.md`
**Notion Guide**: `Enhanced/LifeHub-Notion-Integration-Guide.md`

---

## Distribution Packages

Location: `Projects/LifeHub/Packages/`

- `LifeHub-Pro-Templates-v1.0/` - $49 package
- `LifeHub-Automation-Suite-v1.0/` - $99 package
- `DISTRIBUTION-GUIDE.md` - How to package
- `SALES-PAGE.md` - Marketing copy

---

## Troubleshooting

### Daily Note Not Creating
```bash
# Check LaunchAgent is loaded
launchctl list | grep dailynote

# Check logs
cat ~/Documents/ObsidianVault/.scripts/daily-note-enhanced-error.log

# Reload
launchctl unload ~/Library/LaunchAgents/com.obsidian.lifehub.dailynote.plist
launchctl load ~/Library/LaunchAgents/com.obsidian.lifehub.dailynote.plist
```

### Dataview Not Working
1. Settings → Community Plugins → Enable Dataview
2. Restart Obsidian
3. Check query syntax (case-sensitive)

### Templater Not Prompting
1. Settings → Templater → Check folder path
2. Enable "Trigger on new file"
3. Verify syntax: `<% tp.system.prompt() %>`

### Notion Sync Failing
```bash
# Check token exists
cat ~/.lifehub-notion-token

# Test with dry run
python3 ~/Documents/ObsidianVault/.scripts/sync_to_notion.py --dry-run

# Check logs
cat ~/Documents/ObsidianVault/.scripts/notion-sync.log
```

---

## Development Workflow

1. **Start**: Review STATUS.md and BACKLOG.md
2. **Pick task**: Choose from priority backlog
3. **Implement**: Make changes in vault/scripts
4. **Test**: Use for real in personal vault
5. **Document**: Update STATUS.md with findings
6. **Complete**: Mark done in BACKLOG.md

---

## Project Status

**Feature Completeness**: 70%
- Templates: ✅ 100%
- Documentation: ✅ 95%
- Automation: ⚠️ 50%
- Integrations: ⚠️ 40%
- Business: ❌ 30%

**Next Milestone**: 90% feature completeness by Nov 10

---

## Quick Wins

**Easy (< 1 hour)**:
- Enable daily note auto-population
- Create weekly review LaunchAgent
- Add more example workflows
- Update documentation screenshots

**Medium (2-4 hours)**:
- Test Notion sync end-to-end
- Validate OAuth flows
- Create onboarding checklist
- Record demo video

**Hard (8+ hours)**:
- Simplify installation process
- Build setup wizard GUI
- Test on multiple platforms
- Add AI-powered insights

---

## Success Metrics

**This Week**:
- ✅ Using LifeHub daily
- ✅ Auto-population working
- ✅ Weekly review automated
- ✅ Notion sync tested

**This Month**:
- ✅ MVP scope defined
- ✅ Installation simplified
- ✅ Landing page created
- ✅ Demo video recorded

**This Quarter**:
- ✅ 10 beta users
- ✅ First paying customer
- ✅ $50-100 MRR

---

## Resources

**Obsidian**:
- Docs: https://help.obsidian.md
- Forum: https://forum.obsidian.md
- Discord: https://discord.gg/obsidianmd

**Plugins**:
- Dataview: https://blacksmithgu.github.io/obsidian-dataview/
- Templater: https://silentvoid13.github.io/Templater/

**Integrations**:
- Notion API: https://developers.notion.com/
- Gmail API: https://developers.google.com/gmail
- Calendar API: https://developers.google.com/calendar

**Communities**:
- r/ObsidianMD: https://reddit.com/r/ObsidianMD
- Indie Hackers: https://indiehackers.com
- r/productivity: https://reddit.com/r/productivity

---

## Contact

**Project Owner**: Mike Finneran
**Email**: mike.finneran@gmail.com
**Project Workspace**: ~/.claude/projects/lifehub-2.0/

---

*Print this page for quick reference while developing*
*Last updated: October 27, 2025*
