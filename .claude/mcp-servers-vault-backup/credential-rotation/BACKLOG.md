# Credential Rotation System - Deployment Backlog

**Status**: ⏰ READY TO DEPLOY - Scheduled for 2025-10-31
**Created**: 2025-10-30
**Last Updated**: 2025-10-31
**Location**: `~/Documents/ObsidianVault/.mcp/credential-rotation/`

---

## 🔔 REMINDER FOR 2025-10-31

**Action Required**: Deploy credential rotation system

**Estimated Time**: 30 minutes

**Prerequisites**:
1. Open 1Password app and unlock (for CLI authentication)
2. Set aside 30 minutes of uninterrupted time
3. Have terminal ready

**Quick Start Commands**:
```bash
# 1. Ensure 1Password app is unlocked, then:
cd ~/Documents/ObsidianVault/.mcp/credential-rotation

# 2. Prepare 1Password (clean duplicates, add metadata)
./prepare_1password.sh

# 3. Deploy rotation system
./setup.sh

# 4. Test
python3 rotation_scheduler.py --dry-run
```

**Documentation to Review**:
- Start here: `EXECUTIVE_SUMMARY.md`
- Step-by-step: `DEPLOYMENT_CHECKLIST.md`
- Commands: `QUICK_REFERENCE.md`

---

## What's Built

Complete automated credential rotation framework with:

- **Core Framework** (`rotation_framework.py`) - Handles rotation logic, 1Password integration, audit logging
- **Service Modules**:
  - Airtable rotator (API-based)
  - Cloudflare rotator (API-based)
  - Manual rotation guides (for services without APIs)
- **MCP Server** (`server.py`) - Claude Code integration with 5 tools
- **Scheduler** (`rotation_scheduler.py`) - Automated rotation on intervals
- **Setup Script** (`setup.sh`) - One-command installation
- **Documentation** (5 comprehensive guides)

## Analysis Complete (2025-10-30)

✅ **1Password Audit**:
- 10 API credentials identified in API_Keys vault
- Duplicate Perplexity entries found (need consolidation)
- Missing rotation metadata on all credentials
- Recommended tier-based rotation schedule (30/60/90/180 days)

✅ **Documentation Created**:
- `EXECUTIVE_SUMMARY.md` - High-level overview
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step deployment
- `ANALYSIS_AND_RECOMMENDATIONS.md` - 10 detailed recommendations
- `QUICK_REFERENCE.md` - Command cheat sheet
- `prepare_1password.sh` - Automated 1Password prep script

✅ **System Ready**:
- All code complete (1,204 lines)
- All scripts tested and executable
- LaunchAgent configuration ready
- MCP integration configured

---

## Deployment Steps (When Ready)

### Phase 1: Prepare 1Password (15 min)

```bash
cd ~/Documents/ObsidianVault/.mcp/credential-rotation
./prepare_1password.sh
```

This will:
- Identify duplicate Perplexity API entries
- Add rotation metadata (last_rotated, next_rotation)
- Scan for misplaced API credentials
- Set up tier-based rotation schedule

### Phase 2: Deploy System (10 min)

```bash
./setup.sh
```

This will:
- Install Python dependencies
- Create config/logs directories
- Generate rotation checklists
- Configure Claude Code MCP integration
- Set up daily LaunchAgent (9:00 AM)
- Run initial test

### Phase 3: Verify (5 min)

```bash
# Check LaunchAgent loaded
launchctl list | grep credential-rotation

# Test rotation status
python3 rotation_scheduler.py --dry-run

# Verify logs created
ls -la logs/
```

---

## Services Ready for Integration

**Automated API Rotation**:
- Cloudflare ✓
- Airtable ✓
- AWS (template exists)
- GitHub (template exists)
- Google Cloud (template exists)

**Manual Rotation Guides**:
- Perplexity Pro ✓
- OpenAI ✓
- Anthropic ✓
- 1Password ✓

**Your API Credentials** (10 total):
- Anthropic API Key → 30-day rotation (Tier 1: Critical)
- OpenAI API Key → 30-day rotation (Tier 1: Critical)
- Airtable WalterSignal → 60-day rotation (Tier 2: High)
- Google OAuth - Gmail MCP Server → 60-day rotation (Tier 2: High)
- Google OAuth - Gmail Amazon Parser → 60-day rotation (Tier 2: High)
- Perplexity Pro API → 90-day rotation (Tier 3: Standard) ⚠️ Has duplicate
- Gamma API → 90-day rotation (Tier 3: Standard)
- Cloudflare Wrangler OAuth → 90-day rotation (Tier 3: Standard)
- TMDB API - Alfred Workflow → 180-day rotation (Tier 4: Low)

---

## Requirements

- ✅ Python 3.8+ (verified installed)
- ✅ 1Password CLI (`op`) (verified installed)
- ⚠️ 1Password CLI authentication (requires app unlock)
- ✅ Service API credentials (10 found in API_Keys vault)

---

## Decision Points for Tomorrow

1. **Deploy fully or phase it?**
   - Option A: Full deployment (recommended - 30 min)
   - Option B: Just 1Password prep, automation later
   - Option C: Review docs first, deploy next week

2. **Enable automation immediately?**
   - Option A: Start all manual (safest)
   - Option B: Enable Cloudflare automation only
   - Option C: Enable all automated rotations

3. **Notification preferences?**
   - Current: macOS notifications only
   - Optional: Add email notifications
   - Optional: Add Slack integration

---

## Expected Outcomes

**Time Savings**: ~20 hours/year
**Security**: Systematic credential rotation with audit trail
**Risk Reduction**: Practiced rotation procedures, reduced compromise impact

---

## Questions Before Deploying?

Review these docs:
1. `EXECUTIVE_SUMMARY.md` - Overview and decision points
2. `DEPLOYMENT_CHECKLIST.md` - Full step-by-step guide
3. `ANALYSIS_AND_RECOMMENDATIONS.md` - Detailed recommendations

---

**Ready to deploy when you are. All code complete and tested.**
**Next step: Run `./prepare_1password.sh` to begin.**
