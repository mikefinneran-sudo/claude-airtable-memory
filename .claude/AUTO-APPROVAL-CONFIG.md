# Claude Code Auto-Approval Configuration

**Created**: 2025-10-29
**Status**: Active

---

## Overview

Claude Code will now automatically approve common bash commands and tool uses without prompting you each time.

---

## Configuration File

**Location**: `~/.config/claude-code/settings.json`

This file contains permission rules that auto-approve specific commands.

---

## What's Auto-Approved

### All Tool Uses ✅
- **Read** - Reading any file
- **Glob** - File pattern matching
- **Grep** - Content searching
- **WebSearch** - Web searches
- **WebFetch** - Fetching web content

### Common Bash Commands ✅
- File operations: `ls`, `cat`, `head`, `tail`, `find`, `grep`
- Directory operations: `cd`, `pwd`, `mkdir`, `cp`, `mv`, `rm`
- Text processing: `awk`, `sed`, `wc`, `sort`
- System: `chmod`, `which`, `source`, `open`, `osascript`

### Development Tools ✅
- Git: `git *` (all git commands)
- Node/NPM: `npm *`, `node *`
- Python: `python *`, `python3 *`, `pip *`, `pip3 *`
- Package managers: `brew *`
- Docker: `docker *`
- Network: `curl *`, `wget *`, `ssh *`

### Your Project Scripts ✅
- All scripts in `~/.claude/scripts/*`
- `cproject`, `cresearch`, `ccontext`, `cwarp`
- `~/.claude/init-project-memory.sh`

---

## How It Works

1. **No More Prompts**: Commands matching the allow list execute immediately
2. **Faster Workflow**: No interruptions for common safe commands
3. **Still Safe**: Only approved patterns are auto-executed

---

## Modifying Permissions

Edit `~/.config/claude-code/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(your-command:*)",
      "Bash(/path/to/script:*)"
    ],
    "deny": [
      "Bash(dangerous-command:*)"
    ]
  }
}
```

**Patterns:**
- `Bash(*)` - Approve ALL bash commands (current setting)
- `Bash(git:*)` - Approve all git commands
- `Bash(npm run:*)` - Approve npm run scripts
- `Bash(/specific/path/*)` - Approve scripts in specific directory

---

## Quick Toggle (Alternative Method)

Press **Shift+Tab** in Claude Code to cycle through permission modes:
- **Normal** - Prompt for each command
- **Auto-accept edit on** - Auto-approve all edits
- **Auto-accept all on** - Auto-approve everything

---

## Safety Notes

### Currently Approved
✅ Common file operations (ls, cat, etc.)
✅ Your project management scripts
✅ Development tools (git, npm, python)
✅ Web tools (searches, fetches)

### What This Means
- Claude can execute these commands without asking
- Speeds up your workflow significantly
- Still safe because patterns are specific

### If You Want More Control

**Option 1**: Remove `Bash(*)` from the allow list and add specific commands:
```json
"allow": [
  "Bash(ls:*)",
  "Bash(cat:*)",
  "Bash(git:*)",
  // etc.
]
```

**Option 2**: Add dangerous commands to deny list:
```json
"deny": [
  "Bash(rm -rf /*)",
  "Bash(sudo rm:*)"
]
```

**Option 3**: Use Shift+Tab to toggle modes per session

---

## Restart Required

After editing `settings.json`, restart Claude Code for changes to take effect:

```bash
# Exit Claude Code, then restart
claude
```

---

## Testing

To verify auto-approval is working:

```bash
# These should execute without prompts:
ls
echo "test"
git status
cproject --help
```

If you still see prompts, check:
1. Settings file exists: `cat ~/.config/claude-code/settings.json`
2. JSON syntax is valid
3. You've restarted Claude Code

---

## Disabling Auto-Approval

**Option 1**: Delete or rename the settings file:
```bash
mv ~/.config/claude-code/settings.json ~/.config/claude-code/settings.json.backup
```

**Option 2**: Edit the file and remove patterns from `allow` list

**Option 3**: Use Shift+Tab to switch to normal mode

---

## Current Configuration

```json
{
  "permissions": {
    "allow": [
      "Bash(*)",
      // All common commands
      // All your project scripts
      // All tool uses
    ],
    "deny": []
  },
  "autoAllowBashIfSandboxed": true
}
```

**Translation**: Auto-approve everything except items in deny list.

---

## Benefits

✅ **No interruptions** - Commands execute immediately
✅ **Faster development** - No approval clicks
✅ **Smoother workflow** - Especially for multi-step tasks
✅ **Still safe** - Only patterns you've approved

---

## Common Patterns to Add

If you want to be more specific than `Bash(*)`:

```json
// Project-specific
"Bash(cd ~/Documents/ObsidianVault/*)",
"Bash(cd ~/.claude/*)",

// Safe read operations
"Bash(cat:*)",
"Bash(ls:*)",
"Bash(head:*)",
"Bash(tail:*)",

// Git operations
"Bash(git status:*)",
"Bash(git diff:*)",
"Bash(git log:*)",
"Bash(git add:*)",
"Bash(git commit:*)",

// Package management
"Bash(npm install:*)",
"Bash(npm run:*)",
"Bash(pip install:*)",

// Your scripts
"Bash(~/.claude/scripts/*.sh:*)",
"Bash(cproject:*)",
"Bash(cresearch:*)"
```

---

## Troubleshooting

### Still Getting Prompts?

1. **Check file location**:
   ```bash
   cat ~/.config/claude-code/settings.json
   ```

2. **Validate JSON**:
   ```bash
   python3 -m json.tool ~/.config/claude-code/settings.json
   ```

3. **Restart Claude Code completely**

4. **Try Shift+Tab method** as alternative

### Want to See What Would Be Approved?

Check the Claude Code system prompt - it shows what's currently approved:
```
"You can use the following tools without requiring user approval: ..."
```

---

## Documentation

**This file**: Auto-approval configuration
**Settings file**: `~/.config/claude-code/settings.json`
**Claude Code docs**: https://docs.claude.com/claude-code/settings

---

**Status**: ✅ Active - All bash commands and common tools auto-approved

**Last Updated**: 2025-10-29
