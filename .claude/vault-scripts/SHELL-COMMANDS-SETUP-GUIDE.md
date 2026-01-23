# Shell Commands Plugin Setup Guide
## Auto-Update Daily Notes on Vault Open

**Goal:** Automatically populate your daily note with WalterSignal priorities every time you open Obsidian

**Time:** 5 minutes

---

## Step 1: Install Shell Commands Plugin

1. **Open Obsidian Settings**
   - Click the gear icon (⚙️) in the bottom left
   - OR press `Cmd + ,` (Mac) / `Ctrl + ,` (Windows)

2. **Go to Community Plugins**
   - In the left sidebar, click **"Community plugins"**

3. **Enable Community Plugins** (if not already enabled)
   - If you see "Restricted mode is on", click **"Turn on community plugins"**
   - Confirm by clicking **"Turn on community plugins"** again

4. **Browse Community Plugins**
   - Click the **"Browse"** button
   - This opens the Community Plugins marketplace

5. **Search for "Shell commands"**
   - In the search box, type: `shell commands`
   - Look for the plugin by **Jarkko Linnanvirta**
   - Plugin description: "You can define and run shell commands..."

6. **Install the Plugin**
   - Click on the **"Shell commands"** plugin
   - Click **"Install"**
   - Wait for installation to complete (should take 5-10 seconds)

7. **Enable the Plugin**
   - After installation, click **"Enable"**
   - The button will change from gray to purple/blue

**✅ Plugin Installed!** You'll now see "Shell commands" in your installed plugins list.

---

## Step 2: Configure Shell Commands

1. **Open Shell Commands Settings**
   - Still in Settings, scroll down in the left sidebar
   - Under "Community plugins" section, find and click **"Shell commands"**

2. **Add New Shell Command**
   - Click the **"New shell command"** button (top of the page)
   - This creates a new command entry

3. **Enter the Command**
   - In the **"Shell command"** text field, paste this EXACT text:
   ```
   python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
   ```
   - Make sure there are no extra spaces or line breaks

4. **Give it a Name (Optional but Recommended)**
   - In the **"Alias"** field, type: `Update Daily Note`
   - This makes it easier to identify later

5. **Configure Event Trigger**
   - Scroll down to the **"Events"** section
   - Find **"Vault: After startup"** or **"Obsidian: After startup"**
   - Click the toggle to **enable it** (should turn blue/green)
   - This makes the command run every time you open the vault

6. **Additional Settings (Optional)**
   - **Execute in background:** Toggle ON (prevents popup window)
   - **Output channel:** Select "Notification" (shows success message)

7. **Test the Command (Important!)**
   - Scroll back up to the command
   - Click the **▶️ (play/execute)** button next to your command
   - You should see a notification: "✅ Daily note updated"
   - Check your Daily note - it should be populated!

8. **Save Settings**
   - Click **"Save"** if there's a save button
   - Or just close settings (saves automatically)

---

## Step 3: Verify It Works

1. **Close Obsidian Completely**
   - `Cmd + Q` (Mac) or `Alt + F4` (Windows)
   - Don't just minimize - fully quit the app

2. **Reopen Obsidian**
   - Launch Obsidian again
   - Open your vault

3. **Check Daily Note**
   - Navigate to `Daily/` folder
   - Open today's note (`YYYY-MM-DD.md`)
   - Should see:
     - 🎯 Top 3 Priorities (populated)
     - 💰 Revenue Activities (populated)
     - 📊 Projects (populated)
     - 💡 Ideas & Notes (populated)

4. **Look for Success Notification**
   - When vault opens, you should see a brief notification
   - "✅ Daily note updated" or similar

---

## ✅ Success Checklist

- [x] Shell commands plugin installed
- [x] Shell commands plugin enabled
- [x] New command added with Python script path
- [x] "Vault: After startup" event enabled
- [x] Command tested manually (works)
- [x] Vault reopened and note auto-populated

---

## 🎯 What Happens Now

