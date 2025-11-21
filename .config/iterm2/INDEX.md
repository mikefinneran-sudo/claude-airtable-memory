# iTerm2 Knowledge Base Index

## Quick Start
New to iTerm2? Start here:
1. Read `QUICK_REFERENCE.md` (5 min)
2. Try essential shortcuts
3. Set up shell integration (already done ✓)

## Documentation Structure

### 📘 QUICK_REFERENCE.md
**What:** Essential shortcuts and daily-use commands
**When to read:** Right now, keep handy
**Time:** 5-10 minutes
**Focus:**
- Core keyboard shortcuts
- Tab/pane management
- Copy/paste workflows
- Essential troubleshooting

### 📕 EXPERT_GUIDE.md
**What:** Comprehensive iTerm2 capabilities and advanced features
**When to read:** When you want to level up or need specific feature
**Time:** 30-60 minutes (reference document)
**Focus:**
- Shell integration deep dive
- Triggers and automation
- Python API
- tmux integration
- Dynamic profiles
- Status bar, badges, toolbelt
- Performance optimization

### 📗 CLAUDE_CODE_WORKFLOWS.md
**What:** Practical development layouts optimized for Claude Code
**When to read:** Before starting a coding session
**Time:** 15-20 minutes (pick relevant workflows)
**Focus:**
- 10 ready-to-use layouts
- Setup scripts and automation
- Keyboard shortcuts for each workflow
- Troubleshooting common issues

### 📄 verify-setup.sh
**What:** Verification script for iTerm2 installation
**When to run:** After setup or when troubleshooting
**Usage:** `~/.config/iterm2/verify-setup.sh`

---

## Learning Path

### Level 1: Basic Proficiency (Week 1)
**Goal:** Replace Warp with confidence

**Read:**
- QUICK_REFERENCE.md (all)

**Practice:**
1. Tab management (Cmd+T, Cmd+W, Cmd+1-9)
2. Split panes (Cmd+D, Cmd+Shift+D)
3. Navigate panes (Cmd+Opt+Arrow)
4. Search (Cmd+F)
5. Command marks (Cmd+Shift+Up/Down)

**Daily usage:**
- Use iTerm2 exclusively for 1 week
- Force yourself to use keyboard shortcuts
- Avoid mouse for navigation

### Level 2: Intermediate Power User (Week 2-3)
**Goal:** Optimize development workflow

**Read:**
- CLAUDE_CODE_WORKFLOWS.md (sections 1-5)
- EXPERT_GUIDE.md (sections 1, 4, 12)

**Implement:**
1. Set up split pane layout for TDD
2. Configure triggers for test pass/fail
3. Create dynamic profile for WalterSignal
4. Use command history (Shift+Cmd+;)
5. Enable status bar with useful components

**Practice workflows:**
- Use TDD layout daily
- Set marks before long operations
- Use Cmd+Shift+A to copy output
- Alert on completion (Cmd+Opt+A)

### Level 3: Advanced Automation (Week 4+)
**Goal:** Automate repetitive tasks

**Read:**
- EXPERT_GUIDE.md (all)
- CLAUDE_CODE_WORKFLOWS.md (sections 6-10)

**Build:**
1. Python API script for auto-layout
2. Custom triggers for project-specific needs
3. Dynamic profiles for all projects
4. Keyboard maestro/Alfred integration
5. tmux integration for remote work

**Master:**
- Python API basics
- Trigger regex patterns
- AppleScript integration
- Advanced keyboard shortcuts

---

## Common Tasks → Documentation

### "I want to..."

**...split my terminal for Claude Code + tests**
→ CLAUDE_CODE_WORKFLOWS.md, Workflow 2

**...get notified when builds complete**
→ EXPERT_GUIDE.md, Section 2 (Triggers)

**...jump back to see what command Claude suggested**
→ QUICK_REFERENCE.md, Command Navigation
→ Use: Cmd+Shift+Up

**...copy test output to show Claude**
→ QUICK_REFERENCE.md, Selection shortcuts
→ Use: Cmd+Shift+A, then Cmd+C

**...create different profiles for each project**
→ EXPERT_GUIDE.md, Section 5 (Dynamic Profiles)

**...automate my development setup**
→ CLAUDE_CODE_WORKFLOWS.md, Workflow 3 (automation script)
→ EXPERT_GUIDE.md, Section 3 (Python API)

**...work on a remote server without losing my session**
→ EXPERT_GUIDE.md, Section 6 (tmux integration)
→ CLAUDE_CODE_WORKFLOWS.md, Workflow 5

**...search through my command history**
→ QUICK_REFERENCE.md, Search & History
→ Use: Shift+Cmd+;

**...highlight errors in my terminal automatically**
→ EXPERT_GUIDE.md, Section 2 (Triggers)

**...make file paths in errors clickable**
→ EXPERT_GUIDE.md, Section 9 (Smart Selection)

---

## Quick Reference Shortcuts

