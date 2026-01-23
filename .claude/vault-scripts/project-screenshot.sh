#!/bin/bash
# Capture screenshot for specific project
# Usage: ./project-screenshot.sh ProjectName

if [ -z "$1" ]; then
    echo "Usage: $0 <project-name>"
    echo ""
    echo "Available projects:"
    ls -d /Users/mikefinneran/Documents/ObsidianVault/Projects/*/ | xargs -n 1 basename
    echo ""
    echo "Example: $0 WalterSignal"
    exit 1
fi

PROJECT_NAME="$1"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
PROJECT_DIR="/Users/mikefinneran/Documents/ObsidianVault/Projects/${PROJECT_NAME}/screenshots"
FILENAME="${PROJECT_NAME}_${DATE}.png"

# Create project screenshots directory
mkdir -p "$PROJECT_DIR"

# Capture
open "cleanshot://capture-area?filepath=${PROJECT_DIR}/${FILENAME}"

echo "📸 Capturing screenshot for project: ${PROJECT_NAME}"
echo "✓ Screenshot will be saved to: Projects/${PROJECT_NAME}/screenshots/${FILENAME}"
echo ""
echo "Link in note: ![[screenshots/${FILENAME}]]"
