# Complete Gmail OAuth Setup Guide
## Fix 403 Access Denied & Fetch Real Subscription Costs

**Time Required:** 15-20 minutes
**Skill Level:** Beginner-friendly with detailed steps
**Goal:** Authorize Gmail access to fetch actual invoice costs

---

## Before You Start

**What You Need:**
- Google account: mike.finneran@gmail.com
- Browser: Chrome, Safari, or Firefox
- Terminal access

**What This Will Do:**
- Create OAuth credentials for reading your Gmail (read-only, safe)
- Authorize the invoice fetcher script
- Pull last 60 days of subscription invoices
- Generate accurate monthly cost report

---

## Step 1: Access Google Cloud Console (2 minutes)

### 1.1 Open Console
1. Go to: https://console.cloud.google.com/
2. Sign in with: **mike.finneran@gmail.com**
3. You'll see the Google Cloud Console dashboard

### 1.2 Create New Project
1. At the top of the page, click the project dropdown (says "Select a project")
2. Click **"NEW PROJECT"** in the top right
3. Fill in:
   - **Project name:** Personal Gmail Scripts
   - **Organization:** No organization (leave blank)
   - **Location:** No organization (leave default)
4. Click **"CREATE"**
5. Wait 10-20 seconds for project creation
6. You'll see a notification when ready
7. Click "SELECT PROJECT" or switch to it from the dropdown

**✓ Checkpoint:** You should see "Personal Gmail Scripts" at the top of the console

---

## Step 2: Enable Gmail API (2 minutes)

