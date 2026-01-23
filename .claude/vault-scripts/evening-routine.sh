#!/bin/bash
# Evening routine automation
# Run this at end of day to wrap up

echo "🌙 Evening routine - wrapping up your day..."
echo ""

VAULT="/Users/mikefinneran/Documents/ObsidianVault"
DATE=$(date +%Y-%m-%d)
TOMORROW=$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d "tomorrow" +%Y-%m-%d 2>/dev/null)

# 1. Export today's meetings
echo "🎙️  Exporting today's meetings..."
if [ -f "$HOME/Library/Application Support/Granola/cache-v3.json" ]; then
    "$VAULT/.scripts/granola-export.sh" >/dev/null 2>&1 && \
        echo "   ✓ All meetings exported" || \
        echo "   ℹ️  No meetings to export"
else
    echo "   ℹ️  Granola not available"
fi
echo ""

# 2. Count completed tasks
COMPLETED=$(grep -c "\- \[x\]" "$VAULT/Daily/${DATE}.md" 2>/dev/null || echo "0")
PENDING=$(grep -c "\- \[ \]" "$VAULT/Daily/${DATE}.md" 2>/dev/null || echo "0")

echo "✅ Today's progress:"
echo "   Completed: $COMPLETED tasks"
echo "   Remaining: $PENDING tasks"
echo ""

# 3. Move incomplete tasks to tomorrow
if [ $PENDING -gt 0 ]; then
    echo "📋 Moving incomplete tasks to tomorrow..."

    # Create tomorrow's note if it doesn't exist
    python3 - <<EOF
import os
from datetime import datetime, timedelta

vault = "$VAULT"
tomorrow = "$TOMORROW"
today_file = f"{vault}/Daily/${DATE}.md"
tomorrow_file = f"{vault}/Daily/{tomorrow}.md"

# Create tomorrow's note if needed
if not os.path.exists(tomorrow_file):
    with open(tomorrow_file, 'w') as f:
        f.write(f"# {tomorrow}\\n\\n")
        f.write(f"## Tasks Carried Forward\\n\\n")

# Copy incomplete tasks
if os.path.exists(today_file):
    with open(today_file, 'r') as f:
        lines = f.readlines()

    incomplete = [line for line in lines if '- [ ]' in line]

    if incomplete:
        with open(tomorrow_file, 'a') as f:
            f.write("\\n## Carried from ${DATE}\\n\\n")
            f.writelines(incomplete)

        print(f"   ✓ Moved {len(incomplete)} tasks to {tomorrow}")
EOF
fi
echo ""

# 4. Optimize today's screenshots
echo "🖼️  Optimizing today's screenshots..."
TODAY_SCREENSHOTS=$(find "$VAULT/Resources/Screenshots" -name "*${DATE}*" 2>/dev/null | wc -l | xargs)
if [ "$TODAY_SCREENSHOTS" -gt 0 ]; then
    echo "   Found $TODAY_SCREENSHOTS screenshots"
    if [ -d "/Applications/ImageOptim.app" ]; then
        find "$VAULT/Resources/Screenshots" -name "*${DATE}*" -exec open -a ImageOptim {} \;
        echo "   ✓ Optimization started"
    else
        echo "   ℹ️  ImageOptim not installed"
    fi
else
    echo "   No screenshots from today"
fi
echo ""

# 5. Summary
echo "📊 Today's summary:"
echo "   • Completed $COMPLETED tasks"
echo "   • $PENDING tasks moved to tomorrow"
echo "   • Meetings archived"
echo "   • Screenshots optimized"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Great work today!"
echo "   See you tomorrow: $TOMORROW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
