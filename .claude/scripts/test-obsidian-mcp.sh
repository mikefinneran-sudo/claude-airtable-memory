#!/bin/bash
# Quick test for ObsidianVault MCP Server

echo "🧪 ObsidianVault MCP Server Test"
echo "================================"
echo ""

# Check if server is configured
if claude mcp list 2>/dev/null | grep -q "obsidian-vault.*Connected"; then
    echo "✅ Server is connected"
else
    echo "❌ Server not connected"
    echo ""
    echo "Run: claude mcp add --scope user obsidian-vault python3 ~/Documents/ObsidianVault/.mcp/obsidian_server.py"
    exit 1
fi

echo ""
echo "📝 Test this in a NEW Claude Code session:"
echo ""
echo "   1. Type: exit"
echo "   2. Type: claude"
echo "   3. Ask: Search my vault for MCP"
echo ""
echo "📖 Full test guide: ~/Documents/ObsidianVault/.mcp/TEST-MCP-SERVER.md"
