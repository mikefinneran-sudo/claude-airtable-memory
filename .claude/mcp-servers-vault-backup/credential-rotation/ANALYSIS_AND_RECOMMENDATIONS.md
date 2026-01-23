# Credential Rotation System - Analysis & Recommendations

**Date**: 2025-10-30
**Status**: Ready for Deployment
**Location**: `~/Documents/ObsidianVault/.mcp/credential-rotation/`

---

## Executive Summary

Your automated credential rotation system is **fully built and ready to deploy**. The framework includes enterprise-grade features like 1Password integration, audit logging, automated scheduling, and Claude Code MCP integration.

**Current State**:
- ✅ Code complete (1,204 lines across 6 files)
- ✅ Documentation comprehensive
- ⚠️  Not yet deployed (setup.sh not run)
- ⚠️  1Password needs authentication

**Next Steps**: Run setup script and configure rotation policies.

---

## 1Password Analysis

### Current Inventory

You have **10 API credentials** stored in a dedicated `API_Keys` vault:

| Credential | Category | Tags | Created | Notes |
|-----------|----------|------|---------|-------|
| **Anthropic API Key** | API_CREDENTIAL | ai, llm, claude | 2025-10-30 | ✅ Well-organized |
| **OpenAI API Key** | API_CREDENTIAL | ai, llm, gpt | 2025-10-30 | ✅ Well-organized |
| **Perplexity API Key** | API_CREDENTIAL | ai, research | 2025-10-30 | ⚠️  Duplicate entry (see below) |
| **Perplexity Pro API** | API_CREDENTIAL | - | 2025-10-30 | ⚠️  Duplicate entry (see below) |
| **Gamma API** | API_CREDENTIAL | - | 2025-10-30 | ✅ Ready for rotation |
| **Airtable WalterSignal** | API_CREDENTIAL | - | 2025-10-30 | ✅ Ready for rotation |
| **Google OAuth - Gmail MCP Server** | API_CREDENTIAL | - | 2025-10-30 | 📋 Manual rotation required |
| **Google OAuth - Gmail Amazon Parser** | API_CREDENTIAL | - | 2025-10-30 | 📋 Manual rotation required |
| **Cloudflare Wrangler OAuth** | API_CREDENTIAL | - | 2025-10-30 | 🤖 Automated rotation ready |
| **TMDB API - Alfred Workflow** | API_CREDENTIAL | - | 2025-10-30 | ✅ Ready for rotation |

### Additional Vaults

- **Private**: 367 items (Personal credentials, likely needs organization)
- **Mike and Ashley**: 16 items (Shared accounts)
- **Shared**: 11 items (Shared with others)

---

## Issues Identified

### 1. Duplicate Perplexity Entries

**Problem**: You have two Perplexity API entries:
- `Perplexity API Key` (tagged: ai, research)
- `Perplexity Pro API`

**Impact**: Confusion during rotation, potential for using wrong key

**Recommendation**:
```bash
# Check which one is currently in use
op item get "Perplexity API Key" --vault API_Keys --format json
op item get "Perplexity Pro API" --vault API_Keys --format json

# Delete the unused one
op item delete "Perplexity API Key" --vault API_Keys
# OR
op item delete "Perplexity Pro API" --vault API_Keys
```

**Priority**: High - Complete before deploying rotation system

---

### 2. Missing Rotation Metadata

**Problem**: None of your API credentials have rotation metadata fields

**Impact**: Cannot track when keys were last rotated or when they expire

**Recommendation**: Add custom fields to each credential:
- `last_rotated` - Date of last rotation
- `rotation_frequency` - How often to rotate (e.g., "90 days")
- `next_rotation` - Date of next scheduled rotation
- `rotation_notes` - Any special instructions

**Example**:
```bash
op item edit "Anthropic API Key" \
  --vault API_Keys \
  last_rotated="2025-10-30" \
  rotation_frequency="90 days" \
  next_rotation="2026-01-28" \
  rotation_notes="Automated via rotation framework"
```

**Priority**: High - Required for rotation scheduler to work properly

---

### 3. No Emergency Contacts

**Problem**: No designated contact or escalation path if rotation fails

**Impact**: Service disruption if automated rotation fails during off-hours

