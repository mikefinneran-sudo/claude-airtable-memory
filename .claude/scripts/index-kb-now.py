#!/usr/bin/env python3
"""Quick index to Airtable with hardcoded token"""

import requests
from pathlib import Path
import hashlib
import re
from datetime import datetime

# Token from user
AIRTABLE_TOKEN = "***REMOVED***NWnva6jWv1.e7b44fbc9bb58eb56dc59931c1481d8aaf3e4ce79a195e9cc5c5257f0ec7d398"
BASE_ID = "appXiUbIRnkmFDlfz"
TABLE_NAME = "Knowledge Base"
KB_PATH = Path.home() / "Documents/ObsidianVault/Knowledge-Base"

headers = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

md_files = list(KB_PATH.rglob("*.md"))
print(f"Found {len(md_files)} files")

indexed = 0
for i in range(0, len(md_files), 10):
    batch = md_files[i:i+10]
    records = []

    for fp in batch:
        try:
            content = fp.read_text(encoding='utf-8', errors='ignore')
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else fp.stem
            rel_path = fp.relative_to(KB_PATH)
            topic = str(rel_path.parts[0]) if len(rel_path.parts) > 1 else "Research-Docs"

            records.append({"fields": {
                "Name": title[:100],
                "File Path": str(rel_path),
                "Topic": topic,
                "Word Count": len(content.split()),
                "Summary": content[:500].strip(),
                "File Hash": hashlib.md5(content.encode()).hexdigest(),
                "Last Indexed": datetime.now().isoformat(),
                "File Size (KB)": round(fp.stat().st_size / 1024, 2)
            }})
        except Exception as e:
            print(f"Error: {fp}: {e}")

    if records:
        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
        response = requests.post(url, headers=headers, json={"records": records})

        if response.status_code in [200, 201]:
            indexed += len(records)
            print(f"✓ Indexed {indexed}/{len(md_files)}")
        else:
            print(f"✗ Error: {response.status_code} - {response.text[:200]}")

print(f"\n✓ Complete! Indexed {indexed} files to Airtable")
