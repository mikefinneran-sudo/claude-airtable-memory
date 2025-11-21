# iTerm2 AutoLaunch Setup

## Overview

Automatically launches Claude Code when iTerm2 opens.

**Layout:**
- Full window: Claude Code

**ERP Command Center:**
- Has embedded terminal built-in
- Access via browser: `http://localhost:8000/erp`
- Launch manually: `~/.claude/command-center/launch-erp.sh`

## Setup Instructions

### 1. Grant iTerm2 Full Disk Access

iTerm2 needs full system authorization to access all files and scripts.

**Steps:**
1. Open **System Settings** (or System Preferences on older macOS)
2. Navigate to **Privacy & Security** → **Full Disk Access**
3. Click the lock icon and authenticate
4. Click the **+** button
5. Navigate to `/Applications/` and select **iTerm.app**
6. Toggle iTerm.app to **ON**
7. **Restart iTerm2** for changes to take effect

**Why this is needed:**
- Access to `.claude/` directory scripts
- Read/write to all project files
- Execute Python scripts system-wide
- Full bash command execution

### 2. Install iTerm2 Python Runtime

The AutoLaunch script uses the iTerm2 Python API.

**Steps:**
1. Open iTerm2
2. Go to **Scripts** → **Manage** → **Install Python Runtime**
3. Wait for installation (may take 2-3 minutes)
4. Close and reopen iTerm2

**Verify installation:**
```bash
ls -la "$HOME/Library/ApplicationSupport/iTerm2/iterm2env"
```

### 3. Verify AutoLaunch Script

**Script location:**
```
~/Library/Application Support/iTerm2/Scripts/AutoLaunch/launch_claude.py
```

**Verify it exists:**
```bash
ls -la "$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch/"
```

### 4. Additional macOS Permissions (Optional but Recommended)

For full functionality, also grant iTerm2:

**Automation:**
- System Settings → Privacy & Security → Automation
- Enable iTerm to control other apps if needed

**Accessibility:**
- System Settings → Privacy & Security → Accessibility
- Add iTerm.app for advanced keyboard shortcuts and triggers

**Developer Tools:**
- iTerm2 should automatically request this on first launch
- Required for script execution

## Testing

### Manual Test
1. Quit iTerm2 completely (Cmd+Q)
2. Reopen iTerm2
3. You should see:
   - Claude Code starting automatically

4. To launch ERP with embedded terminal:
   ```bash
   ~/.claude/command-center/launch-erp.sh
   ```
5. Open browser to `http://localhost:8000/erp`
6. Click **⌨️ Terminal** tab to access embedded terminal

### Troubleshooting

**Script doesn't run:**
- Check: Scripts → Manage → Console for error messages
- Verify Python runtime is installed
- Check Full Disk Access is enabled

**ERP doesn't start:**
- Verify script exists: `ls ~/.claude/command-center/launch-erp.sh`
- Test manually: `~/.claude/command-center/launch-erp.sh`
- Check permissions: `chmod +x ~/.claude/command-center/launch-erp.sh`

**Claude doesn't start:**
- Verify `claude` command is in PATH: `which claude`
- Check Claude Code is properly installed

**Split pane layout wrong:**
- Edit layout in: `~/Library/Application Support/iTerm2/Scripts/AutoLaunch/launch_claude.py`
- Adjust `before=False` and vertical split ratios

## Customization

### Change Split Ratio

Edit `launch_claude.py` line 24:

```python
# 70/30 split (current)
right_session = await left_session.async_split_pane(vertical=True, before=False)

# 50/50 split
right_session = await left_session.async_split_pane(vertical=True, before=True)

# Horizontal split instead (top/bottom)
right_session = await left_session.async_split_pane(vertical=False, before=False)
```

### Disable AutoLaunch Temporarily

Rename the AutoLaunch folder:
```bash
cd "$HOME/Library/Application Support/iTerm2/Scripts"
mv AutoLaunch AutoLaunch.disabled
```

Re-enable:
```bash
mv AutoLaunch.disabled AutoLaunch
```

### Add More Panes

Modify `launch_claude.py` to add additional panes:

```python
# Create bottom pane for logs
bottom_session = await right_session.async_split_pane(vertical=False, before=False)
await bottom_session.async_send_text('tail -f ~/.claude/logs/activity.log\n')
```

## File Locations

- **AutoLaunch script:** `~/Library/Application Support/iTerm2/Scripts/AutoLaunch/launch_claude.py`
- **ERP launch script:** `~/.claude/command-center/launch-erp.sh`
- **ERP server:** `~/.claude/command-center/erp_server.py`
- **Python runtime:** `~/Library/ApplicationSupport/iTerm2/iterm2env/`
- **Script logs:** Scripts → Manage → Console

## macOS Security Summary

iTerm2 requires these permissions for full functionality:

| Permission | Required | Purpose |
|------------|----------|---------|
| Full Disk Access | **YES** | Access all files and scripts |
| Developer Tools | **YES** | Execute scripts and commands |
| Automation | Optional | Control other apps |
| Accessibility | Optional | Advanced shortcuts/triggers |

---

**Last Updated:** 2025-11-02
**Maintained by:** Mike Finneran
**Related:** `EXPERT_GUIDE.md`, `CLAUDE_CODE_WORKFLOWS.md`