### Most Used (Memorize These)
```
Cmd + D                 Split vertically
Cmd + Shift + D         Split horizontally
Cmd + Opt + Arrow       Navigate panes
Cmd + Shift + Enter     Maximize pane
Cmd + T                 New tab
Cmd + [1-9]             Switch to tab

Cmd + Shift + Up        Previous command
Cmd + Shift + A         Select command output
Cmd + F                 Search
Cmd + K                 Clear buffer
Shift + Cmd + ;         Command history
```

### Shell Integration
```
Cmd + Shift + M         Set mark
Cmd + Opt + A           Alert on next command
Cmd + Opt + /           Recent directories
```

### Power User
```
Cmd + Opt + B           Toggle toolbelt
Cmd + Shift + H         Paste history
Cmd + ;                 Autocomplete
```

---

## Troubleshooting Index

### Issue → Solution Location

**Bio auth prompts**
→ Already fixed (disabled Warp)

**Lost Claude output in scrollback**
→ CLAUDE_CODE_WORKFLOWS.md, Troubleshooting
→ Use marks (Cmd+Shift+M)

**Terminal feels slow**
→ EXPERT_GUIDE.md, Section 10 (Performance)

**Can't find command Claude suggested**
→ Use Shift+Cmd+; (command history)

**Need same command in multiple panes**
→ EXPERT_GUIDE.md, Section 8 (broadcast input)

**Accidentally closed important pane**
→ CLAUDE_CODE_WORKFLOWS.md, Troubleshooting
→ Save window arrangements

**Shell integration not working**
→ Run verify-setup.sh
→ Source ~/.zshrc

**Want to start fresh**
→ QUICK_REFERENCE.md, Reset instructions

---

## Configuration Files

### Active Configuration
```
~/.config/iterm2/
├── QUICK_REFERENCE.md          ← Basic shortcuts
├── EXPERT_GUIDE.md              ← Advanced features
├── CLAUDE_CODE_WORKFLOWS.md     ← Development layouts
├── INDEX.md                     ← This file
├── verify-setup.sh              ← Setup checker
├── com.googlecode.iterm2.plist  ← Preferences
└── layouts/                     ← Custom layout scripts
```

### System Locations
```
~/Library/Application Support/iTerm2/
├── DynamicProfiles/             ← Project profiles (JSON)
└── Scripts/
    ├── AutoLaunch/              ← Auto-run Python scripts
    └── [manual]/                ← Manual Python scripts

~/.iterm2_shell_integration.zsh  ← Shell integration
```

### Version Control

**Already in git:**
- ~/.config/iterm2/ (this directory)

**Should add to git:**
```bash
cd ~/Library/Application\ Support/iTerm2
git init
git add DynamicProfiles/ Scripts/
git commit -m "iTerm2 configuration"
```

---

## External Resources

### Official Documentation
- **Main docs:** https://iterm2.com/documentation.html
- **Python API:** https://iterm2.com/python-api/
- **Shell integration:** https://iterm2.com/documentation-shell-integration.html
- **Triggers:** https://iterm2.com/documentation-triggers.html

### Community Resources
- **Color schemes:** https://iterm2colorschemes.com/
- **GitHub:** https://github.com/gnachman/iTerm2
- **Reddit:** r/iterm2
- **Stack Overflow:** [iterm2] tag

---

## Maintenance

### Weekly
- Check for iTerm2 updates (auto-checks enabled)
- Review command history for automation opportunities
- Clean up old dynamic profiles if needed

### Monthly
- Backup configuration to git
- Review and update triggers
- Optimize workflows based on usage

### Quarterly
- Read iTerm2 release notes for new features
- Update EXPERT_GUIDE.md with new capabilities
- Share workflows with team (if applicable)

---

## Next Steps for Mike

### Immediate (This Week)
1. ✅ Install and configure iTerm2
2. ✅ Remove Warp
3. ✅ Learn basic shortcuts
4. ⏳ Create WalterSignal dynamic profile
5. ⏳ Set up triggers for test notifications

### Short Term (This Month)
1. ⏳ Master split pane workflows
2. ⏳ Implement TDD layout for daily use
3. ⏳ Create automation scripts for common tasks
4. ⏳ Set up tmux integration for remote work

### Long Term (This Quarter)
1. ⏳ Build Python API scripts for project automation
2. ⏳ Create complete dynamic profiles for all projects
3. ⏳ Integrate with Keyboard Maestro/Alfred
4. ⏳ Share workflows and configurations

---

## Feedback & Iteration

### What's Working
- Document as you discover workflows
- Keep notes in this directory

### What Needs Improvement
- Add to EXPERT_GUIDE.md
- Update workflows based on real usage

### Feature Requests for Future Research
- (Add items here as you discover needs)

---

**Created:** 2025-11-02
**Last Updated:** 2025-11-02
**Maintained By:** Mike Finneran
**For:** WalterSignal Development / Claude Code Sessions

**Status:** Expert-level knowledge base complete
**Confidence:** Ready to provide advanced iTerm2 guidance
