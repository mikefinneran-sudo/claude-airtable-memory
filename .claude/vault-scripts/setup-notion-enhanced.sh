#!/bin/bash
# Enhanced Notion sync setup

echo "📘 Setting up enhanced Notion integration..."
echo ""

# 1. Install notion-client if not present
echo "Checking Python dependencies..."
if python3 -c "import notion_client" 2>/dev/null; then
    echo "✓ notion-client already installed"
else
    echo "Installing notion-client..."
    pip3 install notion-client --user -q
    echo "✓ notion-client installed"
fi

# 2. Create config file
CONFIG_FILE="$HOME/Documents/ObsidianVault/.integrations/notion/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" <<'EOF'
{
  "notion_token_1password": "op://Private/Notion API/token",
  "databases": {
    "client_projects": "YOUR_DATABASE_ID_HERE",
    "daily_notes": "YOUR_DATABASE_ID_HERE",
    "meeting_notes": "YOUR_DATABASE_ID_HERE"
  },
  "sync_settings": {
    "auto_sync": false,
    "sync_interval_minutes": 60,
    "conflict_resolution": "newer_wins"
  }
}
EOF
    echo "✓ Created config file: .integrations/notion/config.json"
    echo "  Edit this file to add your Notion database IDs"
else
    echo "ℹ️  Config file already exists"
fi

# 3. Create sync status tracking
mkdir -p "$HOME/Documents/ObsidianVault/.integrations/notion/sync-status"
echo "✓ Created sync status directory"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Notion setup complete!"
echo ""
echo "Next steps:"
echo "1. Get Notion API token: https://www.notion.so/my-integrations"
echo "2. Store in 1Password:"
echo "   op item create --title='Notion API' token='secret_xxx'"
echo "3. Edit config: .integrations/notion/config.json"
echo "4. Add your database IDs"
echo "5. Test: python3 .scripts/notion-push.py [note-path] [db-id]"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
