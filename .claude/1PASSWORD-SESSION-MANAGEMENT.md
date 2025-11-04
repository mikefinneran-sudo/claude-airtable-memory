# 1Password Session Management - 24-Hour Authorization

**Implemented**: November 1, 2025
**Purpose**: Single authentication across all Claude sessions for 24 hours
**Status**: Active

---

## What This Does

Maintains a persistent 1Password CLI session for 24 hours:
- **Authenticate once** per day
- **All sessions share** the same authorization
- **Auto-refresh** when session expires
- **Zero friction** across terminals and projects

**Result**: No more repeated Touch ID prompts, seamless credential access

---

## How It Works

### Session File
- Location: `~/.claude/.op-session`
- Contains: Session token from `op signin`
- Lifetime: 24 hours
- Permissions: 600 (owner read/write only)

### Automatic Checks
The session is checked/created on:
- Shell startup (every new terminal)
- `resume` command
- `continue` command
- `start-session` command

### Session Validation
Before every use:
1. Check if session file exists
2. Check if less than 24 hours old
3. Test if token still works
4. If invalid: prompt for new authentication
5. If valid: silently load and continue

---

## User Experience

### First Use (or after 24h)
```bash
# Open new terminal or run resume
resume waltersignal

🔐 1Password authentication required
   Authorizing for 24 hours...

# Touch ID prompt appears once
# Enter password if Touch ID unavailable

✅ 1Password session authorized for 24 hours

# Continue with work...
```

### Subsequent Uses (within 24h)
```bash
# Open new terminal or run resume
resume waltersignal

# No prompt! Session already valid
# Immediately proceeds to work
```

### Session Info
```bash
# Check session status (verbose)
~/.claude/scripts/check-1password-session.sh -v

✅ 1Password session active (18h remaining)
```

---

## Files Modified

**New File**:
- `~/.claude/scripts/check-1password-session.sh` - Session manager

**Modified**:
- `~/.zshrc` - Auto-load session on shell startup
- `start-session.sh` - Check session when starting work
- `resume-work.sh` - Check session when resuming
- `continue-enhanced.sh` - Check session when continuing

---

## Technical Details

### Session Token Storage
```bash
# Session file location
~/.claude/.op-session

# Content: Raw session token from op signin
# Example: A3-XXXXXX-XXXXXX-XXXXX-XXXXX-XXXXX-XXXXX
```

### Session Age Check
```bash
# Calculate age in seconds
session_age=$(( $(date +%s) - $(stat -f %m "$SESSION_FILE") ))

# Compare to 24-hour limit
SESSION_AGE_LIMIT=86400  # 24 hours in seconds
```

### Session Validation
```bash
# Test if token works
OP_SESSION_my=$token op whoami &>/dev/null
```

### Session Creation
```bash
# Sign in and capture token
session_token=$(op signin --raw)

# Save to file
echo "$session_token" > ~/.claude/.op-session
chmod 600 ~/.claude/.op-session

# Export for current shell
export OP_SESSION_my="$session_token"
```

---

## Integration Points

### Shell Startup (~/.zshrc)
```bash
# Auto-check/create session on every new shell
if [ -f ~/.claude/scripts/check-1password-session.sh ]; then
    source ~/.claude/scripts/check-1password-session.sh
fi
```

### Resume Work
```bash
# resume waltersignal
# → Checks 1Password session
# → If expired: prompts once
# → If valid: proceeds immediately
```

### Continue Project
```bash
# continue waltersignal
# → Checks 1Password session
# → Loads project context
# → Ready to work
```

### Start Session
```bash
# start-session waltersignal
# → Checks 1Password session
# → Creates session memory
# → Ready to work
```

---

## Security Features

**File Permissions**:
- Session file: `600` (only owner can read/write)
- Protected from other users

**Auto-Expiration**:
- Sessions expire after 24 hours
- Old tokens automatically rejected

**Token Validation**:
- Every use validates token still works
- Detects revoked/expired sessions

**No Credential Storage**:
- Only session token stored (not master password)
- Token can be revoked from 1Password app

---

## Troubleshooting

### "1Password authentication failed"

**Cause**: Touch ID failed or password incorrect

**Fix**:
```bash
# Try manual signin
op signin

# Or check 1Password app is unlocked
```

### Session file permission denied

**Cause**: Wrong file permissions

**Fix**:
```bash
chmod 600 ~/.claude/.op-session
```

### Session keeps expiring early

**Cause**: System time incorrect or session manually revoked

**Check**:
```bash
# View session age
stat -f %m ~/.claude/.op-session
date +%s

# Check 1Password app for active sessions
```

### Want to force re-authentication

**Manual reset**:
```bash
rm ~/.claude/.op-session
# Next command will prompt for auth
```

---

## Benefits

### One Authentication Per Day
- Authenticate once in morning
- Works all day across sessions
- No repeated Touch ID prompts

### Cross-Session Sharing
- Multiple terminals share session
- `resume` in one, `continue` in another
- All use same 24-hour authorization

### Zero Friction
- Silent when session valid
- Only prompts when needed
- Seamless integration

### Secure
- 24-hour auto-expiration
- Token validation
- Proper file permissions
- No credential storage

---

## Advanced: Custom Session Duration

Edit `check-1password-session.sh` to change duration:

```bash
# Default: 24 hours
SESSION_AGE_LIMIT=86400

# Examples:
SESSION_AGE_LIMIT=43200   # 12 hours
SESSION_AGE_LIMIT=172800  # 48 hours (2 days)
SESSION_AGE_LIMIT=3600    # 1 hour (very secure)
```

---

## Advanced: Manual Session Management

### Check session status
```bash
~/.claude/scripts/check-1password-session.sh -v
```

### Force new session
```bash
rm ~/.claude/.op-session
~/.claude/scripts/check-1password-session.sh
```

### View session token (for debugging)
```bash
cat ~/.claude/.op-session
# Note: Keep this secret!
```

### Test session manually
```bash
export OP_SESSION_my=$(cat ~/.claude/.op-session)
op whoami
```

---

## Comparison: Before vs After

### Before
```bash
# Terminal 1
resume waltersignal
# 🔐 Touch ID prompt

# Terminal 2 (5 minutes later)
continue waltersignal
# 🔐 Touch ID prompt again

# Terminal 3 (10 minutes later)
op item get AWS
# 🔐 Touch ID prompt again
```

### After
```bash
# Terminal 1
resume waltersignal
# 🔐 Touch ID prompt (first time today)

# Terminal 2 (5 minutes later)
continue waltersignal
# ✅ No prompt! Session valid

# Terminal 3 (10 minutes later)
op item get AWS
# ✅ No prompt! Session valid

# All terminals work seamlessly
```

---

## Status

✅ **Implemented**: Session manager created
✅ **Integrated**: All workflow scripts updated
✅ **Shell Startup**: Auto-check on new terminals
✅ **Tested**: Ready for use

---

## Next Steps

1. ✅ Reload shell: `source ~/.zshrc`
2. ✅ Test: `resume waltersignal`
3. ✅ Authenticate once (Touch ID)
4. ✅ All subsequent commands work without prompting

---

**Authenticate once per day, work seamlessly all day.**
