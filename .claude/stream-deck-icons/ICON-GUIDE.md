# Stream Deck Icon Guide

**Location:** `~/.claude/stream-deck-icons/`

## How to Apply Icons in Stream Controller

1. **Right-click** the button in Stream Controller
2. Click **"Icon"** or **"Custom Image"**
3. **Browse** to: `/Users/mikefinneran/.claude/stream-deck-icons/`
4. **Select** the appropriate icon below

---

## 🚀 Main Workspace

**launch-workspace.png** → Launch entire workspace layout
- Command: `/bin/bash /Users/mikefinneran/.claude/scripts/launch-workspace.sh`

---

## 🪟 Rectangle Pro - Window Management

**window-left.png** → Move window to left half
- Hotkey: `Ctrl+Opt+Left`

**window-right.png** → Move window to right half
- Hotkey: `Ctrl+Opt+Right`

**window-maximize.png** → Maximize window
- Hotkey: `Ctrl+Opt+Return`

**window-center.png** → Center window
- Hotkey: `Ctrl+Opt+C`

**window-top-left.png** → Top left quarter
- Hotkey: `Ctrl+Opt+U`

**window-top-right.png** → Top right quarter
- Hotkey: `Ctrl+Opt+I`

**window-bottom-left.png** → Bottom left quarter
- Hotkey: `Ctrl+Opt+J`

**window-bottom-right.png** → Bottom right quarter
- Hotkey: `Ctrl+Opt+K`

---

## 🎙️ Wispr Flow (WhisperFlow)

**whisper-record.png** → Start recording
- Action: Click Wispr Flow menu bar icon

**whisper-stop.png** → Stop recording
- Action: Click Wispr Flow menu bar icon

**whisper-open.png** → Open Wispr Flow
- Command: `open -a "Wispr Flow"`

---

## 📂 Project Switching

**project-waltersignal.png** → Switch to WalterSignal
- Command: `/bin/bash /Users/mikefinneran/.claude/scripts/switch-to-waltersignal.sh`

**project-vault.png** → Open ObsidianVault
- Command: `open -a "Obsidian" && cd ~/Documents/ObsidianVault`

**project-research.png** → Research mode
- Command: `/bin/bash /Users/mikefinneran/.claude/scripts/research-mode.sh`

**project-admin.png** → Email/Admin mode
- Command: `/bin/bash /Users/mikefinneran/.claude/scripts/admin-mode.sh`

---

## ⚡ iTerm2 Layouts

**iterm-tdd.png** → TDD layout (Claude | Tests)
- Command: `osascript /Users/mikefinneran/.claude/scripts/iterm-tdd-layout.scpt`

**iterm-fullstack.png** → Full stack layout (3-way split)
- Command: `osascript /Users/mikefinneran/.claude/scripts/iterm-fullstack-layout.scpt`

---

## 🔧 Quick Actions

**context-load.png** → Load context
- Type text: `;ctx` (Alfred snippet)

**session-save.png** → Save session progress
- Command: `/bin/bash /Users/mikefinneran/.claude/scripts/save-session-memory.sh`

**daily-note.png** → Create daily note
- Command: `/bin/bash -c "cd ~/Documents/ObsidianVault && vdaily"`

**airtable-sync.png** → Sync to Airtable
- Command: `at-sync`

**s3-backup.png** → Backup to S3
- Command: `backup-s3`

---

## 🛠️ System Actions

**close-apps.png** → Close all workspace apps
- Command: `killall "Superhuman" "Comet" "Slack" "WhatsApp" "Obsidian" 2>/dev/null`

**refresh.png** → Refresh workspace layout
- Command: `/bin/bash /Users/mikefinneran/.claude/scripts/optimize-workspace-sizes.sh`

---

## 🎨 Icon Colors

- **Blue tones** (Nord theme): Window management, system actions
- **Red**: Stop/close actions
- **Green**: Sync/success actions
- **Yellow/Orange**: Record/capture actions
- **Teal/Aqua**: Projects and quick access

All icons are 144x144 pixels, optimized for Stream Deck standard size.
