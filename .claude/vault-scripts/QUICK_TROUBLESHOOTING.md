# Gmail OAuth - Quick Troubleshooting Reference

**For detailed guide, see:** `GMAIL_OAUTH_COMPLETE_GUIDE.md`

---

## Error: "credentials.json not found"

**Quick Fix:**
```bash
ls /Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail_credentials.json
```

If not found:
1. Check ~/Downloads for `client_secret_*.json`
2. Rename to `gmail_credentials.json`
3. Move to `.scripts` folder

---

## Error: "403 access_denied"

**Cause:** Not authorized as test user

**Quick Fix:**
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Click "Test users" section
3. Verify `mike.finneran@gmail.com` is listed
4. If not, click "+ ADD USERS" and add it
5. Try authorization again

---

## Error: "This app is blocked"

**Cause:** App not in Testing mode

**Quick Fix:**
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Check "Publishing status"
3. Should say "Testing"
4. If "In production", click to unpublish

---

## Warning: "Google hasn't verified this app"

**This is NORMAL** - Click:
1. "Advanced" (bottom left)
2. "Go to Personal Gmail Invoice Fetcher (unsafe)"
3. This is safe - it's YOUR app

---

## No invoices found

**Try:**
```python
# Edit line 169 in fetch-subscription-invoices.py:
start_date = end_date - timedelta(days=90)  # Was 60
```

Or manually search Gmail:
```
subject:(invoice OR receipt) after:2025/09/01
```

---

## Import errors

```bash
pip3 install --user google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## Need to revoke access?

https://myaccount.google.com/permissions

Find "Personal Gmail Invoice Fetcher" → Remove

---

## Quick Commands

**Run invoice fetcher:**
```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
python3 fetch-subscription-invoices.py
```

**Check report:**
```bash
open /Users/mikefinneran/Documents/ObsidianVault/subscription-invoices.md
```

**Re-authorize:**
```bash
rm /Users/mikefinneran/Documents/ObsidianVault/.scripts/gmail_token.pickle
python3 fetch-subscription-invoices.py
```

---

**Full Guide:** `GMAIL_OAUTH_COMPLETE_GUIDE.md`
