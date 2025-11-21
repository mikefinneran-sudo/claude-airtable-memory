# WalterSignal iTerm2 Enhanced Setup

## Quick Start (5 Minutes)

### Option A: Manual Setup (Recommended)

#### 1. Create Triggers (2 minutes)

**Open iTerm2 Preferences:**
- Press `Cmd+,` or iTerm2 → Preferences
- Navigate to: **Profiles → Advanced → Triggers**
- Click **Edit**

**Add these 4 triggers:**

**Trigger 1: Error Highlighting**
```
Regular Expression: (Error|Failed|error|failed|ERROR)
Action: Highlight Text
Parameters:
  - Text: red background
  - Background Color: RGB(239, 68, 68) - Red
```

**Trigger 2: Success Highlighting**
```
Regular Expression: (✓ Compiled|Success|success|BUILD SUCCESS|✓ Ready)
Action: Highlight Text
Parameters:
  - Text: green background
  - Background Color: RGB(34, 197, 94) - Green
```

**Trigger 3: Warning Highlighting**
```
Regular Expression: (Warning|warning|WARN)
Action: Highlight Text
Parameters:
  - Text: yellow background
  - Background Color: RGB(245, 158, 11) - Yellow
```

**Trigger 4: Build Alert**
```
Regular Expression: ✓ Ready in
Action: Post Notification
Parameters:
  - Title: WalterSignal Dashboard
  - Message: Build completed successfully
```

Click **OK** to save.

---

#### 2. Set Badge (30 seconds)

In **Profiles → General**:
- Badge: `WS`
- Badge Color: Purple (RGB: 139, 92, 246)
- Badge Position: Top Right

---

#### 3. Customize Colors (1 minute)

In **Profiles → Colors**:

**Background Colors:**
- Background: Black `#000000`
- Selection: Purple 30% `rgba(139, 92, 246, 0.3)`

**Text Colors:**
- Foreground: White `#FFFFFF`
- Cursor: Purple `#8B5CF6`

**Optional:** Import Snazzy theme and adjust purple accent

---

#### 4. Set Working Directory (30 seconds)

In **Profiles → General → Working Directory**:
- Select: "Directory"
- Enter: `/Users/mikefinneran/.claude/command-center/erp-dashboard`

---

#### 5. Save Profile (30 seconds)

In **Profiles**:
- Click "+" to duplicate current profile
- Rename to: "WalterSignal Development"
- Set as default (optional)

---

### Option B: Automated Setup (Experimental)

Run the setup script:
```bash
~/.config/iterm2/setup-waltersignal-profile.sh
```

Or use iTerm2 Python API:
```bash
~/.config/iterm2/waltersignal-quick-setup.py
```

**Note:** Python API requires iTerm2 Python runtime. If not installed:
1. iTerm2 → Scripts → Manage → Install Python Runtime
2. Wait for installation
3. Run script again

---

## Keyboard Shortcuts Reference

### Split Panes
| Shortcut | Action |
|----------|--------|
| `Cmd+D` | Split vertically (side by side) |
| `Cmd+Shift+D` | Split horizontally (top/bottom) |
| `Cmd+[` | Previous pane |
| `Cmd+]` | Next pane |
| `Cmd+Opt+Arrow` | Jump to pane in direction |
| `Cmd+W` | Close current pane |
| `Cmd+Shift+Enter` | Maximize/restore pane |

