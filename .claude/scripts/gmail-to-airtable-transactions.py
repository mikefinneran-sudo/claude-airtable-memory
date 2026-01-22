#!/usr/bin/env python3
"""
Gmail to Airtable Transaction Importer
Parses Gmail invoices/receipts and creates transactions in the Financial base.

Usage: python gmail-to-airtable-transactions.py
"""

import os
import sys
from datetime import datetime

# Add path for airtable_client
sys.path.insert(0, os.path.expanduser('~/Documents/ObsidianVault/WalterSignal/Code/walterfetch-v2'))

from utils.airtable_client import AirtableClient

# Airtable Financial Base
BASE_ID = "apploDdDLnIunmP8i"
TRANSACTIONS_TABLE = "tblCu5JZkW7IM5D0w"
CATEGORIES_TABLE = "tblxQlSma8lA4YpUv"

# Software Subscriptions category ID (already created)
SOFTWARE_CATEGORY_ID = "recWvFhC1pwMyvrcD"

# Transactions parsed from Gmail (2025)
TRANSACTIONS = [
    # Already added:
    # {"date": "2026-01-03", "description": "Anthropic Claude Max 20x subscription", "amount": -200, "vendor": "Anthropic"},
    # {"date": "2025-12-02", "description": "Anthropic Claude Max 5x subscription", "amount": -100, "vendor": "Anthropic"},
    # {"date": "2025-10-18", "description": "Anthropic Claude Max 5x subscription (prorated)", "amount": -82.82, "vendor": "Anthropic"},
    # {"date": "2025-10-14", "description": "Anthropic Claude Pro subscription", "amount": -20, "vendor": "Anthropic"},
    # {"date": "2025-12-29", "description": "X Premium subscription", "amount": -8, "vendor": "X (Twitter)"},
    # {"date": "2025-11-29", "description": "X Premium subscription", "amount": -8, "vendor": "X (Twitter)"},
    # {"date": "2025-10-29", "description": "X Premium subscription", "amount": -8, "vendor": "X (Twitter)"},
    # {"date": "2025-10-24", "description": "Clay Labs Starter Plan", "amount": -149, "vendor": "Clay Labs"},

    # Remaining to add:
    {"date": "2025-10-27", "description": "Railway Hobby Plan", "amount": -5, "vendor": "Railway Corporation", "notes": "Cloud hosting"},
    {"date": "2025-10-24", "description": "xAI API Credits", "amount": -5, "vendor": "xAI", "notes": "AI API usage"},
    {"date": "2025-12-02", "description": "OpenRouter API Credits", "amount": -10.80, "vendor": "OpenRouter", "notes": "Multi-model AI API"},
    {"date": "2025-12-04", "description": "Remix Design - LaunchOS Lifetime", "amount": -5.34, "vendor": "Remix Design", "notes": "One-time purchase"},
    {"date": "2025-10-27", "description": "Obsidian Sync subscription", "amount": -25, "vendor": "Obsidian", "notes": "Note sync service"},
    {"date": "2025-10-23", "description": "Figma subscription", "amount": -15, "vendor": "Figma", "notes": "Design tool"},
    {"date": "2025-05-17", "description": "1Password Family subscription", "amount": -59.88, "vendor": "1Password", "notes": "Annual password manager"},

    # Utilities & Services
    {"date": "2025-12-22", "description": "Indiana Michigan Power", "amount": -150, "vendor": "I&M Power", "notes": "Electric bill", "category": "Utilities"},
    {"date": "2025-11-21", "description": "Indiana Michigan Power", "amount": -145, "vendor": "I&M Power", "notes": "Electric bill", "category": "Utilities"},
    {"date": "2025-12-19", "description": "Frontier Internet", "amount": -85, "vendor": "Frontier", "notes": "Internet service", "category": "Utilities"},
    {"date": "2025-11-10", "description": "Frontier Internet", "amount": -85, "vendor": "Frontier", "notes": "Internet service", "category": "Utilities"},

    # Property & Auto
    {"date": "2025-12-24", "description": "Mazda Financial Services", "amount": -450, "vendor": "Mazda Financial", "notes": "Car payment", "category": "Auto"},
    {"date": "2025-11-21", "description": "Mazda Financial Services", "amount": -450, "vendor": "Mazda Financial", "notes": "Car payment", "category": "Auto"},
    {"date": "2025-11-10", "description": "Allen County Property Tax", "amount": -1500, "vendor": "Allen County Treasurer", "notes": "Property tax payment", "category": "Property"},
    {"date": "2025-05-12", "description": "Allen County Property Tax", "amount": -1500, "vendor": "Allen County Treasurer", "notes": "Property tax payment", "category": "Property"},

    # Services
    {"date": "2025-12-24", "description": "LandArt lawn service", "amount": -75, "vendor": "LandArt Inc", "notes": "Lawn maintenance", "category": "Home Services"},
    {"date": "2025-11-19", "description": "LandArt lawn service", "amount": -75, "vendor": "LandArt Inc", "notes": "Lawn maintenance", "category": "Home Services"},
    {"date": "2025-10-17", "description": "LandArt lawn service", "amount": -75, "vendor": "LandArt Inc", "notes": "Lawn maintenance", "category": "Home Services"},
]


def main():
    print("Gmail to Airtable Transaction Importer")
    print("=" * 50)

    client = AirtableClient(base_id=BASE_ID, table_id=TRANSACTIONS_TABLE)

    # Get existing categories for lookup
    cat_client = AirtableClient(base_id=BASE_ID, table_id=CATEGORIES_TABLE)
    categories = cat_client.fetch_records()
    cat_lookup = {r['fields'].get('Category Name'): r['id'] for r in categories}

    print(f"\nFound {len(cat_lookup)} categories")
    print(f"Processing {len(TRANSACTIONS)} transactions...\n")

    records_to_create = []

    for txn in TRANSACTIONS:
        # Determine category
        cat_name = txn.get('category', 'Software Subscriptions')
        cat_id = cat_lookup.get(cat_name, SOFTWARE_CATEGORY_ID)

        record = {
            "fields": {
                "Date": txn["date"],
                "Description": txn["description"],
                "Amount": txn["amount"],
                "Transaction Type": "Expense",
                "Vendor/Customer": txn["vendor"],
                "Category": [cat_id],
                "Notes": txn.get("notes", ""),
            }
        }
        records_to_create.append(record)
        print(f"  {txn['date']} | ${abs(txn['amount']):>8.2f} | {txn['vendor'][:20]:<20} | {txn['description'][:40]}")

    print(f"\n{'=' * 50}")
    print(f"Creating {len(records_to_create)} records in Airtable...")

    # Batch create (10 at a time)
    created = client.batch_create(records_to_create)

    print(f"\nSuccess! Created {len(created)} transactions.")
    print(f"\nView at: https://airtable.com/{BASE_ID}/{TRANSACTIONS_TABLE}")


if __name__ == "__main__":
    main()
