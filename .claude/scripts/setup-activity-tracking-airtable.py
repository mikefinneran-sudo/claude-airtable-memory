#!/usr/bin/env python3
"""
Setup Daily Activity Tracking in Airtable
Creates table with schema for session logging and summaries
"""

import os
import requests
import json
from datetime import datetime

# Configuration
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID', 'appActivityTracking')

if not AIRTABLE_TOKEN:
    print("❌ AIRTABLE_TOKEN environment variable not set")
    print("\nGet your token from: https://airtable.com/create/tokens")
    print("Then run: export AIRTABLE_TOKEN='your_token_here'")
    exit(1)

headers = {
    'Authorization': f'Bearer {AIRTABLE_TOKEN}',
    'Content-Type': 'application/json'
}

# Table schema for Daily Activity Log
ACTIVITY_TABLE_SCHEMA = {
    "name": "Daily Activity Log",
    "fields": [
        {
            "name": "Date",
            "type": "dateTime",
            "options": {
                "dateFormat": "YYYY-MM-DD",
                "timeFormat": "12-hour",
                "timeZone": "America/New_York"
            }
        },
        {
            "name": "Project",
            "type": "singleLineText"
        },
        {
            "name": "Session Start",
            "type": "singleLineText"
        },
        {
            "name": "Location",
            "type": "singleLineText"
        },
        {
            "name": "Completed Tasks",
            "type": "number",
            "options": {
                "precision": 0
            }
        },
        {
            "name": "Task Details",
            "type": "multilineText"
        },
        {
            "name": "Decisions Made",
            "type": "multilineText"
        },
        {
            "name": "Files Created",
            "type": "number",
            "options": {
                "precision": 0
            }
        },
        {
            "name": "Files Modified",
            "type": "number",
            "options": {
                "precision": 0
            }
        },
        {
            "name": "Blockers",
            "type": "multilineText"
        },
        {
            "name": "Session Type",
            "type": "singleSelect",
            "options": {
                "choices": [
                    {"name": "Development", "color": "blueLight2"},
                    {"name": "Research", "color": "greenLight2"},
                    {"name": "Planning", "color": "purpleLight2"},
                    {"name": "Bug Fix", "color": "redLight2"},
                    {"name": "Review", "color": "yellowLight2"}
                ]
            }
        },
        {
            "name": "Status",
            "type": "singleSelect",
            "options": {
                "choices": [
                    {"name": "Completed", "color": "greenBright"},
                    {"name": "In Progress", "color": "yellowBright"},
                    {"name": "Blocked", "color": "redBright"}
                ]
            }
        },
        {
            "name": "Duration (mins)",
            "type": "number",
            "options": {
                "precision": 0
            }
        },
        {
            "name": "Tags",
            "type": "multipleSelects",
            "options": {
                "choices": [
                    {"name": "High Priority", "color": "redLight2"},
                    {"name": "Quick Win", "color": "greenLight2"},
                    {"name": "Learning", "color": "blueLight2"},
                    {"name": "Automation", "color": "purpleLight2"},
                    {"name": "Client Work", "color": "orangeLight2"}
                ]
            }
        }
    ]
}

def create_base():
    """Create new base for activity tracking"""
    print("📊 Creating Activity Tracking base...")

    url = "https://api.airtable.com/v0/meta/bases"

    payload = {
        "name": "Claude Activity Tracking",
        "tables": [ACTIVITY_TABLE_SCHEMA]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        base_id = data['id']
        print(f"✅ Base created successfully!")
        print(f"   Base ID: {base_id}")
        print(f"\n   Set in your environment:")
        print(f"   export AIRTABLE_BASE_ID='{base_id}'")

        # Add to shell profile
        shell_profile = os.path.expanduser("~/.zshrc")
        with open(shell_profile, "a") as f:
            f.write(f"\n# Airtable Activity Tracking\n")
            f.write(f"export AIRTABLE_BASE_ID='{base_id}'\n")
        print(f"\n✅ Added to {shell_profile}")

        return base_id
    else:
        print(f"❌ Failed to create base: {response.status_code}")
        print(response.text)
        return None

def create_table_in_existing_base():
    """Create table in existing base"""
    print(f"📊 Creating 'Daily Activity Log' table in base {BASE_ID}...")

    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"

    response = requests.post(url, headers=headers, json=ACTIVITY_TABLE_SCHEMA)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Table created successfully!")
        print(f"   Table ID: {data['id']}")
        return data['id']
    else:
        print(f"❌ Failed to create table: {response.status_code}")
        print(response.text)
        return None

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║          Daily Activity Tracking - Airtable Setup             ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    print("Choose setup option:")
    print("1. Create new base for activity tracking")
    print("2. Add table to existing base")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        base_id = create_base()
        if base_id:
            print("\n✅ Setup complete!")
            print(f"\nNext steps:")
            print(f"1. Reload shell: source ~/.zshrc")
            print(f"2. Test: ~/.claude/scripts/log-activity-to-airtable.sh")

    elif choice == "2":
        if not BASE_ID or BASE_ID == "appActivityTracking":
            print("❌ AIRTABLE_BASE_ID not set or is placeholder")
            print("   Set it with: export AIRTABLE_BASE_ID='your_base_id'")
            exit(1)

        table_id = create_table_in_existing_base()
        if table_id:
            print("\n✅ Setup complete!")
            print(f"\nTest with: ~/.claude/scripts/log-activity-to-airtable.sh")

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
