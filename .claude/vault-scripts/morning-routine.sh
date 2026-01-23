#!/bin/bash
# Morning routine automation
# Run this first thing to set up your day

echo "☀️  Good morning! Setting up your day..."
echo ""

VAULT="/Users/mikefinneran/Documents/ObsidianVault"
DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)

# 1. Create/update daily note
echo "📅 Creating today's daily note..."
python3 "$VAULT/.scripts/update_daily_note.py"
echo "   ✓ Daily note ready: Daily/${DATE}.md"
echo ""

# 2. Export yesterday's meetings
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d 2>/dev/null)
echo "🎙️  Checking for meetings from yesterday..."
if [ -f "$HOME/Library/Application Support/Granola/cache-v3.json" ]; then
    "$VAULT/.scripts/granola-export.sh" >/dev/null 2>&1 && \
        echo "   ✓ Meeting notes exported" || \
        echo "   ℹ️  No new meetings to export"
else
    echo "   ℹ️  Granola not available"
fi
echo ""

# 3. Check for pending action items
echo "✅ Checking pending tasks..."
PENDING=$(grep -c "\- \[ \]" "$VAULT/Daily/${DATE}.md" 2>/dev/null || echo "0")
echo "   You have $PENDING pending tasks today"
echo ""

# 4. Show today's priorities
echo "🎯 Today's focus:"
grep "## Priority" "$VAULT/Daily/${DATE}.md" -A 5 2>/dev/null | tail -5 || echo "   (Set your priorities in the daily note)"
echo ""

# 5. Open vault
echo "📓 Opening vault..."
open -a "Obsidian" "$VAULT"
sleep 1
open "obsidian://open?vault=ObsidianVault&file=Daily/${DATE}.md"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Ready to start your day!"
echo "   Today is $DAY, $DATE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
