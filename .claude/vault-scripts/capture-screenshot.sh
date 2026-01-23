#!/bin/bash
# Capture screenshot to vault with CleanShot X

DATE=$(date +%Y-%m-%d_%H-%M-%S)
SCREENSHOT_DIR="$HOME/Documents/ObsidianVault/Resources/Screenshots"

# Ensure directory exists
mkdir -p "$SCREENSHOT_DIR"

# Trigger CleanShot X area capture
open "cleanshot://capture-area?filepath=${SCREENSHOT_DIR}/screenshot-${DATE}.png"

echo "Screenshot will be saved to: ${SCREENSHOT_DIR}/screenshot-${DATE}.png"
