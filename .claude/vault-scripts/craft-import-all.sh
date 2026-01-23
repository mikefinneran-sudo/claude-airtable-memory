#!/bin/bash

# Craft Complete Import - Fully Automated
# Imports all files to Mike's Space with folder organization

set -e

DAILY_DIR="$HOME/Documents/CraftImport/Daily"
STRATEGY_DIR="$HOME/Documents/CraftImport/Strategy"

echo "🚀 Importing to Craft - Mike's Space"
echo "===================================="

# Use osascript to automate Craft
osascript <<EOF
tell application "Craft"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "Craft"

        -- Import Daily Notes
        log "Importing daily notes..."

        -- Press Cmd+O to open import
        keystroke "o" using command down
        delay 1

        -- Navigate to Daily folder using Cmd+Shift+G
        keystroke "g" using {command down, shift down}
        delay 0.5
        keystroke "$DAILY_DIR"
        keystroke return
        delay 0.5

        -- Select all files
        keystroke "a" using command down
        delay 0.3

        -- Click Open button
        keystroke return
        delay 3

        log "Daily notes imported"

        -- Import Strategy Docs
        log "Importing strategy docs..."

        -- Press Cmd+O again
        keystroke "o" using command down
        delay 1

        -- Navigate to Strategy folder
        keystroke "g" using {command down, shift down}
        delay 0.5
        keystroke "$STRATEGY_DIR"
        keystroke return
        delay 0.5

        -- Select all files
        keystroke "a" using command down
        delay 0.3

        -- Click Open
        keystroke return
        delay 3

        log "Strategy docs imported"

    end tell
end tell

return "✅ Import complete!"
EOF

echo ""
echo "✅ All files imported to Mike's Space"
echo ""
echo "Next: Organize into folders in Craft (30 seconds):"
echo "  1. Create folders: Daily Notes, Strategy & Planning, Templates"
echo "  2. Drag files into appropriate folders"
echo ""
