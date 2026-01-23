#!/usr/bin/env python3
"""
Sync Obsidian Vault to Airtable Knowledge Management Base
Architecture: Obsidian → Airtable → Notion
"""

import os
import json
from pathlib import Path
from datetime import datetime
import re

# Check for Airtable MCP - we'll use claude's mcp__airtable tools
# This script is designed to be called by Claude Code with MCP access

VAULT_PATH = Path.home() / "Documents/ObsidianVault"
AIRTABLE_BASE_ID = "appx922aa4LURWlMI"  # Knowledge Management

# Table mappings
TABLES = {
    "notes": "tblRDZLwwkVjCvd27",      # 📝 Notes
    "documents": "tbl🗂️ Documents",     # Will need actual ID
    "projects": "tblBjIziv9KShsemA",   # 🚀 Projects
}

def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown"""
    if not content.startswith('---'):
        return {}, content

    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content

        frontmatter_text = parts[1].strip()
        body = parts[2].strip()

        # Simple YAML parsing (key: value)
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()

        return frontmatter, body
    except Exception as e:
        print(f"Error parsing frontmatter: {e}")
        return {}, content

def get_content_type(file_path, frontmatter):
    """Determine which Airtable table to use"""

    # Check frontmatter
    if 'type' in frontmatter:
        content_type = frontmatter['type'].lower()
        if 'project' in content_type:
            return 'projects'
        if 'document' in content_type:
            return 'documents'

    # Check file location
    path_str = str(file_path)
    if '/Projects/' in path_str:
        return 'projects'
    if '/Documents/' in path_str or '/Content/' in path_str:
        return 'documents'

    # Default to notes
    return 'notes'

def prepare_airtable_record(file_path, frontmatter, body, content_type):
    """Convert markdown file to Airtable record format"""

    record = {
        "Name": file_path.stem,  # Filename without extension
        "Notes": body[:100000],  # Airtable long text limit
    }

    # Add status if available
    if 'status' in frontmatter:
        status = frontmatter['status'].title()
        if status in ['Todo', 'In Progress', 'Done']:
            record['Status'] = status

    return record

def scan_vault(folder=None):
    """Scan vault and return list of markdown files to sync"""

    base_path = VAULT_PATH / folder if folder else VAULT_PATH

    # Folders to sync
    sync_folders = [
        "Daily",
        "Projects",
        "Content",
        "Resources",
        "Prompts",
    ]

    files_to_sync = []

    for folder_name in sync_folders:
        folder_path = base_path / folder_name
        if not folder_path.exists():
            continue

        # Get all .md files
        for md_file in folder_path.rglob("*.md"):
            # Skip certain files
            if md_file.name.startswith('.'):
                continue
            if '.git' in str(md_file):
                continue
            if 'node_modules' in str(md_file):
                continue

            files_to_sync.append(md_file)

    return files_to_sync

def sync_file_to_airtable(file_path):
    """Sync a single file to Airtable

    NOTE: This function outputs instructions for Claude Code to execute
    using MCP airtable tools. It doesn't directly call Airtable API.
    """

    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse
        frontmatter, body = parse_frontmatter(content)
        content_type = get_content_type(file_path, frontmatter)

        # Prepare record
        record = prepare_airtable_record(file_path, frontmatter, body, content_type)

        return {
            "file": str(file_path.relative_to(VAULT_PATH)),
            "table": content_type,
            "record": record,
            "action": "create_or_update"
        }

    except Exception as e:
        return {
            "file": str(file_path),
            "error": str(e)
        }

def generate_sync_plan():
    """Generate migration plan (dry run)"""

    print("🔍 Scanning Obsidian Vault...")
    print(f"📂 Location: {VAULT_PATH}")
    print(f"🎯 Target: Airtable Knowledge Management ({AIRTABLE_BASE_ID})")
    print()

    files = scan_vault()
    print(f"✅ Found {len(files)} files to sync")
    print()

    # Categorize by table
    by_table = {"notes": [], "documents": [], "projects": []}
    errors = []

    for file_path in files:  # Process ALL files
        result = sync_file_to_airtable(file_path)
        if 'error' in result:
            errors.append(result)
        else:
            by_table[result['table']].append(result)

    # Print plan
    print("📊 SYNC PLAN (All files):")
    print()

    for table_name, records in by_table.items():
        if records:
            print(f"  📋 {table_name.upper()}: {len(records)} files")
            for r in records[:3]:  # Show first 3
                print(f"    • {r['file']}")
            if len(records) > 3:
                print(f"    ... and {len(records) - 3} more")
            print()

    if errors:
        print(f"  ⚠️  ERRORS: {len(errors)} files")
        for e in errors:
            print(f"    • {e['file']}: {e['error']}")

    print()
    print("=" * 60)
    print("📝 NEXT STEPS:")
    print()
    print("This script has generated a sync plan.")
    print("To execute, Claude Code will use MCP Airtable tools:")
    print()
    print("1. mcp__airtable__create_record() for new files")
    print("2. mcp__airtable__update_records() for existing files")
    print("3. Track sync state to avoid duplicates")
    print()
    print("Ready to execute? Tell Claude: 'Execute Airtable sync'")
    print("=" * 60)

    return by_table, errors

if __name__ == "__main__":
    plan, errors = generate_sync_plan()

    # Save plan for Claude to execute
    plan_file = Path(__file__).parent / "airtable-sync-plan.json"
    with open(plan_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "base_id": AIRTABLE_BASE_ID,
            "plan": plan,
            "errors": errors
        }, f, indent=2)

    print(f"\n💾 Plan saved to: {plan_file}")
