#!/bin/bash
# Setup script for Automated Credential Rotation System

set -e

echo "=========================================="
echo "Credential Rotation System - Setup"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python version
echo "Checking Python version..."
if ! python3 --version | grep -q "Python 3"; then
    echo "❌ Python 3 is required"
    exit 1
fi
echo "✅ Python 3 found"

# Check 1Password CLI
echo ""
echo "Checking 1Password CLI..."
if ! command -v op &> /dev/null; then
    echo "❌ 1Password CLI not found"
    echo "Install with: brew install 1password-cli"
    exit 1
fi
echo "✅ 1Password CLI found"

# Check 1Password authentication
echo ""
echo "Checking 1Password authentication..."
if ! op whoami &> /dev/null; then
    echo "⚠️  Not signed into 1Password"
    echo "Run: eval \$(op signin)"
    exit 1
fi
echo "✅ 1Password authenticated"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install --user requests mcp 2>&1 | grep -v "already satisfied" || true
echo "✅ Dependencies installed"

# Create required directories
echo ""
echo "Creating directories..."
mkdir -p logs checklists config
echo "✅ Directories created"

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x rotation_scheduler.py server.py modules/*.py
echo "✅ Scripts made executable"

# Generate manual rotation checklists
echo ""
echo "Generating rotation checklists..."
python3 modules/manual_rotation_guide.py
echo "✅ Checklists generated"

# Create initial config
echo ""
echo "Creating initial configuration..."
cat > config/rotation_config.json << EOF
{
  "services": {
    "Cloudflare": {
      "rotation_days": 90,
      "enabled": true,
      "last_updated": "$(date -Iseconds)"
    },
    "Airtable": {
      "rotation_days": 90,
      "enabled": false,
      "note": "Manual rotation required"
    },
    "Perplexity Pro": {
      "rotation_days": 90,
      "enabled": false,
      "note": "Manual rotation required"
    },
    "Gamma API": {
      "rotation_days": 90,
      "enabled": false,
      "note": "Manual rotation required"
    },
    "Google OAuth": {
      "rotation_days": 180,
      "enabled": false,
      "note": "Manual rotation required"
    }
  },
  "notifications": {
    "enabled": true,
    "methods": ["macos_notification"]
  },
  "schedule": {
    "check_frequency": "daily",
    "check_time": "09:00"
  }
}
EOF
echo "✅ Configuration created"

# Add to Claude Code MCP config
echo ""
echo "Configuring Claude Code MCP integration..."
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ -f "$CLAUDE_CONFIG" ]; then
    # Backup existing config
    cp "$CLAUDE_CONFIG" "$CLAUDE_CONFIG.backup"

    # Add credential-rotation to MCP servers
    python3 << EOF
import json

config_file = "$CLAUDE_CONFIG"
with open(config_file, 'r') as f:
    config = json.load(f)

if 'mcpServers' not in config:
    config['mcpServers'] = {}

config['mcpServers']['credential-rotation'] = {
    'command': 'python3',
    'args': ['$SCRIPT_DIR/server.py']
}

with open(config_file, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ MCP configuration updated")
EOF
else
    echo "⚠️  Claude Code config not found, skipping MCP integration"
fi

# Setup LaunchAgent for automated scheduling (macOS)
echo ""
echo "Setting up automated scheduling..."

LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LAUNCH_AGENT_DIR"

cat > "$LAUNCH_AGENT_DIR/com.waltersignal.credential-rotation.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.waltersignal.credential-rotation</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_DIR/rotation_scheduler.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$SCRIPT_DIR/logs/scheduler_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$SCRIPT_DIR/logs/scheduler_stderr.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# Load the LaunchAgent
launchctl unload "$LAUNCH_AGENT_DIR/com.waltersignal.credential-rotation.plist" 2>/dev/null || true
launchctl load "$LAUNCH_AGENT_DIR/com.waltersignal.credential-rotation.plist"

echo "✅ Scheduled daily rotation check at 9:00 AM"

# Test the system
echo ""
echo "=========================================="
echo "Testing the system..."
echo "=========================================="
echo ""

python3 rotation_scheduler.py

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "The credential rotation system is now configured:"
echo ""
echo "✅ Automated scheduler runs daily at 9:00 AM"
echo "✅ MCP server integrated with Claude Code"
echo "✅ Manual rotation checklists generated"
echo ""
echo "Commands:"
echo "  Manual run: python3 rotation_scheduler.py"
echo "  Check status: python3 -c 'from rotation_framework import *; ...'"
echo "  View logs: tail -f logs/rotation.log"
echo ""
echo "In Claude Code, you can now use commands like:"
echo "  - Check rotation status"
echo "  - Rotate credentials"
echo "  - Get rotation history"
echo ""
echo "Documentation: cat README.md"
echo ""
