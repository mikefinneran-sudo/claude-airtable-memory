# ObsidianVault MCP Server

Production-grade Model Context Protocol server for seamless Obsidian vault access via Claude Desktop.

**Created:** 2025-11-10
**Version:** 1.0.0
**Transport:** stdio
**Status:** ✅ Production Ready

---

## Features

### 🔍 Search & Discovery
- **search_notes**: Fast full-text search using ripgrep with regex support
- **list_recent_notes**: Find recently modified notes (configurable timeframe)
- **get_note_content**: Read any note by path

### 📅 Daily Notes
- **get_daily_note**: Retrieve daily note for any date
- **create_daily_note**: Generate templated daily notes with structured sections

### 📁 Project Management
- **create_project_note**: Create projects from templates (default, research, development)

### 🔒 Security
- **Roots-based access control**: All operations validated against vault path
- **Path traversal protection**: No access outside vault boundaries
- **Comprehensive logging**: All operations logged to stderr for audit

---

## Installation

### Prerequisites
- Python 3.9+ (already installed: `/usr/bin/python3`)
- ripgrep for search (`brew install ripgrep`)
- Claude Desktop app

### Setup Steps

**1. Verify server executable:**
```bash
ls -l ~/Documents/ObsidianVault/.mcp/obsidian_server.py
# Should show: -rwxr-xr-x (executable)
```

**2. Test server:**
```bash
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py 2>/dev/null | \
  python3 -m json.tool
```

**3. Configuration already added to Claude Desktop:**
```json
{
  "mcpServers": {
    "obsidian-vault": {
      "command": "python3",
      "args": [
        "/Users/mikefinneran/Documents/ObsidianVault/.mcp/obsidian_server.py"
      ],
      "env": {
        "VAULT_PATH": "/Users/mikefinneran/Documents/ObsidianVault"
      }
    }
  }
}
```

**4. Restart Claude Desktop** to load the server

---

## Usage Examples

### Search Notes
```
"Search my vault for notes about AI agents"
```
Claude will use `search_notes` tool with ripgrep to find all matching notes.

### Get Today's Daily Note
```
"Show me today's daily note"
```
Uses `get_daily_note` without date parameter (defaults to today).

### Create Daily Note
```
"Create a daily note for tomorrow with 'Meeting with client' in the notes section"
```
Uses `create_daily_note` with date and content parameters.

### List Recent Work
```
"What notes have I modified in the last 3 days?"
```
Uses `list_recent_notes` with days=3.

### Create Project
```
"Create a new research project note called 'AI Safety Study' using the research template"
```
Uses `create_project_note` with template="research".

### Read Specific Note
```
"Show me the content of Projects/WalterSignal.md"
```
Uses `get_note_content` with the relative path.

---

## Available Tools

### search_notes

**Description:** Search Obsidian vault notes using ripgrep. Supports regex patterns.

**Parameters:**
- `query` (string, required): Search query (supports regex)
- `limit` (number, optional): Maximum results to return (default: 10)

**Returns:** List of matches with path, line number, content, and submatches

**Example:**
```json
{
  "query": "project.*status",
  "limit": 5
}
```

---

### get_daily_note

**Description:** Get daily note for specified date (default: today)

**Parameters:**
- `date` (string, optional): Date in YYYY-MM-DD format (defaults to today)

**Returns:** Note content, metadata, and existence status

**Example:**
```json
{
  "date": "2025-11-10"
}
```

---

### create_daily_note

**Description:** Create daily note with optional initial content

**Parameters:**
- `date` (string, optional): Date in YYYY-MM-DD format (defaults to today)
- `content` (string, optional): Initial content for the Notes section

**Returns:** Created note information with full content

**Template Structure:**
```markdown
# Day, Month DD, YYYY

## Morning Review
-

## Tasks
- [ ]

## Notes
{content}

## Evening Review
-

---
Created: YYYY-MM-DD HH:MM
```

---

### list_recent_notes

**Description:** List recently modified notes

**Parameters:**
- `days` (number, optional): Number of days to look back (default: 7)
- `folder` (string, optional): Optional folder to filter (relative to vault)

**Returns:** List of notes with path, name, modified timestamp, and size

**Example:**
```json
{
  "days": 3,
  "folder": "Projects"
}
```

---

### get_note_content

**Description:** Get content of a specific note by path

**Parameters:**
- `path` (string, required): Path to note relative to vault root

**Returns:** Note content, size, modified/created timestamps

**Example:**
```json
{
  "path": "Projects/AI-Training/DEEP-LEARNING-NOTES-ANTHROPIC-COURSES.md"
}
```

---

### create_project_note

**Description:** Create new project note from template

**Parameters:**
- `project_name` (string, required): Name of the project
- `template` (string, optional): Template to use - "default", "research", or "development"

**Returns:** Created project information with full content

**Templates:**

**default:** General project tracking with goals, tasks, resources
**research:** Research-focused with questions, methodology, findings
**development:** Technical projects with tech stack, architecture, implementation plan

