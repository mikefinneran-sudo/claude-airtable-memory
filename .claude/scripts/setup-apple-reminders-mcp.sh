#!/bin/bash
# Setup Apple Reminders MCP Server for Claude Code

set -e

echo "🍎 Setting up Apple Reminders MCP Server..."
echo ""

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not found"
    echo "Install Node.js first: brew install node"
    exit 1
fi

# Create MCP servers directory if needed
MCP_DIR="$HOME/.mcp/apple-reminders"
mkdir -p "$MCP_DIR"

echo "📦 Installing Apple Reminders MCP Server..."
cd "$MCP_DIR"

# Use the shadowfax92 implementation (most popular)
npm install @shadowfax92/apple-reminders-mcp

echo ""
echo "✅ Apple Reminders MCP Server installed"
echo ""
echo "📝 Now updating Claude Desktop config..."

# Path to Claude Desktop config
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Create backup
cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d-%H%M%S)"

# Add Apple Reminders server to config using Python
python3 << 'EOF'
import json
import os

config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")

with open(config_path, 'r') as f:
    config = json.load(f)

# Add apple-reminders server
config['mcpServers']['apple-reminders'] = {
    "command": "npx",
    "args": [
        "-y",
        "@shadowfax92/apple-reminders-mcp"
    ]
}

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Added apple-reminders to Claude Desktop config")
EOF

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart Claude Code (completely quit and reopen)"
echo "2. Grant Reminders access when prompted"
echo "3. Test with: 'Show me my reminders lists'"
echo ""
echo "📚 Documentation:"
echo "   https://github.com/shadowfax92/apple-reminders-mcp"
