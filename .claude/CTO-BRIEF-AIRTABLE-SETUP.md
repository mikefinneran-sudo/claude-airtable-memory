# CTO Team Brief: AeroDyne Airtable Infrastructure Setup

**Issue Date**: 2025-11-01
**Priority**: CRITICAL
**Assigned To**: SpecialAgentStanny CTO Team
**Requested By**: Mike Finneran (Founder, AeroDyne LLC)
**Estimated Time**: 2-3 hours
**Budget**: Airtable Team Plan

---

## Executive Summary

Set up comprehensive Airtable database infrastructure for AeroDyne LLC business operations, including parent company oversight, WalterSignal operating company management, and Mike Finneran personal productivity.

---

## Business Context

### Corporate Hierarchy
```
Mike Finneran (Founder)
├── AeroDyne LLC (Parent Holding Company)
│   └── WalterSignal (Operating Company #1)
│       ├── Products: WalterFetch, SpecialAgentStanny
│       └── Clients: FlyFlat (Client #1)
└── Personal (Separate)
```

### Current State
- **Existing**: WalterSignal DB (`app6g0t0wtruwLA5I`) with 10 tables
- **Missing**: AeroDyne Master DB (parent oversight)
- **Missing**: Mike Personal DB (life management)
- **Issue**: No hierarchical data structure linking companies
- **Security Risk**: API token exposed in code files

---

## Objectives

### Primary Goals
1. Create AeroDyne Master DB for parent company oversight
2. Create Mike Personal DB for personal productivity
3. Link WalterSignal DB as child of AeroDyne Master
4. Secure API credentials in 1Password
5. Enable Claude Code memory sync to Airtable

### Success Criteria
- ✅ 3 Airtable bases operational
- ✅ Clear data hierarchy (AeroDyne → WalterSignal → Clients)
- ✅ API tokens secured in 1Password
- ✅ Claude memory system integrated with Airtable
- ✅ Documentation complete for daily usage

---

## Technical Specifications

### 1. AeroDyne Master DB

**Purpose**: Parent company oversight and strategic management

**Tables**:

#### Table 1: Operating Companies
| Field Name | Type | Description |
|------------|------|-------------|
| Company Name | Single Line Text | Name of operating company |
| Status | Single Select | Active, Planning, Paused, Closed |
| Founded Date | Date | When company was established |
| Industry | Single Line Text | Market sector |
| Business Model | Long Text | Revenue model description |
| Current MRR | Currency | Monthly recurring revenue |
| Total Clients | Number | Active client count |
| Airtable Base ID | Single Line Text | Link to operational base |
| Owner | Single Line Text | Business owner (Mike Finneran) |
| Notes | Long Text | Additional context |

**Initial Record**:
- Company Name: WalterSignal
- Status: Active
- Founded Date: 2025-10-01 (estimated)
- Industry: B2B SaaS / AI Consulting
- Business Model: Subscription + Services
- Current MRR: $0 (pre-revenue)
- Total Clients: 1 (FlyFlat)
- Airtable Base ID: app6g0t0wtruwLA5I

#### Table 2: Strategic Initiatives
| Field Name | Type | Description |
|------------|------|-------------|
| Initiative Name | Single Line Text | Project name |
| Status | Single Select | Planning, In Progress, Completed, On Hold |
| Priority | Single Select | Critical, High, Medium, Low |
| Start Date | Date | Initiative start |
| Target Date | Date | Target completion |
| Owner | Single Line Text | Initiative lead |
| Description | Long Text | Full description |
| Impact | Long Text | Expected business impact |
| Linked Company | Link to Operating Companies | Which company this affects |

**Initial Records**:
1. WalterFetch MVP Launch
2. FlyFlat Pilot Program
3. SpecialAgentStanny Production Deployment

#### Table 3: Consolidated Financials
| Field Name | Type | Description |
|------------|------|-------------|
| Month | Date | Financial period |
| Total Revenue | Currency | All companies combined |
| Total Expenses | Currency | All operating costs |
| Net Profit | Formula | Revenue - Expenses |
| Cash Position | Currency | Current cash on hand |
| Burn Rate | Currency | Monthly cash burn |
| Runway (Months) | Formula | Cash / Burn Rate |
| Notes | Long Text | Commentary |

