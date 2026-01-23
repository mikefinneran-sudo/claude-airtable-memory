#!/bin/bash
# Convert current Superhuman email to task in daily note

VAULT="/Users/mikefinneran/Documents/ObsidianVault"
DATE=$(date +%Y-%m-%d)
DAILY_NOTE="${VAULT}/Daily/${DATE}.md"

echo "✅ Creating task from email..."

# Get email subject via AppleScript
SUBJECT=$(osascript 2>/dev/null <<'EOF'
tell application "System Events"
    if not (exists process "Superhuman") then
        return "ERROR: Superhuman not running"
    end if

    tell process "Superhuman"
        set frontmost to true
        delay 0.2

        # Try to get subject from UI
        # This is a simplified version - may need adjustment
        keystroke "c" using {command down, shift down}
        delay 0.3
    end tell
end tell

return the clipboard
EOF
)

if [ "$SUBJECT" = "ERROR: Superhuman not running" ]; then
    echo "❌ Superhuman is not running"
    exit 1
fi

# Clean subject
SUBJECT_CLEAN=$(echo "$SUBJECT" | head -1 | cut -c 1-80)

if [ -z "$SUBJECT_CLEAN" ]; then
    SUBJECT_CLEAN="Follow up on email"
fi

# Add task to daily note
if [ -f "$DAILY_NOTE" ]; then
    echo "- [ ] 📧 ${SUBJECT_CLEAN} (from Superhuman)" >> "$DAILY_NOTE"
    echo ""
    echo "✓ Task added to daily note:"
    echo "  '${SUBJECT_CLEAN}'"
else
    echo "❌ Daily note not found: ${DATE}.md"
    echo "   Create it first: python3 .scripts/update_daily_note.py"
    exit 1
fi
