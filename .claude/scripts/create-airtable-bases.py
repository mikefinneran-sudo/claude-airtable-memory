#!/usr/bin/env python3
"""
Create Airtable Bases for AeroDyne Business Structure

Creates:
1. AeroDyne Master DB (parent company)
2. Mike Personal DB (personal life management)

Links existing WalterSignal DB as child of AeroDyne.

Author: Mike Finneran
Created: 2025-11-01
"""

import requests
import json
import os
import sys

# Get token from 1Password or environment
# TODO: Move token to 1Password after creation
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN", "REDACTED_AIRTABLE_TOKEN")

API_BASE = "https://api.airtable.com/v0"
META_API_BASE = "https://api.airtable.com/v0/meta"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}


def create_base(workspace_id, name, tables):
    """Create a new Airtable base"""
    url = f"{META_API_BASE}/bases"

    payload = {
        "name": name,
        "workspaceId": workspace_id,
        "tables": tables
    }

    print(f"\n🏗️  Creating base: {name}")

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        base_data = response.json()
        print(f"✅ Created successfully!")
        print(f"   Base ID: {base_data['id']}")
        print(f"   URL: https://airtable.com/{base_data['id']}")
        return base_data
    else:
        print(f"❌ Failed to create base")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def get_workspaces():
    """List available workspaces"""
    # Note: This endpoint might not be available in all Airtable plans
    # Fallback: User provides workspace ID manually
    print("\n📋 Fetching workspaces...")
    print("   (If this fails, you'll need to provide workspace ID manually)")

    # For now, return None and we'll handle manually
    return None


def define_aerodyne_master_tables():
    """Define schema for AeroDyne Master DB"""
    return [
        {
            "name": "Operating Companies",
            "description": "Companies under AeroDyne umbrella",
            "fields": [
                {"name": "Company Name", "type": "singleLineText"},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Active", "color": "greenBright"},
                        {"name": "Planning", "color": "yellowBright"},
                        {"name": "Paused", "color": "grayBright"},
                        {"name": "Closed", "color": "redBright"}
                    ]
                }},
                {"name": "Founded Date", "type": "date"},
                {"name": "Industry", "type": "singleLineText"},
                {"name": "Business Model", "type": "multilineText"},
                {"name": "Current MRR", "type": "currency", "options": {"precision": 2}},
                {"name": "Total Clients", "type": "number", "options": {"precision": 0}},
                {"name": "Airtable Base ID", "type": "singleLineText"},
                {"name": "Owner", "type": "singleLineText"},
                {"name": "Notes", "type": "multilineText"}
            ]
        },
        {
            "name": "Strategic Initiatives",
            "description": "Cross-company strategic projects",
            "fields": [
                {"name": "Initiative Name", "type": "singleLineText"},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Planning", "color": "blueBright"},
                        {"name": "In Progress", "color": "yellowBright"},
                        {"name": "Completed", "color": "greenBright"},
                        {"name": "On Hold", "color": "grayBright"}
                    ]
                }},
                {"name": "Priority", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Critical", "color": "redBright"},
                        {"name": "High", "color": "orangeBright"},
                        {"name": "Medium", "color": "yellowBright"},
                        {"name": "Low", "color": "grayBright"}
                    ]
                }},
                {"name": "Start Date", "type": "date"},
                {"name": "Target Date", "type": "date"},
                {"name": "Owner", "type": "singleLineText"},
                {"name": "Description", "type": "multilineText"},
                {"name": "Impact", "type": "multilineText"}
            ]
        },
        {
            "name": "Consolidated Financials",
            "description": "Company-level financial tracking",
            "fields": [
                {"name": "Month", "type": "date"},
                {"name": "Total Revenue", "type": "currency", "options": {"precision": 2}},
                {"name": "Total Expenses", "type": "currency", "options": {"precision": 2}},
                {"name": "Net Profit", "type": "currency", "options": {"precision": 2}},
                {"name": "Cash Position", "type": "currency", "options": {"precision": 2}},
                {"name": "Notes", "type": "multilineText"}
            ]
        },
        {
            "name": "Company KPIs",
            "description": "Key performance indicators across all companies",
            "fields": [
                {"name": "Metric Name", "type": "singleLineText"},
                {"name": "Company", "type": "singleLineText"},
                {"name": "Current Value", "type": "number"},
                {"name": "Target Value", "type": "number"},
                {"name": "Period", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Daily"},
                        {"name": "Weekly"},
                        {"name": "Monthly"},
                        {"name": "Quarterly"},
                        {"name": "Annually"}
                    ]
                }},
                {"name": "Last Updated", "type": "date"},
                {"name": "Trend", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Up", "color": "greenBright"},
                        {"name": "Flat", "color": "yellowBright"},
                        {"name": "Down", "color": "redBright"}
                    ]
                }}
            ]
        }
    ]