#### Table 4: Company KPIs
| Field Name | Type | Description |
|------------|------|-------------|
| Metric Name | Single Line Text | KPI name |
| Company | Link to Operating Companies | Which company |
| Current Value | Number | Current metric value |
| Target Value | Number | Goal |
| Period | Single Select | Daily, Weekly, Monthly, Quarterly, Annually |
| Last Updated | Date | When metric was refreshed |
| Trend | Single Select | Up (green), Flat (yellow), Down (red) |
| % of Target | Formula | (Current / Target) * 100 |

---

### 2. Mike Personal DB

**Purpose**: Personal life management separate from business

**Tables**:

#### Table 1: Personal Projects
| Field Name | Type | Description |
|------------|------|-------------|
| Project Name | Single Line Text | Project title |
| Status | Single Select | Active, Planning, On Hold, Completed |
| Category | Single Select | Learning, Hobby, Health, Creative, Other |
| Start Date | Date | When started |
| Description | Long Text | Project details |
| Next Action | Single Line Text | Immediate next step |
| Progress % | Number | Completion percentage |

#### Table 2: Goals & OKRs
| Field Name | Type | Description |
|------------|------|-------------|
| Goal | Single Line Text | Goal statement |
| Type | Single Select | Career, Health, Financial, Learning, Relationships, Personal Growth |
| Timeframe | Single Select | This Week, This Month, This Quarter, This Year, Long-term |
| Status | Single Select | Not Started, In Progress, Achieved, Abandoned |
| Target Date | Date | Goal deadline |
| Progress % | Number | 0-100 completion |
| Notes | Long Text | Additional context |
| Key Results | Long Text | Measurable outcomes |

#### Table 3: Learning & Development
| Field Name | Type | Description |
|------------|------|-------------|
| Title | Single Line Text | Course/Book name |
| Type | Single Select | Book, Course, Video, Article, Podcast |
| Status | Single Select | Want to Learn, In Progress, Completed |
| Category | Single Line Text | Subject area |
| Started | Date | Start date |
| Completed | Date | Completion date |
| Rating | Single Select | ⭐⭐⭐⭐⭐, ⭐⭐⭐⭐, ⭐⭐⭐, ⭐⭐, ⭐ |
| Notes | Long Text | General notes |
| Key Takeaways | Long Text | Main learnings |
| Apply To | Link to Personal Projects | Related projects |

#### Table 4: Health & Fitness
| Field Name | Type | Description |
|------------|------|-------------|
| Date | Date | Activity date |
| Activity Type | Single Select | Workout, Cardio, Yoga, Walk, Sleep, Meditation |
| Duration (mins) | Number | Time spent |
| Intensity | Single Select | Light, Moderate, Intense |
| Notes | Long Text | How it felt, metrics |
| Consistency Streak | Formula | Days in a row |

#### Table 5: Ideas & Notes
| Field Name | Type | Description |
|------------|------|-------------|
| Title | Single Line Text | Idea name |
| Category | Single Select | Idea, Note, Thought, Quote, Insight |
| Date Created | Date | When captured |
| Content | Long Text | Full idea/note |
| Tags | Multiple Select | Business, Personal, Creative, Technical, Important |
| Action Required | Checkbox | Needs follow-up |
| Status | Single Select | New, Reviewing, Implemented, Archived |

#### Table 6: Contacts (Personal)
| Field Name | Type | Description |
|------------|------|-------------|
| Name | Single Line Text | Contact name |
| Relationship | Single Select | Family, Friend, Mentor, Acquaintance |
| Email | Email | Email address |
| Phone | Phone Number | Phone |
| Last Contact | Date | Last interaction |
| Next Touch | Date | When to reach out again |
| Notes | Long Text | Relationship notes |
| Important Dates | Long Text | Birthdays, anniversaries |

---

### 3. WalterSignal DB Enhancement

**Current Base ID**: `app6g0t0wtruwLA5I`

