# iTerm2 + Claude Code: Power User Workflows

## Overview
Optimized iTerm2 workflows specifically for Claude Code development sessions. These workflows minimize context switching and maximize productivity.

---

## Workflow 1: Solo Development (Simple)

### Layout
```
┌───────────────────────────────────┐
│                                   │
│        Claude Code Session        │
│                                   │
│                                   │
└───────────────────────────────────┘
```

### Setup
```bash
# Just open iTerm and run claude
claude
```

### When to Use
- Quick fixes
- Code reviews
- Research/exploration
- Single-file edits

### Pro Tips
- Use `Cmd + Shift + A` to select test output and copy to Claude
- Use `Cmd + K` to clear scrollback between tasks
- Use `/clear` in Claude to manage context

---

## Workflow 2: Test-Driven Development

### Layout
```
┌─────────────────┬─────────────────┐
│                 │                 │
│  Claude Code    │   Test Output   │
│                 │  npm test:watch │
│                 │                 │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Start Claude
claude

# Split vertically: Cmd + D
# Terminal 2: Start test watcher
npm run test:watch
# or
pytest --watch
```

### Workflow Steps
1. Describe feature to Claude in left pane
2. Watch tests fail in right pane (TDD)
3. Claude implements in left pane
4. Watch tests pass in right pane
5. Select test output (`Cmd + Shift + A`) if needed for debugging

### Enhanced with Triggers

**Add trigger for test failures:**
- Pattern: `FAIL|ERROR|✗`
- Action: Highlight Text (red)

**Add trigger for test passes:**
- Pattern: `PASS|✓`
- Action: Highlight Text (green)

**Add trigger for test completion:**
- Pattern: `Test Suites: .*`
- Action: Post Notification

### iTerm2 Settings for This Workflow
**Settings → Profiles → Advanced → Triggers → Add:**

```
Pattern: ^\s*(FAIL|ERROR|✗)
Action: Highlight Text
Color: Red Background

Pattern: ^\s*(PASS|✓|OK)
Action: Highlight Text
Color: Green Background

Pattern: (Test Suites:.*|Tests:.*passed)
Action: Post Notification
Text: Tests complete
```

---

## Workflow 3: Full Stack Development

### Layout
```
┌─────────────────┬─────────────────┐
│                 │  Dev Server     │
│  Claude Code    │  localhost:3000 │
│                 ├─────────────────┤
│                 │  Test Watcher   │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Claude
claude

# Split vertically: Cmd + D
# Terminal 2: Dev server
npm run dev

# Split horizontally: Cmd + Shift + D
# Terminal 3: Test watcher
npm run test:watch
```

### Navigation
- `Cmd + Opt + Arrow` to jump between panes
- `Cmd + Shift + Enter` to maximize Claude pane temporarily
- `Cmd + Opt + B` to open toolbelt for command history

### Automation Script

Save as `~/.config/iterm2/layouts/fullstack-dev.sh`:

```bash
#!/bin/bash
# Full stack development layout

# Get current directory for context
PROJECT_DIR=$(pwd)

osascript <<EOF
tell application "iTerm"
    set newWindow to (create window with default profile)
    tell current session of newWindow
        -- Left pane: Claude Code
        write text "claude"

        -- Split vertically for dev server
        set devSession to (split vertically with same profile)
        tell devSession
            write text "npm run dev"

            -- Split horizontally for tests
            set testSession to (split horizontally with same profile)
            tell testSession
                write text "npm run test:watch"
            end tell
        end tell
    end tell
end tell
EOF
```

**Make it executable:**
```bash
chmod +x ~/.config/iterm2/layouts/fullstack-dev.sh
```

**Add alias to ~/.zshrc:**
```bash
alias dev-layout="~/.config/iterm2/layouts/fullstack-dev.sh"
```

---

## Workflow 4: Backend + Database Development

### Layout
```
┌─────────────────┬─────────────────┐
│                 │  API Server     │
│  Claude Code    │  :8000          │
│                 ├─────────────────┤
│                 │  Database       │
│                 │  psql/mongo     │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Claude
claude

# Split vertically: Cmd + D
# Terminal 2: API server
python -m uvicorn main:app --reload

# Split horizontally: Cmd + Shift + D
# Terminal 3: Database REPL
psql database_name
# or
mongo
```

### Pro Tips
- Use marks (`Cmd + Shift + M`) before running migrations
- Use `Cmd + Shift + Up` to jump back to pre-migration state
- Copy SQL/query output with `Cmd + Shift + A`

---

## Workflow 5: Remote Development (SSH + tmux)

