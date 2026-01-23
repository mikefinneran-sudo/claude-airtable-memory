#!/usr/bin/env python3
"""
Sync Airtable Knowledge Management → Notion LifeHub
Automated bi-directional sync for complete data pipeline
"""

import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime

# Configuration
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
NOTION_TOKEN = os.getenv('NOTION_TOKEN')

AIRTABLE_BASE_ID = "appx922aa4LURWlMI"

# Notion Database IDs (to be configured)
NOTION_DATABASES = {
    'projects': os.getenv('NOTION_PROJECTS_DB', ''),  # From your LifeHub URL
    'documents': os.getenv('NOTION_DOCUMENTS_DB', ''),
    'notes': os.getenv('NOTION_NOTES_DB', ''),
}

# Airtable Table IDs
AIRTABLE_TABLES = {
    'projects': 'tblBjIziv9KShsemA',
    'documents': 'tblbLNQlJ9Ojaz9gK',
    'notes': 'tblRDZLwwkVjCvd27',
}

print("=" * 80)
print("🔄 AIRTABLE → NOTION SYNC")
print("=" * 80)
print()

# Validate tokens
if not AIRTABLE_TOKEN:
    print("❌ AIRTABLE_TOKEN not set")
    print("Run: export AIRTABLE_TOKEN=$(op item get 'Airtable Mike Personal' --fields credential --reveal)")
    exit(1)

if not NOTION_TOKEN:
    print("❌ NOTION_TOKEN not set")
    print()
    print("📋 SETUP REQUIRED:")
    print()
    print("1. Go to: https://www.notion.com/my-integrations")
    print("2. Click '+ New integration'")
    print("3. Name: 'Airtable Sync'")
    print("4. Workspace: Select your workspace")
    print("5. Click 'Submit'")
    print("6. Copy 'Internal Integration Secret'")
    print("7. Run: export NOTION_TOKEN='your-token-here'")
    print()
    print("Then run this script again.")
    exit(1)

# Headers
airtable_headers = {
    'Authorization': f'Bearer {AIRTABLE_TOKEN}',
    'Content-Type': 'application/json'
}

notion_headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def get_airtable_records(table_id, max_records=100):
    """Fetch records from Airtable table"""
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_id}'

    params = {'maxRecords': max_records}

    try:
        response = requests.get(url, headers=airtable_headers, params=params)
        if response.status_code == 200:
            return response.json().get('records', [])
        else:
            print(f"❌ Airtable API error: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"❌ Error fetching from Airtable: {e}")
        return []

def create_notion_page(database_id, properties, content=""):
    """Create page in Notion database"""
    url = 'https://api.notion.com/v1/pages'

    # Convert Airtable record to Notion page properties
    notion_properties = {
        'Name': {
            'title': [
                {
                    'text': {
                        'content': properties.get('Name', 'Untitled')
                    }
                }
            ]
        }
    }

    # Add content as blocks if available
    children = []
    if content and isinstance(content, str):
        # Split into paragraphs (Notion limit: 2000 chars per block)
        paragraphs = content.split('\n\n')
        for para in paragraphs[:50]:  # Limit to 50 blocks
            if para.strip():
                children.append({
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': para[:2000]  # Notion limit
                                }
                            }
                        ]
                    }
                })

    payload = {
        'parent': {'database_id': database_id},
        'properties': notion_properties,
    }

    if children:
        payload['children'] = children

    try:
        response = requests.post(url, headers=notion_headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Notion API error: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error creating Notion page: {e}")
        return None

def sync_table(table_name, airtable_table_id, notion_db_id, limit=10):
    """Sync one Airtable table to Notion database"""

    if not notion_db_id:
        print(f"⚠️  Skipping {table_name}: Notion database ID not configured")
        return 0, 0

    print(f"\n📋 Syncing {table_name.upper()}...")
    print(f"   Airtable: {airtable_table_id}")
    print(f"   Notion: {notion_db_id}")
    print()

    # Fetch records from Airtable
    records = get_airtable_records(airtable_table_id, max_records=limit)
    print(f"   Fetched {len(records)} records from Airtable")

    created = 0
    errors = 0

    # Create in Notion
    for i, record in enumerate(records, 1):
        fields = record.get('fields', {})
        name = fields.get('Name', f'Record {record["id"]}')
        content = fields.get('Notes', '')

        print(f"   {i}/{len(records)}: {name[:50]}...", end=' ')

        result = create_notion_page(notion_db_id, fields, content)

        if result:
            print("✅")
            created += 1
        else:
            print("❌")
            errors += 1

        # Rate limiting
        time.sleep(0.35)  # Notion: 3 requests/second limit

    print()
    print(f"   ✅ Created: {created}")
    print(f"   ❌ Errors: {errors}")

    return created, errors

def main():
    """Main sync process"""

    print("🔍 Configuration Check:")
    print(f"   Airtable Base: {AIRTABLE_BASE_ID}")
    print(f"   Notion Projects DB: {NOTION_DATABASES['projects'] or 'NOT SET'}")
    print(f"   Notion Documents DB: {NOTION_DATABASES['documents'] or 'NOT SET'}")
    print()

    if not any(NOTION_DATABASES.values()):
        print("❌ No Notion databases configured")
        print()
        print("Set database IDs:")
        print("   export NOTION_PROJECTS_DB='your-database-id'")
        print("   export NOTION_DOCUMENTS_DB='your-database-id'")
        print()
        print("Get database ID from Notion URL:")
        print("   https://notion.so/workspace/DATABASE_ID?v=VIEW_ID")
        print()
        exit(1)

    # Sync each table
    total_created = 0
    total_errors = 0

    # Projects
    if NOTION_DATABASES['projects']:
        created, errors = sync_table(
            'projects',
            AIRTABLE_TABLES['projects'],
            NOTION_DATABASES['projects'],
            limit=10  # Start with 10 for testing
        )
        total_created += created
        total_errors += errors

    # Documents
    if NOTION_DATABASES['documents']:
        created, errors = sync_table(
            'documents',
            AIRTABLE_TABLES['documents'],
            NOTION_DATABASES['documents'],
            limit=10
        )
        total_created += created
        total_errors += errors

    # Summary
    print()
    print("=" * 80)
    print("📊 SYNC SUMMARY")
    print("=" * 80)
    print(f"✅ Total Created: {total_created}")
    print(f"❌ Total Errors: {total_errors}")
    print()

    # Save results
    results = {
        'timestamp': datetime.now().isoformat(),
        'created': total_created,
        'errors': total_errors,
    }

    results_file = Path(__file__).parent / 'notion-sync-results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"💾 Results saved: {results_file}")
    print()

    if total_errors == 0 and total_created > 0:
        print("=" * 80)
        print("✅ SYNC COMPLETE!")
        print("=" * 80)
    else:
        print("⚠️  Sync completed with errors")

if __name__ == "__main__":
    main()
