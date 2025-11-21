# LifeHub 2.0 - Development Backlog

**Last Updated**: October 27, 2025
**Project**: LifeHub 2.0
**Owner**: Mike Finneran

---

## Backlog Organization

### Priority Levels
- **P0** (Critical): Blocks launch, must do
- **P1** (High): Important for quality, should do
- **P2** (Medium): Nice to have, could do
- **P3** (Low): Future enhancement, might do

### Status Labels
- **Todo**: Not started
- **In Progress**: Currently working
- **Blocked**: Can't proceed yet
- **Done**: Completed
- **Won't Do**: Decided against

---

## P0: Critical (Must Do Before Launch)

### Dogfooding & Testing

**LIFE-001: Enable Personal Daily Note Auto-population**
- **Status**: Todo
- **Priority**: P0
- **Effort**: 30 minutes
- **Description**: Integrate `update_daily_note.py` into LaunchAgent so daily notes auto-populate with tasks
- **Why Critical**: Can't sell a feature we don't use
- **Tasks**:
  - [ ] Update LaunchAgent plist to call update_daily_note.py after creation
  - [ ] Test it runs at 7 AM tomorrow
  - [ ] Verify tasks populate correctly
  - [ ] Document any issues found
- **Blocked By**: None
- **Blocks**: Personal dogfooding

---

**LIFE-002: Test Notion Sync End-to-End**
- **Status**: Todo
- **Priority**: P0
- **Effort**: 2 hours
- **Description**: Set up Notion workspace and verify bidirectional sync works
- **Why Critical**: It's a major v2.0 feature but completely untested
- **Tasks**:
  - [ ] Create Notion integration and get API key
  - [ ] Set up 2-3 databases (Projects, Daily Notes, Clients)
  - [ ] Run `setup-notion-sync.sh`
  - [ ] Execute `sync_to_notion.py`
  - [ ] Verify data appears in Notion
  - [ ] Test mobile access
  - [ ] Document actual workflow
  - [ ] Fix any bugs found
- **Blocked By**: None
- **Blocks**: Notion feature claims

---

**LIFE-003: Use LifeHub 2.0 for 1 Week**
- **Status**: Todo
- **Priority**: P0
- **Effort**: 1 week
- **Description**: Actually use all features daily to find bugs and UX issues
- **Why Critical**: Dogfooding reveals what documentation misses
- **Tasks**:
  - [ ] Enable all automation
  - [ ] Use enhanced templates for all new content
  - [ ] Check dashboard every morning
  - [ ] Run weekly review on Sunday
  - [ ] Track issues in a log
  - [ ] Measure actual time savings
  - [ ] Document workflow patterns
- **Blocked By**: LIFE-001
- **Blocks**: Launch confidence

---

### Essential Features

**LIFE-004: Create Weekly Review Automation**
- **Status**: Todo
- **Priority**: P0
- **Effort**: 1 hour
- **Description**: Create LaunchAgent to auto-create weekly reviews on Sundays
- **Why Critical**: It's documented as a feature but doesn't exist
- **Tasks**:
  - [ ] Write `create_weekly_review.sh` script
  - [ ] Create LaunchAgent plist for Sunday 6 PM
  - [ ] Test template auto-fills correctly
  - [ ] Document usage
- **Blocked By**: None
- **Blocks**: Feature parity with documentation

---

**LIFE-005: Simplify Installation Process**
- **Status**: Todo
- **Priority**: P0
- **Effort**: 3 hours
- **Description**: Create one-command installer that handles everything
- **Why Critical**: Complex setup = low adoption
- **Tasks**:
  - [ ] Write master `install.sh` script
  - [ ] Auto-detect Python 3 or install
  - [ ] Auto-create folders
  - [ ] Auto-copy templates
  - [ ] Auto-configure plugins
  - [ ] Auto-create LaunchAgents
  - [ ] Test on clean macOS
  - [ ] Create uninstall script
- **Blocked By**: None
- **Blocks**: Customer onboarding

---

## P1: High Priority (Should Do Soon)

### Business & Marketing

