#!/usr/bin/env python3
"""
Execute Airtable Migration - Load plan and output MCP commands
This script reads the migration plan and outputs instructions for Claude Code
to execute using MCP Airtable tools.
"""

import json
from pathlib import Path
import time

# Load migration plan
plan_file = Path(__file__).parent / "airtable-sync-plan.json"
with open(plan_file, 'r') as f:
    data = json.load(f)

BASE_ID = data['base_id']
plan = data['plan']
errors = data['errors']

# Table ID mapping
TABLE_IDS = {
    'notes': 'tblRDZLwwkVjCvd27',
    'documents': 'tblbLNQlJ9Ojaz9gK',
    'projects': 'tblBjIziv9KShsemA',
}

print("=" * 80)
print("🚀 AIRTABLE MIGRATION EXECUTION")
print("=" * 80)
print()
print(f"Base ID: {BASE_ID}")
print(f"Total files to migrate: {sum(len(records) for records in plan.values())}")
print()

# Count by table
for table_name, records in plan.items():
    if records:
        print(f"  {table_name.upper()}: {len(records)} files → {TABLE_IDS[table_name]}")
print()

# Generate batch commands for Claude Code to execute
print("=" * 80)
print("📋 MIGRATION COMMANDS (for Claude Code MCP execution)")
print("=" * 80)
print()

# Output records in batches for Claude to execute
batch_size = 10
all_records = []

for table_name, records in plan.items():
    table_id = TABLE_IDS[table_name]

    for record_data in records:
        all_records.append({
            'table': table_name,
            'table_id': table_id,
            'record': record_data['record'],
            'file': record_data['file']
        })

print(f"Total records to create: {len(all_records)}")
print()
print("Ready to execute migration via MCP tools.")
print()

# Save detailed execution plan
execution_plan = {
    'base_id': BASE_ID,
    'table_mapping': TABLE_IDS,
    'records': all_records,
    'batch_size': batch_size,
    'total_records': len(all_records)
}

execution_file = Path(__file__).parent / "airtable-execution-plan.json"
with open(execution_file, 'w') as f:
    json.dump(execution_plan, f, indent=2)

print(f"💾 Execution plan saved: {execution_file}")
print()
print("=" * 80)
print("✅ Ready for Claude Code MCP execution")
print("=" * 80)