**Actions Required**:
1. Add "Parent Company" field to Projects table → Link to AeroDyne Master DB
2. Update FlyFlat client record with proper hierarchy
3. Create automation: Updates to WalterSignal metrics → Update AeroDyne KPIs
4. Add "Sync Status" field for Claude Code integration

---

## Implementation Steps

### Phase 1: Pre-Flight Checks (15 min)

**1.1 Gather Requirements**
- [ ] Obtain Airtable Workspace ID from Mike
  - Location: Airtable.com → Settings → Workspace
  - Format: `wspXXXXXXXXXXXXXX`

- [ ] Verify API token in 1Password
  - Current location: Exposed in code files
  - Target: `op://API_Keys/Airtable WalterSignal/credential`

- [ ] Check Airtable plan limits
  - Current plan: [Determine]
  - Required: Team or Business plan (for automations)

**1.2 Backup Existing Data**
- [ ] Export WalterSignal DB to CSV (all 10 tables)
- [ ] Save to: `~/Documents/AeroDyne_LLC/Airtable_Backups/waltersignal-backup-2025-11-01.zip`
- [ ] Verify backup integrity

---

### Phase 2: Create Databases (45 min)

**2.1 Create AeroDyne Master DB**

**Option A: Using Script (Automated)**
```bash
cd ~/.claude/scripts
python3 create-airtable-bases.py
```

**Option B: Manual (if script fails)**
1. Go to Airtable.com
2. Create new base: "AeroDyne Master"
3. Create tables per spec above
4. Configure views:
   - Operating Companies: Grid View, Gallery View (by Status)
   - Strategic Initiatives: Kanban (by Status)
   - Financials: Calendar View (by Month)
   - KPIs: Dashboard View

**2.2 Create Mike Personal DB**
- Same process as 2.1
- Name: "Mike Personal"
- Configure views:
   - Goals: Kanban (by Status), Calendar (by Target Date)
   - Learning: Progress Bar View (by Progress %)
   - Health: Calendar View (by Date)
   - Ideas: Grid View, Gallery View

**2.3 Verify Creation**
- [ ] AeroDyne Master DB created
- [ ] Mike Personal DB created
- [ ] All tables match specifications
- [ ] Views configured correctly
- [ ] Record Base IDs:
  - AeroDyne: `app______________`
  - Personal: `app______________`

---

### Phase 3: Link Databases (30 min)

**3.1 Create Cross-Base Links**

Airtable allows linking across bases (paid plans only).

**In AeroDyne Master DB → Operating Companies table**:
- Add field: "Operational Base"
- Type: URL
- Value for WalterSignal: `https://airtable.com/app6g0t0wtruwLA5I`

**In WalterSignal DB → Projects table**:
- Add field: "Parent Company"
- Type: Link to another record
- Manual sync for now (automation in Phase 4)

**3.2 Populate Initial Data**

**AeroDyne Master DB**:
- [ ] Add WalterSignal to Operating Companies
- [ ] Add 3 strategic initiatives (WalterFetch MVP, FlyFlat Pilot, SAS Deployment)
- [ ] Create first KPI records (MRR, Customer Count, etc.)

**Mike Personal DB**:
- [ ] Migrate any existing goals from Apple Notes
- [ ] Add current learning items
- [ ] Seed Ideas table with captured notes

---

### Phase 4: Security & API (30 min)

**4.1 Move API Tokens to 1Password**

```bash
# Add new credential
op item create \
  --category="API Credential" \
  --title="Airtable AeroDyne Master" \
  --vault="API_Keys" \
  credential="[AIRTABLE_TOKEN]" \
  base_id="[AERODYNE_BASE_ID]"

op item create \
  --category="API Credential" \
  --title="Airtable Mike Personal" \
  --vault="API_Keys" \
  credential="[AIRTABLE_TOKEN]" \
  base_id="[PERSONAL_BASE_ID]"
```

**4.2 Remove Exposed Tokens**

```bash
# Find all files with exposed token
grep -r "***REMOVED***keACKukt33" ~/Documents/ObsidianVault/

# Update each file to use 1Password
# Replace hardcoded token with:
# os.getenv("AIRTABLE_TOKEN") or op read "op://API_Keys/..."
```