**Recommendation**:
- Add `rotation_owner` field to each credential (e.g., "mike.finneran@gmail.com")
- Set up email/Slack notifications for rotation failures
- Document emergency rotation procedures

**Priority**: Medium

---

### 4. Private Vault Needs Organization

**Problem**: 367 items in "Private" vault suggests potential organizational issues

**Impact**:
- Difficult to audit which credentials exist
- Potential security risk if old/unused credentials remain active
- Hard to determine what needs rotation

**Recommendation**:
1. Run credential audit:
   ```bash
   op item list --vault Private --format json | \
     jq '.[] | select(.category == "API_CREDENTIAL" or .category == "LOGIN") | {title, category, updated_at}'
   ```
2. Identify API credentials that should be in `API_Keys` vault
3. Move API credentials from Private to API_Keys:
   ```bash
   op item move "Item Name" --from-vault Private --to-vault API_Keys
   ```
4. Archive/delete unused credentials

**Priority**: Low (but important for long-term security hygiene)

---

## Recommendations for Improvement

### 1. Implement Rotation Tiers

**Current**: Flat 90-day rotation for all services

**Recommended**: Risk-based rotation schedule:

| Tier | Risk Level | Rotation Frequency | Services |
|------|-----------|-------------------|----------|
| **Tier 1** | Critical | 30 days | Anthropic, OpenAI (production keys) |
| **Tier 2** | High | 60 days | Airtable, Google OAuth (customer data) |
| **Tier 3** | Standard | 90 days | Perplexity, Gamma, TMDB |
| **Tier 4** | Low | 180 days | Personal/testing credentials |

**Implementation**:
```json
// config/rotation_config.json
{
  "services": {
    "Anthropic API Key": {
      "rotation_days": 30,
      "tier": "critical",
      "enabled": true
    },
    "Perplexity Pro API": {
      "rotation_days": 90,
      "tier": "standard",
      "enabled": false
    }
  }
}
```

---

### 2. Add Pre-Rotation Testing

**Current**: System tests credential after rotation

**Recommended**: Add pre-rotation smoke tests

**Implementation**:
```python
# In rotation_framework.py - add to CredentialRotator class
def pre_rotation_check(self):
    """Verify service is healthy before rotating"""
    # Test current credential works
    # Check service status
    # Verify backup/rollback procedure
    pass
```

**Benefits**:
- Don't rotate during service outages
- Confirm rollback procedure works
- Document baseline behavior

---

### 3. Implement Rotation Windows

**Current**: Rotations can happen anytime during daily check

**Recommended**: Define maintenance windows for each service

**Example**:
```json
{
  "Anthropic API Key": {
    "rotation_window": {
      "days": ["Monday", "Wednesday"],
      "time_range": "02:00-04:00",
      "timezone": "America/New_York"
    }
  }
}
```

**Benefits**:
- Rotate during low-traffic periods
- Coordinate with team schedules
- Avoid customer-facing hours

---

### 4. Add Slack/Email Notifications

**Current**: macOS notifications only

**Recommended**: Multi-channel notifications

**Implementation**:
```bash
# Install notification dependencies
pip3 install slack-sdk

# Add to config/rotation_config.json
{
  "notifications": {
    "channels": {
      "macos": {
        "enabled": true,
        "priority": "all"
      },
      "email": {
        "enabled": true,
        "recipients": ["mike.finneran@gmail.com"],
        "priority": "failures_only"
      },
      "slack": {
        "enabled": false,
        "webhook_url": "op://API_Keys/Slack Webhook/url",
        "priority": "critical"
      }
    }
  }
}
```

---

### 5. Create Rotation Playbooks

**Current**: Generic manual guides

**Recommended**: Service-specific playbooks with:
- Prerequisites checklist
- Step-by-step screenshots
- Common error messages and fixes
- Rollback procedures
- Post-rotation validation tests

**Example Structure**:
```
checklists/
├── anthropic_rotation_playbook.md
│   ├── Prerequisites
│   ├── Rotation Steps (with screenshots)
│   ├── Testing Procedure
│   ├── Rollback Steps
│   └── Troubleshooting
├── google_oauth_playbook.md
└── airtable_playbook.md
```