### Layout
```
┌─────────────────┬─────────────────┐
│                 │                 │
│  Local Claude   │  Remote tmux    │
│  Code           │  ssh + tmux -CC │
│                 │                 │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Local Claude
claude

# Split vertically: Cmd + D
# Terminal 2: SSH with tmux integration
ssh user@remote-host -t 'tmux -CC attach || tmux -CC'
```

### Benefits
- Local Claude can read/edit local files
- Remote tmux session persists across disconnects
- Native iTerm2 windows for remote tmux windows
- All iTerm2 features work on remote session

### Use Case
- Deploying to remote server
- Testing on production-like environment
- Working with large datasets that can't be local

---

## Workflow 6: Multiple Project Switching

### Use Dynamic Profiles

Create `~/Library/Application Support/iTerm2/DynamicProfiles/projects.json`:

```json
{
  "Profiles": [
    {
      "Name": "WalterSignal",
      "Guid": "waltersignal-guid",
      "Working Directory": "~/Documents/ObsidianVault/Projects/WalterSignal",
      "Custom Directory": "Yes",
      "Badge Text": "WS",
      "Initial Text": "clear && echo 'WalterSignal Development' && ls",
      "Shortcut": "W"
    },
    {
      "Name": "FlyFlat",
      "Guid": "flyflat-guid",
      "Working Directory": "~/Documents/ObsidianVault/Projects/FlyFlat",
      "Custom Directory": "Yes",
      "Badge Text": "FF",
      "Initial Text": "clear && echo 'FlyFlat Development' && ls",
      "Shortcut": "F"
    }
  ]
}
```

**Usage:**
1. `Cmd + O` (open profile)
2. Type "W" for WalterSignal or "F" for FlyFlat
3. New window opens in correct directory with badge

---

## Workflow 7: Code Review Session

### Layout
```
┌─────────────────┬─────────────────┐
│                 │                 │
│  Claude Code    │  git diff       │
│  (review)       │  or             │
│                 │  gh pr view     │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Claude
claude

# Split vertically: Cmd + D
# Terminal 2: View changes
git diff main...feature-branch

# Or view PR
gh pr view 123
```

### Workflow
1. Review diff in right pane
2. Ask Claude for review in left pane
3. Use `Cmd + Shift + A` to select diff sections
4. Paste into Claude for specific feedback
5. Implement changes in Claude pane

### Enhanced with Smart Selection

**Add smart selection rule:**
**Settings → Profiles → Advanced → Smart Selection**

```
Regex: ([a-zA-Z0-9_/\-\.]+):(\d+)
Action: Open with command
Command: code --goto "\1:\2"
```

Now you can Cmd+Click file paths in diffs to open in VS Code.

---

## Workflow 8: Documentation Writing

### Layout
```
┌─────────────────┬─────────────────┐
│                 │                 │
│  Claude Code    │  Live Preview   │
│  (MD editing)   │  (browser)      │
│                 │                 │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Claude
claude

# Split vertically: Cmd + D
# Terminal 2: Live preview server
npx live-server --open=README.md
# or
grip README.md
```

### Workflow
1. Write documentation with Claude in left pane
2. See live preview in right pane (browser)
3. Iterate on formatting and content

---

## Workflow 9: Debugging Session

### Layout
```
┌─────────────────┬─────────────────┐
│                 │  Debugger       │
│  Claude Code    │  pdb/node       │
│                 │  --inspect      │
│                 ├─────────────────┤
│                 │  Logs           │
│                 │  tail -f        │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Claude
claude

# Split vertically: Cmd + D
# Terminal 2: Debugger
node --inspect-brk app.js

# Split horizontally: Cmd + Shift + D
# Terminal 3: Logs
tail -f logs/app.log
```

### Triggers for Debugging

```
Pattern: (Exception|Traceback|Error:)
Action: Highlight Line (red)

Pattern: \[DEBUG\]
Action: Change Style (gray foreground)

Pattern: \[ERROR\]
Action: Post Notification
```

### Workflow
1. Reproduce bug in debugger pane
2. Watch logs in bottom pane
3. Copy error output (`Cmd + Shift + A`)
4. Paste to Claude for analysis
5. Implement fix suggested by Claude

---

## Workflow 10: Performance Profiling

### Layout
```
┌─────────────────┬─────────────────┐
│                 │  Profiler       │
│  Claude Code    │  py-spy/clinic  │
│                 ├─────────────────┤
│                 │  htop/Activity  │
└─────────────────┴─────────────────┘
```

### Setup
```bash
# Terminal 1: Claude
claude

# Split vertically: Cmd + D
# Terminal 2: Profiler
py-spy top --pid $(pgrep python)
# or
clinic doctor -- node app.js

# Split horizontally: Cmd + Shift + D
# Terminal 3: System monitor
htop
```

