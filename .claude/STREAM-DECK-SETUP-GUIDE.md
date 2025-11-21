# Stream Deck Setup Guide
**Device:** cn002_354c
**Date:** 2025-11-05
**Software:** Stream Controller.app

## Rectangle Pro Default Shortcuts

Open Rectangle Pro > Settings to verify these shortcuts match yours:

| Action | Default Shortcut | Stream Deck Label |
|--------|-----------------|-------------------|
| Left Half | `⌃⌥←` (Ctrl+Opt+Left) | ◀️ Left |
| Right Half | `⌃⌥→` (Ctrl+Opt+Right) | Right ▶️ |
| Top Half | `⌃⌥↑` (Ctrl+Opt+Up) | ⬆️ Top |
| Bottom Half | `⌃⌥↓` (Ctrl+Opt+Down) | Bottom ⬇️ |
| Maximize | `⌃⌥↵` (Ctrl+Opt+Return) | ⬜ Max |
| Center | `⌃⌥C` | 🎯 Center |
| Top Left | `⌃⌥U` | ↖️ TL |
| Top Right | `⌃⌥I` | ↗️ TR |
| Bottom Left | `⌃⌥J` | ↙️ BL |
| Bottom Right | `⌃⌥K` | ↘️ BR |

## Wispr Flow (WhisperFlow) Controls

| Action | Method | Stream Deck Label |
|--------|--------|-------------------|
| Start Recording | Click menu bar icon | 🎙️ Record |
| Stop Recording | Click menu bar icon again | ⏹️ Stop |
| Open App | `open -a "Wispr Flow"` | 🗣️ Wispr |

## Project Context Switching

### WalterSignal Project
```bash
#!/bin/bash
# Switch to WalterSignal context
cd ~/Documents/ObsidianVault/Projects/WalterSignal
open -a "iTerm"
open -a "Obsidian"
osascript -e 'tell application "iTerm" to create window with default profile command "cd ~/Documents/ObsidianVault/Projects/WalterSignal && clear"'
```
Save as: `~/.claude/scripts/switch-to-waltersignal.sh`

### ObsidianVault Daily Note
```bash
#!/bin/bash
# Open vault and create daily note
vault  # your alias
vdaily # your alias for daily note
```
Save as: `~/.claude/scripts/open-daily-note.sh`

### Research Mode
```bash
#!/bin/bash
# Open research tools
open -a "Google Chrome"
open -a "Obsidian"
open ~/Documents/ObsidianVault/Projects/Preplexity\ Pro\ Research/
```
Save as: `~/.claude/scripts/research-mode.sh`

### Email/Admin Mode
```bash
#!/bin/bash
# Open admin tools
open -a "Google Chrome" "https://gmail.com"
open -a "Google Chrome" "https://airtable.com/appOaLuicKSlV6nMh/tblBacklog"
open -a "Google Chrome" "https://calendar.google.com"
```
Save as: `~/.claude/scripts/admin-mode.sh`

## iTerm2 Layout Shortcuts

### TDD Layout (Claude | Tests)
```applescript
tell application "iTerm"
    create window with default profile
    tell current session of current window
        split horizontally with default profile
    end tell
end tell
```
Save as: `~/.claude/scripts/iterm-tdd-layout.scpt`

### Full Stack Layout (Claude | Dev Server | Tests)
```applescript
tell application "iTerm"
    create window with default profile
    tell current session of current window
        split horizontally with default profile
        split vertically with default profile
    end tell
end tell
```
Save as: `~/.claude/scripts/iterm-fullstack-layout.scpt`

## Quick Actions

| Action | Command | Stream Deck Label |
|--------|---------|-------------------|
| Load Context | `;ctx` (Alfred snippet) | 🧠 Context |
| Save Progress | `~/.claude/scripts/save-session-memory.sh` | 💾 Save |
| Daily Note | `vdaily` | 📅 Daily |
| Airtable Sync | `at-sync` | 🔄 Sync |
| S3 Backup | `backup-s3` | ☁️ Backup |

## Stream Controller Setup Instructions

### 1. Create Scripts
```bash
# Make scripts directory if needed
mkdir -p ~/.claude/scripts

# Make scripts executable
chmod +x ~/.claude/scripts/switch-to-*.sh
chmod +x ~/.claude/scripts/*-mode.sh
```

### 2. Configure Buttons in Stream Controller

**For each button:**
1. Click the button in Stream Controller
2. Choose action type: **"Hotkey"** or **"Execute Command"**
3. Enter the shortcut or command path
4. Add custom icon/label

**Example: Left Half Window**
- Action: Hotkey
- Shortcut: Ctrl+Opt+Left
- Label: ◀️ Left

**Example: WalterSignal Project**
- Action: Execute Command
- Command: `/bin/bash ~/.claude/scripts/switch-to-waltersignal.sh`
- Label: 🚀 WS

### 3. Suggested Button Layout (15-key Stream Deck)

```
┌────────┬────────┬────────┬────────┬────────┐
│ ◀️ Left│ ⬜ Max │Right ▶️│🎙️Record│🗣️Wispr │
├────────┼────────┼────────┼────────┼────────┤
│↖️ TL   │⬆️ Top  │↗️ TR   │⏹️ Stop │🧠Context│
├────────┼────────┼────────┼────────┼────────┤
│↙️ BL   │Bottom⬇️│↘️ BR   │💾 Save │🔄 Sync  │
└────────┴────────┴────────┴────────┴────────┘
```

### 4. Alternative Layout (Project-Focused)

```
┌────────┬────────┬────────┬────────┬────────┐
│🚀 WS   │📝 Vault│🔬Research│📧Admin│🧠Context│
├────────┼────────┼────────┼────────┼────────┤
│ ◀️ Left│ ⬜ Max │Right ▶️│⬆️ Top  │Bottom⬇️ │
├────────┼────────┼────────┼────────┼────────┤
│🎙️Record│⏹️ Stop │💾 Save │🔄 Sync │📅 Daily │
└────────┴────────┴────────┴────────┴────────┘
```

## Testing Your Setup

Run each script manually first:
```bash
# Test WalterSignal switch
bash ~/.claude/scripts/switch-to-waltersignal.sh

# Test iTerm layout
osascript ~/.claude/scripts/iterm-tdd-layout.scpt

# Test daily note
vdaily

# Test Airtable sync
at-sync
```

## Troubleshooting

**Script won't run from Stream Controller:**
- Check permissions: `chmod +x script-name.sh`
- Use full path: `/bin/bash /Users/mikefinneran/.claude/scripts/script-name.sh`
- Check logs: `~/Library/Logs/Stream Controller_debug.log`

**Shortcuts not working:**
- Verify in Rectangle Pro settings
- Try manually first (Cmd+Opt+Left)
- Check if another app is using the same shortcut

**WhisperFlow not responding:**
- Make sure "Wispr Flow" is running
- Try: `open -a "Wispr Flow"`
- Check menu bar for icon

## Next Steps

1. Create all scripts above
2. Test each script manually
3. Configure buttons in Stream Controller one at a time
4. Test each button after configuration
5. Adjust labels/icons as needed
6. Export configuration for backup

## Backup Your Configuration

Stream Controller stores config at:
`~/Library/Application Support/Elgato/StreamDeck/` or similar

Export regularly for backup!