### Marks & Navigation
| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+M` | Set mark (bookmark) |
| `Cmd+Shift+Up` | Jump to previous mark |
| `Cmd+Shift+Down` | Jump to next mark |
| `Cmd+Shift+A` | Select command output |

### Alerts & Toolbelt
| Shortcut | Action |
|----------|--------|
| `Cmd+Opt+A` | Alert on next command completion |
| `Cmd+Opt+B` | Toggle toolbelt (show captured output) |
| `Cmd+Shift+H` | Show command history |

### Window Management
| Shortcut | Action |
|----------|--------|
| `Cmd+N` | New window |
| `Cmd+T` | New tab |
| `Cmd+O` | Open profiles menu |
| `Cmd+Opt+E` | Search all tabs |

---

## Recommended Layouts

### Layout 1: TDD Workflow (Test-Driven Development)
```
┌─────────────────────────────┬─────────────────────────────┐
│                             │                             │
│   Claude Code               │   Test Watcher              │
│   (Work with AI)            │   npm run test -- --watch   │
│                             │                             │
│   - Write code              │   - See test results        │
│   - Get suggestions         │   - Green/Red highlights    │
│   - Iterate                 │   - Instant feedback        │
│                             │                             │
└─────────────────────────────┴─────────────────────────────┘
```

Setup:
1. Press `Cmd+D` to split
2. Right pane: `npm run test -- --watch`
3. Left pane: Continue with Claude Code

---

### Layout 2: Full Stack Development
```
┌─────────────────────────────┬─────────────────────────────┐
│                             │   Dev Server                │
│                             │   npm run dev               │
│   Claude Code               ├─────────────────────────────┤
│   (Work with AI)            │   Test Watcher              │
│                             │   npm run test -- --watch   │
│                             │                             │
└─────────────────────────────┴─────────────────────────────┘
```

Setup:
1. Press `Cmd+D` to split vertically
2. In right pane, press `Cmd+Shift+D` to split horizontally
3. Top right: `npm run dev`
4. Bottom right: `npm run test -- --watch`

---

### Layout 3: Debugging (3 panes)
```
┌─────────────────────────────┬─────────────────────────────┐
│                             │   Dev Server + Logs         │
│   Claude Code               │   npm run dev               │
│   (Work with AI)            │                             │
│                             ├─────────────────────────────┤
│                             │   Database / API Logs       │
│                             │   tail -f logs/server.log   │
└─────────────────────────────┴─────────────────────────────┘
```

---

## WalterSignal Specific Setup

### Current Dashboard Development

**Right Pane Command:**
```bash
cd ~/.claude/command-center/erp-dashboard
npm run dev
```

**Watch For:**
- ✅ `✓ Ready in XXXms` - Green highlight (server started)
- ✅ `✓ Compiled in XXXms` - Green highlight (changes compiled)
- ❌ `Error: ...` - Red highlight (build error)
- ⚠️  `Warning: ...` - Yellow highlight (warning)

**Dashboard URL:** http://localhost:3000

---

### Alert on Build Complete

Before running long builds:
1. Press `Cmd+Opt+A` in the pane running the build
2. Run your build command
3. Switch to other work
4. Get notification when build completes

**Example:**
```bash
# In right pane
cd ~/.claude/command-center/erp-dashboard
# Press Cmd+Opt+A first
npm run build
# Go back to left pane, continue working
# You'll get notification when build finishes
```

---

## Troubleshooting

### Triggers Not Working

**Check:**
1. Triggers are enabled (checkbox in Triggers editor)
2. Regular expressions are exact (case-sensitive)
3. iTerm2 is latest version

**Test:**
```bash
echo "Error: test error"        # Should highlight red
echo "✓ Compiled successfully"  # Should highlight green
echo "Warning: test warning"    # Should highlight yellow
```

### Badge Not Showing

**Fix:**
1. Preferences → Appearance → General
2. Check "Show per-pane title bar with split panes"
3. Restart iTerm2

### Colors Not Applied

**Fix:**
1. Make sure you're using the WalterSignal profile
2. Check: Preferences → Profiles → Colors
3. Click "Color Presets" → Export → Save
4. Reimport if needed

### Python API Not Working

**Install iTerm2 Python Runtime:**
1. iTerm2 → Scripts → Manage
2. Click "Install Python Runtime"
3. Wait for installation (2-3 minutes)
4. Run script again

---

## Advanced Tips

### Auto-Start Split Pane

Create alias in `~/.zshrc`:
```bash
alias ws-dev='cd ~/.claude/command-center/erp-dashboard && npm run dev'
```

Then just type `ws-dev` in any pane.

### Save Arrangement

1. Set up your preferred layout
2. Window → Save Window Arrangement
3. Name it "WalterSignal Dev"
4. Restore anytime: Window → Restore Window Arrangement

### Captured Output

Use toolbelt to capture important output:
1. Press `Cmd+Opt+B` to show toolbelt
2. Click "Captured Output" tab
3. Output from triggers appears here
4. Double-click to jump to that moment

### Command History Search

Press `Cmd+Shift+H` to search command history:
- See all commands you've run
- Filter by date
- Re-run commands
- Copy commands

---

## Quick Test

Run this to verify your setup:

```bash
# Test all triggers
echo "✓ Compiled successfully"  # Should be green
sleep 1
echo "Error: Something failed"   # Should be red
sleep 1
echo "Warning: Check this"       # Should be yellow
sleep 1
echo "✓ Ready in 123ms"          # Should trigger notification
```

---

## Support

**Issues?**
- Check iTerm2 docs: https://iterm2.com/documentation.html
- iTerm2 Python API: https://iterm2.com/python-api/
- WalterSignal issues: Log in project notes

**Performance:**
- If triggers slow down terminal, reduce regex complexity
- Use "Look for trigger less often" option in Advanced

---

**Version:** 1.0
**Last Updated:** 2025-11-03
**For:** WalterSignal ERP Dashboard Development