---

### 6. Implement Credential Versioning

**Current**: Single credential stored in 1Password

**Recommended**: Keep last 2 versions during transition

**Implementation**:
```bash
# Store old credential as backup during rotation
op item edit "Anthropic API Key" \
  credential="NEW_KEY" \
  previous_credential="OLD_KEY" \
  previous_rotated_at="2025-10-30"

# After 24 hours of successful operation, remove previous_credential
```

**Benefits**:
- Fast rollback if new key has issues
- Grace period for services to update
- Audit trail of key changes

---

### 7. Add Rotation Dry-Run Mode

**Current**: Live rotation only

**Recommended**: Test mode for validation

**Implementation**:
```bash
# Test rotation without actually changing credentials
python3 rotation_scheduler.py --dry-run

# Output: Shows what WOULD be rotated without doing it
```

---

### 8. Implement Credential Dependencies

**Current**: Each credential rotated independently

**Problem**: Some credentials are used by multiple services

**Example**: Your Google OAuth credentials are used by:
- Gmail MCP Server
- Gmail Amazon Parser

**Recommendation**: Track dependencies
```json
{
  "Google OAuth - Gmail MCP Server": {
    "dependencies": [
      "~/Documents/ObsidianVault/Projects/gmail-mcp-server/",
      "~/Projects/amazon-parser/"
    ],
    "restart_commands": [
      "Restart Claude Code (MCP reload)",
      "Restart amazon-parser service"
    ]
  }
}
```

---

### 9. Create Rotation Dashboard

**Current**: Command-line only

**Recommended**: Simple HTML dashboard

**Features**:
- Visual timeline of last/next rotations
- Red/yellow/green status indicators
- Quick action buttons ("Rotate Now", "View Guide")
- Audit log viewer

**Quick Implementation**:
```bash
# Generate static HTML dashboard
python3 generate_dashboard.py > dashboard.html
open dashboard.html
```

---

### 10. Add Cost Tracking

**Problem**: Some API key rotations may have rate limits or costs