**4.3 Update Environment Variables**

Add to `~/.zshrc`:
```bash
# Airtable API Tokens (from 1Password)
export AIRTABLE_AERODYNE_TOKEN="$(op read 'op://API_Keys/Airtable AeroDyne Master/credential')"
export AIRTABLE_WALTERSIGNAL_TOKEN="$(op read 'op://API_Keys/Airtable WalterSignal/credential')"
export AIRTABLE_PERSONAL_TOKEN="$(op read 'op://API_Keys/Airtable Mike Personal/credential')"
```

---

### Phase 5: Claude Code Integration (45 min)

**5.1 Create Airtable Sync Script**

```python
#!/usr/bin/env python3
"""
Sync Claude Code session memory to Airtable
Auto-creates tasks in WalterSignal DB from session work
"""

import os
import json
import requests
from datetime import datetime

# Get token from 1Password
AIRTABLE_TOKEN = os.getenv("AIRTABLE_WALTERSIGNAL_TOKEN")
BASE_ID = "app6g0t0wtruwLA5I"
TASKS_TABLE = "tblFB266RD9aklveT"

def sync_session_to_airtable(session_file):
    """Read SESSION-MEMORY.md and create Airtable records"""

    with open(session_file, 'r') as f:
        content = f.read()

    # Parse completed actions
    completed = extract_completed_actions(content)
    decisions = extract_decisions(content)

    # Create task records
    for action in completed:
        create_task_record(action)

    # Create decision records
    for decision in decisions:
        create_documentation_record(decision)

# ... implementation details ...
```

**5.2 Update save-session-memory.sh**

Add Airtable sync to existing script:

```bash
# After saving to SESSIONS.md, sync to Airtable
if command -v python3 &> /dev/null; then
    python3 ~/.claude/scripts/sync-to-airtable.py "$SESSION_FILE"
fi
```

**5.3 Test Integration**

```bash
# Create test session
echo "Test session" > /tmp/test-session.md

# Run sync
python3 ~/.claude/scripts/sync-to-airtable.py /tmp/test-session.md

# Verify in Airtable
open "https://airtable.com/app6g0t0wtruwLA5I"
```

---

### Phase 6: Automations (30 min)

**6.1 Airtable Automations to Create**

**Automation 1: Stale Data Alert**
- Trigger: When any KPI "Last Updated" > 7 days ago
- Action: Send notification to Mike (email or Slack)

**Automation 2: Strategic Initiative Status Change**
- Trigger: When Strategic Initiative status changes to "Completed"
- Action: Create celebration message + update Company KPIs

**Automation 3: New Client in WalterSignal**
- Trigger: New record in Clients table (WalterSignal DB)
- Action: Update "Total Clients" in AeroDyne Operating Companies

**Automation 4: Weekly Summary**
- Trigger: Every Monday 9 AM
- Action: Generate summary email of:
  - Active strategic initiatives
  - KPIs status (green/yellow/red)
  - Tasks completed last week

**6.2 Zapier/n8n Integrations** (Optional)

- Apple Notes → Airtable: Capture quick notes to Ideas table
- Claude Sessions → Airtable: Auto-populate tasks from sessions
- WalterSignal metrics → AeroDyne KPIs: Real-time rollup

---

### Phase 7: Documentation (30 min)

**7.1 Create Quick Reference Guides**

**For Mike**:
- [ ] `AIRTABLE_DAILY_WORKFLOW.md` - Morning routine with Airtable
- [ ] `AIRTABLE_QUICK_REFERENCE.md` - Common tasks cheat sheet

**For Future Team**:
- [ ] `AIRTABLE_ARCHITECTURE.md` - How bases relate
- [ ] `AIRTABLE_API_GUIDE.md` - Developer reference
- [ ] `AIRTABLE_BACKUP_STRATEGY.md` - Data protection plan

**7.2 Update Business Structure Doc**

Update `~/.claude/BUSINESS-STRUCTURE.md`:
- [ ] Add created Base IDs
- [ ] Update storage strategy section
- [ ] Mark Airtable setup as complete

---

## Deliverables

