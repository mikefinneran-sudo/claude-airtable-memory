#!/bin/bash
# Switch to WalterSignal project context

# Navigate to project
cd ~/Documents/ObsidianVault/Projects/WalterSignal

# Open Obsidian
open -a "Obsidian"

# Open iTerm with project directory
osascript <<EOF
tell application "iTerm"
    activate
    create window with default profile command "cd ~/Documents/ObsidianVault/Projects/WalterSignal && clear && echo 'WalterSignal Project Ready'"
end tell
EOF