**Recommendation**: Track API usage before rotation
```bash
# Before rotating expensive APIs (Anthropic, OpenAI)
python3 check_api_usage.py --service "Anthropic API Key"
# Output: Current month usage, cost, remaining quota

# Decision: Rotate now or wait until billing cycle reset?
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] **Consolidate Perplexity API credentials** (delete duplicate)
- [ ] **Add rotation metadata** to all 10 API credentials
  - [ ] Anthropic API Key
  - [ ] OpenAI API Key
  - [ ] Perplexity Pro API
  - [ ] Gamma API
  - [ ] Airtable WalterSignal
  - [ ] Google OAuth - Gmail MCP Server
  - [ ] Google OAuth - Gmail Amazon Parser
  - [ ] Cloudflare Wrangler OAuth
  - [ ] TMDB API - Alfred Workflow
- [ ] **Audit Private vault** for misplaced API credentials
- [ ] **Sign into 1Password CLI**: `eval $(op signin)`
- [ ] **Backup current config**: `cp -r ~/Library/Application\ Support/Claude ~/Library/Application\ Support/Claude.backup`

### Deployment

- [ ] **Run setup script**:
  ```bash
  cd ~/Documents/ObsidianVault/.mcp/credential-rotation
  chmod +x setup.sh
  ./setup.sh
  ```
- [ ] **Verify LaunchAgent loaded**:
  ```bash
  launchctl list | grep credential-rotation
  ```
- [ ] **Test manual rotation (dry-run first)**:
  ```bash
  python3 rotation_scheduler.py --dry-run
  ```
- [ ] **Verify MCP integration**:
  - Restart Claude Code
  - Test command: "Check credential rotation status"

### Post-Deployment

- [ ] **Customize rotation schedule** in `config/rotation_config.json`
- [ ] **Generate manual rotation checklists**:
  ```bash
  python3 modules/manual_rotation_guide.py
  ```
- [ ] **Set calendar reminders** for manual rotations (Google OAuth, etc.)
- [ ] **Document emergency procedures** in BACKLOG.md
- [ ] **Schedule first rotation** for low-risk service (TMDB API)
- [ ] **Monitor audit log** for 1 week: `tail -f logs/audit.jsonl`

---

## Security Best Practices

### Immediate Actions

1. **Enable 2FA on all API provider accounts**
   - Anthropic Console
   - OpenAI Platform
   - Perplexity API
   - Airtable
   - Google Cloud Console

2. **Set API key permissions to minimum required**
   - Review Airtable token scopes
   - Check Google OAuth scopes
   - Limit Cloudflare token permissions

3. **Enable API usage alerts**
   - Set spend limits on OpenAI/Anthropic
   - Configure usage alerts in Google Cloud
   - Monitor for anomalous API usage

### Ongoing Practices

1. **Review audit logs monthly**
   ```bash
   cat logs/audit.jsonl | jq 'select(.timestamp > "2025-10-01")'
   ```

2. **Rotate credentials immediately if**:
   - Credential appears in logs/code
   - Service reports breach
   - Employee/contractor offboarding
   - Suspicious API usage detected

3. **Test rollback procedures quarterly**
   - Verify old credentials are actually revoked
   - Confirm new credentials work across all services
   - Document any issues encountered

---

## Cost-Benefit Analysis

### Time Savings

**Current Manual Rotation** (per credential):
- Research how to rotate: 10 min
- Generate new key: 5 min
- Update 1Password: 2 min
- Update services: 10 min
- Test: 5 min
- Revoke old key: 3 min
**Total: 35 minutes per credential**

**With Automation** (Cloudflare example):
- Automated rotation: 2 min
- Verification: 3 min
**Total: 5 minutes per credential**

**Annual Savings** (10 credentials × 4 rotations/year):
- Manual: 10 × 4 × 35 min = **23.3 hours/year**
- Automated: 10 × 4 × 5 min = **3.3 hours/year**
- **Savings: 20 hours/year**

### Risk Reduction

**Without Rotation**:
- Risk of credential compromise increases over time
- No audit trail of key changes
- Forgotten credentials remain active
- Emergency rotation is chaotic and error-prone

**With Rotation**:
- Reduced blast radius if key compromised
- Complete audit trail
- Systematic review forces cleanup
- Practiced emergency procedures

---

## Implementation Priority

### Week 1: Foundation
1. Clean up 1Password (remove duplicates, add metadata)
2. Run setup.sh and verify installation
3. Test with TMDB API (low-risk)

### Week 2: Core Services
4. Enable Cloudflare automated rotation
5. Create detailed playbooks for manual rotations
6. Schedule first manual rotation (Perplexity)

### Week 3: Advanced Features
7. Add email notifications
8. Create rotation dashboard
9. Implement dry-run mode

### Week 4: Optimization
10. Set up rotation windows
11. Document dependencies
12. Create emergency procedures

---

## Questions to Consider

1. **Notification Preferences**: Email, Slack, or macOS only?
2. **Rotation Schedule**: Keep 90-day default or implement tiered approach?
3. **Manual vs Automated**: Which services should remain manual?
4. **Team Access**: Should others have access to rotation system?
5. **Backup Strategy**: How to handle failed rotations?

---

## Additional Resources

### Documentation
- Main README: `.mcp/credential-rotation/README.md`
- Setup Guide: `.mcp/credential-rotation/setup.sh`
- BACKLOG: `.mcp/credential-rotation/BACKLOG.md`

### Logs & Audit
- Rotation log: `logs/rotation.log`
- Audit trail: `logs/audit.jsonl`
- Scheduler output: `logs/scheduler_stdout.log`

### Configuration
- Service config: `config/rotation_config.json`
- LaunchAgent: `~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist`

---

## Next Steps

1. **Review this analysis** and prioritize recommendations
2. **Complete pre-deployment checklist**
3. **Run setup script**: `cd ~/.mcp/credential-rotation && ./setup.sh`
4. **Test with low-risk credential** (TMDB API)
5. **Schedule manual rotations** for critical services
6. **Monitor and iterate** based on audit logs

---

**Status**: Ready for deployment
**Estimated Setup Time**: 30 minutes
**Estimated Weekly Maintenance**: 5 minutes
**Annual Time Savings**: 20 hours

---

*Generated: 2025-10-30*
*Next Review: After first week of deployment*