def define_personal_tables():
    """Define schema for Mike Personal DB"""
    return [
        {
            "name": "Personal Projects",
            "description": "Non-business projects and hobbies",
            "fields": [
                {"name": "Project Name", "type": "singleLineText"},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Active", "color": "greenBright"},
                        {"name": "Planning", "color": "blueBright"},
                        {"name": "On Hold", "color": "grayBright"},
                        {"name": "Completed", "color": "purpleBright"}
                    ]
                }},
                {"name": "Category", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Learning"},
                        {"name": "Hobby"},
                        {"name": "Health"},
                        {"name": "Creative"},
                        {"name": "Other"}
                    ]
                }},
                {"name": "Start Date", "type": "date"},
                {"name": "Description", "type": "multilineText"},
                {"name": "Next Action", "type": "singleLineText"}
            ]
        },
        {
            "name": "Goals & OKRs",
            "description": "Personal goals and objectives",
            "fields": [
                {"name": "Goal", "type": "singleLineText"},
                {"name": "Type", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Career"},
                        {"name": "Health"},
                        {"name": "Financial"},
                        {"name": "Learning"},
                        {"name": "Relationships"},
                        {"name": "Personal Growth"}
                    ]
                }},
                {"name": "Timeframe", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "This Week"},
                        {"name": "This Month"},
                        {"name": "This Quarter"},
                        {"name": "This Year"},
                        {"name": "Long-term"}
                    ]
                }},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Not Started", "color": "grayBright"},
                        {"name": "In Progress", "color": "yellowBright"},
                        {"name": "Achieved", "color": "greenBright"},
                        {"name": "Abandoned", "color": "redBright"}
                    ]
                }},
                {"name": "Target Date", "type": "date"},
                {"name": "Progress %", "type": "number"},
                {"name": "Notes", "type": "multilineText"}
            ]
        },
        {
            "name": "Learning & Development",
            "description": "Courses, books, skills to learn",
            "fields": [
                {"name": "Title", "type": "singleLineText"},
                {"name": "Type", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Book"},
                        {"name": "Course"},
                        {"name": "Video"},
                        {"name": "Article"},
                        {"name": "Podcast"}
                    ]
                }},
                {"name": "Status", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Want to Learn", "color": "blueBright"},
                        {"name": "In Progress", "color": "yellowBright"},
                        {"name": "Completed", "color": "greenBright"}
                    ]
                }},
                {"name": "Category", "type": "singleLineText"},
                {"name": "Started", "type": "date"},
                {"name": "Completed", "type": "date"},
                {"name": "Rating", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "⭐⭐⭐⭐⭐"},
                        {"name": "⭐⭐⭐⭐"},
                        {"name": "⭐⭐⭐"},
                        {"name": "⭐⭐"},
                        {"name": "⭐"}
                    ]
                }},
                {"name": "Notes", "type": "multilineText"},
                {"name": "Key Takeaways", "type": "multilineText"}
            ]
        },
        {
            "name": "Health & Fitness",
            "description": "Track workouts, habits, health metrics",
            "fields": [
                {"name": "Date", "type": "date"},
                {"name": "Activity Type", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Workout"},
                        {"name": "Cardio"},
                        {"name": "Yoga"},
                        {"name": "Walk"},
                        {"name": "Sleep"},
                        {"name": "Meditation"}
                    ]
                }},
                {"name": "Duration (mins)", "type": "number"},
                {"name": "Intensity", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Light"},
                        {"name": "Moderate"},
                        {"name": "Intense"}
                    ]
                }},
                {"name": "Notes", "type": "multilineText"}
            ]
        },
        {
            "name": "Ideas & Notes",
            "description": "Capture ideas, thoughts, random notes",
            "fields": [
                {"name": "Title", "type": "singleLineText"},
                {"name": "Category", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Idea"},
                        {"name": "Note"},
                        {"name": "Thought"},
                        {"name": "Quote"},
                        {"name": "Insight"}
                    ]
                }},
                {"name": "Date Created", "type": "date"},
                {"name": "Content", "type": "multilineText"},
                {"name": "Tags", "type": "multipleSelects", "options": {
                    "choices": [
                        {"name": "Business"},
                        {"name": "Personal"},
                        {"name": "Creative"},
                        {"name": "Technical"},
                        {"name": "Important"}
                    ]
                }},
                {"name": "Action Required", "type": "checkbox"}
            ]
        },
        {
            "name": "Contacts (Personal)",
            "description": "Personal relationships, not business contacts",
            "fields": [
                {"name": "Name", "type": "singleLineText"},
                {"name": "Relationship", "type": "singleSelect", "options": {
                    "choices": [
                        {"name": "Family"},
                        {"name": "Friend"},
                        {"name": "Mentor"},
                        {"name": "Acquaintance"}
                    ]
                }},
                {"name": "Email", "type": "email"},
                {"name": "Phone", "type": "phoneNumber"},
                {"name": "Last Contact", "type": "date"},
                {"name": "Notes", "type": "multilineText"}
            ]
        }
    ]


