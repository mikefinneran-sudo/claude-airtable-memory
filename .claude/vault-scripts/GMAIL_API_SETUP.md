# Gmail API Setup for Invoice Fetching

**Purpose:** Access your Gmail to fetch actual subscription invoices and verify tech stack costs

**Time Required:** 5-10 minutes

---

## Step 1: Enable Gmail API

1. Go to **Google Cloud Console**: https://console.cloud.google.com/
2. Select your project (or create new project called "Personal Scripts")
3. Click **Enable APIs and Services**
4. Search for "Gmail API"
5. Click **Enable**

---

## Step 2: Create OAuth Credentials

1. In Google Cloud Console, go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External**
   - App name: "Personal Gmail Scripts"
   - User support email: mike.finneran@gmail.com
   - Developer contact: mike.finneran@gmail.com
   - Scopes: Add Gmail read-only scope
   - Test users: Add mike.finneran@gmail.com
   - Save and continue
4. Back to Create OAuth Client ID:
   - Application type: **Desktop app**
   - Name: "Invoice Fetcher"
   - Click **Create**
5. Click **Download JSON**
6. Save the file as:
   ```
   /Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail_credentials.json
   ```

---

## Step 3: Run the Invoice Fetcher

Once credentials are saved, run:

```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
chmod +x fetch-subscription-invoices.py
python3 fetch-subscription-invoices.py
```

**First run:**
- A browser window will open
- Sign in with mike.finneran@gmail.com
- Click "Allow" to grant read access
- The script will save a token for future use

**Output:**
- Searches last 60 days of invoices
- Creates: `/Users/mikefinneran/Documents/ObsidianVault/subscription-invoices.md`
- Shows actual monthly costs from real invoices

---

## Troubleshooting

### Error: "Access blocked: This app's request is invalid"
- OAuth consent screen not configured
- Add mike.finneran@gmail.com as a test user
- Make sure app is in "Testing" mode (not "Production")

### Error: "credentials.json not found"
- Download OAuth credentials from Google Cloud Console
- Save as `gmail_credentials.json` (not `credentials.json`)
- Check file is in `/Users/mikefinneran/Documents/ObsidianVault/.scripts/`

### No invoices found
- Check date range (currently 60 days)
- Verify email patterns match your invoice emails
- Some services may use different "from" addresses

---

## What This Script Does

**Searches for:**
- Claude/Anthropic invoices
- Perplexity invoices
- Cursor invoices
- Figma invoices
- Gamma invoices
- GitHub invoices
- Vercel invoices
- OpenAI API invoices
- And 7 other services

**Privacy:**
- Read-only access (cannot send emails or modify)
- Runs locally on your machine
- Token stored securely in `.scripts/gmail_token.pickle`
- No data sent to external services

---

## Next Steps After Running

1. Review generated report: `subscription-invoices.md`
2. Compare to `operating-costs.md` for accuracy
3. Update `current-tech-stack.md` with actual invoice amounts
4. Update Dashboard with verified monthly costs

---

**Last Updated:** 2025-10-29
**Estimated Setup Time:** 5-10 minutes
**Run Frequency:** Monthly (to verify costs)