**Every time you open Obsidian:**
1. Shell Commands plugin runs automatically
2. Python script checks which WalterSignal files exist
3. Determines current project phase
4. Populates daily note with relevant priorities
5. Updates revenue activities and project tasks
6. Only updates once per day (won't duplicate)

**The script is smart:**
- Detects your current project phase
- Suggests next actions based on progress
- Marks completed tasks with ✅
- Links to relevant files with [[wiki links]]

---

## 🔧 Optional Enhancements

### Add Manual Hotkey

If you want to trigger updates manually:

1. In Shell commands settings, find your command
2. Click **"Add hotkey"** or go to Hotkeys section
3. Search for "Update Daily Note"
4. Assign a hotkey (e.g., `Cmd + Shift + D`)
5. Now press your hotkey anytime to refresh the note

### Disable Auto-Update Temporarily

If you want to pause auto-updates:

1. Go to Shell commands settings
2. Find "Vault: After startup" toggle
3. Turn it OFF
4. Updates will stop until you turn it back on

### Run on Note Open

To update when you open the daily note (not just vault open):

1. In Shell commands settings
2. Enable **"File: After open"** event
3. Set file filter to: `Daily/*.md`

---

## 🐛 Troubleshooting

### "Command not found" or "python3: command not found"

**Fix:** Find your Python path
```bash
# In Terminal, run:
which python3

# Copy the full path (e.g., /usr/local/bin/python3)
# Update command to use that path:
/usr/local/bin/python3 /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
```

### No notification appears

**Check:**
1. Settings → Shell commands → Your command
2. Make sure "Execute in background" is ON
3. Set "Output channel" to "Notification"

### Daily note not updating

**Debug:**
1. Test command manually (click ▶️ button)
2. Check for error messages
3. Verify daily note exists in `Daily/` folder
4. Check state file:
   ```bash
   cat /Users/mikefinneran/Documents/ObsidianVault/.scripts/daily_note_state.json
   ```

### Updates happen twice

**Fix:** Only one trigger should be enabled
- Either "Vault: After startup" OR
- "File: After open"
- Not both (unless you want both)

### Permission denied

**Fix:** Make script executable
```bash
chmod +x /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
```

---

## 📱 Mobile Setup (iOS/Android)

**Note:** Shell commands don't work on mobile Obsidian

**Alternatives for mobile:**
- Use Templater plugin for mobile
- Or just update notes on desktop
- Mobile syncs via iCloud/Dropbox

---

## 🎨 Customization

### Change What Gets Populated

Edit the Python script:
```bash
# Open in your editor:
code /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py

# Or use nano:
nano /Users/mikefinneran/Documents/ObsidianVault/.scripts/update_daily_note.py
```

**Key functions to customize:**
- `get_waltersignal_priorities()` - Top 3 priorities
- `get_revenue_activities()` - Revenue tasks
- `get_project_tasks()` - Project checklist

### Add More Projects

Currently tracks:
- WalterSignal/WalterFetch
- LifeHub

To add FlyFlat or other projects, edit `get_project_tasks()` function.

---

## 📊 Monitoring

### Check Last Update

```bash
cat /Users/mikefinneran/Documents/ObsidianVault/.scripts/daily_note_state.json
```

Shows:
- Last update date
- Previous priorities
- Update status

### Force Fresh Update

```bash
# Delete state file to force update:
rm /Users/mikefinneran/Documents/ObsidianVault/.scripts/daily_note_state.json

# Then reopen Obsidian
```

---

## ✨ What You Just Automated

**Before:**
- Open Obsidian
- Create daily note manually
- Copy/paste priorities from project files
- Update tasks manually
- 10-15 minutes of setup time

**After:**
- Open Obsidian
- Daily note auto-populates with current priorities
- Tasks updated based on project progress
- 0 minutes of manual work
- **You saved 10-15 min every day!**

**Annual time savings: 60+ hours** 🎉

---

## 🚀 Next Steps

Now that auto-population works:

1. **Use your daily note** - It's your command center
2. **Check off tasks** as you complete them
3. **Add custom notes** in the Ideas section
4. **Review at end of day** - Mark what's done
5. **Tomorrow** - Fresh priorities auto-populate

---

## 📞 Support

**If you get stuck:**
1. Read troubleshooting section above
2. Test script manually: `python3 .scripts/update_daily_note.py`
3. Check Shell commands plugin docs
4. Ask me for help!

---

**Setup complete! Your daily notes will now auto-populate every time you open Obsidian.** ✨

**Last Updated:** 2025-10-23
**Script Location:** `.scripts/update_daily_note.py`
**Plugin:** Shell commands by Jarkko Linnanvirta
