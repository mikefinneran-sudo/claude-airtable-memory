# iTerm2 Quick Reference

## Why iTerm2 over Warp
- **Zero authentication prompts** - just works
- **Rock solid stability** - battle-tested terminal
- **Lightweight** - native Mac app, not Electron
- **Stays out of your way** - no AI suggestions competing with Claude Code
- **Unlimited customization** - complete control

## Essential Keyboard Shortcuts

### Tab Management
- `Cmd + T` - New tab
- `Cmd + W` - Close tab
- `Cmd + [number]` - Switch to tab [number]
- `Cmd + Left/Right` - Previous/Next tab

### Split Panes
- `Cmd + D` - Split pane vertically
- `Cmd + Shift + D` - Split pane horizontally
- `Cmd + Option + Arrow` - Navigate between panes
- `Cmd + Shift + Enter` - Maximize/restore current pane

### Search & History
- `Cmd + F` - Search (regex supported)
- `Cmd + Shift + H` - Paste history
- `Cmd + ;` - Autocomplete (based on command history)
- `Cmd + Option + E` - Search all tabs

### Selection & Copy/Paste
- `Cmd + C` - Copy (auto-copies selection)
- `Cmd + V` - Paste
- `Triple-click` - Select entire line
- `Cmd + Click` - Open URL or file

### Window Management
- `Cmd + N` - New window
- `Cmd + Shift + N` - New window with same profile
- `Cmd + Option + I` - Broadcast to all panes in tab
- `Cmd + Shift + I` - Broadcast to all panes in all tabs

### Marks & Navigation
- `Cmd + Shift + M` - Set mark
- `Cmd + Shift + Up/Down` - Jump to previous/next mark
- `Cmd + Shift + A` - Select output of last command

## Shell Integration Features (Already Configured)

### Command History
- Shell integration automatically tracks all commands
- Click on command start markers in left gutter
- `Cmd + Shift + Up` jumps to previous command

### Working Directory Tracking
- iTerm2 knows your current directory
- New tabs/panes open in current directory
- Useful for command history context

### Status Bar (Optional)
- Right-click window title bar → Edit Session
- Configure components: CPU, memory, git branch, etc.

## Best Practices for Claude Code

### Recommended Workflow
1. Open iTerm2
2. Create project-specific profiles (Preferences → Profiles)
3. Use split panes for multi-tasking:
   - Left: Claude Code session
   - Right: Test output, logs, or server
4. Use marks (`Cmd+Shift+M`) before long operations

### Profile Setup (Optional)
Create profiles for different projects:
1. `Cmd + ,` → Profiles
2. Duplicate default profile
3. Name it (e.g., "WalterSignal")
4. Set working directory to project root
5. Customize colors, fonts as needed

## Performance Tips

### Already Configured
- Unlimited scrollback (uses disk cache)
- Shell integration enabled
- Auto-copy on selection
- No unnecessary animations
- API server enabled for automation

### If Performance Issues
- Disable transparency: Preferences → Profiles → Window → Transparency
- Reduce scrollback: Preferences → Profiles → Terminal → Scrollback lines
- Turn off shell integration (rare)

## Customization Quick Hits

### Change Theme
`Cmd + ,` → Profiles → Colors → Color Presets → [choose]

**Recommended presets:**
- Solarized Dark (classic, readable)
- Tomorrow Night (modern, clean)
- Tango Dark (vibrant)

### Change Font
`Cmd + ,` → Profiles → Text → Font

**Recommended fonts:**
- SF Mono (system default, excellent)
- Menlo (classic Mac monospace)
- JetBrains Mono (ligatures, modern)
- Fira Code (ligatures, popular)

### Hotkey Window (Advanced)
1. `Cmd + ,` → Keys → Hotkey
2. Enable "Show/hide all windows with a system-wide hotkey"
3. Set to `Option + Space` (or your preference)
4. Instant drop-down terminal from anywhere

## Troubleshooting

### Shell Integration Not Working
```bash
curl -L https://iterm2.com/shell_integration/zsh | bash
source ~/.zshrc
```

### Reset to Defaults
```bash
rm ~/.config/iterm2/com.googlecode.iterm2.plist
defaults delete com.googlecode.iterm2
```

### Performance Issues
1. Check CPU usage: `top` or Activity Monitor
2. Reduce scrollback buffer
3. Disable shell integration temporarily

## Migration from Warp

### What You'll Miss (Spoiler: Not Much)
- AI command suggestions (you have Claude Code)
- Block-based UI (panes are better)
- Modern design (iTerm2 is clean enough)

### What You'll Gain
- No bio auth prompts
- Faster, more stable
- Lower memory usage
- Better with tmux/screen
- More keyboard shortcuts
- True Unix terminal experience

## Quick Commands

### Open iTerm2 from CLI
```bash
open -a iTerm
```

### Open new tab with command
```bash
osascript -e 'tell application "iTerm" to create window with default profile command "ls -la"'
```

### Export/Import Settings
**Export:** Preferences → General → Preferences → Save preferences to a custom folder
**Import:** Point to folder on new machine

---

**Configuration Location:** `~/.config/iterm2/`
**Shell Integration:** `~/.iterm2_shell_integration.zsh`
**Docs:** https://iterm2.com/documentation.html

*Configured: 2025-11-02*
*For: Mike Finneran / WalterSignal Projects*
