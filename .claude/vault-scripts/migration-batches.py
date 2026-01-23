#!/usr/bin/env python3
"""
Generate batches for Airtable migration
Outputs records in groups for Claude Code MCP processing
"""

import json
import sys

# Load execution plan
with open('airtable-execution-plan.json', 'r') as f:
    data = json.load(f)

BASE_ID = data['base_id']
records = data['records']
batch_size = 10

# Get batch number from command line (default to all)
batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else None

total_batches = (len(records) + batch_size - 1) // batch_size

if batch_num is not None:
    # Output single batch
    start = (batch_num - 1) * batch_size
    end = min(start + batch_size, len(records))
    batch_records = records[start:end]

    print(f"Batch {batch_num}/{total_batches}")
    print(f"Records: {start+1}-{end} of {len(records)}")
    print()

    for i, rec in enumerate(batch_records, start+1):
        print(json.dumps({
            'index': i,
            'file': rec['file'],
            'baseId': BASE_ID,
            'tableId': rec['table_id'],
            'fields': rec['record']
        }))
else:
    # Output summary
    print(f"Total records: {len(records)}")
    print(f"Total batches: {total_batches}")
    print(f"Batch size: {batch_size}")
    print()

    # Count by table
    by_table = {}
    for rec in records:
        table = rec['table']
        by_table[table] = by_table.get(table, 0) + 1

    print("By table:")
    for table, count in by_table.items():
        print(f"  {table}: {count}")
