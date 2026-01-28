# Apple Reminders Integration for Claude Code

## Setup Complete ✅

Apple Reminders MCP server is now configured and ready to use.

## Your Reminder Lists

Current lists detected:
- **Household** - Home tasks
- **To Do** - General tasks
- **Grocery** - Shopping items
- **Workshop** - Project work

## How to Use

### View Reminders
```
Show me all my reminders
List reminders in "To Do"
What's in my Household list?
```

### Create Reminders
```
Add "Buy milk" to Grocery list
Create reminder: "Call dentist" in To Do, due tomorrow
Add "Fix sink" to Household with note "Check under cabinet"
```

### Update Reminders
```
Mark "Buy milk" as complete
Update due date for "Call dentist" to Friday
Add note to "Fix sink": "Need wrench"
```

### Delete Reminders
```
Delete "Buy milk" from Grocery
Remove completed items from To Do
```

## Project Management Use Cases

### WalterSignal Projects
```
Create reminder: "Update LinkedIn scraper rate limits" in Workshop, due Monday
Add "Deploy safety system to DGX" to To Do
```

### Client Work
```
Show me all Workshop reminders
Create reminder: "BladeMafia payment processing" in To Do, due this Friday
```

### Weekly Reviews
```
Show me all overdue reminders
List all incomplete tasks
What reminders are due this week?
```

## Integration with Claude Code Workflows

### During Development
When working on tasks, you can tell Claude:
- "Add this to my To Do list"
- "Remind me to test this on Friday"
- "Create a Workshop reminder for the next feature"

### Session Handoff
At end of session:
- "Add my open tasks to Reminders"
- "Create reminders for the blockers we found"

## Technical Details

**MCP Server**: shadowfax92/apple-reminders-mcp
**Location**: `~/.mcp/apple-reminders-mcp/`
**Config**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Features**:
- Full CRUD operations
- Due dates and notes support
- Multiple lists
- Completion tracking
- Native Mac Reminders integration

## Restart Required

**IMPORTANT**: You must restart Claude Code for the integration to activate.

1. Quit Claude Code completely (Cmd+Q)
2. Reopen Claude Code
3. First time: macOS will ask for Reminders access - **grant permission**
4. Test: "Show me my reminder lists"

## Permissions

When you first use Reminders, macOS will prompt:
> "Claude Code would like to access your Reminders"

Click **Allow** to enable the integration.

## Troubleshooting

**If reminders don't work after restart**:
1. Check System Settings → Privacy & Security → Reminders
2. Ensure Claude is in the allowed apps list
3. Try: `osascript -e 'tell application "Reminders" to get name of every list'` in terminal

**If MCP server fails to start**:
```bash
cd ~/.mcp/apple-reminders-mcp
npm install
node build/index.js
```

## Sources

- [Apple Reminders MCP on GitHub](https://github.com/shadowfax92/apple-reminders-mcp)
- [Awesome MCP Servers](https://mcpservers.org/servers/shadowfax92/apple-reminders-mcp)
- [MCP Documentation](https://modelcontextprotocol.io/)
