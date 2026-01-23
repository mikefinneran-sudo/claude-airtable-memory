# Google Calendar Sync Setup Guide

**Time to complete:** 20-30 minutes
**What you'll get:** Today's meetings in your daily notes automatically

---

## What Calendar Sync Does

✅ Syncs Google Calendar events to daily notes
✅ Shows today's meetings when you open your daily note
✅ Includes meeting times, attendees, and topics
✅ Updates automatically
✅ Works offline once synced

---

## Step 1: Install Python Dependencies (2 min)

```bash
pip3 install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## Step 2: Enable Calendar API (10 min)

### Use Same Project or Create New

**Option A: Use existing project (if you set up Gmail sync)**
1. Go to https://console.cloud.google.com
2. Select your existing "LifeHub Gmail Sync" project

**Option B: Create new project**
1. Go to https://console.cloud.google.com
2. Click **"Select a project"** → **"New Project"**
3. Name: "LifeHub Calendar Sync"
4. Click **"Create"**

### Enable Calendar API

1. In the project, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google Calendar API"**
3. Click **"Google Calendar API"** → **"Enable"**

### Create OAuth Credentials (if new project)

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
6. Name: **LifeHub Calendar**
7. Click **"Create"**
8. **Download JSON** file
9. Save as: `/Users/mikefinneran/Documents/ObsidianVault/.scripts/credentials-calendar.json`

**If using same project as Gmail:**
- You can reuse the same credentials file
- Or create separate credentials for organization

---

## Step 3: Run OAuth Flow (5 min)

```bash
cd ~/Documents/ObsidianVault/.scripts
python3 sync_calendar.py
```

**What happens:**
1. Browser opens with Google login
2. Select your account
3. Click **"Advanced"** → **"Go to LifeHub (unsafe)"**
4. Click **"Allow"** for Calendar access
5. Close browser
6. Script creates `token-calendar.pickle` file

**First sync will download upcoming events.**

---

## Step 4: Configure Sync Settings (Optional)

Edit sync script:

```bash
nano ~/Documents/ObsidianVault/.scripts/sync_calendar.py
```

Customize settings:

```python
SETTINGS = {
    "days_ahead": 7,        # How many days to sync
    "calendars": ["primary"], # Which calendars ("primary" = your main calendar)
    "min_duration": 15,      # Ignore events shorter than 15 min
    "include_declined": False # Don't show declined events
}
```

---

## Step 5: Test Sync

```bash
# Run manual sync
python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py

# Check results
cat ~/Documents/ObsidianVault/Daily/$(date +%Y-%m-%d).md
```

You should see your calendar events added to today's note!

---

## Step 6: Automate Sync

### Option A: Sync with daily note (Recommended)

Calendar sync runs automatically when daily note is created (already configured in LaunchAgent).

### Option B: Sync every hour

Create LaunchAgent:

```bash
cat > ~/Library/LaunchAgents/com.lifehub.calendar-sync.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.lifehub.calendar-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/sync_calendar.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/calendar-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/calendar-sync-error.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.lifehub.calendar-sync.plist
```

---

## Usage

### Manual Sync
```bash
python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py
```

### View in Daily Notes
Open today's note - calendar events appear in a dedicated section

### Sync Multiple Calendars

Edit script to include multiple calendars:

```python
CALENDARS = [
    "primary",                          # Your main calendar
    "work@company.com",                 # Work calendar
    "family12345@group.calendar.google.com"  # Shared calendar
]
```

Find calendar IDs in Google Calendar settings.

---

## What Gets Synced

**Included in sync:**
- ✅ Event title
- ✅ Start/end time
- ✅ Location (if set)
- ✅ Attendees (if any)
- ✅ Description (first 200 characters)
- ✅ Meeting link (Zoom, Meet, etc.)

**Formatted as markdown:**
```markdown
## 📅 Today's Calendar

### 9:00 AM - 10:00 AM: Team Standup
**Location:** Zoom
**Attendees:** Alice, Bob, Carol
**Link:** https://zoom.us/j/123456789

### 2:00 PM - 3:00 PM: Client Meeting
**Location:** Office, Conference Room A
**Attendees:** John Smith (Client)
**Notes:** Discuss Q4 deliverables
```

---

## Troubleshooting

### "credentials-calendar.json not found"
- Download from Google Cloud Console
- Save to `.scripts/` folder
- Rename to `credentials-calendar.json`

### "Token has been expired or revoked"
```bash
# Delete old token
rm ~/Documents/ObsidianVault/.scripts/token-calendar.pickle

# Re-run OAuth flow
python3 ~/Documents/ObsidianVault/.scripts/sync_calendar.py
```

### Events not showing in daily note
- Check that daily note has been created
- Verify calendar has events today
- Check sync log for errors

### "Access blocked: LifeHub hasn't completed Google verification"
- Click "Advanced" → "Go to LifeHub (unsafe)"
- Normal for personal use apps
- Your data stays private

---

## Privacy & Security

✅ **OAuth 2.0** - Secure, industry-standard
✅ **Local storage** - Calendar data on your computer only
✅ **Revocable** - Revoke access anytime in Google Account
✅ **Read-only** - Script only reads, never creates or modifies events

---

## Benefits

Once set up:
- ✅ Meetings automatically appear in daily notes
- ✅ No need to check multiple apps
- ✅ Prepare for meetings by reviewing notes
- ✅ Link meeting notes to projects
- ✅ Offline access to schedule

---

## Advanced: Meeting Preparation

Create a Dataview query in your daily note template to show:
- Meetings in next 2 hours
- Project context for each meeting
- Previous meeting notes

Example query:
```markdown
## 🔜 Upcoming Meetings

```dataview
TABLE time, attendees
FROM "Calendar"
WHERE date = date(today)
  AND time > time(now)
SORT time ASC
```
```

---

**Need help?** Check logs:
```bash
tail -f ~/Documents/ObsidianVault/.scripts/calendar-sync.log
```

---

*Setup guide created: 2025-10-21*
