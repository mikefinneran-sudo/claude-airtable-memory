# FlyFlat Notion Sync - Quick Setup

**You already have:** ✅ Notion sync script + token

**Just need:** The Database ID for your FlyFlat weekly updates

---

## Steps (5 minutes)

### 1. In your FlyFlat Notion workspace:

Create a database called **"Weekly Updates"** with these properties:

| Property | Type | Description |
|----------|------|-------------|
| **Name** | Title | Auto-filled with "Week XX - Date" |
| **Week** | Number | Week number (1-52) |
| **Date** | Date | Friday date |
| **Status** | Select | Options: Draft, Sent, Archived |
| **Project** | Select | Fixed value: FlyFlat |
| **Recipient** | Text | Fixed value: Omar |

### 2. Share database with integration:

- Click **"..."** menu (top right of database)
- Click **"Add connections"**
- Select **"LifeHub Sync"** (or your integration name)

### 3. Get Database ID:

- Copy the database URL
- It looks like: `notion.so/[workspace]/[DATABASE_ID]?v=...`
- The DATABASE_ID is a 32-character string with dashes
- Example: `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6`

### 4. Update config:

Open: `.scripts/notion-sync-config.json`

Replace this line:
```json
"notion_database_id": "REPLACE_WITH_FLYFLAT_UPDATES_DB_ID",
```

With your actual ID:
```json
"notion_database_id": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
```

Save the file.

### 5. Test it:

```bash
# Create a test update manually
cd /Users/mikefinneran/Documents/ObsidianVault
.scripts/create_flyflat_update.sh

# It will:
# 1. Create the update in Projects/FlyFlat/Weekly-Updates/
# 2. Auto-sync to Notion
# 3. Show success message
```

---

## How It Works

**Every Friday 9 AM PT (12 PM ET):**

1. LaunchAgent runs `create_flyflat_update.sh`
2. Script creates markdown file with template
3. Script auto-syncs to Notion
4. You get notification in Obsidian
5. Fill in the template
6. Re-sync with: `python3 .scripts/sync_to_notion.py --folder "Projects/FlyFlat/Weekly-Updates"`
7. Send link to Omar

---

## Notion Database Properties Explained

**Automatically filled from Obsidian:**
- **Week**: From frontmatter `week: 43`
- **Date**: From frontmatter `date: 2025-10-27`
- **Status**: From frontmatter `status: draft`
- **Project**: From frontmatter `project: FlyFlat`
- **Recipient**: From frontmatter `recipient: Omar`

**Full content**: The entire markdown is synced as the page body

---

## Manual Sync Anytime

```bash
# Sync all FlyFlat updates
python3 .scripts/sync_to_notion.py --folder "Projects/FlyFlat/Weekly-Updates"

# Sync everything
python3 .scripts/sync_to_notion.py

# Dry run (see what would sync)
python3 .scripts/sync_to_notion.py --dry-run
```

---

## Troubleshooting

**"Database ID not found"**
- Make sure you shared the database with your integration
- Check the ID has no spaces or extra characters

**"Token invalid"**
- Your token is at `~/.lifehub-notion-token`
- Re-run: `.scripts/setup-notion-sync.sh` to update it

**"Sync failed"**
- Check logs: `.scripts/notion-sync.log`
- Test connection: `python3 .scripts/sync_to_notion.py --dry-run`

---

**Ready? Just paste your Database ID into the config and you're done!**
