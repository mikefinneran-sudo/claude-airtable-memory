# S3 Integration System

**Created**: November 1, 2025
**Purpose**: Automated backup and archival storage using AWS S3
**Status**: Ready to configure

---

## What This Does

Complete S3 integration for long-term archival and disaster recovery:
- **Automatic Daily Backups** to S3
- **One-Command Restore** from any backup
- **Intelligent Compression** (STANDARD_IA storage class)
- **Version Control** with S3 versioning
- **Encryption** at rest (AES256)

**Result**: Never lose work, restore from anywhere, pay-as-you-go cloud storage

---

## Quick Start

### 1. Setup S3 (One-Time)

```bash
# Install AWS CLI and configure credentials
s3-setup
```

Choose configuration method:
- **Option 1**: Enter AWS credentials manually
- **Option 2**: Retrieve from 1Password (if available)

Script will:
- Install AWS CLI
- Configure credentials
- Create S3 bucket (optional)
- Enable versioning and encryption
- Add environment variables to ~/.zshrc

### 2. Test Backup

```bash
# Reload environment
source ~/.zshrc

# Run first backup
backup-s3
```

### 3. Setup Automated Backups (Optional)

```bash
~/.claude/scripts/setup-automated-s3-backups.sh
```

Choose schedule:
- **Daily** at 2 AM (recommended)
- **Weekly** on Sunday at 2 AM
- **Custom** schedule

---

## Commands

### Backup to S3
```bash
backup-s3
```

Backs up:
- Session archives (all .md files from session-archive/)
- Project workspaces (all projects/)
- Memory files (SESSION-MEMORY.md, WORKING-CONTEXT.md)
- Configuration (aliases, scripts, .zshrc)
- Utilities repository (custom scripts)
- Documentation (all system guides)

### Restore from S3
```bash
restore-s3
```

Interactive restore:
1. Lists all available backups
2. Select backup by number
3. Preview manifest
4. Confirm restore
5. Automatically backs up current state first
6. Restores selected backup

### Setup/Reconfigure
```bash
s3-setup
```

---

## What Gets Backed Up

```
backup-YYYY-MM-DD-HHMMSS.tar.gz
├── session-archives/       # All session .md files
├── projects/               # All project workspaces
│   ├── waltersignal/
│   ├── flyflat/
│   └── utilities-repo-setup/
├── memory/                 # Current memory state
│   ├── SESSION-MEMORY.md
│   ├── WORKING-CONTEXT.md
│   └── CLAUDE.md
├── config/                 # Configuration files
│   ├── setup-aliases.sh
│   ├── init-project-memory.sh
│   └── zshrc-backup
├── utilities/              # Custom scripts repository
└── docs/                   # System documentation
    ├── MEMORY-OPTIMIZATION-COMPLETE.md
    ├── SCRIPTS-ARCHIVAL-SYSTEM.md
    └── ACTIVITY-TRACKING-SYSTEM.md
```

Plus `MANIFEST.txt` with backup metadata.

---

## S3 Bucket Structure

```
s3://your-bucket-name/
└── claude-backups/
    ├── backup-2025-11-01-140532.tar.gz
    ├── backup-2025-11-02-020000.tar.gz
    ├── backup-2025-11-03-020000.tar.gz
    └── ...
```

**Storage Class**: `STANDARD_IA` (Infrequent Access)
- Lower cost for long-term storage
- Perfect for backups accessed occasionally

**Versioning**: Enabled
- Previous versions preserved
- Accidental deletion protected

**Encryption**: AES256
- Data encrypted at rest
- Automatic encryption

---

## Cost Estimates

**Storage Costs** (STANDARD_IA):
- $0.0125 per GB/month (US East)
- Typical backup: ~50-200 MB compressed
- Monthly cost: $0.001 - $0.003 (less than a penny)

**Daily Backups for 1 Year**:
- 365 backups × 100 MB = 36.5 GB
- Cost: ~$0.46/month ($5.50/year)

**With Lifecycle Policy** (auto-delete old backups):
- Keep 30 days: ~$0.04/month
- Keep 90 days: ~$0.12/month

---

## Automated Backups

### Setup
```bash
~/.claude/scripts/setup-automated-s3-backups.sh
```

Creates launchd agent (macOS equivalent of cron) that runs backups automatically.

### Check Status
```bash
# View running agents
launchctl list | grep claude

# View logs
tail -f ~/.claude/logs/s3-backup.log
tail -f ~/.claude/logs/s3-backup-error.log
```

### Manage
```bash
# Unload (disable)
launchctl unload ~/Library/LaunchAgents/com.claude.s3backup.plist

# Reload (enable)
launchctl load ~/Library/LaunchAgents/com.claude.s3backup.plist

# Test now
backup-s3
```

---

## Disaster Recovery

### Complete System Loss

If you lose your laptop or need to set up a new machine:

