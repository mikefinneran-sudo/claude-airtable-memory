#!/bin/bash
# OCR screen region and add extracted text to daily note

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M)
DAILY_NOTE="/Users/mikefinneran/Documents/ObsidianVault/Daily/${DATE}.md"

echo "📸 Starting OCR capture..."
echo "   Select the area with text to extract"

# Trigger OCR
open "cleanshot://ocr"

# Wait for OCR to complete and copy to clipboard
sleep 4

# Get clipboard content
OCR_TEXT=$(pbpaste)

if [ -z "$OCR_TEXT" ]; then
    echo "❌ No text extracted. Make sure CleanShot X OCR completed."
    exit 1
fi

# Append to daily note
if [ -f "$DAILY_NOTE" ]; then
    echo "" >> "$DAILY_NOTE"
    echo "## OCR Extract - ${TIME}" >> "$DAILY_NOTE"
    echo '```' >> "$DAILY_NOTE"
    echo "$OCR_TEXT" >> "$DAILY_NOTE"
    echo '```' >> "$DAILY_NOTE"
    echo "" >> "$DAILY_NOTE"
    echo "✓ OCR text added to daily note: Daily/${DATE}.md"
    echo ""
    echo "Extracted text:"
    echo "─────────────────"
    echo "$OCR_TEXT"
    echo "─────────────────"
else
    echo "⚠️  Daily note not found: ${DATE}.md"
    echo "   Text is still in clipboard. Create note first:"
    echo "   python3 .scripts/update_daily_note.py"
fi
