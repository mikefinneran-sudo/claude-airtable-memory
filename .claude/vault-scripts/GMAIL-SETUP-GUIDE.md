# Gmail Sync Setup Guide

**Time to complete:** 20-30 minutes (mostly Google OAuth setup)
**What you'll get:** Priority emails in your daily notes

---

## What Gmail Sync Does

✅ Syncs your Gmail inbox to Obsidian notes
✅ Filters by labels, senders, date range
✅ Shows unread/priority emails in daily notes
✅ Markdown formatting for easy reading
✅ Works offline once synced

---

## Step 1: Install Python Dependencies (2 min)

```bash
pip3 install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## Step 2: Enable Gmail API (10 min)

### Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click **"Select a project"** → **"New Project"**
3. Name: "LifeHub Gmail Sync"
4. Click **"Create"**

### Enable Gmail API

1. In the project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Gmail API"**
3. Click **"Gmail API"** → **"Enable"**

### Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: **LifeHub**
   - User support email: your email
   - Developer contact: your email
   - Click **"Save and Continue"** through all steps
4. Back to Credentials, click **"+ Create Credentials"** → **"OAuth client ID"**
5. Application type: **Desktop app**
6. Name: **LifeHub Gmail**
7. Click **"Create"**
8. **Download JSON** file
9. Save as: `/Users/mikefinneran/Documents/ObsidianVault/.scripts/credentials-gmail.json`

---

## Step 3: Run OAuth Flow (5 min)

```bash
cd ~/Documents/ObsidianVault/.scripts
python3 sync_gmail.py
```

**What happens:**
1. Browser opens with Google login
2. Select your account
3. Click **"Advanced"** → **"Go to LifeHub (unsafe)"**
4. Click **"Allow"** for Gmail access
5. Close browser
6. Script creates `token-gmail.pickle` file

**First sync will take a minute to download emails.**

---

## Step 4: Configure Filters (Optional)

Edit sync script to filter emails:

```bash
nano ~/Documents/ObsidianVault/.scripts/sync_gmail.py
```

Find the `FILTERS` section and customize:

```python
FILTERS = {
    "labels": ["IMPORTANT", "CATEGORY_PERSONAL"],  # Which labels
    "exclude_senders": ["noreply@", "no-reply@"],  # Skip these senders
    "max_age_days": 7,  # Only sync last 7 days
    "max_emails": 50   # Limit per sync
}
```

---

## Step 5: Test Sync

```bash
# Run manual sync
python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py

# Check results
ls -la ~/Documents/ObsidianVault/Inbox/Email/
```

---

## Step 6: Automate (Optional)

### Option A: Run with daily notes

Add to your daily note LaunchAgent:

```bash
# Edit LaunchAgent
nano ~/Library/LaunchAgents/com.lifehub.dailynote-enhanced.plist

# Add Gmail sync after daily note creation
```

### Option B: Separate schedule (e.g., every 2 hours)

Create LaunchAgent:

```bash
cat > ~/Library/LaunchAgents/com.lifehub.gmail-sync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lifehub.gmail-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/sync_gmail.py</string>
    </array>
    <key>StartInterval</key>
    <integer>7200</integer>
    <key>StandardOutPath</key>
    <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail-sync-error.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.lifehub.gmail-sync.plist
```

---

## Usage

### Manual Sync
```bash
python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py
```

### Check Synced Emails
Look in: `~/Documents/ObsidianVault/Inbox/Email/`

### View in Dashboard
Your dashboard can show priority emails automatically with Dataview

---

## Troubleshooting

### "credentials-gmail.json not found"
- Download from Google Cloud Console
- Save to `.scripts/` folder
- Rename to `credentials-gmail.json`

### "Token has been expired or revoked"
```bash
# Delete old token
rm ~/Documents/ObsidianVault/.scripts/token-gmail.pickle

# Re-run OAuth flow
python3 ~/Documents/ObsidianVault/.scripts/sync_gmail.py
```

### "Access blocked: LifeHub hasn't completed Google verification"
- Click "Advanced" → "Go to LifeHub (unsafe)"
- This is normal for personal use apps

### Not syncing all emails
- Check filters in script
- Verify labels exist in Gmail
- Increase `max_emails` limit

---

## Privacy & Security

✅ **OAuth 2.0** - Secure, industry-standard authentication
✅ **Local storage** - Emails stored on your computer only
✅ **Revocable** - Revoke access anytime in Google Account settings
✅ **Read-only** - Script only reads, never sends or deletes emails

---

## Benefits

Once set up:
- ✅ Priority emails in your daily notes
- ✅ Offline access to recent emails
- ✅ Centralized workspace (everything in Obsidian)
- ✅ Search emails with Obsidian search
- ✅ Link emails to projects

---

**Need help?** Check logs:
```bash
tail -f ~/Documents/ObsidianVault/.scripts/gmail-sync.log
```

---

*Setup guide created: 2025-10-21*
