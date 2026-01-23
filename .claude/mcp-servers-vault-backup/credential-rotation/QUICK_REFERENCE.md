# Credential Rotation - Quick Reference

**Location**: `~/Documents/ObsidianVault/.mcp/credential-rotation/`

---

## Deployment (First Time Only)

```bash
# Authenticate to 1Password
eval $(op signin)

# Prepare 1Password (add metadata, clean duplicates)
cd ~/Documents/ObsidianVault/.mcp/credential-rotation
./prepare_1password.sh

# Deploy system
./setup.sh

# Test
python3 rotation_scheduler.py --dry-run
```

---

## Daily Commands

### Check Rotation Status

```bash
python3 rotation_scheduler.py
```

### View Recent Rotations

```bash
tail -20 logs/audit.jsonl | jq
```

### Get Manual Rotation Guide

```bash
python3 modules/manual_rotation_guide.py "Service Name"
```

---

## Claude Code Commands

```
"Check credential rotation status"
"List credentials due for rotation"
"Show rotation history for Anthropic"
"Get manual rotation guide for Perplexity"
"Test if my Cloudflare credentials work"
```

---

## 1Password Commands

### View Credential

```bash
op item get "Anthropic API Key" --vault API_Keys
```

### Update Credential

```bash
op item edit "Service Name" --vault API_Keys credential="NEW_VALUE"
```

### Add Rotation Metadata

```bash
op item edit "Service Name" --vault API_Keys \
  "last_rotated[date]=$(date +%Y-%m-%d)" \
  "next_rotation[date]=$(date -v+90d +%Y-%m-%d)"
```

### List All API Keys

```bash
op item list --vault API_Keys --format json | jq
```

---

## Scheduler Management

### Check Status

```bash
launchctl list | grep credential-rotation
```

### Manually Trigger

```bash
launchctl start com.waltersignal.credential-rotation
```

### Disable Scheduler

```bash
launchctl unload ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

### Re-enable Scheduler

```bash
launchctl load ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

---

## Logs

### Rotation Log

```bash
tail -f logs/rotation.log
```

### Audit Log (JSON)

```bash
cat logs/audit.jsonl | jq
```

### Scheduler Output

```bash
tail -f logs/scheduler_stdout.log
```

### Scheduler Errors

```bash
tail -f logs/scheduler_stderr.log
```

---

## Common Queries

### Failed Rotations

```bash
cat logs/audit.jsonl | jq 'select(.status == "failed")'
```

### Successful Rotations

```bash
cat logs/audit.jsonl | jq 'select(.status == "success")'
```

### Rotations for Specific Service

```bash
cat logs/audit.jsonl | jq 'select(.service == "Anthropic API Key")'
```

### Last 10 Rotations

```bash
tail -10 logs/audit.jsonl | jq
```

---

## Service-Specific Rotation

### Cloudflare (Automated)

```bash
python3 modules/cloudflare_rotator.py rotate
```

### Airtable (Test Credential)

```bash
python3 modules/airtable_rotator.py test YOUR_TOKEN
```

### Manual Services

```bash
# Get step-by-step guide
python3 modules/manual_rotation_guide.py "Perplexity Pro"
python3 modules/manual_rotation_guide.py "Gamma API"
python3 modules/manual_rotation_guide.py "Google OAuth"
```

---

## Configuration

### Edit Rotation Policies

```bash
nano config/rotation_config.json
```

### Change Schedule Time

```bash
nano ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
# Edit <integer>9</integer> to change hour
launchctl unload ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
launchctl load ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

---

## Troubleshooting

### "unauthorized: authentication required"

```bash
eval $(op signin)
```

### "LaunchAgent not running"

```bash
launchctl load ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

### "MCP server not responding"

```bash
# Test server manually
python3 server.py

# Restart Claude Code
```

### "Python dependencies missing"

```bash
pip3 install --user requests mcp
```

---

## Emergency Rotation

If credential compromised, rotate immediately:

```bash
# 1. Sign into 1Password
eval $(op signin)

# 2. Get manual rotation guide
python3 modules/manual_rotation_guide.py "Service Name"

# 3. Follow guide to rotate manually

# 4. Log the rotation
# (automatic if using manual_rotation_guide.py)

# 5. Update all services using the credential

# 6. Monitor logs for issues
tail -f logs/rotation.log
```

---

## File Locations

| File | Location |
|------|----------|
| **Main directory** | `~/Documents/ObsidianVault/.mcp/credential-rotation/` |
| **Config** | `config/rotation_config.json` |
| **Audit log** | `logs/audit.jsonl` |
| **Rotation log** | `logs/rotation.log` |
| **LaunchAgent** | `~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist` |
| **Claude config** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Checklists** | `checklists/*.md` |

---

## Documentation

| Document | Purpose |
|----------|---------|
| **EXECUTIVE_SUMMARY.md** | High-level overview and next steps |
| **DEPLOYMENT_CHECKLIST.md** | Step-by-step deployment guide |
| **ANALYSIS_AND_RECOMMENDATIONS.md** | Detailed analysis with 10 recommendations |
| **README.md** | Complete system documentation |
| **QUICK_REFERENCE.md** | This file - command cheat sheet |
| **BACKLOG.md** | Deployment status and todos |

---

## Quick Wins

### Today (5 minutes)

```bash
# Check what you have
op item list --vault API_Keys
```

### This Week (30 minutes)

```bash
# Deploy the system
./prepare_1password.sh
./setup.sh
```

### Next Week (15 minutes)

```bash
# First manual rotation (TMDB API)
python3 modules/manual_rotation_guide.py "TMDB"
```

---

## Support

**Check logs first**:
```bash
tail -50 logs/rotation.log
cat logs/audit.jsonl | jq 'select(.status == "failed")'
```

**Review documentation**:
- README.md - System overview
- TROUBLESHOOTING section in README.md

**Test components**:
```bash
# Test 1Password connection
op whoami

# Test framework imports
python3 -c "import rotation_framework; print('OK')"

# Test scheduler
python3 rotation_scheduler.py --dry-run
```

---

**Last Updated**: 2025-10-30
**Status**: Ready to deploy