### Workflow
1. Identify bottleneck in profiler
2. Copy profile output
3. Analyze with Claude
4. Implement optimization
5. Re-run profiler to verify improvement

---

## Universal Keyboard Shortcuts for All Workflows

### Core Navigation
```
Cmd + Opt + Left/Right/Up/Down    Navigate between panes
Cmd + Shift + Enter               Maximize current pane
Cmd + ]                           Next pane
Cmd + [                           Previous pane
```

### Copy & Paste Workflow
```
Cmd + Shift + A                   Select last command output
Cmd + C                           Copy selection
Cmd + V                           Paste to Claude
```

### Session Management
```
Cmd + T                           New tab (new project)
Cmd + W                           Close tab
Cmd + Shift + I                   Broadcast to all panes (dangerous!)
```

### Quick Actions
```
Cmd + K                           Clear scrollback (clean slate)
Cmd + ;                           Autocomplete from history
Shift + Cmd + ;                   Command history popup
Cmd + Opt + /                     Recent directories
```

---

## Advanced: Python API Automation

### Auto-Setup Development Layout

Save as `~/Library/Application Support/iTerm2/Scripts/AutoLaunch/dev-setup.py`:

```python
#!/usr/bin/env python3
import iterm2

async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Watch for new windows
    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            session = app.get_session_by_id(session_id)

            # Get working directory
            working_dir = await session.async_get_variable("path")

            # If in a project directory, auto-setup panes
            if "WalterSignal" in working_dir:
                await setup_waltersignal_layout(session)

async def setup_waltersignal_layout(session):
    """Auto-setup layout for WalterSignal project"""
    # Split for test runner
    test_pane = await session.async_split_pane(vertical=True)
    await test_pane.async_send_text("npm run test:watch\n")

    # Split for dev server
    dev_pane = await test_pane.async_split_pane(vertical=False)
    await dev_pane.async_send_text("npm run dev\n")

iterm2.run_forever(main)
```

**This script automatically:**
1. Detects when you cd into WalterSignal directory
2. Auto-creates test and dev server panes
3. Starts watchers automatically

---

## Troubleshooting Common Issues

### Issue: Claude output gets lost in scrollback
**Solution:** Use marks before long operations
```
Cmd + Shift + M (set mark)
# Run Claude command
Cmd + Shift + Up (jump back to mark)
```

### Issue: Tests running too fast to read
**Solution:** Add trigger to capture test results
```
Pattern: (Tests: .*)
Action: Capture Output
```
Then view in toolbelt: `Cmd + Opt + B`

### Issue: Can't find command Claude suggested
**Solution:** Use command history
```
Shift + Cmd + ; (command history popup)
# Search for command
```

### Issue: Need to run same command in all panes
**Solution:** Broadcast input
```
Cmd + Shift + I (broadcast to all panes in all tabs)
# Or right-click pane title → Broadcast Input
```

**⚠️ Warning:** Be careful with broadcast mode in production!

### Issue: Pane layout reset after accidental close
**Solution:** Window arrangements
```
Window → Save Window Arrangement (Cmd + Shift + S)
Window → Restore Window Arrangement
```

---

## Cheatsheet: Quick Command Reference

```bash
# Start Claude in project
cd ~/Documents/ObsidianVault/Projects/WalterSignal
claude

# Split for tests (vertical)
Cmd + D → npm run test:watch

# Split for dev server (horizontal from tests)
Cmd + Opt + Right (navigate to test pane)
Cmd + Shift + D → npm run dev

# Jump to Claude pane
Cmd + Opt + Left (twice)

# Maximize Claude pane for focus
Cmd + Shift + Enter

# Copy test output to show Claude
(In test pane) Cmd + Shift + A → Cmd + C
(In Claude pane) Cmd + V

# Clear Claude pane before new task
Cmd + K (or type /clear in Claude)

# Jump back to last command
Cmd + Shift + Up

# Get recent directories
Cmd + Opt + /

# Show toolbelt for command history
Cmd + Opt + B
```

---

## Project Context: CLAUDE.md Best Practices

### Overview
CLAUDE.md is the most powerful feature for "training" Claude Code to understand your project. It's automatically read when starting a session, providing persistent memory.

### Hierarchical Loading Strategy

Claude Code loads context in this order:
```
~/.claude/CLAUDE.md              # Global defaults
repo_root/CLAUDE.md              # Project-specific (commit to Git)
repo_root/CLAUDE.local.md        # Local overrides (.gitignored)
```

Context inherits from parent and child directories - perfect for monorepos.

### Creating CLAUDE.md

**Quick Start:**
```bash
cd your-project
claude
> /init
```

This creates `CLAUDE.md` in your project root.

### What to Include