**Example:**
```json
{
  "project_name": "Claude MCP Integration",
  "template": "development"
}
```

---

## Architecture

### Transport: stdio
- Client (Claude Desktop) launches server as subprocess
- Communication via stdin/stdout using JSON-RPC 2.0
- Logging to stderr (not visible to client)
- Automatic process lifecycle management

### Security Model
- **Roots validation**: All paths validated against vault root
- **No external access**: Server cannot access files outside vault
- **Path sanitization**: Project names sanitized for safe filenames
- **Audit logging**: All operations logged with timestamps

### Performance
- **ripgrep**: Blazing fast search (Rust-based)
- **Async operations**: Non-blocking I/O for responsiveness
- **Minimal dependencies**: Python 3 standard library only (except ripgrep CLI)

---

## Troubleshooting

### Server Not Showing in Claude Desktop

**Check configuration:**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Verify obsidian-vault entry exists**

**Restart Claude Desktop completely:**
```bash
killall Claude
open -a Claude
```

### Search Not Working

**Install ripgrep:**
```bash
brew install ripgrep
```

**Verify installation:**
```bash
which rg
# Should output: /opt/homebrew/bin/rg
```

### Path Access Denied

**Check vault path in config:**
```bash
echo $VAULT_PATH
```

**Should be:** `/Users/mikefinneran/Documents/ObsidianVault`

**Verify vault exists:**
```bash
ls ~/Documents/ObsidianVault
```

### Server Crashes

**Check logs (stderr output visible in Claude Desktop developer console):**
1. Open Claude Desktop
2. Go to View → Developer → Toggle Developer Tools
3. Check Console tab for error messages
4. Look for lines starting with `[INFO]`, `[ERROR]`, etc.

**Manual test:**
```bash
echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py
```

---

## Development

### Running Tests

**Initialize test:**
```bash
echo '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{}}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py 2>&1
```

**List tools:**
```bash
echo '{"jsonrpc":"2.0","method":"tools/list","id":2}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py 2>/dev/null
```

**Search test:**
```bash
echo '{"jsonrpc":"2.0","method":"tools/call","id":3,"params":{"name":"search_notes","arguments":{"query":"project","limit":3}}}' | \
  python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py 2>/dev/null | \
  python3 -m json.tool
```

### Adding New Tools

1. **Add method to ObsidianVaultServer class**
2. **Add tool definition to tools/list response**
3. **Add handler in tools/call method**
4. **Test with echo commands**
5. **Document in this README**

### Logging

All logs go to stderr with format:
```
[TIMESTAMP] [LEVEL] Message
```

**Levels:**
- `INFO`: Normal operations
- `DEBUG`: Detailed method calls
- `WARNING`: Security violations, unexpected conditions
- `ERROR`: Failures, exceptions

---

## Production Lessons Applied

Based on deep training from Anthropic courses:

### From "Building Effective AI Agents"
- ✅ **Poka-yoke tool design**: Clear parameter descriptions, explicit boundaries
- ✅ **Absolute paths**: All file operations use absolute paths (learned from SWE-bench)
- ✅ **Comprehensive error handling**: Every operation has fallback behavior
- ✅ **Transparency**: All operations logged for debugging

### From "Advanced MCP Topics"
- ✅ **stdio transport**: Optimal for local, single-user access
- ✅ **Roots-based security**: Path validation on every file operation
- ✅ **Progress potential**: Infrastructure for progress notifications (future enhancement)
- ✅ **JSON-RPC compliance**: Strict adherence to MCP specification

### From "Claude with Bedrock"
- ✅ **Production-ready**: Comprehensive error handling, logging, security
- ✅ **Performance**: Efficient search with ripgrep, async operations
- ✅ **Scalability**: Architecture supports future enhancements (resources, prompts, sampling)

---

## Future Enhancements

### Phase 2 (Week 2)
- [ ] Add MCP resources for vault://daily/* and vault://projects/*
- [ ] Implement progress notifications for long searches
- [ ] Add batch operations (search + summarize)

### Phase 3 (Month 2)
- [ ] Sampling integration: Ask Claude to categorize notes
- [ ] Graph navigation: Backlinks, forward links
- [ ] Tag management: List, search, create

### Phase 4 (Month 3)
- [ ] Streamable HTTP transport for multi-user access
- [ ] Vector embeddings for semantic search
- [ ] Integration with external tools (git, backups)

---

## Support

**Documentation:** This README
**Training Material:** `~/Documents/ObsidianVault/Projects/AI-Training/`
**Server Code:** `~/Documents/ObsidianVault/.mcp/obsidian_server.py`
**Configuration:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**For issues:**
1. Check troubleshooting section above
2. Review logs in Claude Desktop developer console
3. Test server manually with echo commands
4. Verify ripgrep installation

---

## License

Internal use only - Mike Finneran AI Consulting
Created with Claude (Anthropic's AI Assistant)
Training applied from Anthropic official courses

**Version:** 1.0.0
**Last Updated:** 2025-11-10
**Status:** ✅ Production Ready
