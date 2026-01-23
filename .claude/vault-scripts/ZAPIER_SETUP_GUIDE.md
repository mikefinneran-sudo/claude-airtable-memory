# Zapier Setup Guide: Airtable → Notion Sync
## Step-by-Step Setup (10 minutes)

---

## Step 1: Create Zapier Account

**Go to:** https://zapier.com/sign-up

- Sign up with your email: mike.finneran@gmail.com
- Confirm email
- Choose plan:
  - **Free:** 100 tasks/month (good for testing)
  - **Starter:** $19.99/month, 750 tasks/month (recommended)

---

## Step 2: Create New Zap

1. Click **"Create Zap"** button (top left or center of dashboard)
2. You'll see: **Trigger → Action** workflow builder

---

## Step 3: Set Up Trigger (Airtable)

### 3.1: Choose Trigger App
- Search: **"Airtable"**
- Click on Airtable

### 3.2: Choose Trigger Event
- Select: **"New Record in View"**
- Click **Continue**

### 3.3: Connect Airtable Account
- Click **"Sign in to Airtable"**
- You'll be redirected to Airtable
- Click **"Grant access"**
- You'll return to Zapier

### 3.4: Configure Trigger
Fill in these details:

**Base:** Knowledge Management
- (Select from dropdown - should show: appx922aa4LURWlMI)

**Table:** Choose one to start:
- **🗂️ Documents** (for daily notes and resources)
- OR **🚀 Projects** (for project files)

**View:** Grid view (default view)

**Trigger Column:** (leave empty for all new records)

Click **Continue**

### 3.5: Test Trigger
- Click **"Test trigger"**
- Zapier will fetch a sample record from Airtable
- You should see record data appear
- Click **Continue**

---

## Step 4: Set Up Action (Notion)

### 4.1: Choose Action App
- Click **"+"** to add action
- Search: **"Notion"**
- Click on Notion

### 4.2: Choose Action Event
- Select: **"Create Database Item"**
- Click **Continue**

### 4.3: Connect Notion Account
- Click **"Sign in to Notion"**
- You'll be redirected to Notion
- Select your workspace
- Click **"Select pages"**
- Check: **LifeHub - Projects** (or your database)
- Click **"Allow access"**
- You'll return to Zapier

### 4.4: Configure Action

**Database:** LifeHub - Projects
- (Select from dropdown)

**Page Content:**

Map Airtable fields to Notion:

1. **Title/Name:**
   - Click field → "Custom"
   - Select: **"Name"** (from Airtable trigger data)

2. **Content (if your database has content property):**
   - Click field
   - Select: **"Notes"** (from Airtable trigger data)

3. **Any other properties you want to sync**

Click **Continue**

### 4.5: Test Action
- Click **"Test step"**
- Zapier will create a test record in Notion
- Check Notion to verify it appeared
- Click **Continue**

---

## Step 5: Enable the Zap

1. **Name your Zap:**
   - Click "Untitled Zap" at top
   - Name it: "Airtable Documents → Notion"

2. **Turn it on:**
   - Toggle switch to **ON** (top right)
   - Click **"Publish"**

---

## Step 6: Create Second Zap (For Projects Table)

Repeat Steps 2-5 for the Projects table:

- **Trigger:** Airtable → 🚀 Projects table
- **Action:** Notion → Create in LifeHub Projects (or separate database)
- **Name:** "Airtable Projects → Notion"

---

## What Happens Now

### Automatic Sync
- **When:** Any new record is added to Airtable
- **What:** Zapier creates it in Notion within 1-15 minutes
- **Frequency:** Real-time (paid plan) or every 15 min (free plan)

### Existing Records
Zapier only syncs **NEW** records going forward. To sync existing 670 records:

**Option A: Bulk Import (Manual)**
1. Export from Airtable as CSV
2. Import CSV to Notion database
3. Takes 15 minutes

**Option B: Trigger Re-sync**
1. Add a new field to each record in Airtable
2. Zapier detects as "new" and syncs
3. Takes a few hours (automated)

**Option C: Use Python script for one-time bulk sync**
- I already built this: `sync-airtable-to-notion.py`
- Creates Notion integration
- Syncs all 670 records
- Takes 5 minutes

---

## Monitoring & Management

### Check Zap History
- Go to: https://zapier.com/app/history
- See all synced records
- View any errors

### Pause/Resume Zap
- Go to: https://zapier.com/app/zaps
- Toggle any Zap on/off

### Edit Zap
- Click Zap name
- Click "Edit"
- Modify trigger or action

---

## Pricing

### Free Plan
- 100 tasks/month
- 5 Zaps
- 15-minute check interval
- Good for: Testing

### Starter Plan ($19.99/month)
- 750 tasks/month
- 20 Zaps
- 15-minute check interval
- Good for: Production

### Professional Plan ($49/month)
- 2,000 tasks/month
- Unlimited Zaps
- 2-minute check interval
- Multi-step Zaps
- Good for: Heavy usage

**Recommendation:** Start with Free to test, upgrade to Starter for production

---

## Alternative: Bulk Sync Existing Records

If you want to sync the 670 existing records right now:

### Quick Option: CSV Import

1. **Export from Airtable:**
```bash
# Open Airtable
# Click "..." on Documents table
# Click "Download CSV"
# Repeat for Projects table
```

2. **Import to Notion:**
```bash
# Open Notion database
# Click "..." menu
# Click "Import"
# Select "CSV"
# Upload the CSV file
# Map columns
# Click "Import"
```

This takes 15 minutes total and syncs everything.

---

## Troubleshooting

### "Can't find my Airtable base"
- Make sure you granted Zapier access to the correct Airtable account
- Refresh the connection

### "Can't find my Notion database"
- Make sure you selected the database when connecting Notion
- Try disconnecting and reconnecting Notion

### "Zap isn't triggering"
- Check Zap is turned ON
- Verify trigger conditions are met
- Check Zap History for errors

### "Records not appearing in Notion"
- Check Notion database properties match Airtable fields
- Look in Zap History for failed tasks
- Verify Notion database permissions

---

## Complete Architecture

Once Zapier is running:

```
Obsidian Vault
     ↓
Airtable (670 records) ← Manual updates
     ↓
   [Zapier Automation] ← YOU ARE HERE
     ↓
Notion LifeHub
     ↓
Team Collaboration
```

---

## Summary

**What Zapier Does:**
- Watches Airtable for new records
- Automatically creates them in Notion
- Runs every 1-15 minutes
- Handles errors and retries

**What You Need to Do:**
1. Create Zapier account ✓
2. Connect Airtable ✓
3. Connect Notion ✓
4. Configure field mappings ✓
5. Turn on Zap ✓
6. (Optional) Bulk import existing 670 records

**Time:** 10 minutes for setup, 15 minutes for bulk import

---

**Ready to start? Go to:** https://zapier.com/sign-up