**High Priority:**
```markdown
# Project Context

## Tech Stack
- Framework: Next.js 14
- Testing: Jest (test files: *.test.ts)
- Database: PostgreSQL
- ORM: Prisma

## Common Commands
- Tests: `npm test`
- Dev server: `npm run dev`
- Build: `npm run build`
- Deploy: `./deploy.sh`

## Code Conventions
- Branch naming: `feature/description`
- No emojis in commit messages
- Prefer functional components
- Always write tests first (TDD)

## Important Files
- Core utilities: `src/lib/utils.ts`
- API routes: `src/app/api/`
- Types: `src/types/index.ts`

## Testing Guidelines
- Test files next to source: `component.tsx` → `component.test.tsx`
- Use data-testid for E2E tests
- Mock external APIs in unit tests
```

### What NOT to Include

**Avoid:**
- Code that should be in actual source files
- Secrets or credentials (use CLAUDE.local.md)
- Overly detailed documentation (link to docs instead)
- File contents that Claude can read directly

**Keep It Concise:**
- Target: 100-300 lines
- If longer: break into linked documents
- Update as project evolves

### Live Updates During Session

Press `#` during a Claude session to save an instruction to CLAUDE.md:

```
> Remember: We always use Zod for validation
[Claude saves to CLAUDE.md]
```

### Example: TDD Workflow with CLAUDE.md

**CLAUDE.md:**
```markdown
# Testing Protocol

This project uses Jest. Follow TDD strictly:

1. Write failing test first
2. Confirm test fails with expected error
3. Write minimal implementation to pass
4. Refactor for clarity

Test files: `*.test.js`
Run tests: `npm test`
Coverage: `npm run coverage` (must be >80%)
```

**Session:**
```bash
claude
> Write a failing test for /api/user endpoint
# Claude knows to use Jest, knows file naming, knows to make it fail first
> The test fails as expected. Write minimal implementation.
# Claude knows to make it just barely pass
> Refactor for clarity
# Claude knows your conventions from CLAUDE.md
```

### Multi-Project Setup

**Global defaults:**
`~/.claude/CLAUDE.md`
```markdown
# Global Preferences

## Writing Style
- Clear, concise commit messages
- No emojis
- Prefer TypeScript over JavaScript

## Testing
- Always write tests
- Use descriptive test names
```

**Project-specific:**
`~/projects/waltersignal/CLAUDE.md`
```markdown
# WalterSignal Project

[Includes global defaults automatically]

## Specific to this project
- Client code in: `~/projects/waltersignal-client/`
- Server code in: `~/projects/waltersignal-server/`
- Deploy: `./deploy-to-lightsail.sh`
```

### Maintenance

**Monthly Review:**
```bash
# Review and update
vim CLAUDE.md

# Test it works
claude "Summarize our testing protocol"
# Claude should recite from CLAUDE.md
```

**Version Control:**
```bash
# Commit project-specific
git add CLAUDE.md
git commit -m "Update Claude context for new testing approach"

# Ignore local overrides
echo "CLAUDE.local.md" >> .gitignore
git add .gitignore
```

### Pro Tips

1. **Start Minimal:** Begin with 20-30 lines, grow organically
2. **Test It:** Ask Claude to summarize - verify it read your context
3. **Team Alignment:** Commit CLAUDE.md so whole team benefits
4. **Local Secrets:** Use CLAUDE.local.md for machine-specific config
5. **Monorepo Strategy:** Parent CLAUDE.md for shared, child for specific

### Common Patterns

**Microservices:**
```
~/projects/
  CLAUDE.md              # Shared conventions
  service-a/
    CLAUDE.md            # Service A specifics
  service-b/
    CLAUDE.md            # Service B specifics
```

**Full Stack:**
```
~/project/
  CLAUDE.md              # Overall architecture
  frontend/
    CLAUDE.md            # React conventions
  backend/
    CLAUDE.md            # API conventions
```

**Documentation:** See CLAUDE_CODE_INTEGRATION.md for complete guide

---

## Next Level: Create Your Own Workflows

### Template for New Workflows

1. **Identify the task:**
   - What are you building?
   - What tools do you need visible?

2. **Design the layout:**
   - Draw it on paper first
   - Consider what needs most screen space

3. **Create the automation:**
   - Write shell script to start services
   - Or Python API script for complex layouts

4. **Add triggers:**
   - What output needs highlighting?
   - What events need notifications?

5. **Test and iterate:**
   - Use for a day
   - Adjust based on friction points

### Share Your Workflows

Save to git and share:
```bash
cd ~/.config/iterm2
git add layouts/ workflows/
git commit -m "Add new workflow for X"
git push
```

---

**Last Updated:** 2025-11-02
**For:** Mike Finneran / Claude Code Development
**More Info:** See EXPERT_GUIDE.md for advanced features
