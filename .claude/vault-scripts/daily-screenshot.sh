#!/bin/bash
# Capture screenshot for today's daily note
# Automatically links screenshot in daily note

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H-%M-%S)
DAILY_DIR="/Users/mikefinneran/Documents/ObsidianVault/Daily/attachments"
FILENAME="${DATE}_screenshot_${TIME}.png"

# Ensure directory exists
mkdir -p "$DAILY_DIR"

# Trigger CleanShot X
open "cleanshot://capture-area?filepath=${DAILY_DIR}/${FILENAME}"

echo "📸 Capturing screenshot for daily note..."
echo "   File: ${FILENAME}"

# Wait for capture to complete
sleep 2

# Append to today's daily note
DAILY_NOTE="/Users/mikefinneran/Documents/ObsidianVault/Daily/${DATE}.md"
if [ -f "$DAILY_NOTE" ]; then
    echo "" >> "$DAILY_NOTE"
    echo "## Screenshot - ${TIME//-/:}" >> "$DAILY_NOTE"
    echo "![[attachments/${FILENAME}]]" >> "$DAILY_NOTE"
    echo "" >> "$DAILY_NOTE"
    echo "✓ Screenshot added to daily note: Daily/${DATE}.md"
else
    echo "⚠️  Daily note not found. Screenshot saved to: Daily/attachments/${FILENAME}"
    echo "   Create today's note first: python3 .scripts/update_daily_note.py"
fi
