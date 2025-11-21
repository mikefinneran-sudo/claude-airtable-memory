#!/usr/bin/env python3
import subprocess
import requests

# Get token
result = subprocess.run(['op', 'item', 'get', 'Airtable', '--fields', 'label=credential'],
                       capture_output=True, text=True, check=True)
AIRTABLE_TOKEN = result.stdout.strip()
BASE_ID = "appXiUbIRnkmFDlfz"

headers = {"Authorization": f"Bearer {AIRTABLE_TOKEN}", "Content-Type": "application/json"}

# Create Knowledge Base table
table_def = {
    "name": "Knowledge Base",
    "description": "Index of all research documents",
    "fields": [
        {"name": "Name", "type": "singleLineText"},
        {"name": "File Path", "type": "singleLineText"},
        {"name": "Topic", "type": "singleSelect", "options": {"choices": [
            {"name": "AI-ML"}, {"name": "Web-Development"}, {"name": "Infrastructure-DevOps"},
            {"name": "Business-Products"}, {"name": "Development-Tools"},
            {"name": "Research-Docs"}, {"name": "Client-Projects"}
        ]}},
        {"name": "Subtopic", "type": "singleLineText"},
        {"name": "Word Count", "type": "number", "options": {"precision": 0}},
        {"name": "Tags", "type": "singleLineText"},
        {"name": "Summary", "type": "multilineText"},
        {"name": "File Hash", "type": "singleLineText"},
        {"name": "Last Indexed", "type": "dateTime", "options": {"dateFormat": {"name": "iso"}}},
        {"name": "File Size (KB)", "type": "number", "options": {"precision": 2}}
    ]
}

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
response = requests.post(url, headers=headers, json=table_def)

if response.status_code in [200, 201]:
    print("✓ Knowledge Base table created!")
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