**LIFE-006: Create Landing Page**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 4 hours
- **Description**: Simple, conversion-focused landing page
- **Components**:
  - [ ] Headline and value proposition
  - [ ] 3-5 key benefits
  - [ ] Screenshots/GIFs
  - [ ] Pricing table
  - [ ] Email capture form
  - [ ] FAQ section
  - [ ] Download/purchase button
- **Tools**: Carrd, Webflow, or simple HTML
- **Blocked By**: LIFE-003 (need real screenshots)
- **Blocks**: Customer acquisition

---

**LIFE-007: Record Demo Video**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 3 hours
- **Description**: 5-10 minute walkthrough showing real usage
- **Outline**:
  - [ ] Write script
  - [ ] Record screen with real workflow
  - [ ] Show morning routine (2 min)
  - [ ] Show project creation (2 min)
  - [ ] Show dashboard updates (2 min)
  - [ ] Show weekly review (2 min)
  - [ ] Show mobile access (2 min)
  - [ ] Edit and add captions
  - [ ] Upload to YouTube
- **Tools**: Loom, ScreenFlow, or QuickTime
- **Blocked By**: LIFE-003 (need actual usage)
- **Blocks**: Marketing effectiveness

---

**LIFE-008: Define MVP Feature Set**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Decide what's essential vs what can wait
- **Questions**:
  - [ ] Is Gmail sync required for MVP?
  - [ ] Is Calendar sync required for MVP?
  - [ ] Is Notion sync required or nice-to-have?
  - [ ] What's the minimum viable automation?
  - [ ] What documentation is essential?
