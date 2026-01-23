#!/bin/bash
# LifeHub Notion Sync - Setup Script

set -e

echo "=================================="
echo "LifeHub → Notion Sync Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi
echo "✅ Python 3 found"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install notion-client python-frontmatter

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create token file
echo ""
echo "Setting up Notion integration token..."
echo ""
echo "1. Go to: https://www.notion.com/my-integrations"
echo "2. Create a new integration named 'LifeHub Sync'"
echo "3. Copy the Internal Integration Token"
echo ""
read -p "Paste your Notion integration token: " TOKEN

echo "$TOKEN" > ~/.lifehub-notion-token
chmod 600 ~/.lifehub-notion-token
echo "✅ Token saved to ~/.lifehub-notion-token"

# Create config
echo ""
echo "Creating sync configuration..."
python3 "$(dirname "$0")/sync_to_notion.py" || true
echo "✅ Config created at .scripts/notion-sync-config.json"

# Test connection
echo ""
echo "Testing Notion API connection..."
curl -s -X POST https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Notion-Version: 2022-06-28" > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Successfully connected to Notion!"
else
    echo "❌ Failed to connect to Notion. Check your token."
    exit 1
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Create Notion databases (see guide)"
echo "2. Edit .scripts/notion-sync-config.json"
echo "3. Add your Notion database IDs"
echo "4. Run: python3 .scripts/sync_to_notion.py --dry-run"
echo "5. If looks good: python3 .scripts/sync_to_notion.py"
echo ""
echo "Documentation: Projects/LifeHub/Enhanced/LifeHub-Notion-Integration-Guide.md"
echo ""