def main():
    print("=" * 70)
    print("AeroDyne Business Structure - Airtable Setup")
    print("=" * 70)

    # For base creation, user needs to provide workspace ID
    # This can be found in Airtable URL or account settings

    print("\n⚠️  SETUP REQUIRED:")
    print("To create bases, you need your Airtable Workspace ID.")
    print("Find it in Airtable > Settings > Workspace > Workspace ID")
    print()

    workspace_id = input("Enter Workspace ID (or 'skip' to just see schemas): ").strip()

    if workspace_id.lower() == 'skip':
        print("\n📋 AeroDyne Master DB Schema:")
        print(json.dumps(define_aerodyne_master_tables(), indent=2))
        print("\n📋 Mike Personal DB Schema:")
        print(json.dumps(define_personal_tables(), indent=2))
        print("\n✅ Schemas displayed. Run again with Workspace ID to create bases.")
        return

    # Create AeroDyne Master DB
    aerodyne_base = create_base(
        workspace_id,
        "AeroDyne Master",
        define_aerodyne_master_tables()
    )

    # Create Mike Personal DB
    personal_base = create_base(
        workspace_id,
        "Mike Personal",
        define_personal_tables()
    )

    print("\n" + "=" * 70)
    print("✅ BASE CREATION COMPLETE")
    print("=" * 70)

    if aerodyne_base:
        print(f"\n📊 AeroDyne Master DB")
        print(f"   ID: {aerodyne_base['id']}")
        print(f"   URL: https://airtable.com/{aerodyne_base['id']}")

    if personal_base:
        print(f"\n📊 Mike Personal DB")
        print(f"   ID: {personal_base['id']}")
        print(f"   URL: https://airtable.com/{personal_base['id']}")

    print(f"\n📊 WalterSignal DB (Existing)")
    print(f"   ID: app6g0t0wtruwLA5I")
    print(f"   URL: https://airtable.com/app6g0t0wtruwLA5I")

    print("\n🔒 NEXT STEPS:")
    print("1. Move API tokens to 1Password:")
    print("   - op://API_Keys/Airtable AeroDyne/credential")
    print("   - op://API_Keys/Airtable Personal/credential")
    print("2. Add WalterSignal as child company in AeroDyne Master")
    print("3. Configure automations between bases")
    print("4. Set up Claude memory sync to Airtable")


if __name__ == "__main__":
    main()
