# Notion Sync Setup Guide

**Time to complete:** 15-20 minutes
**What you'll get:** Mobile access to your vault via Notion

---

## Step 1: Get Notion API Token (5 min)

1. Go to https://www.notion.com/my-integrations
2. Click **"+ New integration"**
3. Name it: "LifeHub Sync"
4. Select your workspace
5. Click **"Submit"**
6. Copy the **Internal Integration Token** (starts with `secret_`)

---

## Step 2: Save API Token (1 min)

```bash
# Save token to file (replace YOUR_TOKEN with actual token)
echo "secret_YOUR_TOKEN_HERE" > ~/.lifehub-notion-token
chmod 600 ~/.lifehub-notion-token
```

---

## Step 3: Create Notion Databases (5-10 min)

You need to create these databases in Notion:

### Database 1: Projects
1. In Notion, create a new page called "LifeHub Projects"
2. Type `/database` and select "Table - Inline"
3. Add these properties:
   - Name (Title) - default
   - Status (Select): planning, active, paused, completed, archived
   - Priority (Select): high, medium, low
   - Deadline (Date)
   - Progress (Number)
   - Start Date (Date)
   - Owner (Text)
   - Category (Select): business, product, personal, learning
   - Client (Text)
   - Revenue Potential (Number)

### Database 2: Clients (Optional)
1. Create page "LifeHub Clients"
2. Type `/database` and select "Table - Inline"
3. Add properties:
   - Name (Title)
   - Status (Select): lead, active, paused, churned
   - Industry (Text)
   - Company Size (Text)
   - Lifetime Value (Number)
   - Monthly Value (Number)
   - First Contact (Date)
   - Last Contact (Date)

### Database 3: Daily Notes (Optional)
1. Create page "LifeHub Daily"
2. Type `/database` and select "Table - Inline"
3. Add properties:
   - Date (Date)
   - Day of Week (Text)
   - Energy Level (Select): 1-5
   - Mood (Select)

---

## Step 4: Get Database IDs (5 min)

For each database:

1. Click the **"..." menu** (top right)
2. Select **"Copy link to view"**
3. Extract the ID from the URL

**URL format:**
```
https://notion.so/DATABASE_ID?v=VIEW_ID
                ^^^^^^^^^^^^
                This is your Database ID
```

**Example:**
```
https://notion.so/abc123def456?v=xyz789
                 ^^^^^^^^^^^
                 Database ID = abc123def456
```

---

## Step 5: Share Databases with Integration (IMPORTANT!)

For EACH database:

1. Open the database in Notion
2. Click **"..."** menu (top right)
3. Select **"Connections"** → **"Connect to"**
4. Find and select **"LifeHub Sync"** (your integration)
5. Confirm

**If you skip this, sync will fail!**

---

## Step 6: Configure Sync Script (5 min)

Edit the config file:

```bash
nano /Users/mikefinneran/Documents/ObsidianVault/.scripts/notion-sync-config.json
```

Update with your database IDs:

```json
{
  "mappings": [
    {
      "obsidian_folder": "Projects/_Active",
      "notion_database_id": "YOUR_PROJECTS_DATABASE_ID",
      "type_filter": "project",
      "property_mapping": {
        "status": "Status",
        "priority": "Priority",
        "deadline": "Deadline",
        "progress": "Progress",
        "start-date": "Start Date",
        "owner": "Owner",
        "category": "Category",
        "client": "Client",
        "revenue-potential": "Revenue Potential"
      }
    },
    {
      "obsidian_folder": "Clients",
      "notion_database_id": "YOUR_CLIENTS_DATABASE_ID",
      "type_filter": "client",
      "property_mapping": {
        "status": "Status",
        "industry": "Industry",
        "company-size": "Company Size",
        "lifetime-value": "Lifetime Value",
        "monthly-value": "Monthly Value",
        "first-contact": "First Contact",
        "last-contact": "Last Contact"
      }
    }
  ]
}
```

---

## Step 7: Test Sync (2 min)

```bash
# Test without actually syncing (dry run)
python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/sync_to_notion.py --dry-run

# If that looks good, do real sync
python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/sync_to_notion.py
```

**Check Notion** - You should see your projects appear!

---

## Step 8: Automate Sync (Optional)

Add to crontab to run automatically:

```bash
# Edit crontab
crontab -e

# Add this line (sync every evening at 8 PM)
0 20 * * * python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/sync_to_notion.py >> /Users/mikefinneran/Documents/ObsidianVault/.scripts/notion-sync-cron.log 2>&1
```

Or create a LaunchAgent for more reliable scheduling.

---

## Troubleshooting

### "Token file not found"
```bash
# Check file exists
cat ~/.lifehub-notion-token

# If not, create it
echo "secret_YOUR_TOKEN" > ~/.lifehub-notion-token
```

### "Unauthorized" or "Object not found"
- Make sure you **shared the database** with your integration (Step 5)
- Check database ID is correct
- Verify token is valid

### "Property not found"
- Property names must match exactly (case-sensitive)
- Check spelling in both Notion and config file

### No items syncing
- Check `type` frontmatter in your Obsidian notes
- Verify folder paths in config
- Use `--dry-run` to see what would sync

---

## Usage

### Manual Sync
```bash
python3 ~/.scripts/sync_to_notion.py
```

### Sync Specific Folder
```bash
python3 ~/.scripts/sync_to_notion.py --folder Projects
```

### Test Without Syncing
```bash
python3 ~/.scripts/sync_to_notion.py --dry-run
```

---

## Benefits Once Set Up

✅ **Mobile access** - Check projects on your phone via Notion app
✅ **Team collaboration** - Share databases with team members
✅ **Client portals** - Share specific views with clients
✅ **Web access** - Access anywhere with internet
✅ **Automatic backup** - Your data in two places

---

**Need help?** Check sync logs:
```bash
tail -f ~/.scripts/notion-sync.log
```

---

*Setup guide created: 2025-10-21*
