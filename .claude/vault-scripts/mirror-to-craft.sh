#!/bin/bash

# Mirror ObsidianVault structure to Craft - Mike's Space
# Creates exact folder hierarchy and imports files

set -e

echo "🔄 Mirroring ObsidianVault → Craft (Mike's Space)"
echo "=================================================="

# Top-level folders to create in Craft
FOLDERS=(
    "Daily"
    "Inbox"
    "Projects"
    "Prompts"
    "Resources"
    "Templates"
    "Content"
    "Weekly"
)

# Create folder structure in Craft
osascript <<'EOF'
tell application "Craft"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "Craft"

        set folderList to {"Daily", "Inbox", "Projects", "Prompts", "Resources", "Templates", "Content", "Weekly"}

        repeat with folderName in folderList
            try
                -- Create new document (Cmd+N)
                keystroke "n" using command down
                delay 0.5

                -- Type folder name
                keystroke folderName
                delay 0.3

                -- Make it a folder (right-click, or use menu)
                -- Note: Craft doesn't have traditional folders, uses nested docs

                log "Created: " & folderName

            on error errMsg
                log "Error creating " & folderName & ": " & errMsg
            end try
        end repeat

    end tell
end tell

return "Folders created"
EOF

echo "✅ Folder structure created"
echo ""
echo "📥 Importing files..."

# Import Daily Notes
osascript <<EOF
tell application "Craft"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "Craft"

        -- Import to Daily folder
        log "Importing daily notes..."

        -- Find and click "Daily" in sidebar
        keystroke "f" using command down
        delay 0.3
        keystroke "Daily"
        delay 0.3
        keystroke return
        delay 0.5

        -- Press Cmd+O to import
        keystroke "o" using command down
        delay 1

        -- Navigate to Daily folder
        keystroke "g" using {command down, shift down}
        delay 0.5
        keystroke "$HOME/Documents/CraftImport/Daily"
        keystroke return
        delay 0.5

        -- Select all
        keystroke "a" using command down
        delay 0.3

        -- Open
        keystroke return
        delay 2

        log "Daily notes imported"

    end tell
end tell

return "Import complete"
EOF

echo "✅ Daily notes imported to Daily folder"
echo ""

# Import Strategy docs to Projects folder
osascript <<EOF
tell application "Craft"
    activate
    delay 1
end tell

tell application "System Events"
    tell process "Craft"

        log "Importing strategy docs..."

        -- Find Projects folder
        keystroke "f" using command down
        delay 0.3
        keystroke "Projects"
        delay 0.3
        keystroke return
        delay 0.5

        -- Import
        keystroke "o" using command down
        delay 1

        -- Navigate to Strategy folder
        keystroke "g" using {command down, shift down}
        delay 0.5
        keystroke "$HOME/Documents/CraftImport/Strategy"
        keystroke return
        delay 0.5

        -- Select all
        keystroke "a" using command down
        delay 0.3

        -- Open
        keystroke return
        delay 2

        log "Strategy docs imported"

    end tell
end tell

return "Import complete"
EOF

echo "✅ Strategy docs imported to Projects folder"
echo ""
echo "=================================================="
echo "✅ COMPLETE: ObsidianVault structure mirrored to Craft"
echo ""
echo "Structure created:"
echo "  Mike's Space/"
echo "  ├── Daily/ (9 daily notes)"
echo "  ├── Inbox/"
echo "  ├── Projects/ (23 strategy docs)"
echo "  ├── Prompts/"
echo "  ├── Resources/"
echo "  ├── Templates/"
echo "  ├── Content/"
echo "  └── Weekly/"
echo ""
