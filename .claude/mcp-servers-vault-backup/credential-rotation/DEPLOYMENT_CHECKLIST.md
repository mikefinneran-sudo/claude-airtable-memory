# Credential Rotation System - Deployment Checklist

**Date**: 2025-10-30
**Location**: `~/Documents/ObsidianVault/.mcp/credential-rotation/`
**Estimated Time**: 30 minutes

---

## Pre-Flight Checks

- [ ] 1Password CLI installed: `op --version`
- [ ] Python 3 installed: `python3 --version`
- [ ] Signed into 1Password: `eval $(op signin)`
- [ ] Backup Claude Code config: `cp -r ~/Library/Application\ Support/Claude ~/Library/Application\ Support/Claude.backup` (if exists)

---

## Phase 1: Prepare 1Password (15 minutes)

### Step 1: Consolidate Duplicate Credentials

```bash
# Sign into 1Password
eval $(op signin)

# Run preparation script
cd ~/Documents/ObsidianVault/.mcp/credential-rotation
chmod +x prepare_1password.sh
./prepare_1password.sh
```

**What this does**:
- Identifies duplicate Perplexity API entries
- Adds rotation metadata to all 10 credentials
- Scans Private vault for misplaced API credentials
- Sets up tier-based rotation schedule

### Step 2: Manual Review

- [ ] Delete duplicate Perplexity entry (script will show you which one)
- [ ] Verify metadata added correctly:
  ```bash
  op item get "Anthropic API Key" --vault API_Keys --format json | jq
  ```
- [ ] Move any API credentials from Private vault to API_Keys vault

---

## Phase 2: Deploy Rotation System (10 minutes)

### Step 3: Run Setup Script

```bash
cd ~/Documents/ObsidianVault/.mcp/credential-rotation
chmod +x setup.sh
./setup.sh
```

**What this does**:
- Installs Python dependencies
- Creates config/logs directories
- Generates manual rotation checklists
- Configures Claude Code MCP integration
- Sets up daily LaunchAgent (9:00 AM)
- Runs initial test

### Step 4: Verify Installation

```bash
# Check LaunchAgent is loaded
launchctl list | grep credential-rotation

# Check logs were created
ls -la logs/

# Check config was created
cat config/rotation_config.json

# Verify MCP integration
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep credential-rotation
```

Expected output:
- LaunchAgent shows PID or 0 (loaded)
- `logs/` directory exists (may be empty)
- `config/rotation_config.json` exists with service definitions
- MCP config includes credential-rotation entry

---

## Phase 3: Test and Configure (5 minutes)

### Step 5: Dry Run Test

```bash
cd ~/Documents/ObsidianVault/.mcp/credential-rotation

# Test without actually rotating
python3 rotation_scheduler.py --dry-run
```

Expected output: List of services and their rotation status

### Step 6: Customize Configuration

Edit `config/rotation_config.json`:

```json
{
  "services": {
    "Anthropic API Key": {
      "rotation_days": 30,
      "enabled": false,  // Start disabled, enable when ready
      "tier": "critical"
    },
    "Cloudflare Wrangler OAuth": {
      "rotation_days": 90,
      "enabled": true,  // Only enable if you want automated rotation
      "tier": "standard"
    }
  }
}
```

**Recommendation**: Start with all services disabled, test one at a time

### Step 7: Test Claude Code Integration

1. Restart Claude Code (quit and reopen)
2. In Claude Code, try these commands:
   - "Check credential rotation status"
   - "List credentials due for rotation"
   - "Show rotation history"

If MCP server works, you'll get meaningful responses. If not, check logs.

---

## Phase 4: First Rotation (Manual)

### Step 8: Schedule First Rotation

Start with lowest-risk credential: **TMDB API - Alfred Workflow**

```bash
# Get manual rotation guide
python3 modules/manual_rotation_guide.py "TMDB"

# Follow the checklist generated in checklists/
cat checklists/tmdb_rotation.md
```

### Step 9: Document Results

After successful rotation:

```bash
# Check audit log
cat logs/audit.jsonl | jq 'select(.service == "TMDB")'

# Verify in 1Password
op item get "TMDB API - Alfred Workflow" --vault API_Keys --format json | \
  jq '.fields[] | select(.label | contains("rotation"))'
```

---

## Troubleshooting

### "unauthorized: authentication required"

```bash
eval $(op signin)
```

### "LaunchAgent failed to load"

```bash
# Check syntax
plutil ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist

# View error logs
cat logs/scheduler_stderr.log
```

### "MCP server not responding"

```bash
# Test server manually
cd ~/Documents/ObsidianVault/.mcp/credential-rotation
python3 server.py

# If errors, check dependencies
pip3 install --user requests mcp
```

### "Python module not found"

```bash
# Install dependencies
pip3 install --user requests mcp

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install requests mcp
```

---

## Post-Deployment

### Immediate (This Week)

- [ ] Monitor daily scheduler runs: `tail -f logs/scheduler_stdout.log`
- [ ] Review audit log: `cat logs/audit.jsonl | jq`
- [ ] Test manual rotation for one low-risk service
- [ ] Set calendar reminders for manual rotations

### Week 2

- [ ] Enable automated rotation for Cloudflare (if desired)
- [ ] Create detailed playbooks for critical services (Anthropic, OpenAI)
- [ ] Set up email notifications (optional)

### Week 3

- [ ] Review first week of audit logs
- [ ] Adjust rotation frequencies based on usage
- [ ] Enable rotation for additional services
- [ ] Document any issues encountered

### Monthly

- [ ] Review audit logs: `cat logs/audit.jsonl | jq`
- [ ] Verify rotation metadata is current
- [ ] Test emergency rotation procedure
- [ ] Clean up old/unused credentials

---

## Rollback Plan

If something goes wrong:

### Rollback Claude Code Config

```bash
# Restore backup
rm ~/Library/Application\ Support/Claude/claude_desktop_config.json
cp ~/Library/Application\ Support/Claude.backup/claude_desktop_config.json \
   ~/Library/Application\ Support/Claude/
```

### Disable LaunchAgent

```bash
launchctl unload ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

### Restore Old Credential

```bash
# If rotation went wrong, update back to old value
op item edit "Service Name" --vault API_Keys credential="OLD_VALUE"
```

---

## Success Criteria

✅ System successfully deployed when:
- [ ] LaunchAgent is loaded and running
- [ ] Audit log exists and is writable
- [ ] Claude Code MCP integration responds
- [ ] At least one manual rotation completed successfully
- [ ] Rotation metadata visible in 1Password

---

## Quick Reference

### Daily Commands

```bash
# Check rotation status
python3 rotation_scheduler.py

# View recent activity
tail -20 logs/audit.jsonl | jq

# Manual rotation guide
python3 modules/manual_rotation_guide.py "Service Name"
```

### Maintenance Commands

```bash
# Restart scheduler
launchctl unload ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
launchctl load ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist

# View logs
tail -f logs/rotation.log
tail -f logs/scheduler_stdout.log

# Edit configuration
nano config/rotation_config.json
```

---

## Next Steps After Deployment

1. Read: `ANALYSIS_AND_RECOMMENDATIONS.md` for optimization ideas
2. Create: Service-specific rotation playbooks
3. Schedule: Calendar reminders for manual rotations
4. Monitor: Audit logs for first week
5. Iterate: Adjust rotation frequencies based on usage

---

**Status**: Ready to Deploy
**Last Updated**: 2025-10-30
**Next Review**: After first successful rotation

Good luck! 🚀
