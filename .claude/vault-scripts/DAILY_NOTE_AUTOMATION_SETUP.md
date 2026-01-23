# Daily Note Auto-Update Setup

Your daily note automation script is ready! Here are 3 ways to set it up:

---

## ✅ OPTION 1: Obsidian Shell Commands Plugin (RECOMMENDED)

**Best for:** Automatic updates when vault opens

### Setup:
1. Open Obsidian Settings (⚙️)
2. Go to Community Plugins
3. Search and install **"Shell commands"** plugin
4. Enable the plugin
5. In Shell commands settings:
   - Add new shell command: `python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py`
   - Set execution event: **"On startup"** (runs when vault opens)
   - Optional: Add to hotkey for manual trigger

**Result:** Daily note auto-updates every time you open Obsidian

---

## ⚡ OPTION 2: Manual Run (Quick Test)

**Best for:** Testing or manual updates

### Run from Terminal:
```bash
python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
```

**Result:** Updates today's daily note immediately

---

## 🔄 OPTION 3: Cron Job (Background Automation)

**Best for:** Updates even when Obsidian is closed

### Setup:
1. Open Terminal
2. Edit crontab:
   ```bash
   crontab -e
   ```

3. Add this line (runs at 6 AM daily):
   ```
   0 6 * * * /usr/bin/python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
   ```

4. Save and exit

**Result:** Daily note auto-updates at 6 AM every day

---

## 📋 What the Script Does

**Automatic Priority Detection:**
- Checks which WalterSignal files exist
- Determines current project phase
- Suggests next actions based on progress

**Sections Updated:**
- 🎯 Top 3 Priorities (dynamic based on project state)
- 💰 Revenue Activities (customer outreach tasks)
- 📊 Projects (WalterFetch progress + completed tasks)
- 💡 Ideas & Notes (current strategic insights)

**Smart Logic:**
- Only updates once per day (won't duplicate)
- Marks completed tasks with ✅
- Suggests next steps based on what's done
- Links to relevant project files with [[wiki links]]

---

## 🛠️ Customization

### Edit Priorities Logic:
Open: `.scripts/update_daily_note.py`

**Key functions to customize:**
- `get_waltersignal_priorities()` - Change top 3 priorities
- `get_revenue_activities()` - Modify revenue tasks
- `get_project_tasks()` - Adjust project checklist

### Add More Projects:
Currently tracks:
- WalterFetch/WalterSignal
- LifeHub

To add more, edit the `get_project_tasks()` function.

---

## 🐛 Troubleshooting

**Script not running?**
1. Check it's executable: `ls -la ~/.../update_daily_note.py`
2. Test manually: `python3 update_daily_note.py`
3. Check error output

**Daily note not updating?**
1. Verify daily note exists in `Daily/` folder
2. Check state file: `.scripts/daily_note_state.json`
3. Delete state file to force update

**Want to reset?**
```bash
rm /Users/mikefinneran/Documents/ObsidianVault/.scripts/daily_note_state.json
```

---

## 📊 State Tracking

The script uses `.scripts/daily_note_state.json` to:
- Track last update date
- Avoid duplicate updates
- Remember previous priorities

**View current state:**
```bash
cat /Users/mikefinneran/Documents/ObsidianVault/.scripts/daily_note_state.json
```

---

## ✨ Future Enhancements

**Possible additions:**
- Pull from GitHub issues/PRs
- Track revenue metrics automatically
- Integrate with calendar events
- Pull todos from project management tools
- Smart priority ranking based on deadlines

---

**Quick Start:** Install Shell Commands plugin → Add command → Set to run on startup → Done!

**Last Updated:** 2025-10-20