- **Output**: Clear feature list for v2.0 launch
- **Blocked By**: LIFE-003 (dogfooding reveals what's important)
- **Blocks**: Focused development

---

### Testing & Validation

**LIFE-009: Test Installation on Clean macOS**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Verify installation works on fresh Mac
- **Tasks**:
  - [ ] Set up VM or test Mac
  - [ ] Run installer from scratch
  - [ ] Follow documentation step-by-step
  - [ ] Note any confusing steps
  - [ ] Document actual time to install
  - [ ] Verify all features work
  - [ ] Fix any issues found
- **Blocked By**: LIFE-005 (installer)
- **Blocks**: Customer success

---

**LIFE-010: Validate Windows WSL Installation**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 3 hours
- **Description**: Ensure LifeHub works on Windows via WSL
- **Tasks**:
  - [ ] Test on Windows 11 WSL2
  - [ ] Document required setup
  - [ ] Test all automation scripts
  - [ ] Verify LaunchAgent alternatives (cron)
  - [ ] Update documentation for Windows
- **Blocked By**: LIFE-005
- **Blocks**: Windows customer support

---

**LIFE-011: Test OAuth Flows**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: Validate Gmail and Calendar OAuth setup works
- **Tasks**:
  - [ ] Run Gmail OAuth wizard
  - [ ] Document actual steps required
  - [ ] Test token refresh works
  - [ ] Run Calendar OAuth wizard
  - [ ] Test sync works
  - [ ] Document any issues
  - [ ] Simplify if too complex
- **Blocked By**: None (can do independently)
- **Blocks**: Integration features

---

### Documentation

**LIFE-012: Create Customer Onboarding Checklist**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 1 hour
- **Description**: Step-by-step checklist for new customers
- **Format**: Simple markdown checklist
- **Sections**:
  - [ ] Pre-installation requirements
  - [ ] Installation steps
  - [ ] Initial configuration
  - [ ] First daily note
  - [ ] First project
  - [ ] First weekly review
  - [ ] Customization options
  - [ ] Getting help
- **Blocked By**: LIFE-003 (dogfooding), LIFE-009 (clean install)
- **Blocks**: Customer success

---

**LIFE-013: Create Support Documentation**
- **Status**: Todo
- **Priority**: P1
- **Effort**: 2 hours
- **Description**: How to help customers who have issues
- **Sections**:
  - [ ] Common issues and fixes
  - [ ] How to report bugs
  - [ ] How to request features
  - [ ] Community resources
  - [ ] Contact information
  - [ ] Response time expectations
- **Blocked By**: LIFE-003 (real issues)
- **Blocks**: Launch confidence

---

## P2: Medium Priority (Nice to Have)

### Automation Enhancements

**LIFE-014: Auto-backup Before Sync**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 1 hour
- **Description**: Automatically backup vault before running syncs
- **Why**: Safety net for sync operations
- **Tasks**:
  - [ ] Write backup script
  - [ ] Integrate into sync scripts
  - [ ] Test restore process
  - [ ] Document backup location

---

**LIFE-015: Better Error Handling in Python Scripts**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 2 hours
- **Description**: Improve error messages and logging
- **Tasks**:
  - [ ] Add try/catch blocks
  - [ ] Log to dedicated files
  - [ ] Show user-friendly error messages
  - [ ] Add debug mode flag

---

**LIFE-016: Create Setup Wizard GUI**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 8 hours
- **Description**: Graphical setup instead of command line
- **Why**: Easier for non-technical users
- **Tools**: Electron, Python TKinter, or web-based
- **Scope**: Consider vs complexity trade-off

---

### Feature Additions

**LIFE-017: Add Email/Slack Notifications**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 3 hours
- **Description**: Send notifications for important events
- **Events**:
  - [ ] Daily note created
  - [ ] Weekly review due
  - [ ] Project deadline approaching
  - [ ] High-priority task due today
- **Delivery**: Email or Slack webhook

---

**LIFE-018: Build Time Tracking Integration**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 4 hours
- **Description**: Integrate with Toggl or RescueTime
- **Why**: Better insights into actual time spent
- **Tasks**:
  - [ ] Research APIs
  - [ ] Build sync script
  - [ ] Add to daily notes
  - [ ] Create time reports

---

**LIFE-019: Add AI-Powered Insights**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 8 hours
- **Description**: Use Claude API to analyze patterns and suggest improvements
- **Features**:
  - [ ] Analyze task completion patterns
  - [ ] Suggest priority adjustments
  - [ ] Identify bottlenecks
  - [ ] Generate weekly insights
- **Cost**: Claude API usage

---

### Platform Expansion

**LIFE-020: Test Linux Installation**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 2 hours
- **Description**: Ensure works on Ubuntu/Debian
- **Tasks**:
  - [ ] Test on Ubuntu 22.04
  - [ ] Test on Debian 11
  - [ ] Document any issues
  - [ ] Update installer for Linux

---

**LIFE-021: Create iOS Shortcuts Integration**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 4 hours
- **Description**: Alternative to Notion for mobile quick capture
- **Features**:
  - [ ] Quick task capture
  - [ ] Voice note to daily note
  - [ ] Check today's priorities
  - [ ] Update project status
- **Delivery**: Share via RoutineHub

---

### Distribution

**LIFE-022: Create Gumroad Product Listing**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 1 hour
- **Description**: Set up payment processing
- **Tasks**:
  - [ ] Create Gumroad account
  - [ ] Upload product
  - [ ] Set pricing
  - [ ] Write product description
  - [ ] Add screenshots
  - [ ] Link demo video
- **Blocked By**: LIFE-006, LIFE-007

---

**LIFE-023: Build Community Discord/Forum**
- **Status**: Todo
- **Priority**: P2
- **Effort**: 2 hours
- **Description**: Place for users to help each other
- **Platform**: Discord or Circle
- **Sections**:
  - [ ] Announcements
  - [ ] General discussion
  - [ ] Feature requests
  - [ ] Troubleshooting
  - [ ] Showcase (user setups)

---

## P3: Low Priority (Future)

### Advanced Features

**LIFE-024: Team Collaboration Features**
- **Status**: Won't Do (for now)
- **Priority**: P3
- **Description**: Multi-user workspace features
- **Why Later**: Focus on individual users first

---

**LIFE-025: White Label Version**
- **Status**: Won't Do (for now)
- **Priority**: P3
- **Description**: Let agencies brand and resell
- **Why Later**: Complexity vs revenue potential unknown

---

**LIFE-026: Native Mobile Apps**
- **Status**: Won't Do (for now)
- **Priority**: P3
- **Description**: iOS and Android native apps
- **Why Later**: Notion provides mobile access, native apps are expensive

---

**LIFE-027: AWS Lambda Migration**
- **Status**: Blocked
- **Priority**: P3
- **Description**: Move automation to cloud (Phase 3)
- **Why Later**: Not needed until 200+ customers
- **Blocked By**: Phase 1 and 2 completion

---

## Completed Items

### Done

**LIFE-000: Create Enhanced Templates**
- **Status**: Done (Oct 20, 2025)
- **Effort**: 4 hours
- **Notes**: Daily, Project, Client, Weekly Review all enhanced with Dataview and Templater

**LIFE-000: Build Auto-updating Dashboard**
- **Status**: Done (Oct 20, 2025)
- **Effort**: 2 hours
- **Notes**: Fully functional with dynamic queries

**LIFE-000: Write Comprehensive Documentation**
- **Status**: Done (Oct 20, 2025)
- **Effort**: 6 hours
- **Notes**: Guides, FAQs, summaries all created

**LIFE-000: Create Distribution Packages**
- **Status**: Done (Oct 21, 2025)
- **Effort**: 3 hours
- **Notes**: Pro Templates and Automation Suite packaged

---

## Sprint Planning

### This Week (Oct 27 - Nov 3)
**Goal**: Enable personal automation and test core features

Priority tasks:
1. LIFE-001: Enable daily note auto-population
2. LIFE-004: Create weekly review automation
3. LIFE-003: Use LifeHub for 1 week
4. LIFE-002: Test Notion sync

**Success**: Using 90%+ of LifeHub features daily

---

### Next Sprint (Nov 4 - Nov 10)
**Goal**: Validate MVP and prepare for launch

Priority tasks:
1. LIFE-008: Define MVP feature set
2. LIFE-005: Simplify installation
3. LIFE-009: Test on clean Mac
4. LIFE-012: Create onboarding checklist

**Success**: Clear MVP scope, installation tested

---

### Sprint 3 (Nov 11 - Nov 17)
**Goal**: Create marketing materials

Priority tasks:
1. LIFE-006: Create landing page
2. LIFE-007: Record demo video
3. LIFE-013: Create support docs
4. LIFE-022: Set up Gumroad

**Success**: Ready to acquire first customer

---

## Notes & Context

### Decision Log

**2025-10-27**: Created backlog structure
- Prioritized dogfooding over new features
- Focused on validation over expansion
- De-prioritized Phase 3 (cloud) features

### Open Questions

1. **Gmail/Calendar sync**: Essential or optional for MVP?
   - **Context**: Built but untested, may be complex for users
   - **Decision needed by**: After dogfooding (LIFE-003)

2. **Notion sync**: Core feature or premium add-on?
   - **Context**: Major v2.0 feature but adds complexity
   - **Decision needed by**: After testing (LIFE-002)

3. **Pricing**: Stick with $3/$10/$20 or adjust?
   - **Context**: No market validation yet
   - **Decision needed by**: Before launch

4. **Support**: How much can one person handle?
   - **Context**: Solo founder, limited time
   - **Decision needed by**: Before first customer

### Dependencies

```
LIFE-001 → LIFE-003 → LIFE-008
    ↓         ↓         ↓
LIFE-004   LIFE-006  LIFE-005
    ↓         ↓         ↓
LIFE-002   LIFE-007  LIFE-009
                ↓         ↓
            LIFE-022  LIFE-012
                        ↓
                    Launch
```

---

## Backlog Management

**How to use this backlog**:
1. Review weekly to adjust priorities
2. Move items to STATUS.md when started
3. Add new items as they're discovered
4. Archive completed items
5. Re-evaluate P2/P3 items monthly

**Sources of new items**:
- Dogfooding discoveries
- Customer feedback (when we have customers)
- Technical debt
- Market opportunities
- Competitive analysis

---

*Backlog maintained in: `/Users/mikefinneran/.claude/projects/lifehub-2.0/BACKLOG.md`*
*Last reviewed: October 27, 2025*
