# Google Passkey Fix - Automated Solution

## Problem
Google's passkey requirement is locking you out daily from `mike.finneran@gmail.com`.

## Solution
This automated script will:
1. Disable "Skip password when possible" setting
2. Delete ALL passkeys from your Google account
3. Take screenshots of each step for verification

## Quick Start

### Step 1: Setup (One-time)
```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
./setup-passkey-fix.sh
```

This will install Puppeteer (browser automation library).

### Step 2: Run the Fix
```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts
node fix-google-passkeys.js
```

### Step 3: Follow the Prompts
1. Browser window will open
2. **Log in to your Google account** (mike.finneran@gmail.com)
3. Press ENTER in the terminal when logged in
4. Script will automate all the clicking
5. Script will show you what was changed
6. Press ENTER to close browser

## What Happens

### Phase 1: Disable Passkey Requirement
- Navigates to https://myaccount.google.com/security
- Finds "Skip password when possible" toggle
- Turns it OFF
- Takes screenshot

### Phase 2: Delete All Passkeys
- Navigates to https://myaccount.google.com/signinoptions/passkeys
- Finds all passkey entries
- Clicks delete on each one
- Confirms deletion
- Repeats until all are deleted
- Takes screenshots of each deletion

### Phase 3: Verification
- Shows summary of what was changed
- Saves all screenshots to `google-passkey-screenshots/`
- Confirms completion

## Expected Output

```
🚀 Google Passkey Disabler Starting...

🔐 Step 0: Please log in to your Google account...
⏸️  Press ENTER after you have successfully logged in...

🔧 Step 1: Disabling "Skip password when possible" setting...
📸 Screenshot saved: .../security-page.png
✅ Found "Skip password when possible" toggle - it is ON
✅ Successfully disabled "Skip password when possible"

🗑️  Step 2: Deleting all passkeys...
📸 Screenshot saved: .../passkeys-page-initial.png
🗑️  Deleting passkey 1...
✅ Confirmed deletion
🗑️  Deleting passkey 2...
✅ Confirmed deletion
✅ No more passkeys found to delete

============================================================
✅ COMPLETED!
============================================================
📊 Summary:
   - "Skip password when possible": DISABLED
   - Passkeys deleted: 2
   - Screenshots saved to: .../google-passkey-screenshots
============================================================
```

## Troubleshooting

### If toggles/buttons aren't found automatically:
The script will pause and ask you to do it manually, then press ENTER to continue.

### If you see "Could not find confirmation button":
The passkey was likely deleted anyway. Check the screenshots.

### If the script hangs:
1. Check the browser window - Google may be asking for 2FA
2. Complete any verification steps
3. Press ENTER in terminal to continue

### To run it again:
Just run: `node fix-google-passkeys.js`

## Files Created

- `fix-google-passkeys.js` - Main automation script
- `setup-passkey-fix.sh` - Setup/installation script
- `package.json` - Node.js dependencies
- `node_modules/` - Puppeteer library
- `google-passkey-screenshots/` - Screenshots from each run

## After Running

1. Test logging in to Gmail normally
2. You should NOT be prompted for passkeys
3. You CAN still use your password normally
4. If issues persist, check screenshots to verify changes

## Security Notes

- Script runs locally on your machine
- No credentials are stored
- You log in manually in the browser
- Screenshots are saved locally only
- Safe to delete screenshots after verification

## Support

If this doesn't work, share the screenshots with Claude and we'll debug together.

---
Created: 2025-11-01
Last Updated: 2025-11-01
