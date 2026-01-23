# FlyFlat Notion Integration Setup

**Created**: 2025-10-27
**Purpose**: Sync weekly FlyFlat updates to Notion team workspace

---

## What You Need

### 1. Notion Integration Token
1. Go to https://www.notion.com/my-integrations
2. Click **"+ New integration"**
3. Name: "FlyFlat Weekly Updates"
4. Associated workspace: **Select your fly-flat Notion workspace**
5. Capabilities: Read, Update, Insert content
6. Click **Submit**
7. Copy the **Internal Integration Token** (starts with `secret_`)

### 2. Notion Database ID
1. In Notion, create a database called **"Weekly Updates"**
2. Add these properties:
   - **Week** (Number)
   - **Date** (Date)
   - **Status** (Select: Draft, Sent, Archived)
   - **Project** (Select: FlyFlat)
   - **Hours** (Number)
   - **Revenue** (Number)
   - **Summary** (Text)
   - **Link** (URL - link to Obsidian file)

3. Share the database with your integration:
   - Click "..." menu in top right
   - Click "Add connections"
   - Select "FlyFlat Weekly Updates"

4. Get the Database ID:
   - Copy the database URL
   - Extract ID from: `notion.so/[workspace]/[DATABASE_ID]?v=...`
   - It's a 32-character string with dashes

---

## Setup Instructions

### Step 1: Save Credentials

Run this in terminal:
```bash
# Add to your environment variables
echo 'export NOTION_FLYFLAT_TOKEN="secret_YOUR_TOKEN_HERE"' >> ~/.zshrc
echo 'export NOTION_FLYFLAT_DB_ID="YOUR_DATABASE_ID_HERE"' >> ~/.zshrc
source ~/.zshrc
```

### Step 2: Test Connection

```bash
# Test if Notion API is accessible
curl -X POST https://api.notion.com/v1/databases/$NOTION_FLYFLAT_DB_ID/query \
  -H "Authorization: Bearer $NOTION_FLYFLAT_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json"
```

If you see JSON response (not an error), you're connected! ✅

### Step 3: Install Python Notion Client

```bash
pip3 install notion-client
```

---

## Automatic Sync Setup

I'll create a Python script that:
1. Reads the weekly update from Obsidian
2. Parses the content
3. Creates a Notion page in your database
4. Links back to the Obsidian file

**When ready, tell me:**
- ✅ I have the Notion token
- ✅ I have the Database ID
- ✅ Both are saved in ~/.zshrc

Then I'll build the sync script.

---

## Manual Sync (For Now)

Until auto-sync is ready, here's the workflow:

**Every Friday 9 AM PT (12 PM ET):**
1. Script creates update in `Projects/FlyFlat/Weekly-Updates/YYYY-MM-DD-Week-XX-Update.md`
2. You'll get a notification (Obsidian will show new file)
3. **Fill in the template** with your weekly data
4. **Copy to Notion** manually (or wait for auto-sync)
5. Send to Omar via email/Slack

---

## Update Template Sections

**Required sections to fill:**
- ✅ Completed This Week
- 🎯 In Progress
- 📅 Next Week's Plan
- 💰 Financial Update
- 🚨 Issues & Concerns

**Auto-populated:**
- Date, week number
- Template structure

---

## Notion Database Schema

Your Notion database should have these columns:

| Property | Type | Purpose |
|----------|------|---------|
| **Name** | Title | "Week XX - YYYY-MM-DD" |
| **Week** | Number | Week number (1-52) |
| **Date** | Date | Friday date |
| **Status** | Select | Draft / Sent / Archived |
| **Project** | Select | FlyFlat |
| **Hours** | Number | Total hours this week |
| **Revenue** | Number | Revenue generated |
| **Summary** | Text | Executive summary |
| **Link** | URL | Link to Obsidian file |
| **Full Update** | Rich Text | Full markdown content |

---

## Email Template for Omar

Subject: **FlyFlat Weekly Update - Week [XX]**

Body:
```
Hi Omar,

Here's this week's update for FlyFlat:

📊 Quick Summary:
- Hours: [X]
- Key deliverables: [X completed]
- Status: 🟢 On track

Full update in Notion: [link]

Let me know if you have questions or need anything else!

Best,
Mike
```

---

## Next Steps

**Option 1: Notion Auto-Sync**
- Provide Notion token + Database ID
- I'll build Python script to auto-sync
- Runs automatically after update is created

**Option 2: Manual Copy**
- Keep using generated Obsidian file
- Copy to Notion manually
- Still get automated reminders

**Which do you prefer?**

---

## Troubleshooting

**LaunchAgent not firing?**
```bash
launchctl list | grep flyflat
# Should show: com.flyflat.weeklyupdate

# Check logs:
tail -f /Users/mikefinneran/Documents/ObsidianVault/.scripts/flyflat-update.log
```

**Can't find update file?**
- Location: `Projects/FlyFlat/Weekly-Updates/`
- Filename: `YYYY-MM-DD-Week-XX-Update.md`
- Check Obsidian's file explorer

**Notion connection failing?**
- Verify token in ~/.zshrc
- Check database is shared with integration
- Test with curl command above

---

**Questions? Let me know and I'll help set it up!**
