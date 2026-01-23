# Automated Credential Rotation System

**Enterprise-grade credential management with automated rotation, audit logging, and 1Password integration**

---

## Overview

This system provides:
- **Automated API key rotation** for supported services (Cloudflare)
- **Manual rotation guides** for services requiring manual process
- **1Password integration** for secure credential storage
- **Audit logging** of all rotation attempts
- **Claude Code MCP integration** for AI-assisted management
- **Scheduled checks** via macOS LaunchAgent
- **macOS notifications** for rotation events

---

## Quick Start

### 1. Setup

```bash
cd ~/.mcp/credential-rotation
./setup.sh
```

This will:
- Install dependencies
- Configure MCP server
- Setup scheduled rotation checks
- Generate rotation checklists
- Create initial audit log

### 2. Check Status

**Via Claude Code:**
```
Ask me to check credential rotation status
```

**Via Command Line:**
```bash
python3 rotation_scheduler.py
```

### 3. Rotate a Credential

**Automated (Cloudflare):**
```bash
# Via Claude Code
"Rotate my Cloudflare credentials"

# Via Python
python3 modules/cloudflare_rotator.py rotate
```

**Manual (Other Services):**
```bash
# Get step-by-step guide
python3 modules/manual_rotation_guide.py "Perplexity Pro"
```

---

## Architecture

### Components

```
credential-rotation/
├── rotation_framework.py       # Core framework
├── server.py                   # MCP server for Claude Code
├── rotation_scheduler.py       # Automated scheduler
├── setup.sh                    # One-time setup script
│
├── modules/                    # Service-specific rotators
│   ├── cloudflare_rotator.py  # Automated Cloudflare rotation
│   ├── airtable_rotator.py    # Airtable guide + tester
│   └── manual_rotation_guide.py
│
├── logs/                       # Audit and execution logs
│   ├── audit.jsonl            # Rotation history
│   ├── rotation.log           # Detailed logs
│   └── scheduler_*.log        # Scheduler output
│
├── config/                     # Configuration
│   └── rotation_config.json   # Service rotation policies
│
└── checklists/                # Manual rotation guides
    ├── perplexity_pro_rotation.md
    ├── gamma_api_rotation.md
    └── google_oauth_rotation.md
```

### Rotation Flow

```
1. Scheduler Check
   ↓
2. Check Last Rotation Date
   ↓
3. Needs Rotation? → No → Skip
   ↓ Yes
4. Generate New Credential
   ↓
5. Update 1Password
   ↓
6. Test New Credential
   ↓ Pass
7. Revoke Old Credential
   ↓
8. Log to Audit
   ↓
9. Send Notification
```

---

## Supported Services

### Fully Automated
- ✅ **Cloudflare** - API tokens via Cloudflare API

### Semi-Automated (Manual Creation + Automated Testing)
- ⚙️  **Airtable** - Manual creation, automated testing

### Manual (With Guided Checklists)
- 📋 **Perplexity Pro** - Step-by-step guide
- 📋 **Gamma API** - Step-by-step guide
- 📋 **Google OAuth** - Step-by-step guide
- 📋 **TMDB API** - Step-by-step guide

---

## Usage

### Via Claude Code (Recommended)

The MCP server provides natural language commands:

```
"Check which credentials need rotation"
"Rotate my Cloudflare credentials"
"Show me rotation history for Airtable"
"Give me the manual rotation guide for Perplexity"
"Test if my Cloudflare token is working"
"Schedule Airtable rotation every 60 days"
```

### Via Command Line

#### Check Status
```bash
python3 rotation_scheduler.py
```

#### Rotate Cloudflare
```bash
python3 modules/cloudflare_rotator.py rotate
```

#### Get Manual Guide
```bash
python3 modules/manual_rotation_guide.py "Perplexity Pro"
```

#### View Audit Log
```bash
cat logs/audit.jsonl | jq
```

#### Test Credentials
```bash
python3 modules/airtable_rotator.py test YOUR_TOKEN
python3 modules/cloudflare_rotator.py test
```

---

## Rotation Policies

Default rotation frequencies:

| Service | Frequency | Method |
|---------|-----------|--------|
| Cloudflare | 90 days | Automated |
| Airtable | 90 days | Manual |
| Perplexity Pro | 90 days | Manual |
| Gamma API | 90 days | Manual |
| Google OAuth | 180 days | Manual |
| TMDB API | 180 days | Manual |

Customize in `config/rotation_config.json`

