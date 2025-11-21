# iTerm2 Expert Guide

## Overview
This guide documents advanced iTerm2 capabilities for power users, focusing on automation, scripting, and workflow optimization for software development with Claude Code.

---

## 1. Shell Integration Mastery

### What It Enables
Shell integration transforms iTerm2 from a basic terminal into an intelligent development environment.

### Key Features

#### Command Navigation
- **Cmd + Shift + Up/Down**: Jump between command prompts (marks)
- **Cmd + Shift + A**: Select output of last command (copy test results, logs)
- **Click left gutter**: Jump to specific command execution point

#### Directory Intelligence
- **Cmd + Opt + /**: Popup showing recent directories (frecency-sorted)
- Directory tracking persists even over SSH
- New tabs/splits automatically use current directory

#### Command History
- **Shift + Cmd + ;**: Command history popup (searchable)
- **Cmd + ;**: Autocomplete from history
- Toolbelt shows command history sidebar

#### File Operations Over SSH
- **Right-click filename**: Download with scp
- **Option + drag file**: Upload to remote host via scp
- Menu bar shows upload/download progress

#### Smart Alerts
- **Cmd + Opt + A**: Alert when next command completes (perfect for long builds)
- Command status indicators (red mark = failed command)

### Setup Verification
```bash
# Check if shell integration is active
echo $ITERM_SESSION_ID
# Should output a session ID

# Test command marks
ls
# You should see a blue triangle in left gutter
```

---

## 2. Triggers: Automation Without Code

### What They Are
Triggers execute actions when terminal output matches regex patterns. Think of them as "if-then" rules for your terminal.

### Common Use Cases

#### 1. Build Status Notifications
**Pattern:** `BUILD (SUCCESS|FAILED)`
**Action:** Post Notification
**Use:** Get macOS notifications when builds complete

#### 2. Auto-highlighting Errors
**Pattern:** `(ERROR|FATAL|Exception)`
**Action:** Highlight Text (red background)
**Use:** Instantly spot errors in logs

#### 3. Password Prompt Detection
**Pattern:** `^Password:`
**Action:** Show Alert
**Use:** Get attention when sudo requires password
**Important:** Enable "Instant" mode

#### 4. Auto-navigate to Error Files
**Pattern:** `File "([^"]+)", line (\d+)`
**Action:** Make Hyperlink
**Parameter:** `file://\1:\2`
**Use:** Cmd+Click Python tracebacks to open in editor

#### 5. Capture Test Results
**Pattern:** `PASS|FAIL`
**Action:** Capture Output
**Use:** Collect test results in dedicated toolbelt

### Setup Location
**Settings → Profiles → Advanced → Triggers → Edit**

### Pro Tips
- Use `Instant` mode for prompts without newlines
- Test regex patterns at regex101.com first
- Use capture groups `()` with `\1`, `\2` in parameters
- Order matters: put specific patterns before general ones

---

## 3. Python API: Programmatic Control

### What You Can Do
Control iTerm2 programmatically to automate complex workflows.

### Installation
```bash
pip3 install iterm2
```

### Example Use Cases

#### 1. Auto-split for Development
Create a script that opens:
- Left pane: Claude Code
- Top right: Test watcher (`npm run test:watch`)
- Bottom right: Development server (`npm run dev`)

```python
#!/usr/bin/env python3
import iterm2

async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window
    if window is not None:
        # Get current session
        session = window.current_tab.current_session

        # Split vertically (Claude Code | other)
        right = await session.async_split_pane(vertical=True)

        # Split right pane horizontally (tests | dev server)
        bottom_right = await right.async_split_pane(vertical=False)

        # Send commands
        await right.async_send_text('npm run test:watch\n')
        await bottom_right.async_send_text('npm run dev\n')

iterm2.run_until_complete(main)
```

#### 2. Project Launcher
Create profiles on-the-fly for different projects:
```python
async def open_project(project_name, working_dir):
    app = await iterm2.async_get_app(connection)

    # Create custom profile
    profile = await iterm2.LocalWriteOnlyProfile.async_get(connection)
    await profile.async_set_name(project_name)
    await profile.async_set_initial_directory(working_dir)

    # Open window with profile
    await app.async_create_window(profile=profile)
```

#### 3. Status Bar Updates
Show custom information in status bar:
```python
async def update_status_bar(connection, text):
    component = iterm2.StatusBarComponent(
        short_description="Custom",
        detailed_description="Custom status",
        knobs=[],
        exemplar="[Status]",
        update_cadence=None,
        identifier="com.example.custom-status"
    )

    await component.async_register(connection)
```

### Running Scripts

**Auto-launch script:**
1. Save to `~/Library/Application Support/iTerm2/Scripts/AutoLaunch/`
2. Scripts run automatically on iTerm2 start

**Manual scripts:**
1. Save to `~/Library/Application Support/iTerm2/Scripts/`
2. Access via **Scripts → [Your Script]**

**API Documentation:**
https://iterm2.com/python-api/

---

## 4. Advanced Keyboard Workflows

### Navigation Shortcuts

#### Window & Tab Management
```
Cmd + N                     New window
Cmd + T                     New tab
Cmd + [1-9]                 Switch to tab N
Cmd + Opt + [1-9]           Switch to window N
Cmd + W                     Close tab
Cmd + Shift + W             Close window
Cmd + [/]                   Previous/next tab
Cmd + Shift + [/]           Move tab left/right
```

#### Split Pane Navigation
```
Cmd + D                     Split vertically
Cmd + Shift + D             Split horizontally
Cmd + Opt + Arrow           Navigate between panes
Cmd + [                     Previous pane
Cmd + ]                     Next pane
Cmd + Shift + Enter         Maximize/restore pane
```

#### Search & Selection
```
Cmd + F                     Search (with regex support)
Cmd + E                     Find next match
Cmd + Shift + E             Find previous match
Cmd + A                     Select all
Cmd + Click                 Open URL or file path
Triple Click                Select entire line
```

#### Shell Integration Shortcuts
```
Cmd + Shift + Up            Previous command mark
Cmd + Shift + Down          Next command mark
Cmd + Shift + A             Select last command output
Cmd + Opt + A               Alert on next mark
Shift + Cmd + ;             Command history popup
Cmd + ;                     Autocomplete from history
Cmd + Opt + /               Recent directories
```

#### Clipboard & Paste
```
Cmd + C                     Copy (auto-copies selection)
Cmd + V                     Paste
Cmd + Shift + V             Paste slowly (for vim, etc.)
Cmd + Shift + H             Paste history
Cmd + Opt + E               Search all tabs
```

### Custom Key Bindings

**Settings → Keys → Key Bindings → +**

#### Useful Custom Mappings

**Clear scrollback on Cmd+K:**
- Keyboard Shortcut: `Cmd + K`
- Action: `Clear Buffer`

**Quick directory jump:**
- Keyboard Shortcut: `Cmd + Shift + O`
- Action: `Send Text`
- Parameter: `cd ~/Documents/ObsidianVault/Projects/WalterSignal\n`

**Run last command:**
- Keyboard Shortcut: `Cmd + R`
- Action: `Send Text`
- Parameter: `!!\n`

### Leader Key System

Set up a "leader" key for vim-style two-keystroke shortcuts:

**Settings → Keys → Leader → Cmd + B**

Then create bindings like:
- `Leader + t` → New tab
- `Leader + s` → Split pane
- `Leader + c` → Close pane

---

## 5. Dynamic Profiles: Configuration as Code

### Why Use Them
- Version control your terminal configurations
- Share profiles across machines via git
- Programmatically generate profiles for projects

### Setup

**1. Create directory:**
```bash
mkdir -p ~/Library/Application\ Support/iTerm2/DynamicProfiles
```

**2. Create profile file:**
```bash
cd ~/Library/Application\ Support/iTerm2/DynamicProfiles
```

**3. Example: Project-based profiles**
```json
{
  "Profiles": [
    {
      "Name": "WalterSignal",
      "Guid": "UNIQUE-GUID-1",
      "Working Directory": "~/Documents/ObsidianVault/Projects/WalterSignal",
      "Custom Directory": "Yes",
      "Badge Text": "WS",
      "Background Color": {
        "Red Component": 0.1,
        "Green Component": 0.1,
        "Blue Component": 0.15
      }
    },
    {
      "Name": "FlyFlat",
      "Guid": "UNIQUE-GUID-2",
      "Working Directory": "~/Documents/ObsidianVault/Projects/FlyFlat",
      "Custom Directory": "Yes",
      "Badge Text": "FF",
      "Background Color": {
        "Red Component": 0.1,
        "Green Component": 0.15,
        "Blue Component": 0.1
      }
    }
  ]
}
```

**4. Generate unique GUIDs:**
```bash
uuidgen  # Run for each profile
```

**5. Make profiles editable:**
Add `"Rewritable": true` to allow UI changes

### Advanced: SSH Host Profiles

```json
{
  "Profiles": [
    {
      "Name": "Production Server",
      "Guid": "UNIQUE-GUID-3",
      "Custom Command": "Yes",
      "Command": "ssh user@prod.example.com",
      "Badge Text": "PROD ⚠️",
      "Background Color": {
        "Red Component": 0.2,
        "Green Component": 0,
        "Blue Component": 0
      }
    }
  ]
}
```

### Version Control Setup

```bash
cd ~/.config/iterm2
ln -s ~/Library/Application\ Support/iTerm2/DynamicProfiles ./profiles
git add profiles/
git commit -m "Add iTerm2 dynamic profiles"
```

---

## 6. tmux Integration Mode

### When to Use
- Working on remote servers
- Need session persistence (survive disconnects)
- Multi-window workflows that need to survive reboots

### How It's Different
Traditional tmux: All windows in one terminal, requires prefix keys
iTerm2 + tmux: Native windows/tabs, no prefix keys, iTerm2 features work

### Setup

**On remote server:**
```bash
# Install tmux
brew install tmux  # or apt-get install tmux

# Basic ~/.tmux.conf
set -g default-terminal "screen-256color"
set -g mouse on
```

**From iTerm2:**
```bash
# Connect with integration
ssh user@host
tmux -CC

# Or connect in one command
ssh user@host -t 'tmux -CC attach || tmux -CC'
```

### Commands in tmux Integration

```
esc         Detach from tmux (session keeps running)
X           Force quit (kills tmux)
L           Toggle logging
C           Run custom tmux command
```

### Native Actions

Everything works natively:
- Close tab → kills tmux window
- Split pane → creates tmux split
- Resize → adjusts tmux dimensions
- Search → uses iTerm2 search
- Scrollback → full iTerm2 history

### Reattaching

```bash
# List sessions
tmux ls

# Reattach with integration
tmux -CC attach -t session-name

# Or use last session
tmux -CC attach
```

---

## 7. Status Bar Configuration

### Setup
**Settings → Profiles → Session → Configure Status Bar**

### Useful Components for Development

**System Monitoring:**
- CPU Utilization
- Memory Utilization
- Network Throughput

**Git Information:**
- Git Status (requires shell integration)

**Session Info:**
- Current Directory
- Host Name
- User Name

**Custom Components (via Python API):**
- Test pass/fail status
- Build status
- API response times
- Custom project info

### Layout Tips
- Place critical info on left (always visible)
- Use icons mode to save space
- Enable auto-hide when not needed

---

## 8. Claude Code Integration Workflows

### Optimal Layout for Development

#### Setup 1: Side-by-side Development
```
┌─────────────────┬─────────────────┐
│                 │                 │
│  Claude Code    │   Test Output   │
│                 │   (npm test)    │
│                 │                 │
└─────────────────┴─────────────────┘
```

**Commands:**
```bash
# In Claude Code pane
claude

# Split vertically: Cmd + D
# In new pane
npm run test:watch
```

#### Setup 2: Full Stack Development
```
┌─────────────────┬─────────────────┐
│                 │   Dev Server    │
│  Claude Code    │  (npm run dev)  │
│                 ├─────────────────┤
│                 │  Test Watcher   │
└─────────────────┴─────────────────┘
```

**Automation script:** (save as `~/dev-layout.sh`)
```bash
#!/bin/bash
# Open iTerm with development layout
osascript <<EOF
tell application "iTerm"
    create window with default profile
    tell current session of current window
        split vertically with default profile
        tell second session of current tab of current window
            write text "npm run dev"
            split horizontally with default profile
            tell third session of current tab of current window
                write text "npm run test:watch"
            end tell
        end tell
    end tell
end tell
EOF
```

### Triggers for Claude Code Workflows

#### Auto-highlight Claude suggestions
**Pattern:** `(SUGGESTION|TODO|FIXME|NOTE)`
**Action:** Highlight Text
**Color:** Yellow background

#### Capture test failures
**Pattern:** `FAIL.*`
**Action:** Capture Output

#### Alert on build completion
**Pattern:** `Build (complete|failed)`
**Action:** Post Notification

---

## 9. Model Context Protocol (MCP) Integration

### Overview
MCP allows AI applications (Claude Desktop or claude-code CLI) to control iTerm2 programmatically via the `iterm-mcp` server.

**Key Capabilities:**
- `write_to_terminal` - Execute commands in iTerm2
- `read_terminal_output` - Capture command results
- Full automation of terminal workflows from AI

### Quick Setup: Claude Desktop → iTerm2

**Method 1: Smithery (Recommended)**
```bash
npx -y @smithery/cli install iterm-mcp --client claude
```

**Method 2: Manual Configuration**
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "iterm-mcp": {
      "command": "npx",
      "args": ["-y", "iterm-mcp"]
    }
  }
}
```

**Method 3: Desktop Extensions**
- Open Claude Desktop
- Settings → Extensions
- Install "iTerm2" extension

### Advanced: Claude Code CLI → iTerm2

The claude-code CLI can also act as an MCP host:

```bash
claude mcp add-json "iterm-mcp" '{"command":"npx","args":["-y","iterm-mcp"]}'
```

### 🚨 CRITICAL: macOS Permissions

**This is the #1 failure point.** The iterm-mcp server uses AppleScript and requires explicit permissions.

**Steps:**

1. **Automation Permissions:**
   - macOS Settings → Privacy & Security → Automation
   - Find "Claude" (or "iTerm.app" for CLI usage)
   - Enable checkbox for: **iTerm.app**

2. **Accessibility Permissions:**
   - Privacy & Security → Accessibility
   - Add your host application

3. **Restart & Verify:**
   - Quit and restart host application completely
   - Test: Ask "What tools do you have?"
   - Should list: `write_to_terminal`, `read_terminal_output`

### Troubleshooting

**MCP Not Working:**
- Check permissions in System Settings (most common issue)
- Restart Claude Desktop / iTerm2 completely
- Verify config file syntax (valid JSON)
- Check Console.app for AppleScript errors

**For detailed Claude Code + MCP setup, see:**
`~/.config/iterm2/CLAUDE_CODE_INTEGRATION.md`

---

## 10. Advanced Selection & Copy

### Smart Selection

**Settings → Profiles → Advanced → Smart Selection**

Add custom rules for:

**Python files with line numbers:**
- Regex: `([a-zA-Z0-9_/\-\.]+\.py):(\d+)`
- Precision: Normal
- Action: Open with editor at line

**URLs (extended):**
- Regex: `https?://[^\s]+`
- Action: Open URL

**File paths:**
- Regex: `(/[a-zA-Z0-9_/\-\.]+)`
- Action: Open file

### Copy Modes

**Normal copy:** `Cmd + C`
**Copy with styles:** `Cmd + Opt + Shift + C` (preserves colors)
**Paste without formatting:** `Cmd + Opt + Shift + V`

### Selection Shortcuts

```
Triple-click                    Select entire line
Cmd + Click                     Open file/URL
Option + drag                   Rectangular selection
Cmd + Shift + A                 Select last command output
Shift + Click                   Extend selection
```

---

## 10. Debugging & Performance

### Debugging Terminal Output

**Capture output:**
**Shell → Captured Output**
- Automatically saves trigger-matched lines
- Searchable, exportable

**Session logging:**
**Shell → Start/Stop Logging**
- Records everything to file
- Useful for debugging automation

### Performance Optimization

#### If terminal feels slow:

**1. Reduce scrollback:**
**Settings → Profiles → Terminal → Scrollback lines**
- Set to 10,000 instead of unlimited for remote sessions

**2. Disable shell integration:**
- For very high-throughput scenarios (log tailing)
- Remove from .zshrc temporarily

**3. Use triggers sparingly:**
- Each trigger = regex evaluation on every line
- Disable unused triggers

**4. Check for CPU-heavy coprocesses:**
```bash
# In iTerm2
Settings → Profiles → Advanced → Coprocess
# Verify nothing unexpected is running
```

### Debug iTerm2 itself

**Enable debug logging:**
**Settings → Advanced → (search "debug")**
- Turn on relevant debug logging
- Check Console.app for logs

---

## 11. Badges: Visual Session Identification

### Setup
**Settings → Profiles → General → Badge**

### Useful Badge Text

**Show environment:**
```
\(session.terminalName) - \(user.gitBranch)
```

**Show host for SSH:**
```
\(session.hostname)
```

**Show custom project:**
```
WalterSignal
```

### Variables Available
- `\(session.username)`
- `\(session.hostname)`
- `\(session.path)` - working directory
- `\(user.gitBranch)` - current git branch
- Custom variables via Python API

---

## 12. Toolbelt: Sidebar Utilities

**Enable:** **View → Show Toolbelt** or `Cmd + Opt + B`

### Available Tools

**Captured Output:**
- Shows lines matched by Capture Output triggers
- Searchable, click to jump to source

**Command History:**
- Complete command history
- Click to re-run commands

**Recent Directories:**
- Frecency-sorted directory list
- Click to cd to directory

**Notes:**
- Scratch pad for session notes
- Persists across sessions

**Jobs:**
- Currently running jobs in session

### Custom Tools
Via Python API, create custom toolbelt components showing:
- Test coverage percentages
- Build status
- API health checks
- Custom project metrics

---

## 13. Inline Images

### Supported Protocols
- imgcat (iTerm2's custom protocol)
- Sixel graphics

### Use Cases

**View images in terminal:**
```bash
# Using imgcat
brew install iterm2
imgcat screenshot.png

# Built-in support
cat image.png  # May render depending on shell integration
```

**Matplotlib integration:**
```python
# In Python/iPython with matplotlib
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.show()  # Renders inline in iTerm2
```

---

## 14. Hotkey Windows

### Setup

**Settings → Keys → Hotkey**

**Enable:** "Show/hide all windows with a system-wide hotkey"
**Recommended:** `Option + Space`

### Use Cases

- **Instant terminal access** from any app
- **Overlay terminal** on top of browser/IDE
- **Scratchpad terminal** for quick commands

### Configuration

**Auto-hide:** Hide window when it loses focus
**Animate:** Smooth slide-in animation
**Pin:** Keep visible even when clicked away

### Profile Configuration

Create a dedicated "Hotkey Window" profile:
- Transparency: 90%
- Blur: Yes
- Working Directory: Home
- Window Size: Full width, 60% height

---

## 15. Keyboard Maestro & Alfred Integration

### iTerm2 + Keyboard Maestro

**Example: Quick Project Switcher**

```applescript
-- Keyboard Maestro macro
tell application "iTerm"
    create window with profile "WalterSignal"
end tell
```

### iTerm2 + Alfred

**Custom Alfred Workflow:**

```bash
# Open iTerm in specific directory
osascript -e "tell application \"iTerm\"
    create window with default profile command \"cd ~/Projects/WalterSignal && claude\"
end tell"
```

---

## 16. Color Schemes & Themes

### Popular Themes for Development

**Dark themes:**
- Solarized Dark (easy on eyes)
- Tomorrow Night (modern, clean)
- Monokai (high contrast)
- Dracula (purple accent)

**Light themes:**
- Solarized Light
- Tomorrow
- GitHub Light

### Import Themes

**Method 1: From website**
Visit: https://iterm2colorschemes.com/

**Method 2: Manual installation**
```bash
cd ~/Downloads
curl -O https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/master/schemes/Solarized%20Dark.itermcolors
```

**Import:**
**Settings → Profiles → Colors → Color Presets → Import**

### Custom Colors for Claude Code

Create a profile optimized for code review:
- Background: Very dark (#0a0a0a)
- Foreground: Light gray (#e0e0e0)
- Cursor: Bright cyan (easy to spot)
- Selection: Subtle blue

---

## 17. Automatic Profile Switching

### Setup
**Settings → Profiles → Advanced → Automatic Profile Switching**

### Use Cases

**Switch on SSH:**
```
Username: user
Hostname: prod.server.com
Profile: Production (red background)
```

**Switch by directory:**
```
Path: ~/Documents/ObsidianVault/Projects/WalterSignal
Profile: WalterSignal (custom badge, colors)
```

### Safety Profile for Production

Create a "Production" profile with:
- Red/orange background tint
- Badge: "PRODUCTION ⚠️"
- Requires confirmation for certain commands (via triggers)

---

## 18. Export & Backup

### Export Settings

**Full preferences:**
**Settings → General → Preferences → Save preferences to custom folder**

**Recommended location:**
```bash
~/Documents/ObsidianVault/.config/iterm2/
```

Then version control:
```bash
cd ~/Documents/ObsidianVault
git add .config/iterm2/
git commit -m "Backup iTerm2 config"
```

### What to backup

- Dynamic Profiles directory
- Scripts directory
- Custom color schemes
- Key bindings (if custom)

### Sync Across Machines

**Option 1: Git**
```bash
# Machine 1
cd ~/Library/Application\ Support/iTerm2
git init
git add DynamicProfiles/ Scripts/
git commit -m "Initial iTerm2 setup"
git push origin main

# Machine 2
cd ~/Library/Application\ Support/iTerm2
git clone your-repo .
```

**Option 2: iCloud/Dropbox**
```bash
# Point preferences to cloud folder
# Settings → General → Preferences → Load preferences from custom folder
```

---

## Quick Reference: Essential Commands

```bash
# Shell Integration
Cmd + Shift + Up/Down       Navigate command marks
Cmd + Shift + A             Select last command output
Cmd + Opt + A               Alert on next command
Shift + Cmd + ;             Command history
Cmd + Opt + /               Recent directories

# Window Management
Cmd + D                     Split vertically
Cmd + Shift + D             Split horizontally
Cmd + Opt + Arrow           Navigate panes
Cmd + Shift + Enter         Maximize/restore pane

# Search & Selection
Cmd + F                     Search
Cmd + Shift + H             Paste history
Triple-click                Select line

# Productivity
Cmd + ;                     Autocomplete from history
Cmd + K                     Clear buffer
Cmd + Opt + B               Toggle toolbelt
```

---

## Next Steps

1. **Configure shell integration** (already done ✓)
2. **Create dynamic profiles** for WalterSignal projects
3. **Set up triggers** for build notifications and error highlighting
4. **Customize key bindings** for common tasks
5. **Explore Python API** for advanced automation
6. **Set up tmux integration** for remote work

---

**Last Updated:** 2025-11-02
**For:** Mike Finneran / WalterSignal Development
**Configuration Location:** `~/.config/iterm2/`
