# Quick Setup - Shell Commands for Daily Notes

## 🚀 5-Minute Setup

### 1. Install Plugin
- Open Obsidian Settings (⚙️)
- Community plugins → Browse
- Search: **"Shell commands"**
- Install → Enable

### 2. Add Command
- Settings → Shell commands → New shell command
- **Command:**
  ```
  python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
  ```
- **Alias:** Update Daily Note
- **Event:** Enable "Vault: After startup" ✓

### 3. Test
- Click ▶️ (execute button)
- Should see: "✅ Daily note updated"
- Check today's Daily note - populated!

### 4. Verify
- Close Obsidian (`Cmd + Q`)
- Reopen Obsidian
- Daily note auto-updates ✨

## ✅ Done!

**Full guide:** `.scripts/SHELL-COMMANDS-SETUP-GUIDE.md`

**Troubleshooting:**
- Test manually: `python3 .scripts/update_daily_note.py`
- Check: `.scripts/daily_note_state.json`
- Reset: `rm .scripts/daily_note_state.json`
