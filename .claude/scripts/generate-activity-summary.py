#!/usr/bin/env python3
"""
Generate Activity Summary from Airtable
Query activity log and create summaries by timeframe
"""

import os
import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = "Daily Activity Log"

if not AIRTABLE_TOKEN or not BASE_ID:
    print("❌ Missing environment variables")
    print("   Required: AIRTABLE_TOKEN and AIRTABLE_BASE_ID")
    exit(1)

headers = {
    'Authorization': f'Bearer {AIRTABLE_TOKEN}',
    'Content-Type': 'application/json'
}

def fetch_activities(days=7):
    """Fetch activities from last N days"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

    # Calculate date filter
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Airtable filter formula
    formula = f"IS_AFTER({{Date}}, '{since_date}')"

    params = {
        'filterByFormula': formula,
        'sort[0][field]': 'Date',
        'sort[0][direction]': 'desc'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get('records', [])
    else:
        print(f"❌ Failed to fetch activities: {response.status_code}")
        print(response.text)
        return []

def generate_summary(records, timeframe="week"):
    """Generate summary from activity records"""

    if not records:
        print(f"No activities found for the last {timeframe}")
        return

    # Aggregate stats
    stats = {
        'total_sessions': len(records),
        'total_tasks': 0,
        'total_files_created': 0,
        'total_files_modified': 0,
        'projects': defaultdict(int),
        'session_types': defaultdict(int),
        'blockers': [],
        'top_decisions': []
    }

    for record in records:
        fields = record.get('fields', {})

        stats['total_tasks'] += fields.get('Completed Tasks', 0)
        stats['total_files_created'] += fields.get('Files Created', 0)
        stats['total_files_modified'] += fields.get('Files Modified', 0)

        project = fields.get('Project', 'Unknown')
        stats['projects'][project] += 1

        session_type = fields.get('Session Type', 'Unknown')
        stats['session_types'][session_type] += 1

        blockers = fields.get('Blockers', '')
        if blockers:
            stats['blockers'].append(blockers)

        decisions = fields.get('Decisions Made', '')
        if decisions:
            stats['top_decisions'].append(decisions)

    # Print summary
    print("╔════════════════════════════════════════════════════════════════╗")
    print(f"║          Activity Summary - Last {timeframe.capitalize():<25}       ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")

    print(f"📊 Overall Statistics")
    print(f"   Total Sessions: {stats['total_sessions']}")
    print(f"   Tasks Completed: {stats['total_tasks']}")
    print(f"   Files Created: {stats['total_files_created']}")
    print(f"   Files Modified: {stats['total_files_modified']}")
    print()

    print("📁 Projects Worked On")
    for project, count in sorted(stats['projects'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {project}: {count} sessions")
    print()

    print("🏷️  Session Types")
    for session_type, count in sorted(stats['session_types'].items(), key=lambda x: x[1], reverse=True):
        print(f"   {session_type}: {count} sessions")
    print()

    if stats['blockers']:
        print("⚠️  Active Blockers")
        for blocker in stats['blockers'][:5]:
            print(f"   - {blocker}")
        print()

    if stats['top_decisions']:
        print("💡 Key Decisions Made")
        for decision in stats['top_decisions'][:5]:
            if decision:
                decisions_list = decision.split(',')
                for d in decisions_list[:3]:
                    if d.strip():
                        print(f"   - {d.strip()}")
        print()

    # Recent sessions detail
    print("📝 Recent Sessions")
    for record in records[:5]:
        fields = record.get('fields', {})
        date = fields.get('Date', '')[:10] if fields.get('Date') else 'Unknown'
        project = fields.get('Project', 'Unknown')
        tasks = fields.get('Completed Tasks', 0)
        status = fields.get('Status', 'Unknown')

        print(f"   {date} | {project} | {tasks} tasks | {status}")

    print()

def export_to_markdown(records, timeframe="week"):
    """Export summary to markdown file"""
    filename = f"activity-summary-{timeframe}-{datetime.now().strftime('%Y-%m-%d')}.md"
    filepath = os.path.expanduser(f"~/.claude/{filename}")

    with open(filepath, 'w') as f:
        f.write(f"# Activity Summary - Last {timeframe.capitalize()}\n\n")
        f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

        # Write stats (similar to generate_summary but in markdown)
        stats = {
            'total_sessions': len(records),
            'total_tasks': sum(r.get('fields', {}).get('Completed Tasks', 0) for r in records),
            'total_files_created': sum(r.get('fields', {}).get('Files Created', 0) for r in records),
            'total_files_modified': sum(r.get('fields', {}).get('Files Modified', 0) for r in records),
        }

        f.write("## Overall Statistics\n\n")
        f.write(f"- Total Sessions: {stats['total_sessions']}\n")
        f.write(f"- Tasks Completed: {stats['total_tasks']}\n")
        f.write(f"- Files Created: {stats['total_files_created']}\n")
        f.write(f"- Files Modified: {stats['total_files_modified']}\n\n")

        f.write("## Sessions\n\n")
        for record in records:
            fields = record.get('fields', {})
            date = fields.get('Date', '')[:10] if fields.get('Date') else 'Unknown'
            project = fields.get('Project', 'Unknown')
            tasks = fields.get('Completed Tasks', 0)

            f.write(f"### {date} - {project}\n\n")
            f.write(f"- Tasks: {tasks}\n")

            task_details = fields.get('Task Details', '')
            if task_details:
                f.write(f"- Details: {task_details}\n")

            f.write("\n")

    print(f"✅ Summary exported to: {filepath}")
    return filepath

def main():
    import sys

    timeframe = sys.argv[1] if len(sys.argv) > 1 else "week"

    # Map timeframe to days
    timeframe_map = {
        'day': 1,
        'week': 7,
        'month': 30,
        'quarter': 90
    }

    days = timeframe_map.get(timeframe, 7)

    print(f"📊 Fetching activities from last {days} days...\n")

    records = fetch_activities(days)

    if not records:
        print("No activities found")
        return

    # Generate terminal summary
    generate_summary(records, timeframe)

    # Ask to export
    export = input("\nExport to markdown? (y/N): ").strip().lower()
    if export == 'y':
        filepath = export_to_markdown(records, timeframe)
        print(f"\n✅ Done! View with: cat {filepath}")

if __name__ == "__main__":
    main()
