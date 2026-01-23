# Test ObsidianVault MCP Server

**Quick test commands for your NEW Claude Code session**

---

## Step 1: Exit This Session

```bash
exit
```

Or press `Ctrl+C`

---

## Step 2: Start Fresh Claude Code

```bash
claude
```

---

## Step 3: Test Commands (Copy & Paste These)

### Test 1: Search
```
Search my vault for "MCP" and show me the results
```

**Expected:** Should find notes mentioning MCP (Model Context Protocol)

---

### Test 2: Recent Notes
```
Show me notes I modified in the last 2 days
```

**Expected:** List of recently modified notes with paths and timestamps

---

### Test 3: Daily Note
```
Show me today's daily note
```

**Expected:** Content of today's daily note (or message that it doesn't exist)

---

### Test 4: Create Project
```
Create a new project note called "MCP Testing" using the development template
```

**Expected:** Creates `Projects/MCP-Testing.md` with development template

---

### Test 5: Read Specific Note
```
Read the content of Projects/AI-Training/OBSIDIAN-MCP-SERVER-BUILD-SUMMARY.md
```

**Expected:** Full content of the build summary document

---

## Troubleshooting

### If tools still don't work:

**Check MCP server status:**
```bash
claude mcp list
```

**Should see:**
```
obsidian-vault: python3 /Users/mikefinneran/Documents/ObsidianVault/.mcp/obsidian_server.py - ✓ Connected
```

### If it says "Failed to connect":

**Check logs:**
```bash
tail -n 50 ~/Library/Logs/Claude/mcp-server-obsidian-vault.log
```

**Manual test:**
```bash
echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py 2>&1 | head -5
```

Should see: `[INFO] ObsidianVault MCP Server initialized`

---

## Available Tools (6)

When working, you'll have access to:

1. ✅ **search_notes** - Fast ripgrep search across vault
2. ✅ **get_daily_note** - Retrieve daily notes by date
3. ✅ **create_daily_note** - Generate templated daily notes
4. ✅ **list_recent_notes** - Find recently modified notes
5. ✅ **get_note_content** - Read specific notes by path
6. ✅ **create_project_note** - Create projects from templates

---

## Success Indicators

**Working correctly when:**
- Commands execute without errors
- Returns actual note content/search results
- Can create new notes and read them back
- Performance is fast (<500ms for searches)

**Not working when:**
- "I don't have access to that tool"
- "Tool not found" errors
- Empty results when notes definitely exist
- Server shows as "Failed to connect" in mcp list

---

## Quick Reference

**Server location:** `~/Documents/ObsidianVault/.mcp/obsidian_server.py`
**Logs location:** `~/Library/Logs/Claude/mcp-server-obsidian-vault.log`
**Config location:** `~/.claude.json` (under mcpServers)
**Full docs:** `~/Documents/ObsidianVault/.mcp/README.md`

---

**Ready to test!** Exit this session and start fresh. 🚀
