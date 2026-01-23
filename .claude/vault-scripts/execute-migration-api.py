#!/usr/bin/env python3
"""
Execute Airtable Migration via Direct API
Uses Airtable REST API for efficient batch processing
"""

import json
import os
import time
import requests
from pathlib import Path

# Get Airtable token
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
if not AIRTABLE_TOKEN:
    print("❌ AIRTABLE_TOKEN not set")
    print("Run: export AIRTABLE_TOKEN='your-token'")
    exit(1)

# Load execution plan
plan_file = Path(__file__).parent / "airtable-execution-plan.json"
with open(plan_file, 'r') as f:
    data = json.load(f)

BASE_ID = data['base_id']
records = data['records']

print("=" * 80)
print("🚀 AIRTABLE MIGRATION - API EXECUTION")
print("=" * 80)
print(f"Base: {BASE_ID}")
print(f"Total records: {len(records)}")
print()

# Airtable API allows batch creates of up to 10 records at a time
BATCH_SIZE = 10
API_DELAY = 0.25  # 250ms between requests (Airtable: 5 req/sec limit)

headers = {
    'Authorization': f'Bearer {AIRTABLE_TOKEN}',
    'Content-Type': 'application/json'
}

# Track results
created = []
errors = []

# Process by table
by_table = {}
for rec in records:
    table_id = rec['table_id']
    if table_id not in by_table:
        by_table[table_id] = []
    by_table[table_id].append(rec)

# Process each table
for table_id, table_records in by_table.items():
    table_name = table_records[0]['table']
    print(f"\n📋 Processing {table_name.upper()} ({len(table_records)} records)...")

    # Process in batches
    for i in range(0, len(table_records), BATCH_SIZE):
        batch = table_records[i:i+BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(table_records) + BATCH_SIZE - 1) // BATCH_SIZE

        # Prepare batch payload
        payload = {
            'records': [{'fields': rec['record']} for rec in batch]
        }

        # Make API request
        url = f'https://api.airtable.com/v0/{BASE_ID}/{table_id}'

        try:
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                created.extend(result['records'])
                print(f"  ✅ Batch {batch_num}/{total_batches}: {len(result['records'])} records created")
            else:
                error_msg = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                print(f"  ❌ Batch {batch_num}/{total_batches}: Error {response.status_code}")
                print(f"     {error_msg}")
                errors.append({
                    'batch': batch_num,
                    'records': [rec['file'] for rec in batch],
                    'error': error_msg
                })

            # Rate limiting
            time.sleep(API_DELAY)

        except Exception as e:
            print(f"  ❌ Batch {batch_num}/{total_batches}: Exception {str(e)}")
            errors.append({
                'batch': batch_num,
                'records': [rec['file'] for rec in batch],
                'error': str(e)
            })

print()
print("=" * 80)
print("📊 MIGRATION SUMMARY")
print("=" * 80)
print(f"✅ Created: {len(created)} records")
print(f"❌ Errors: {len(errors)} batches")
print()

if errors:
    print("Error details:")
    for err in errors:
        print(f"  Batch {err['batch']}: {err['error']}")
        print(f"    Files: {', '.join(err['records'][:3])}...")
    print()

# Save results
results_file = Path(__file__).parent / "migration-results.json"
with open(results_file, 'w') as f:
    json.dump({
        'created': len(created),
        'errors': errors,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }, f, indent=2)

print(f"💾 Results saved: {results_file}")
print()
print("=" * 80)
if len(created) == len(records):
    print("✅ MIGRATION COMPLETE!")
else:
    print(f"⚠️  Migration incomplete: {len(created)}/{len(records)} records created")
print("=" * 80)