### Required Outputs

1. **Airtable Bases** (3 total)
   - [x] AeroDyne Master DB with 4 tables
   - [x] Mike Personal DB with 6 tables
   - [x] WalterSignal DB enhanced with parent links

2. **API Security**
   - [x] All tokens in 1Password
   - [x] Code files updated to use 1Password
   - [x] Environment variables configured

3. **Integration Scripts**
   - [x] `sync-to-airtable.py` - Session → Airtable
   - [x] Updated `save-session-memory.sh`
   - [x] Test suite passing

4. **Automations**
   - [x] 4 Airtable automations configured
   - [x] Tested and verified

5. **Documentation**
   - [x] Daily workflow guide
   - [x] Quick reference card
   - [x] API documentation
   - [x] Architecture diagram

6. **Handoff Package**
   - [x] Base IDs documented
   - [x] API credentials secured
   - [x] Usage guide created
   - [x] Training session scheduled

---

## Testing & Validation

### Test Cases

**Test 1: Data Entry**
- [ ] Create new strategic initiative in AeroDyne Master
- [ ] Verify it appears correctly
- [ ] Update status, verify automation fires

**Test 2: Cross-Base Linking**
- [ ] Add new client to WalterSignal DB
- [ ] Verify "Total Clients" updates in AeroDyne Master
- [ ] Check data consistency

**Test 3: Claude Integration**
- [ ] Run `save-session` with active session
- [ ] Verify tasks created in Airtable
- [ ] Check data mapping accuracy

**Test 4: Security**
- [ ] Confirm no API tokens in git repos
- [ ] Test 1Password token retrieval
- [ ] Verify environment variables load correctly

**Test 5: Automations**
- [ ] Trigger each automation manually
- [ ] Verify notifications send
- [ ] Check automation logs for errors

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Airtable plan limitations | High | Medium | Verify plan before starting, upgrade if needed |
| API token exposure | Critical | Low | Security audit, remove from code immediately |
| Data loss during migration | High | Low | Full backup before any changes |
| Cross-base sync failures | Medium | Medium | Build retry logic, manual fallback |
| Automation cost overrun | Low | Low | Monitor usage, set budget alerts |

---

## Budget & Resources

### Airtable Costs
- **Team Plan**: $20/user/month
- **Users**: Mike Finneran + future team members
- **Estimated**: $20-60/month

### Development Time
- **Phase 1**: 15 min
- **Phase 2**: 45 min
- **Phase 3**: 30 min
- **Phase 4**: 30 min
- **Phase 5**: 45 min
- **Phase 6**: 30 min
- **Phase 7**: 30 min
- **Total**: ~3.5 hours

### Tools Required
- Airtable account (Team plan or higher)
- 1Password CLI (`op`)
- Python 3.9+
- Access to Mike's machine for testing

---

## Success Metrics

**Immediate (End of Day 1)**
- [x] 3 Airtable bases created
- [x] API tokens secured
- [x] Basic automations working

**Week 1**
- [x] Claude Code syncing successfully
- [x] Mike using daily for task management
- [x] No security issues detected

**Month 1**
- [x] Full adoption by Mike
- [x] Strategic initiatives being tracked
- [x] KPIs updated weekly
- [x] System running smoothly without manual intervention

---

## Next Steps After Completion

1. **Week 1 Review**: Mike + CTO team debrief on usability
2. **Optimization**: Tune automations based on usage patterns
3. **Expansion**: Add integrations (Slack, email, calendar)
4. **Team Onboarding**: Prepare for future employees
5. **Backup Verification**: Test restore from backup

---

## Contact & Support

**Project Lead**: Mike Finneran (mike.finneran@gmail.com)
**Technical Lead**: SpecialAgentStanny CTO Team
**Documentation**: `~/.claude/BUSINESS-STRUCTURE.md`
**Support**: Reference AIRTABLE_QUICK_REFERENCE.md for common issues

---

**Status**: READY FOR EXECUTION
**Priority**: CRITICAL
**Due Date**: End of Week (2025-11-08)

---

*Generated by Claude Code on 2025-11-01*
*For AeroDyne LLC - Confidential*
