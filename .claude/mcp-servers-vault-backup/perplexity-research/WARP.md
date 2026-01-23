# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **Perplexity Pro MCP Server** that integrates Perplexity AI search capabilities into Claude Code through the Model Context Protocol (MCP). It provides three research tools for AI-powered web search with citations.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip3 install -r requirements.txt

# Make server executable
chmod +x server.py

# Quick setup (automated)
./setup.sh
```

### Running and Testing
```bash
# Run the MCP server directly (for debugging)
python3 server.py

# Test API key environment variable
echo $PERPLEXITY_API_KEY

# Verify dependencies are installed
pip3 show mcp httpx python-dotenv
```

### Development Workflow
```bash
# Check if server is executable
ls -la server.py

# Test server response (manual testing)
python3 -c "import asyncio; from server import main; asyncio.run(main())"

# Validate MCP integration
# Add to Claude Code config and restart Claude
```

## Architecture

### Core Components

**MCP Server (`server.py`)**
- Single-file Python server implementing MCP protocol
- Async HTTP client using `httpx` for Perplexity API calls
- Three main tool handlers with different research strategies

**Tool Architecture:**
1. **`perplexity_search`** - Direct search with filtering options
2. **`perplexity_deep_research`** - Iterative multi-query research
3. **`perplexity_compare`** - Structured entity comparison

### Key Classes and Methods

**`PerplexityMCP` class:**
- `setup_handlers()` - Registers MCP tool definitions and handlers
- `perplexity_search()` - Core API interaction method
- `perplexity_deep_research()` - Orchestrates multiple searches
- `perplexity_compare()` - Formats comparison queries

### API Integration Pattern
```python
# Standard pattern used throughout:
1. Validate API key exists
2. Build request payload with model/parameters
3. Make async HTTP request to Perplexity API  
4. Parse response and extract content/citations
5. Format as TextContent for MCP response
```

### Error Handling Strategy
- API key validation before requests
- HTTP error catching with user-friendly messages
- Graceful degradation for missing optional parameters
- Timeout handling (60s default)

## Configuration

### Required Environment Variables
- `PERPLEXITY_API_KEY` - Perplexity Pro API key (required)

### Claude Code Integration
Must be added to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "perplexity-research": {
      "command": "python3",
      "args": ["/full/path/to/server.py"],
      "env": {
        "PERPLEXITY_API_KEY": "pplx-xxxxx"
      }
    }
  }
}
```

## Key Dependencies
- `mcp>=0.9.0` - Model Context Protocol implementation
- `httpx>=0.27.0` - Async HTTP client for API calls  
- `python-dotenv>=1.0.0` - Environment variable management

## Usage Patterns

The server responds to natural language requests in Claude Code:
- "Use Perplexity to research [topic]" → `perplexity_search`
- "Deep research on [topic]" → `perplexity_deep_research`  
- "Compare [A] vs [B]" → `perplexity_compare`

## API Models Available
- `llama-3.1-sonar-small-128k-online` (fastest)
- `llama-3.1-sonar-large-128k-online` (default, balanced)
- `llama-3.1-sonar-huge-128k-online` (most accurate)

## Troubleshooting

### Common Issues
1. **"PERPLEXITY_API_KEY environment variable not set"**
   - Verify: `echo $PERPLEXITY_API_KEY`
   - Add to shell profile or use .env file

2. **"401 Unauthorized"**
   - API key invalid or expired
   - Regenerate in Perplexity Pro settings

3. **"MCP server not showing up"**
   - Check Claude Code config syntax
   - Restart Claude completely
   - Verify server.py is executable

4. **"Module 'mcp' not found"**
   - Run: `pip3 install -r requirements.txt`

### Testing the Server
```bash
# Check if all dependencies are available
python3 -c "import mcp, httpx, dotenv; print('All imports successful')"

# Verify server starts without errors
timeout 5 python3 server.py || echo "Server startup test complete"
```