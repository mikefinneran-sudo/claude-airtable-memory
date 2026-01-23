#!/bin/bash
# Quick setup script for Perplexity MCP

echo "🔧 Setting up Perplexity Pro MCP Server..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make server executable
chmod +x server.py

# Check for API key
if [ -z "$PERPLEXITY_API_KEY" ]; then
    echo "⚠️  PERPLEXITY_API_KEY environment variable not set"
    echo ""
    echo "Please add your Perplexity API key:"
    echo "1. Get API key from https://perplexity.ai (Pro account required)"
    echo "2. Add to ~/.zshrc:  export PERPLEXITY_API_KEY='pplx-xxxxx'"
    echo "3. Reload: source ~/.zshrc"
    echo ""
else
    echo "✅ PERPLEXITY_API_KEY found"
fi

# Check Claude Code config
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ ! -f "$CLAUDE_CONFIG" ]; then
    echo "⚠️  Claude Code config not found"
    echo "Creating config file..."
    mkdir -p "$(dirname "$CLAUDE_CONFIG")"
    echo '{
  "mcpServers": {
    "perplexity-research": {
      "command": "python3",
      "args": [
        "'$(pwd)'/server.py"
      ]
    }
  }
}' > "$CLAUDE_CONFIG"
    echo "✅ Created Claude Code config"
else
    echo "⚠️  Claude Code config exists. Please manually add:"
    echo ""
    echo '{
  "mcpServers": {
    "perplexity-research": {
      "command": "python3",
      "args": [
        "'$(pwd)'/server.py"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "your-key-here"
      }
    }
  }
}'
    echo ""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set PERPLEXITY_API_KEY if not already set"
echo "2. Restart Claude Code"
echo "3. Test with: 'Use Perplexity to search for: [your query]'"