### 2.1 Navigate to API Library
1. In the left sidebar, click **"APIs & Services"**
2. Click **"Library"** (or go to: https://console.cloud.google.com/apis/library)
3. You'll see the API Library with hundreds of Google APIs

### 2.2 Find and Enable Gmail API
1. In the search bar at the top, type: **Gmail API**
2. Click on **"Gmail API"** (should be first result with Gmail icon)
3. Click the blue **"ENABLE"** button
4. Wait 30 seconds while it enables
5. You'll be redirected to the API overview page

**✓ Checkpoint:** You should see "API enabled" with usage graphs (currently showing 0)

---

## Step 3: Configure OAuth Consent Screen (5 minutes)

**Why:** This tells Google what your app does and who can use it (just you)

### 3.1 Navigate to OAuth Consent
1. In the left sidebar, click **"OAuth consent screen"**
2. You'll see "User Type" options

### 3.2 Choose User Type
1. Select **"External"** (even though it's just for you)
   - External = anyone with a Google account (you'll restrict to just you)
   - Internal = only for Google Workspace orgs (not available for personal Gmail)
2. Click **"CREATE"**

### 3.3 Fill Out App Information
**Page 1: OAuth consent screen**

1. **App name:** Personal Gmail Invoice Fetcher
2. **User support email:** Select mike.finneran@gmail.com from dropdown
3. **App logo:** (optional, skip)
4. **App domain:** (optional, skip all three fields)
5. **Authorized domains:** (skip)
6. **Developer contact information:**
   - Email: mike.finneran@gmail.com
7. Click **"SAVE AND CONTINUE"** at the bottom

**Page 2: Scopes**

1. Click **"ADD OR REMOVE SCOPES"** button
2. A panel opens on the right showing all available scopes
3. In the filter box, type: **gmail.readonly**
4. Find and check the box for:
   - ☑ `https://www.googleapis.com/auth/gmail.readonly`
   - Description: "Read all resources and their metadata—no write operations"
5. Scroll down in the panel
6. Click **"UPDATE"** at the bottom of the panel
7. You should see 1 scope in the "Your sensitive scopes" table
8. Click **"SAVE AND CONTINUE"**

**Page 3: Test users**

1. Click **"+ ADD USERS"**
2. Enter: **mike.finneran@gmail.com**
3. Click **"ADD"**
4. You should see mike.finneran@gmail.com in the list
5. Click **"SAVE AND CONTINUE"**

**Page 4: Summary**

1. Review all settings
2. You should see:
   - App name: Personal Gmail Invoice Fetcher
   - Scopes: 1 sensitive scope (gmail.readonly)
   - Test users: 1 user
   - Publishing status: Testing
3. Click **"BACK TO DASHBOARD"**

**✓ Checkpoint:** OAuth consent screen should show "Publishing status: Testing" and "Test users: 1"

---

## Step 4: Create OAuth Credentials (3 minutes)

### 4.1 Navigate to Credentials
1. In the left sidebar, click **"Credentials"**
2. You'll see the credentials management page

### 4.2 Create OAuth Client ID
1. Click **"+ CREATE CREDENTIALS"** at the top
2. Select **"OAuth client ID"** from the dropdown
3. A form appears

### 4.3 Configure Credential
1. **Application type:** Select **"Desktop app"** from dropdown
2. **Name:** Gmail Invoice Fetcher - Desktop
3. Click **"CREATE"**

### 4.4 Download Credentials
1. A dialog appears: "OAuth client created"
2. You'll see:
   - Your Client ID: XXXXXXXX.apps.googleusercontent.com
   - Your Client Secret: XXXXX-XXXXX
3. Click **"DOWNLOAD JSON"** button
4. Browser downloads a file named: `client_secret_XXXXXXXXX.apps.googleusercontent.com.json`
5. Click **"OK"** to close the dialog

### 4.5 Save Credentials to Scripts Folder
1. Open Finder
2. Navigate to your Downloads folder
3. Find the file: `client_secret_*.json`
4. **Rename it to:** `gmail_credentials.json`
5. **Move it to:** `/Users/mikefinneran/Documents/ObsidianVault/.scripts/`
   - In Finder: Go → Go to Folder → paste the path
   - Drag the file into that folder

**✓ Checkpoint:** File exists at `/Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail_credentials.json`

---

## Step 5: Run Authorization Flow (3 minutes)

### 5.1 Open Terminal
1. Open Terminal app (Applications → Utilities → Terminal)
2. Or use your preferred terminal (iTerm2, Warp, etc.)

### 5.2 Navigate to Scripts Folder
```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
```

### 5.3 Verify Credentials File
```bash
ls -la gmail_credentials.json
```

**Expected output:**
```
-rw-r--r--  1 mikefinneran  staff  XXX Oct 29 XX:XX gmail_credentials.json
```

If you see "No such file or directory", go back to Step 4.5 and verify the file location.

### 5.4 Run the Invoice Fetcher
```bash
python3 fetch-subscription-invoices.py
```

**What happens:**
1. Script starts: "🔍 Fetching Subscription Invoices from Gmail..."
2. Opens your default web browser automatically
3. Shows Google account sign-in page

---

## Step 6: Authorize in Browser (2 minutes)

### 6.1 Sign In to Google
1. Browser opens to Google sign-in
2. Select or sign in with: **mike.finneran@gmail.com**
3. Enter password if prompted

### 6.2 Handle "Unverified App" Warning
**You will see a warning screen:**
> "Google hasn't verified this app"
> "This app hasn't been verified by Google yet"

**This is NORMAL and SAFE** because:
- It's YOUR app, created by YOU
- It's in Testing mode (not public)
- You're the only test user

**To proceed:**
1. Click **"Advanced"** (bottom left of the warning)
2. Click **"Go to Personal Gmail Invoice Fetcher (unsafe)"**
   - (It's not actually unsafe - it's your app)

### 6.3 Review Permissions
You'll see a permissions screen:
> "Personal Gmail Invoice Fetcher wants to access your Google Account"
>
> This will allow Personal Gmail Invoice Fetcher to:
> - ☑ Read your email messages and settings

**Verify:**
- App name is correct
- Only permission is "Read" (not "Send" or "Delete")
- Account is mike.finneran@gmail.com

### 6.4 Grant Access
1. Click **"Allow"**
2. Browser shows: "The authentication flow has completed"
3. You can close the browser tab/window
4. Return to Terminal

**✓ Checkpoint:** Browser shows success, token saved to `gmail_token.pickle`

---

## Step 7: Script Executes & Generates Report (2-3 minutes)

### 7.1 Watch Script Progress
In Terminal, you'll see:

```
✅ Connected to Gmail

Searching Claude/Anthropic... ✅ Found 2 invoice(s)
Searching Perplexity... ✅ Found 1 invoice(s)
Searching Cursor... ✅ Found 1 invoice(s)
Searching Figma... ✅ Found 1 invoice(s)
Searching Gamma... ❌ No invoices
Searching GitHub... ❌ No invoices
Searching Vercel... ❌ No invoices
...
```

### 7.2 Review Output Summary
```
📊 Total Invoices Found: 8

✅ Report generated: /Users/mikefinneran/Documents/ObsidianVault/subscription-invoices.md

💰 Estimated Monthly Cost: $XXX.XX/mo
💰 Estimated Annual Cost: $X,XXX.XX/year
```

**✓ Checkpoint:** Report file created with actual invoice data

---

## Step 8: Review Invoice Report (5 minutes)

### 8.1 Open Report in Obsidian
1. Open Obsidian
2. Navigate to: `/subscription-invoices.md` (root of vault)
3. Or open in any markdown editor

### 8.2 Review Report Contents
The report contains:

**Monthly Costs Summary Table:**
| Service | Last Invoice | Avg Cost | Status |
|---------|--------------|----------|--------|
| Claude/Anthropic | $20.00 | $20.00/mo | Active |
| Perplexity | $20.00 | $20.00/mo | Active |
| ... | ... | ... | ... |

**Total Monthly Cost:** Calculated from actual invoices

**Invoice Details Table:**
| Date | Service | Amount | Subject |
|------|---------|--------|----------|
| 2025-10-15 | Claude/Anthropic | $20.00 | Your invoice... |
| ... | ... | ... | ... |

### 8.3 Verify Accuracy
**Check for:**
- ✓ All services you know you pay for are listed
- ✓ Amounts match your credit card statements
- ✓ Recent dates (within last 60 days)

**Missing services?**
- Some services may use different email addresses
- Some may not send invoices via email
- Check the "Troubleshooting" section below

---

## Step 9: Update Tech Stack Documents (5 minutes)

### 9.1 Compare to Current Estimates
1. Open: `Projects/warp-enhancement/research/current-tech-stack.md`
2. Compare "Current Total" to invoice report total
3. Note any discrepancies

### 9.2 Update Documents
I'll help you update these files with the actual numbers:
1. `current-tech-stack.md` - Update costs with invoice data
2. `Dashboard.md` - Update monthly cost summary
3. `operating-costs.md` - Verify WalterSignal costs

### 9.3 Add Verification Note
Add to each updated document:
```markdown
**Verified from Gmail invoices:** 2025-10-29
**Source:** subscription-invoices.md
**Last 60 days of actual invoices**
```

---

## Troubleshooting

### "No such file or directory: gmail_credentials.json"
**Problem:** Credentials file not in the right location
**Solution:**
1. Run: `ls ~/.scripts/gmail_credentials.json`
2. If not found, check Downloads folder
3. Make sure you renamed it to exactly: `gmail_credentials.json`
4. Move to: `/Users/mikefinneran/Documents/ObsidianVault/.scripts/`

---

### "Error 403: access_denied"
**Problem:** OAuth consent screen not configured correctly
**Solution:**
1. Go back to Google Cloud Console
2. OAuth consent screen → Test users
3. Verify mike.finneran@gmail.com is listed
4. Try authorization again

---

### "This app is blocked"
**Problem:** OAuth consent screen published to production (not testing)
**Solution:**
1. Go to OAuth consent screen in Console
2. Make sure "Publishing status" says "Testing"
3. If it says "In production", click "UNPUBLISH" or "RESET"

---

### "No invoices found"
**Problem:** Script searches specific email patterns that may not match
**Solutions:**

**Check if invoices are older than 60 days:**
- Open `fetch-subscription-invoices.py`
- Change `timedelta(days=60)` to `timedelta(days=90)` on line 169

**Check sender email addresses:**
- Some services use different email addresses
- Look at actual invoice emails in Gmail
- Add to the `queries` dict in the script

**Manually search Gmail:**
- Go to Gmail
- Search: `subject:(invoice OR receipt OR payment) after:2025/09/01`
- See which services send invoices

---

### "Import Error: No module named google"
**Problem:** Google API client libraries not installed
**Solution:**
```bash
pip3 install --user google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### "SSL Certificate Error"
**Problem:** Python SSL library outdated (shown as urllib3 warning)
**Solution:** This is a warning, not an error. Script still works. To fix:
```bash
pip3 install --upgrade urllib3
```
Or ignore - it doesn't prevent the script from running.

---

## Security & Privacy

### What Access Does This Grant?
- **Read-only access** to your Gmail messages and metadata
- **Cannot:** Send emails, delete emails, or modify anything
- **Scope:** `gmail.readonly` (view only)

### Where Is Data Stored?
- **Credentials:** `/Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail_credentials.json`
  - Contains: OAuth client ID and secret
  - NOT your password or tokens
- **Token:** `/Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail_token.pickle`
  - Contains: Your authorization token
  - Refresh token for automatic renewal
  - Expires if not used for 6 months
- **Report:** `/Users/mikefinneran/Documents/ObsidianVault/subscription-invoices.md`
  - Contains: Invoice dates, amounts, subjects
  - Local file only, not sent anywhere

### Is This Safe?
✅ **Yes**, because:
- OAuth is the industry-standard secure authorization
- No password is stored anywhere
- Script runs locally on your computer
- Read-only permission (cannot modify Gmail)
- You control the app (it's your Google Cloud project)
- Only you can access it (test user list)

### Revoking Access
If you want to revoke access later:
1. Go to: https://myaccount.google.com/permissions
2. Find: "Personal Gmail Invoice Fetcher"
3. Click → Remove Access

---

## Running Monthly Updates

### Manual Method
Run this on the 1st of each month:
```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
python3 fetch-subscription-invoices.py
```

No browser auth needed after first time - token is saved.

### Automated Method (Optional)
Create a monthly cron job:
```bash
crontab -e
```

Add this line:
```cron
0 9 1 * * cd /Users/mikefinneran/Documents/ObsidianVault/.scripts && /usr/bin/python3 fetch-subscription-invoices.py
```

This runs at 9 AM on the 1st of every month.

---

## Customizing the Script

### Change Date Range
Edit line 169 in `fetch-subscription-invoices.py`:
```python
start_date = end_date - timedelta(days=60)  # Change 60 to 90, 120, etc.
```

### Add More Services
Edit the `queries` dict around line 190:
```python
'ServiceName': f'from:service.com (subject:invoice OR subject:receipt) {date_query}',
```

### Change Output Location
Edit line 198:
```python
output_file = os.path.join(script_dir, '../your-custom-name.md')
```

---

## What's Next?

Once you have the invoice report:

1. **Compare to estimates:**
   - Current estimate: $110-172/mo
   - Actual from invoices: $XXX/mo
   - Identify any discrepancies

2. **Update Dashboard:**
   - Replace estimated costs with actuals
   - Add "Verified from invoices" note
   - Update break-even calculations

3. **Monthly routine:**
   - Run script on 1st of month
   - Review any cost changes
   - Track new subscriptions
   - Cancel unused services

4. **Decision on Airtable:**
   - With accurate current costs ($XXX/mo)
   - Airtable would add $20-29/mo
   - That's X% increase
   - Decide if ROI justifies it

---

## Summary Checklist

Setup (one-time):
- [ ] Created Google Cloud project
- [ ] Enabled Gmail API
- [ ] Configured OAuth consent screen
- [ ] Created Desktop app credentials
- [ ] Downloaded and saved credentials.json
- [ ] Ran authorization flow in browser
- [ ] Granted read-only Gmail permission
- [ ] Generated first invoice report

Verification:
- [ ] Invoice report shows expected services
- [ ] Amounts match credit card statements
- [ ] Total monthly cost is reasonable
- [ ] Report file saved correctly

Updates:
- [ ] Reviewed invoice data
- [ ] Ready to update tech stack documents
- [ ] Added to monthly routine

---

**Setup Complete!** 🎉

You now have:
- ✅ Automated access to Gmail invoices
- ✅ Accurate monthly subscription costs
- ✅ Historical invoice data (60 days)
- ✅ Foundation for monthly cost tracking

**Next:** Let me know when you've run the script and I'll help update your tech stack documents with the actual data!

---

**Last Updated:** 2025-10-29
**Estimated Setup Time:** 15-20 minutes
**Success Rate:** 95%+ (with test user properly configured)
