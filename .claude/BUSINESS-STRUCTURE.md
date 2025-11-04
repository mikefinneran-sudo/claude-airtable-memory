# AeroDyne Business Structure

**Founder**: Mike Finneran
**Email**: mike.finneran@gmail.com

---

## Corporate Hierarchy

```
Mike Finneran (Founder)
│
├── AeroDyne LLC (Parent Holding Company)
│   │
│   ├── WalterSignal (Operating Company #1)
│   │   ├── Products
│   │   │   ├── WalterFetch (Lead generation SaaS)
│   │   │   ├── SpecialAgentStanny (Internal automation)
│   │   │   └── Custom App Development
│   │   │
│   │   ├── Clients
│   │   │   ├── FlyFlat (Client #1) - Luxury travel concierge
│   │   │   └── [Future clients]
│   │   │
│   │   └── Services
│   │       ├── AI Consulting
│   │       ├── Data Enrichment
│   │       └── Content & Marketing
│   │
│   └── [Future Operating Companies]
│
└── Personal (Separate from business)
    ├── Personal projects
    ├── Learning & research
    └── Life management
```

---

## Airtable Database Architecture

### Master Databases

#### 1. AeroDyne Master DB (TO CREATE)
**Purpose**: Parent company oversight, cross-company metrics
**Tables**:
- Operating Companies
- Consolidated Financials
- Strategic Initiatives
- Company-level KPIs

#### 2. WalterSignal DB (EXISTS)
**Base ID**: `app6g0t0wtruwLA5I`
**URL**: https://airtable.com/app6g0t0wtruwLA5I
**Purpose**: WalterSignal operations, projects, clients
**Tables** (10 existing):
- Tasks
- Projects
- Sprints
- Milestones
- Documentation
- Deployments
- Metrics
- Clients (includes FlyFlat)
- Tech Stack Management
- Table 1

#### 3. Mike Personal DB (TO CREATE)
**Purpose**: Personal life, learning, non-business projects
**Tables** (to design):
- Personal Projects
- Learning & Development
- Health & Fitness
- Financial Planning (personal)
- Goals & OKRs
- Notes & Ideas
- Reading List
- Contacts (personal)

---

## Storage Strategy

### Primary Storage: Airtable
**Why**: Single source of truth, structured data, API access, automations

**What goes here**:
- All business data (AeroDyne, WalterSignal, clients)
- Project management (tasks, sprints, milestones)
- Client information
- Metrics & KPIs
- Personal data (separate base)

### Secondary: Apple Notes
**Why**: Quick capture, mobile-friendly, searchable

**What goes here**:
- Quick notes during meetings
- Ideas and brainstorming
- Temporary information
- Daily journal entries
- Reference materials

**Sync strategy**: Weekly export important notes to Airtable

### Tertiary: ObsidianVault (Git)
**Status**: STILL ACTIVE (used Oct 31, 2025)
**Why**: Version-controlled documentation, markdown files, code

**What goes here**:
- Technical documentation
- Code files (WalterFetch, SpecialAgentStanny)
- Research documents
- Strategy documents
- Proposals and pitch decks

**Sync strategy**: Keep for now, gradually migrate to Airtable + Apple Notes

### Development: ~/.claude/
**Why**: Claude Code memory and session management

**What goes here**:
- Session memory (active work)
- Project workspaces
- Working context
- Scripts and automation

**Sync strategy**: Auto-sync to Airtable on save-session

---

## Data Flow

```
Daily Work:
  Apple Notes (quick capture)
    ↓
  Airtable (structured storage)
    ↓
  ~/.claude/ (Claude context)

Development:
  ObsidianVault (code & docs)
    ↓
  GitHub (version control)
    ↓
  Airtable (metadata & status)

Claude Code:
  ~/.claude/SESSION-MEMORY.md (active work)
    ↓
  save-session script
    ↓
  Airtable Tasks table (permanent record)
```

---

## Migration Plan

### Phase 1: Airtable Setup (This Session)
- [x] Document business structure
- [ ] Create AeroDyne Master DB
- [ ] Create Mike Personal DB
- [ ] Link WalterSignal DB to AeroDyne
- [ ] Design Personal DB schema

### Phase 2: Memory Integration (Next)
- [ ] Build Airtable sync for ~/.claude/
- [ ] Auto-create Airtable tasks from session work
- [ ] Sync project status to Airtable
- [ ] Apple Notes → Airtable automation

### Phase 3: ObsidianVault Decision (Week 2)
- [ ] Audit what's actively used in Obsidian
- [ ] Migrate or archive inactive content
- [ ] Decide: Keep or fully deprecate
- [ ] If keep: Define clear use cases

---

## Business Entity Details

### AeroDyne LLC
**Type**: Limited Liability Company
**Jurisdiction**: [TBD - check formation docs]
**Purpose**: Holding company for operating businesses
**Structure**: Single-member LLC (Mike Finneran)
**Files Location**: `~/Library/CloudStorage/GoogleDrive-mike.finneran@gmail.com/My Drive/Documents/Business/AeroDyne_LLC`

### WalterSignal
**Type**: Operating company / DBA under AeroDyne
**Status**: Stealth mode, MVP development
**Primary Revenue**: B2B SaaS (WalterFetch)
**Target Market**: Private Equity firms (Tier 2-3)
**Current MRR**: $0 (pre-revenue)
**Goal Q1 2026**: $3,000 MRR (3 pilot customers @ $999/mo)

### FlyFlat (Client)
**Type**: Client of WalterSignal
**Industry**: Luxury travel concierge
**Relationship**: First client, pilot customer
**Services Provided**: [TBD - define scope]

---

## Key Principles

### 1. Airtable = Source of Truth
- All important data must be in Airtable
- Other systems sync TO Airtable, not FROM
- Airtable is backup-safe (cloud provider)

### 2. Separation of Concerns
- **AeroDyne DB**: Company-level, high-level strategy
- **WalterSignal DB**: Operations, projects, clients
- **Personal DB**: Completely separate from business

### 3. Data Sovereignty
- Business data owned by AeroDyne LLC
- Personal data owned by Mike Finneran
- Clear boundaries, no mixing

### 4. API-First
- Everything accessible via Airtable API
- Enables automation (Zapier, n8n, custom scripts)
- Claude Code can read/write directly

---

## Security & Access

### Airtable API Tokens
**Current issue**: Token exposed in code files
**Fix needed**: Move to 1Password immediately

**Token storage** (should be):
- `op://API_Keys/Airtable AeroDyne/credential` (master)
- `op://API_Keys/Airtable WalterSignal/credential` (operating)
- `op://API_Keys/Airtable Personal/credential` (personal)

### Access Control
- **Mike Finneran**: Full access to all bases
- **Future employees**: Role-based access per base
- **Automations**: Service accounts with limited scope

---

## Next Actions

### Immediate (This Session)
1. Create AeroDyne Master DB in Airtable
2. Create Mike Personal DB in Airtable
3. Move API tokens to 1Password
4. Update memory system to sync with Airtable

### This Week
1. Define Personal DB schema with Mike
2. Migrate critical data to Airtable
3. Build Apple Notes → Airtable sync
4. Test memory system → Airtable integration

### This Month
1. Audit ObsidianVault usage
2. Decision: Keep or deprecate Obsidian
3. Full data migration plan
4. Establish weekly review process

---

**Created**: 2025-11-01
**Owner**: Mike Finneran
**Review**: Weekly until structure stabilizes
