# ObsidianVault MCP Server - Quick Start

**Status:** ✅ Installed and configured
**Last Updated:** 2025-11-10

---

## Instant Usage (Claude Desktop)

Just talk naturally to Claude! The server is already configured and running.

### What You Can Ask:

**Search:**
- "Search my vault for notes about AI"
- "Find all mentions of 'WalterSignal' in my notes"
- "Search Projects folder for 'deployment'"

**Daily Notes:**
- "Show me today's daily note"
- "Get my daily note from last Friday"
- "Create tomorrow's daily note"
- "Create a daily note with 'Call client at 2pm' in it"

**Recent Activity:**
- "What notes did I modify in the last 3 days?"
- "Show recent changes in my Projects folder"
- "List notes I worked on this week"

**Project Management:**
- "Create a new project note for 'AI Research'"
- "Create a development project for 'MCP Server'"
- "Create a research project for 'Claude Training'"

**Read Notes:**
- "Show me the content of Projects/WalterSignal.md"
- "Read my AI-Training notes"

---

## Verify Installation

```bash
# 1. Check server exists
ls -l ~/Documents/ObsidianVault/.mcp/obsidian_server.py

# 2. Test server
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py 2>/dev/null | \
  python3 -m json.tool | head -20

# 3. Check Claude Desktop config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep -A 8 obsidian-vault

# 4. Restart Claude Desktop
killall Claude && sleep 2 && open -a Claude
```

---

## Available Tools (6)

1. **search_notes** - Fast search with ripgrep
2. **get_daily_note** - Retrieve daily notes
3. **create_daily_note** - Generate templated daily notes
4. **list_recent_notes** - Find recently modified notes
5. **get_note_content** - Read specific notes
6. **create_project_note** - Create project from templates

---

## Common Issues

**Server not visible in Claude:**
→ Restart Claude Desktop completely

**Search returns nothing:**
→ Install ripgrep: `brew install ripgrep`

**Can't access notes:**
→ Check vault path: `ls ~/Documents/ObsidianVault`

**Want to see logs:**
→ Claude Desktop → View → Developer → Toggle Developer Tools → Console

---

## File Locations

**Server:** `~/Documents/ObsidianVault/.mcp/obsidian_server.py`
**Config:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Docs:** `~/Documents/ObsidianVault/.mcp/README.md`
**Vault:** `~/Documents/ObsidianVault/`

---

## Next Steps

**Now:**
1. Restart Claude Desktop (if not done already)
2. Try: "Search my vault for 'AI'"
3. Try: "Show today's daily note"

**Later:**
- Read full README.md for all features
- Explore project templates
- Set up automated workflows

---

**You're all set!** Just start asking Claude to work with your Obsidian vault.
