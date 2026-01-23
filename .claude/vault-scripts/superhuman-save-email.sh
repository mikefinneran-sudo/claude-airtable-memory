#!/bin/bash
# Save current Superhuman email to vault

VAULT="/Users/mikefinneran/Documents/ObsidianVault"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H-%M)
INBOX="${VAULT}/Inbox"

mkdir -p "$INBOX"

echo "📧 Saving email from Superhuman..."

# Run AppleScript to get email content
EMAIL_CONTENT=$(osascript 2>/dev/null <<'EOF'
tell application "System Events"
    # Check if Superhuman is running
    if not (exists process "Superhuman") then
        return "ERROR: Superhuman not running"
    end if

    tell process "Superhuman"
        set frontmost to true
        delay 0.3

        # Select all and copy
        keystroke "a" using {command down}
        delay 0.2
        keystroke "c" using {command down}
        delay 0.4
    end tell
end tell

return the clipboard
EOF
)

if [ "$EMAIL_CONTENT" = "ERROR: Superhuman not running" ]; then
    echo "❌ Superhuman is not running"
    echo "   Open Superhuman and try again"
    exit 1
fi

if [ -z "$EMAIL_CONTENT" ]; then
    echo "❌ Could not copy email content"
    echo "   Make sure an email is open in Superhuman"
    exit 1
fi

# Extract subject from first line (simple heuristic)
SUBJECT_RAW=$(echo "$EMAIL_CONTENT" | head -1)
SUBJECT_CLEAN=$(echo "$SUBJECT_RAW" | sed 's/[^a-zA-Z0-9 ]//g' | sed 's/  */ /g' | cut -c 1-50 | tr ' ' '-')

if [ -z "$SUBJECT_CLEAN" ]; then
    SUBJECT_CLEAN="Email"
fi

FILENAME="Email-${DATE}-${TIME}-${SUBJECT_CLEAN}.md"

# Save to vault
cat > "${INBOX}/${FILENAME}" <<EOF
# Email: ${SUBJECT_RAW}

**Date:** ${DATE} ${TIME}
**Source:** Superhuman
**Saved:** $(date +"%Y-%m-%d %H:%M")

---

## Content

${EMAIL_CONTENT}

---

## Action Items

- [ ]

## Links
- [[Daily/${DATE}]]

Tags: #email #inbox

EOF

# Add to daily note
DAILY_NOTE="${VAULT}/Daily/${DATE}.md"
if [ -f "$DAILY_NOTE" ]; then
    echo "" >> "$DAILY_NOTE"
    echo "## 📧 Email Saved: ${SUBJECT_RAW}" >> "$DAILY_NOTE"
    echo "[[Inbox/${FILENAME%.md}]]" >> "$DAILY_NOTE"
    echo "" >> "$DAILY_NOTE"
fi

echo ""
echo "✓ Email saved: ${FILENAME}"
echo "  Location: Inbox/${FILENAME}"
if [ -f "$DAILY_NOTE" ]; then
    echo "  Linked in: Daily/${DATE}.md"
fi
echo ""