---

## Scheduling

### Automated Daily Checks

The system runs daily at 9:00 AM via macOS LaunchAgent:

```bash
# Check schedule status
launchctl list | grep credential-rotation

# Manually trigger
launchctl start com.waltersignal.credential-rotation

# Disable
launchctl unload ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist

# Re-enable
launchctl load ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

### Custom Schedule

Edit `~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist`:

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>9</integer>  <!-- Change time here -->
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

Then reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
launchctl load ~/Library/LaunchAgents/com.waltersignal.credential-rotation.plist
```

---

## Audit Logging

All rotation attempts are logged to `logs/audit.jsonl`:

```json
{
  "timestamp": "2025-10-30T09:00:00",
  "service": "Cloudflare",
  "status": "success",
  "details": "Rotated successfully"
}
```

### Query Audit Log

```bash
# All rotations
cat logs/audit.jsonl | jq

# Successful rotations
cat logs/audit.jsonl | jq 'select(.status == "success")'

# Failed rotations
cat logs/audit.jsonl | jq 'select(.status == "failed")'

# Rotations for specific service
cat logs/audit.jsonl | jq 'select(.service == "Cloudflare")'

# Last 10 rotations
tail -10 logs/audit.jsonl | jq
```

---

## Adding New Services

### For Automated Rotation

1. Create rotator module:

```python
# modules/myservice_rotator.py
from rotation_framework import CredentialRotator

class MyServiceRotator(CredentialRotator):
    def __init__(self):
        super().__init__(
            service_name="MyService",
            op_item="MyService API Key",
            rotation_days=90
        )

    def generate_new_credential(self):
        # Call service API to create new key
        pass

    def revoke_old_credential(self, old_credential):
        # Call service API to revoke old key
        pass

    def test_credential(self, credential):
        # Test if credential works
        pass
```

2. Register in `rotation_scheduler.py`:

```python
from modules.myservice_rotator import MyServiceRotator

rotator = MyServiceRotator()
scheduler.register_rotator(rotator)
```

3. Add to MCP server in `server.py`

### For Manual Rotation

Add to `modules/manual_rotation_guide.py`:

```python
MANUAL_ROTATION_GUIDES["MyService"] = {
    "url": "https://myservice.com/settings/api",
    "steps": [
        "1. Go to settings...",
        "2. Create new key...",
        # etc.
    ],
    "test_command": "curl -H 'Authorization: Bearer KEY' ...",
    "rotation_frequency": "Every 90 days"
}
```

---

## Troubleshooting

### "unauthorized: authentication required"
```bash
eval $(op signin)
```

### Scheduler not running
```bash
# Check LaunchAgent status
launchctl list | grep credential-rotation

# View logs
cat logs/scheduler_stderr.log
```

### Rotation failed
```bash
# Check detailed logs
tail -50 logs/rotation.log

# Check audit log
cat logs/audit.jsonl | jq 'select(.status == "failed")'
```

### MCP server not working
```bash
# Test server manually
python3 server.py

# Check Claude Code config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Restart Claude Code
```

---

## Security Considerations

1. **1Password Integration**
   - All credentials stored encrypted in 1Password
   - Requires authentication to access
   - Audit trail of all access

2. **Audit Logging**
   - Complete history of all rotation attempts
   - Immutable append-only log
   - Includes timestamps and details

3. **Credential Testing**
   - New credentials tested before old ones revoked
   - Automatic rollback on test failure
   - Prevents service disruption

4. **Secure Rotation**
   - Old credentials revoked after successful rotation
   - Minimizes window of dual-key exposure
   - Notifications for all rotation events

---

## Best Practices

1. **Regular Monitoring**
   - Check rotation status weekly
   - Review audit logs monthly
   - Respond to rotation notifications promptly

2. **Rotation Frequency**
   - Security-critical: 30-60 days
   - Standard services: 90 days
   - Low-risk services: 180 days

3. **Manual Rotations**
   - Follow checklists exactly
   - Test thoroughly before revoking old keys
   - Document in audit log

4. **Emergency Rotation**
   - Force rotation if key compromised
   - Update all affected services immediately
   - Review access logs

---

## Support

- **Documentation**: This README
- **Logs**: `logs/rotation.log`
- **Audit**: `logs/audit.jsonl`
- **Checklists**: `checklists/*.md`
- **Configuration**: `config/rotation_config.json`

---

**Built with ❤️ for enterprise-grade credential security**
