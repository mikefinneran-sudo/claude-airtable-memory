#!/bin/bash
# Extract action items from latest Granola meeting and add to daily note

GRANOLA_CACHE="$HOME/Library/Application Support/Granola/cache-v3.json"
DATE=$(date +%Y-%m-%d)
DAILY_NOTE="/Users/mikefinneran/Documents/ObsidianVault/Daily/${DATE}.md"

if [ ! -f "$GRANOLA_CACHE" ]; then
    echo "❌ Granola cache not found"
    exit 1
fi

if [ ! -f "$DAILY_NOTE" ]; then
    echo "❌ Daily note not found: ${DATE}.md"
    echo "Create it first: python3 .scripts/update_daily_note.py"
    exit 1
fi

echo "🎯 Extracting action items from meeting..."
echo ""

python3 - <<EOF
import json
import re

with open("$GRANOLA_CACHE", 'r') as f:
    data = json.load(f)

if data.get('meetings'):
    latest = data['meetings'][-1]
    notes = latest.get('notes', '')
    title = latest.get('title', 'Meeting')

    # Extract action items (lines with - [ ] or starting with -, *, •)
    lines = notes.split('\\n')
    actions = []

    for line in lines:
        line = line.strip()
        # Match task items or bullet points that look like actions
        if re.match(r'^[\-\*•]\s*\[.\]', line) or \
           (re.match(r'^[\-\*•]', line) and any(word in line.lower() for word in ['todo', 'action', 'follow up', 'schedule', 'send', 'create', 'update'])):
            actions.append(line)

    if actions:
        with open("$DAILY_NOTE", 'a') as f:
            f.write(f"\\n## Action Items from {title}\\n\\n")
            for action in actions:
                # Ensure checkbox format
                if '[ ]' not in action:
                    action = f"- [ ] {action.lstrip('-*• ')}"
                f.write(f"{action}\\n")

        print(f"✓ Added {len(actions)} action items to daily note")
        print("")
        print("Action items:")
        for action in actions:
            print(f"  {action}")
    else:
        print("No action items found in meeting notes")

EOF