```bash
# 1. Install AWS CLI
brew install awscli

# 2. Configure AWS credentials
aws configure

# 3. Download restore script
curl -o restore.sh https://raw.githubusercontent.com/YOUR-REPO/utilities-repo-setup/main/restore-from-s3.sh
chmod +x restore.sh

# 4. Run restore
./restore.sh
```

### Restore Specific Backup
```bash
restore-s3
# Select backup number from list
# Confirm restore
```

### Partial Restore

Download and extract manually:

```bash
# List backups
aws s3 ls s3://your-bucket/claude-backups/

# Download specific backup
aws s3 cp s3://your-bucket/claude-backups/backup-2025-11-01-140532.tar.gz .

# Extract
tar -xzf backup-2025-11-01-140532.tar.gz

# View contents
ls backup-2025-11-01-140532/

# Restore only what you need
cp -R backup-2025-11-01-140532/projects/waltersignal ~/.claude/projects/
```

---

## Advanced: Lifecycle Policies

Auto-delete old backups to save costs:

```bash
# Keep only 30 days of backups
aws s3api put-bucket-lifecycle-configuration \
  --bucket your-bucket-name \
  --lifecycle-configuration '{
    "Rules": [{
      "Id": "delete-old-backups",
      "Status": "Enabled",
      "Prefix": "claude-backups/",
      "Expiration": {
        "Days": 30
      }
    }]
  }'
```

**Options**:
- 7 days: Ultra-short retention
- 30 days: Recommended for frequent work
- 90 days: Quarter retention
- 365 days: Full year retention

---

## Advanced: Multi-Region Backup

For extra redundancy, replicate to another region:

```bash
# Enable replication
aws s3api put-bucket-replication \
  --bucket your-primary-bucket \
  --replication-configuration '{
    "Role": "arn:aws:iam::YOUR-ACCOUNT:role/s3-replication",
    "Rules": [{
      "Status": "Enabled",
      "Priority": 1,
      "Destination": {
        "Bucket": "arn:aws:s3:::your-backup-bucket",
        "ReplicationTime": {
          "Status": "Enabled",
          "Time": { "Minutes": 15 }
        }
      }
    }]
  }'
```

---

## Environment Variables

Required in `~/.zshrc`:

```bash
# S3 Backup Configuration
export S3_BACKUP_BUCKET='your-bucket-name'
```

Auto-added by setup script.

---

## Files Created

1. `~/.claude/scripts/setup-s3-integration.sh`
   - Installs AWS CLI and configures credentials

2. `~/.claude/scripts/backup-to-s3.sh`
   - Main backup script

3. `~/.claude/scripts/restore-from-s3.sh`
   - Interactive restore script

4. `~/.claude/scripts/setup-automated-s3-backups.sh`
   - Configures daily automated backups

**Modified**:
- `setup-aliases.sh` - Added S3 commands

---

## Use Cases

### Daily Automatic Backups
```bash
# Setup once
~/.claude/scripts/setup-automated-s3-backups.sh
# Backups happen automatically at 2 AM daily
```

### Before Major Changes
```bash
# Manual backup before risky operation
backup-s3
# Do risky thing
# If needed: restore-s3
```

### Moving to New Machine
```bash
# On new machine
s3-setup
restore-s3
# Select latest backup
# Resume work immediately
```

### Disaster Recovery
```bash
# Lost laptop? No problem.
# Install AWS CLI
# Configure credentials
# Restore latest backup
```

---

## Troubleshooting

### "AWS CLI not found"
```bash
# Install manually
brew install awscli
# Or run setup
s3-setup
```

### "Credentials not configured"
```bash
aws configure
# Enter Access Key ID, Secret Access Key, region
```

### "Bucket does not exist"
```bash
# Create bucket manually
aws s3 mb s3://your-bucket-name

# Or run setup to create
s3-setup
```

### "Permission denied"
- Check AWS IAM permissions
- Need: s3:PutObject, s3:GetObject, s3:ListBucket

### Backup too large
- Check what's being backed up
- Exclude large files if needed
- Typical backup: 50-200 MB compressed

---

## Security Best Practices

**Credentials**:
- Use 1Password to store AWS credentials
- Never commit credentials to git
- Rotate access keys quarterly

**Bucket Permissions**:
- Enable MFA delete for extra protection
- Use IAM roles when possible
- Block public access

**Encryption**:
- Enabled by default (AES256)
- Consider AWS KMS for extra control

---

## Next Steps

1. ✅ Run setup: `s3-setup`
2. ✅ Test backup: `backup-s3`
3. ✅ Setup automation: `~/.claude/scripts/setup-automated-s3-backups.sh`
4. ✅ Configure lifecycle policy (optional)

---

**Status**: Production Ready
**Automated**: Optional daily backups
**Recovery Time**: ~5 minutes from any backup

---

**Quick Reference**:
- Setup: `s3-setup`
- Backup: `backup-s3`
- Restore: `restore-s3`
- Automation: `~/.claude/scripts/setup-automated-s3-backups.sh`
