# Notion Integration Setup Guide
## Quick 5-Minute Setup for Airtable → Notion Sync

---

## Step 1: Create Notion Integration (2 minutes)

1. **Open Notion Integrations:**
   - Go to: https://www.notion.com/my-integrations
   - Or: Notion Settings → Integrations → "Develop your own integrations"

2. **Create New Integration:**
   - Click **"+ New integration"**
   - Name: `Airtable Sync`
   - Associated workspace: Select your workspace
   - Type: Internal integration
   - Click **"Submit"**

3. **Copy Integration Token:**
   - You'll see: "Internal Integration Secret"
   - Click **"Show"** then **"Copy"**
   - Save this token (you'll need it in Step 3)

---

## Step 2: Get Your Notion Database IDs (2 minutes)

### Your Existing Database

You already have: **LifeHub - Projects**
- URL: https://www.notion.so/LifeHub-Projects-292f55156d0d806b91e9d55546d57032

**Extract Database ID:**
- The ID is: `292f55156d0d806b91e9d55546d57032`
- This is your **NOTION_PROJECTS_DB**

### Create Additional Database (Optional)

For Documents/Daily Notes:

1. In Notion, type `/database` → "Table - Full page"
2. Name it: "LifeHub - Documents"
3. Add properties:
   - Name (Title) - auto-created
   - Content (Text) - for note content
   - Date (Date) - for daily notes
   - Type (Select) - daily-note, resource, etc.

4. **Share with Integration:**
   - Click "..." menu in top right
   - Click "Connections"
   - Find "Airtable Sync" integration
   - Click "Connect"

5. **Get Database ID:**
   - Open database as full page
   - Copy URL: `https://notion.so/workspace/DATABASE_ID?v=VIEW_ID`
   - The DATABASE_ID is between workspace and `?v=`
   - This is your **NOTION_DOCUMENTS_DB**

---

## Step 3: Configure Environment Variables (1 minute)

```bash
# Notion Integration Token
export NOTION_TOKEN='secret_PASTE_YOUR_TOKEN_HERE'

# Notion Database IDs
export NOTION_PROJECTS_DB='292f55156d0d806b91e9d55546d57032'
export NOTION_DOCUMENTS_DB='PASTE_YOUR_DOCUMENTS_DB_ID_HERE'

# Airtable Token (already configured)
export AIRTABLE_TOKEN=$(op item get "Airtable Mike Personal" --fields credential --reveal)
```

**Save to shell profile (optional):**
```bash
echo "export NOTION_TOKEN='your-token'" >> ~/.zshrc
echo "export NOTION_PROJECTS_DB='292f55156d0d806b91e9d55546d57032'" >> ~/.zshrc
echo "export NOTION_DOCUMENTS_DB='your-db-id'" >> ~/.zshrc
```

---

## Step 4: Test the Sync (1 minute)

```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts

# Test sync (10 records per table)
python3 sync-airtable-to-notion.py
```

**Expected Output:**
```
🔄 AIRTABLE → NOTION SYNC
================================================================================

🔍 Configuration Check:
   Airtable Base: appx922aa4LURWlMI
   Notion Projects DB: 292f55156d0d806b91e9d55546d57032
   Notion Documents DB: [your-db-id]

📋 Syncing PROJECTS...
   Fetched 10 records from Airtable
   1/10: COMPLETION_SUMMARY... ✅
   2/10: LAUNCH_GUIDE... ✅
   ...

   ✅ Created: 10
   ❌ Errors: 0

================================================================================
✅ SYNC COMPLETE!
================================================================================
```

---

## Step 5: Full Sync (Optional)

Once test succeeds, edit the script to sync all records:

```bash
# Edit sync limits in sync-airtable-to-notion.py
# Change: limit=10
# To: limit=1000

# Then run full sync
python3 sync-airtable-to-notion.py
```

---

## Troubleshooting

### Error: "NOTION_TOKEN not set"
**Solution:** Run the export command from Step 3

### Error: "database_id is invalid"
**Solution:**
1. Make sure database is shared with integration (Step 2)
2. Verify database ID is correct (32 characters, no dashes)

### Error: "Validation failed"
**Solution:** Update Notion API version in script header

### Error: Rate limit exceeded
**Solution:** Script already includes rate limiting (0.35s delay)

---

## Automated Daily Sync (Optional)

Create a cron job or LaunchAgent:

```bash
# Run daily at 2 AM
0 2 * * * cd /Users/mikefinneran/Documents/ObsidianVault/.scripts && /usr/bin/python3 sync-airtable-to-notion.py >> notion-sync.log 2>&1
```

Or use a LaunchAgent (more reliable on macOS):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mikefinneran.notion-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/sync-airtable-to-notion.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/notion-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/mikefinneran/Documents/ObsidianVault/.scripts/notion-sync-error.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>NOTION_TOKEN</key>
        <string>YOUR_TOKEN_HERE</string>
        <key>NOTION_PROJECTS_DB</key>
        <string>292f55156d0d806b91e9d55546d57032</string>
        <key>NOTION_DOCUMENTS_DB</key>
        <string>YOUR_DB_ID_HERE</string>
        <key>AIRTABLE_TOKEN</key>
        <string>YOUR_AIRTABLE_TOKEN</string>
    </dict>
</dict>
</plist>
```

Save to: `~/Library/LaunchAgents/com.mikefinneran.notion-sync.plist`

Load with: `launchctl load ~/Library/LaunchAgents/com.mikefinneran.notion-sync.plist`

---

## Complete Pipeline Status

Once this is running:

```
Obsidian Vault (1,118 files)
          ↓
   [Manual/Scripted Updates]
          ↓
Airtable Knowledge Management (670 records)
          ↓
   [Automated Daily Sync]  ← YOU ARE HERE
          ↓
Notion LifeHub Workspace
          ↓
   [Team Collaboration]
```

---

## Support

**Script Location:** `/Users/mikefinneran/Documents/ObsidianVault/.scripts/sync-airtable-to-notion.py`

**Log Files:**
- `notion-sync-results.json` - Last sync results
- `notion-sync.log` - Cron/LaunchAgent logs
- `notion-sync-error.log` - Error logs

**EA Team:** Available for troubleshooting

---

**Estimated Setup Time:** 5 minutes
**Difficulty:** Easy
**Prerequisites:** Notion account, Airtable data (✅ already migrated)
