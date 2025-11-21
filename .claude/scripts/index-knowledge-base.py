#!/usr/bin/env python3
"""
Knowledge Base Airtable Indexer
Indexes all markdown files in Knowledge Base to Airtable
"""

import os
import json
from pathlib import Path
from datetime import datetime
import hashlib
import re
import subprocess

# Get Airtable credentials from 1Password
def get_airtable_token():
    try:
        result = subprocess.run(
            ['op', 'item', 'get', 'Airtable Mike Personal', '--fields', 'credential'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None

AIRTABLE_TOKEN = "***REMOVED***NWnva6jWv1.e7b44fbc9bb58eb56dc59931c1481d8aaf3e4ce79a195e9cc5c5257f0ec7d398"
BASE_ID = "appXiUbIRnkmFDlfz"
TABLE_NAME = "Knowledge Base"

KB_PATH = Path.home() / "Documents/ObsidianVault/Knowledge-Base"

def extract_metadata(file_path):
    """Extract metadata from markdown file"""
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    # Get file hash for change detection
    file_hash = hashlib.md5(content.encode()).hexdigest()
    
    # Extract title (first # header or filename)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem
    
    # Get topic from path
    rel_path = file_path.relative_to(KB_PATH)
    topic = str(rel_path.parts[0]) if len(rel_path.parts) > 1 else "Root"
    
    # Get subtopic
    subtopic = str(rel_path.parts[1]) if len(rel_path.parts) > 2 else None
    
    # Count words
    word_count = len(content.split())
    
    # Extract tags (look for #tag format)
    tags = re.findall(r'#(\w+)', content)
    tags = list(set(tags))[:10]
    
    # Get first 500 chars as summary
    summary = content[:500].strip()
    
    return {
        "Name": title,
        "File Path": str(rel_path),
        "Topic": topic,
        "Subtopic": subtopic,
        "Word Count": word_count,
        "Tags": ", ".join(tags) if tags else None,
        "Summary": summary,
        "File Hash": file_hash,
        "Last Indexed": datetime.now().isoformat(),
        "File Size (KB)": round(file_path.stat().st_size / 1024, 2)
    }

def index_knowledge_base():
    """Index all markdown files to Airtable"""
    import requests
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Get all markdown files
    md_files = list(KB_PATH.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files")
    
    # Process in batches of 10 (Airtable limit)
    batch_size = 10
    indexed = 0
    
    for i in range(0, len(md_files), batch_size):
        batch = md_files[i:i + batch_size]
        records = []
        
        for file_path in batch:
            try:
                metadata = extract_metadata(file_path)
                records.append({"fields": metadata})
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Create records in Airtable
        if records:
            url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
            response = requests.post(url, headers=headers, json={"records": records})
            
            if response.status_code in [200, 201]:
                indexed += len(records)
                print(f"Indexed {indexed}/{len(md_files)} files...")
            else:
                print(f"Error: {response.status_code} - {response.text}")
    
    print(f"Indexing complete! Total indexed: {indexed}")
    return indexed

if __name__ == "__main__":
    try:
        indexed = index_knowledge_base()
        print(f"✓ Successfully indexed {indexed} files")
    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)
