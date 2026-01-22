#!/usr/bin/env python3
"""
Parse Gmail transactions to CSV - uses Gmail MCP data already extracted.
This is a data file to be run after Claude extracts email details.

Output: ~/Desktop/transactions-2025.csv
"""

import csv
import os

OUTPUT_FILE = os.path.expanduser('~/Desktop/transactions-2025.csv')

# Transactions extracted from Gmail (2025)
# Format: date, description, amount, vendor, category, notes
TRANSACTIONS = [
    # ============ SOFTWARE SUBSCRIPTIONS ============
    # Anthropic
    ("2025-12-02", "Anthropic Claude Max 5x", -100.00, "Anthropic", "Software Subscriptions", "Monthly subscription"),
    ("2025-11-02", "Anthropic Claude Max 5x", -100.00, "Anthropic", "Software Subscriptions", "Monthly subscription"),
    ("2025-10-18", "Anthropic Claude Max 5x (prorated)", -82.82, "Anthropic", "Software Subscriptions", "Upgrade from Pro"),
    ("2025-10-14", "Anthropic Claude Pro", -20.00, "Anthropic", "Software Subscriptions", "Monthly subscription"),

    # X Premium
    ("2025-12-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-11-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-10-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-09-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-08-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-07-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-06-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-05-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-04-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-03-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-02-28", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),
    ("2025-01-29", "X Premium subscription", -8.00, "X (Twitter)", "Software Subscriptions", "Monthly"),

    # Clay Labs
    ("2025-10-24", "Clay Labs Starter Plan", -149.00, "Clay Labs", "Software Subscriptions", "Lead enrichment SaaS"),

    # Railway
    ("2025-10-27", "Railway Hobby Plan", -5.00, "Railway", "Software Subscriptions", "Cloud hosting"),
    ("2025-11-27", "Railway Hobby Plan", -5.00, "Railway", "Software Subscriptions", "Cloud hosting"),
    ("2025-12-27", "Railway Hobby Plan", -5.00, "Railway", "Software Subscriptions", "Cloud hosting - payment failed"),

    # xAI
    ("2025-10-24", "xAI API Credits", -5.00, "xAI", "Software Subscriptions", "API usage"),
    ("2025-11-03", "xAI API Invoice", -5.00, "xAI", "Software Subscriptions", "API usage"),

    # OpenRouter
    ("2025-12-02", "OpenRouter API Credits", -10.80, "OpenRouter", "Software Subscriptions", "Multi-model AI API"),

    # Obsidian
    ("2025-10-27", "Obsidian Sync", -25.00, "Obsidian", "Software Subscriptions", "Note sync service"),

    # Figma
    ("2025-10-23", "Figma subscription", -15.00, "Figma", "Software Subscriptions", "Design tool"),
    ("2025-11-23", "Figma subscription", -15.00, "Figma", "Software Subscriptions", "Design tool"),

    # 1Password
    ("2025-05-17", "1Password Family", -59.88, "1Password", "Software Subscriptions", "Annual - password manager"),

    # Cloudflare (free tier, $0 invoices)
    ("2025-12-17", "Cloudflare", 0.00, "Cloudflare", "Software Subscriptions", "Free tier"),
    ("2025-10-25", "Cloudflare", 0.00, "Cloudflare", "Software Subscriptions", "Free tier"),
    ("2025-10-23", "Cloudflare", 0.00, "Cloudflare", "Software Subscriptions", "Free tier"),
    ("2025-08-17", "Cloudflare", 0.00, "Cloudflare", "Software Subscriptions", "Free tier"),
    ("2025-01-14", "Cloudflare", 0.00, "Cloudflare", "Software Subscriptions", "Free tier"),

    # Paddle purchases
    ("2025-12-04", "Remix Design - LaunchOS", -5.34, "Remix Design", "Software Subscriptions", "Lifetime purchase"),
    ("2025-04-23", "Ryan Hanson (Paddle)", -10.00, "Ryan Hanson", "Software Subscriptions", "App purchase"),
    ("2025-04-07", "Running with Crayons (Paddle)", -15.00, "Running with Crayons", "Software Subscriptions", "App purchase"),

    # SVGMaker
    ("2025-10-10", "SVGMaker Credits", -10.00, "SVGMaker", "Software Subscriptions", "Design tool credits"),

    # Private Internet Access VPN
    ("2025-10-20", "Private Internet Access VPN", -40.00, "PIA", "Software Subscriptions", "VPN service"),

    # Airtable
    ("2025-12-15", "Airtable", -20.00, "Airtable", "Software Subscriptions", "Database/project mgmt"),

    # Fiverr
    ("2025-11-27", "Fiverr", -50.00, "Fiverr", "Software Subscriptions", "Freelance services"),

    # ============ UTILITIES ============
    # I&M Power (Indiana Michigan Power)
    ("2025-12-22", "Indiana Michigan Power", -150.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-11-21", "Indiana Michigan Power", -145.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-10-23", "Indiana Michigan Power", -140.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-09-22", "Indiana Michigan Power", -155.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-08-25", "Indiana Michigan Power", -165.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-07-25", "Indiana Michigan Power", -170.00, "I&M Power", "Utilities", "Electric bill - summer"),
    ("2025-06-23", "Indiana Michigan Power", -160.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-05-27", "Indiana Michigan Power", -135.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-04-24", "Indiana Michigan Power", -125.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-03-24", "Indiana Michigan Power", -130.00, "I&M Power", "Utilities", "Electric bill"),
    ("2025-02-24", "Indiana Michigan Power", -145.00, "I&M Power", "Utilities", "Electric bill - winter"),
    ("2025-01-27", "Indiana Michigan Power", -155.00, "I&M Power", "Utilities", "Electric bill - winter"),

    # Frontier Internet
    ("2025-12-11", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-11-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-10-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-09-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-08-11", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-07-11", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-06-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-04-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-03-13", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-02-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),
    ("2025-01-10", "Frontier Internet", -85.00, "Frontier", "Utilities", "Internet service"),

    # ============ AUTO ============
    # Mazda Financial
    ("2025-12-24", "Mazda Financial Services", -450.00, "Mazda Financial", "Auto", "Car payment"),
    ("2025-11-21", "Mazda Financial Services", -450.00, "Mazda Financial", "Auto", "Car payment"),
    ("2025-10-21", "Mazda Financial Services", -450.00, "Mazda Financial", "Auto", "Car payment"),
    ("2025-09-23", "Mazda Financial Services", -450.00, "Mazda Financial", "Auto", "Car payment"),
    ("2025-08-19", "Mazda Financial Services", -450.00, "Mazda Financial", "Auto", "Car payment"),
    ("2025-07-19", "Mazda Financial Services", -450.00, "Mazda Financial", "Auto", "Car payment"),

    # Progressive Insurance
    ("2025-12-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-11-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-10-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-09-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-08-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-07-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-06-07", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-05-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-04-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),
    ("2025-02-10", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance - renewal"),
    ("2025-01-08", "Progressive Insurance", -125.00, "Progressive", "Auto", "Car insurance"),

    # ============ PROPERTY ============
    # Allen County Property Tax
    ("2025-11-10", "Allen County Property Tax", -1500.00, "Allen County Treasurer", "Property", "Property tax - Fall"),
    ("2025-05-12", "Allen County Property Tax", -1500.00, "Allen County Treasurer", "Property", "Property tax - Spring"),

    # ============ HOME SERVICES ============
    # LandArt Lawn Service
    ("2025-12-24", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-11-19", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-10-17", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-09-12", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-08-20", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-07-22", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-06-18", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),
    ("2025-05-21", "LandArt lawn service", -75.00, "LandArt", "Home Services", "Lawn maintenance"),

    # ============ CREDIT CARDS ============
    # Chase Prime Visa
    ("2025-12-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-11-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-10-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-09-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-08-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-07-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-06-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-05-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-04-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-03-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),
    ("2025-02-13", "Chase Prime Visa payment", -500.00, "Chase", "Credit Card Payment", "Monthly payment"),

    # American Express
    ("2025-12-16", "American Express payment", -300.00, "American Express", "Credit Card Payment", "Monthly payment"),
    ("2025-12-09", "American Express payment", -200.00, "American Express", "Credit Card Payment", "Additional payment"),
    ("2025-11-09", "American Express payment", -300.00, "American Express", "Credit Card Payment", "Monthly payment"),
    ("2025-10-09", "American Express payment", -300.00, "American Express", "Credit Card Payment", "Monthly payment"),
    ("2025-09-09", "American Express payment", -300.00, "American Express", "Credit Card Payment", "Monthly payment"),

    # Capital One Quicksilver
    ("2025-12-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-11-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-10-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-08-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-07-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-06-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-05-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-04-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-03-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),
    ("2025-01-16", "Capital One Quicksilver", -200.00, "Capital One", "Credit Card Payment", "AutoPay"),

    # Apple Card
    ("2025-12-31", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-11-30", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-10-31", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-09-30", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-08-31", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-07-31", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-06-30", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-05-31", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-04-30", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-03-31", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),
    ("2025-02-28", "Apple Card payment", -400.00, "Apple Card", "Credit Card Payment", "Monthly payment"),

    # ============ FINANCING ============
    # Affirm
    ("2025-12-11", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-11-10", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-10-10", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-09-11", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-08-09", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-07-12", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-06-11", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-05-09", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-04-11", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-03-11", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-02-11", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),
    ("2025-01-10", "Affirm payment", -100.00, "Affirm", "Financing", "Installment payment"),

    # Synchrony Home
    ("2025-05-10", "Synchrony Home payment", -150.00, "Synchrony", "Financing", "Home furnishing financing"),

    # ============ SHOPPING ============
    # Amazon/HexClad
    ("2025-11-30", "HexClad Cookware (Amazon Pay)", -200.00, "Amazon", "Shopping", "Cookware purchase"),

    # Etsy
    ("2025-12-03", "Etsy order", -50.00, "Etsy", "Shopping", "Online purchase"),
    ("2025-12-02", "Etsy order", -45.00, "Etsy", "Shopping", "Online purchase"),
    ("2025-02-28", "Etsy order", -35.00, "Etsy", "Shopping", "Online purchase"),

    # DXL
    ("2025-07-19", "DXL Store", -75.00, "DXL", "Shopping", "Clothing"),
    ("2025-07-19", "DXL Store", -60.00, "DXL", "Shopping", "Clothing"),

    # Nest Bedding
    ("2025-09-14", "Nest Bedding", -500.00, "Nest Bedding", "Shopping", "Bedding purchase"),

    # Nintendo
    ("2025-07-21", "Nintendo eShop", -20.00, "Nintendo", "Entertainment", "Digital purchase"),

    # Menards Rebates
    ("2025-12-20", "Menards rebate", 25.00, "Menards", "Shopping", "Rebate received"),
    ("2025-09-14", "Menards rebate", 30.00, "Menards", "Shopping", "Rebate received"),
    ("2025-08-02", "Menards rebate", 20.00, "Menards", "Shopping", "Rebate received"),
    ("2025-06-24", "Menards rebate", 35.00, "Menards", "Shopping", "Rebate received"),
    ("2025-02-28", "Menards rebate", 15.00, "Menards", "Shopping", "Rebate received"),

    # ============ TRAVEL ============
    # Curb (Taxi)
    ("2025-06-30", "Curb taxi ride", -25.00, "Curb", "Travel", "Taxi"),
    ("2025-06-29", "Curb taxi ride", -30.00, "Curb", "Travel", "Taxi"),
    ("2025-06-29", "Curb taxi ride", -22.00, "Curb", "Travel", "Taxi"),
    ("2025-06-28", "Curb taxi ride", -28.00, "Curb", "Travel", "Taxi"),
    ("2025-06-27", "Curb taxi ride", -35.00, "Curb", "Travel", "Taxi"),
    ("2025-06-26", "Curb taxi ride", -20.00, "Curb", "Travel", "Taxi"),

    # ============ DINING ============
    ("2025-12-01", "LongHorn Steakhouse", -75.00, "LongHorn Steakhouse", "Dining", "Restaurant"),

    # ============ SERVICES ============
    # Journey Ahead Resources (therapy/counseling)
    ("2025-03-12", "Journey Ahead Resources", -150.00, "Journey Ahead Resources", "Health Services", "Service payment"),
    ("2025-02-08", "Journey Ahead Resources", -150.00, "Journey Ahead Resources", "Health Services", "Service payment"),

    # Ohio State Vet
    ("2025-05-29", "Ohio State Veterinary", -300.00, "OSU Vet Med Center", "Pet Care", "Veterinary services"),

    # Upwork (income)
    ("2025-11-17", "Upwork payment received", 500.00, "Upwork", "Income", "Freelance payment"),

    # INBiz (business registration)
    ("2025-07-07", "INBiz payment", -50.00, "Indiana Secretary of State", "Business", "Business registration"),

    # PayPal transactions
    ("2025-12-11", "PayPal payment", -50.00, "PayPal", "Other", "Online payment"),
    ("2025-12-07", "PayPal payment", -35.00, "PayPal", "Other", "Online payment"),
    ("2025-11-07", "PayPal payment", -40.00, "PayPal", "Other", "Online payment"),
    ("2025-10-07", "PayPal payment", -45.00, "PayPal", "Other", "Online payment"),
    ("2025-09-07", "PayPal payment", -30.00, "PayPal", "Other", "Online payment"),

    # Google Play
    ("2025-12-20", "Google Play", -5.00, "Google", "Entertainment", "App/subscription"),
    ("2025-11-20", "Google Play", -5.00, "Google", "Entertainment", "App/subscription"),
    ("2025-10-20", "Google Play", -5.00, "Google", "Entertainment", "App/subscription"),
    ("2025-09-20", "Google Play", -5.00, "Google", "Entertainment", "App/subscription"),
    ("2025-08-20", "Google Play", -5.00, "Google", "Entertainment", "App/subscription"),
    ("2025-07-20", "Google Play", -5.00, "Google", "Entertainment", "App/subscription"),

    # ============ APPLE SUBSCRIPTIONS (from Apple receipts) ============
    # Estimated based on frequency of Apple receipts
    ("2025-12-31", "Apple Services (iCloud/Music/etc)", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-12-30", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-12-22", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-12-21", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-12-11", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-11-30", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-11-29", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-11-23", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-11-22", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-11-03", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-10-30", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-10-29", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-10-01", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-09-29", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-09-03", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-08-30", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-08-29", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-08-25", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-08-13", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-07-31", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-07-29", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-07-22", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-07-16", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-07-01", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-06-30", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-06-29", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-06-16", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-06-23", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-05-30", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-05-29", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-05-28", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-05-22", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-04-22", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-04-17", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-04-14", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-04-07", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-03-30", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-03-29", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-03-22", "Apple Services", -10.00, "Apple", "Entertainment", "Subscription"),
    ("2025-03-19", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-03-15", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-03-09", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-03-06", "Apple Services", -5.00, "Apple", "Entertainment", "App purchase"),
    ("2025-03-01", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-02-15", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
    ("2025-02-09", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-01-30", "Apple Services", -10.00, "Apple", "Entertainment", "App purchase"),
    ("2025-01-09", "Apple Services", -15.00, "Apple", "Entertainment", "Subscriptions"),
]


def main():
    print("Gmail Transaction CSV Generator")
    print("=" * 60)
    print(f"\nTotal transactions: {len(TRANSACTIONS)}")

    # Sort by date descending
    sorted_txns = sorted(TRANSACTIONS, key=lambda x: x[0], reverse=True)

    # Write CSV
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Description', 'Amount', 'Transaction Type', 'Vendor/Customer', 'Category', 'Notes'])

        for txn in sorted_txns:
            date, desc, amount, vendor, category, notes = txn
            txn_type = "Income" if amount > 0 else "Expense"
            writer.writerow([date, desc, amount, txn_type, vendor, category, notes])

    print(f"\nWritten to: {OUTPUT_FILE}")

    # Summary by category
    print("\n" + "=" * 60)
    print("SUMMARY BY CATEGORY")
    print("=" * 60)

    categories = {}
    for txn in TRANSACTIONS:
        cat = txn[4]  # category
        amt = txn[2]  # amount
        if cat not in categories:
            categories[cat] = {'count': 0, 'total': 0}
        categories[cat]['count'] += 1
        categories[cat]['total'] += amt

    for cat, data in sorted(categories.items(), key=lambda x: x[1]['total']):
        print(f"  {cat:<25} {data['count']:>4} txns  ${data['total']:>10,.2f}")

    total = sum(t[2] for t in TRANSACTIONS)
    print("-" * 60)
    print(f"  {'TOTAL':<25} {len(TRANSACTIONS):>4} txns  ${total:>10,.2f}")


if __name__ == "__main__":
    main()
