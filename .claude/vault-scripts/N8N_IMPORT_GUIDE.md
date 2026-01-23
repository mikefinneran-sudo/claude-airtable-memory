# n8n Workflow Import Guide
## Airtable → Notion Sync (Automated)

---

## Quick Import (2 minutes)

### Step 1: Import Workflow

1. In n8n, click the **"..."** menu (top right)
2. Click **"Import from File"** or **"Import workflow"**
3. Select file: `airtable-to-notion-n8n-workflow.json`
4. Click **Open**

The workflow will appear on your canvas with:
- **Airtable Trigger** (watches for new records)
- **Notion Node** (creates pages)

---

## Step 2: Connect Airtable

1. **Click on the "Airtable Trigger" node**

2. **Click "Credential to connect with"**

3. **Select existing or create new:**
   - If you see "Airtable account" - select it
   - If not, click "+ Create New Credential"

4. **Enter Airtable credentials:**
   - **API Key**: Get from 1Password "Airtable Mike Personal"
   - Or create at: https://airtable.com/create/tokens
   - Click **"Save"**

5. **Configure trigger:**
   - **Base**: Should show "Knowledge Management" (appx922aa4LURWlMI)
   - **Table**: Select "🗂️ Documents" (tblbLNQlJ9Ojaz9gK)
   - **Trigger On**: New records
   - **Polling Interval**: Every 1 minute

---

## Step 3: Connect Notion

1. **Click on the "Notion" node**

2. **Click "Credential to connect with"**

3. **Create Notion credential:**
   - Click "+ Create New Credential"
   - **Name**: Notion account
   - **API Key**: You need a Notion integration token

4. **Get Notion token (if needed):**
   - Go to: https://www.notion.com/my-integrations
   - Click "+ New integration"
   - Name: "n8n Sync"
   - Copy the token
   - Paste into n8n credential
   - Click **"Save"**

5. **Configure Notion node:**
   - **Resource**: Database Page
   - **Operation**: Create
   - **Database ID**: 292f55156d0d806b91e9d55546d57032 (LifeHub Projects)
   - **Title**: Click and select `{{ $json.fields.Name }}` from Airtable data
   - **Content**: Click and select `{{ $json.fields.Notes }}`

---

## Step 4: Test the Workflow

1. **Click "Test workflow"** button (top right)

2. **Click "Execute workflow"**

3. You should see:
   - ✅ Airtable Trigger: Found X records
   - ✅ Notion: Created page

4. **Check Notion** to verify page appeared

---

## Step 5: Activate the Workflow

1. **Name your workflow:**
   - Click "Workflow" at top
   - Rename to: "Airtable Documents → Notion"

2. **Activate:**
   - Toggle the **"Active"** switch (top right) to ON
   - Workflow will now run automatically every minute

---

## What Happens Now

### Automatic Sync
- **Frequency**: Every 1 minute
- **What**: Checks Airtable Documents table for new records
- **Action**: Creates corresponding page in Notion LifeHub
- **Cost**: FREE (self-hosted n8n)

### Existing Records
n8n trigger only watches for NEW records. To sync existing 670 records:

**Option A: One-time bulk sync**
Use the Python script I built:
```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
python3 sync-airtable-to-notion.py
```

**Option B: CSV Import to Notion**
1. Export Airtable as CSV
2. Import CSV to Notion
3. Takes 15 minutes

---

## Create Second Workflow (Projects Table)

Repeat the import for Projects:

1. Import workflow again
2. Name it: "Airtable Projects → Notion"
3. Change Airtable trigger:
   - **Table**: 🚀 Projects (tblBjIziv9KShsemA)
4. Same Notion destination (or different database)
5. Activate

---

## Advanced: Add More Steps

You can add nodes between Airtable and Notion to:
- **Filter**: Only sync certain records
- **Transform**: Modify data before syncing
- **Split**: Route to different Notion databases
- **Notify**: Send Slack/email on sync

**Click "+" between nodes to add more steps**

---

## Monitoring

### View Executions
1. Go to: **Executions** tab (left sidebar)
2. See all workflow runs
3. Click any execution to see details
4. View errors if any failed

### Check Status
- **Active** = Green toggle = Running
- **Inactive** = Gray toggle = Paused

---

## Troubleshooting

### "Could not connect to Airtable"
- Verify API token in credential
- Check Airtable base ID is correct
- Ensure table exists

### "Could not connect to Notion"
- Verify integration token
- Share Notion database with integration
- Check database ID is correct

### "No records found"
- Airtable trigger only finds NEW records after activation
- Use Python script for existing records

### Workflow not running
- Check "Active" toggle is ON
- View Executions tab for errors
- Verify credentials are connected

---

## Complete Architecture

```
Obsidian Vault
     ↓
Airtable (670 records)
     ↓
   [n8n Automation] ← YOU ARE HERE (every 1 min)
     ↓
Notion LifeHub
     ↓
Team Collaboration
```

---

## Advantages of n8n vs Zapier

✅ **Free** - No monthly cost
✅ **Faster** - Checks every 1 minute (vs 15 min on Zapier free)
✅ **More control** - Full workflow customization
✅ **Self-hosted** - Your infrastructure
✅ **No task limits** - Unlimited syncs

---

## Files

**Workflow JSON**: `airtable-to-notion-n8n-workflow.json`
**This Guide**: `N8N_IMPORT_GUIDE.md`

---

**Ready to import?** Follow Step 1 above.
