# Google Passkey Fix - Quick Start

## One Command to Fix Everything

```bash
cd /Users/mikefinneran/Documents/ObsidianVault/.scripts && ./run-passkey-fix.sh
```

## What Happens

1. Browser opens automatically
2. You log in to mike.finneran@gmail.com
3. Press ENTER in terminal
4. Script disables passkey requirement
5. Script deletes all passkeys
6. Screenshots saved for verification
7. Done!

## Files Location

All files are in: `/Users/mikefinneran/Documents/ObsidianVault/.scripts/`

- `run-passkey-fix.sh` - **← RUN THIS**
- `fix-google-passkeys.js` - Main automation script
- `GOOGLE-PASSKEY-FIX-README.md` - Full documentation
- `google-passkey-screenshots/` - Verification screenshots

## Expected Time

2-3 minutes total (mostly waiting for you to log in)

## What Gets Changed

### Before:
- ✅ "Skip password when possible" is ON
- ✅ Multiple passkeys exist
- ❌ Daily lockouts from Gmail

### After:
- ❌ "Skip password when possible" is OFF
- ❌ Zero passkeys
- ✅ Normal password login works

## If Something Goes Wrong

1. Check screenshots in `google-passkey-screenshots/`
2. Run the script again (it's safe to run multiple times)
3. Manually verify at:
   - Security: https://myaccount.google.com/security
   - Passkeys: https://myaccount.google.com/signinoptions/passkeys

## Support

If issues persist, the screenshots will show exactly what happened. Share them with Claude for debugging.

---

**Status:** Ready to Run
**Last Updated:** 2025-11-01
**Account:** mike.finneran@gmail.com
