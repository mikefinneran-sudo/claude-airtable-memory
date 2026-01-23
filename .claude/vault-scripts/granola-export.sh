#!/bin/bash
# Export latest Granola meeting to vault

VAULT_PATH="/Users/mikefinneran/Documents/ObsidianVault"
GRANOLA_CACHE="$HOME/Library/Application Support/Granola/cache-v3.json"
MEETINGS_DIR="${VAULT_PATH}/Projects/WalterSignal/Meetings"
DATE=$(date +%Y-%m-%d)

mkdir -p "$MEETINGS_DIR"

if [ ! -f "$GRANOLA_CACHE" ]; then
    echo "❌ Granola cache not found at:"
    echo "   $GRANOLA_CACHE"
    echo ""
    echo "Make sure Granola app has recorded meetings."
    exit 1
fi

echo "📝 Exporting latest Granola meeting..."
echo ""

# Parse Granola cache and export latest meeting
python3 - <<EOF
import json
import os
from datetime import datetime

cache_file = "$GRANOLA_CACHE"
meetings_dir = "$MEETINGS_DIR"

try:
    with open(cache_file, 'r') as f:
        data = json.load(f)

    # Get most recent meeting
    if 'meetings' in data and len(data['meetings']) > 0:
        latest = data['meetings'][-1]

        title = latest.get('title', 'Untitled Meeting')
        transcript = latest.get('transcript', '')
        notes = latest.get('notes', '')
        summary = latest.get('summary', '')
        date_str = latest.get('date', '$DATE')
        duration = latest.get('duration', 'Unknown')

        # Create safe filename
        safe_title = title.replace(' ', '-').replace('/', '-')
        filename = f"{date_str}_{safe_title}.md"
        filepath = os.path.join(meetings_dir, filename)

        # Write meeting note
        with open(filepath, 'w') as f:
            f.write(f"# {title}\\n\\n")
            f.write(f"**Date:** {date_str}\\n")
            f.write(f"**Duration:** {duration}\\n")
            f.write(f"**Source:** Granola\\n\\n")

            if summary:
                f.write(f"## Summary\\n\\n{summary}\\n\\n")

            if notes:
                f.write(f"## AI Notes\\n\\n{notes}\\n\\n")

            if transcript:
                f.write(f"## Transcript\\n\\n{transcript}\\n\\n")

            f.write(f"---\\n\\n")
            f.write(f"## Links\\n")
            f.write(f"- [[Daily/{date_str}]]\\n\\n")
            f.write(f"Tags: #meeting #granola\\n")

        print(f"✓ Exported: {filename}")
        print(f"  Location: Meetings/{filename}")
        print(f"  Duration: {duration}")
    else:
        print("No meetings found in Granola cache")
        print("Record a meeting first, then try again.")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
EOF
