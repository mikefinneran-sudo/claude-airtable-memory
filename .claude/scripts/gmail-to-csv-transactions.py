#!/usr/bin/env python3
"""
Gmail Transaction Parser - Exports to CSV for Airtable import
Searches Gmail for all payment/receipt emails and creates a CSV.
Now parses HTML emails for better Amazon/order extraction.

Usage: python3 gmail-to-csv-transactions.py
Output: ~/Desktop/transactions-2025.csv
"""

import csv
import re
import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import base64
from html.parser import HTMLParser

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Output file
OUTPUT_FILE = os.path.expanduser('~/Desktop/transactions-2025.csv')

# Search queries for different transaction types
SEARCH_QUERIES = [
    'subject:(receipt OR invoice OR payment OR "order confirmation") after:2025/01/01 before:2026/01/01',
    'from:amazon subject:(shipped OR delivered OR "your order") after:2025/01/01 before:2026/01/01',
    'from:(bladehq OR dlttrading OR smkw OR knifecenter) after:2025/01/01 before:2026/01/01',
    'from:etsy subject:(purchase OR receipt OR shipped) after:2025/01/01 before:2026/01/01',
]

class HTMLTextExtractor(HTMLParser):
    """Extract text from HTML, preserving dollar amounts."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_data = False

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.skip_data = True

    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.skip_data = False

    def handle_data(self, data):
        if not self.skip_data:
            self.text.append(data)

    def get_text(self):
        return ' '.join(self.text)

def html_to_text(html):
    """Convert HTML to plain text."""
    try:
        parser = HTMLTextExtractor()
        parser.feed(html)
        return parser.get_text()
    except:
        # Fallback: strip tags with regex
        return re.sub(r'<[^>]+>', ' ', html)

def get_gmail_service():
    """Authenticate and return Gmail service."""
    creds = None
    token_path = os.path.expanduser('~/.claude/scripts/gmail_token.pickle')
    creds_path = os.path.expanduser('~/Documents/custom-scripts/gmail/credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"ERROR: credentials.json not found at {creds_path}")
                print("Please set up Gmail API credentials first.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def extract_amount(text):
    """Extract dollar amount from text - improved patterns."""
    # Clean up text
    text = re.sub(r'\s+', ' ', text)

    patterns = [
        # Order/Grand total patterns (prioritize these)
        r'(?:Grand\s*)?Total[:\s]*\$?\s*([\d,]+\.\d{2})',
        r'Order\s*Total[:\s]*\$?\s*([\d,]+\.\d{2})',
        r'Amount\s*(?:Charged|Due|Paid)?[:\s]*\$?\s*([\d,]+\.\d{2})',
        # Standard dollar amounts
        r'\$\s*([\d,]+\.\d{2})',
        r'USD\s*([\d,]+\.\d{2})',
        r'Paid[:\s]+\$?\s*([\d,]+\.\d{2})',
        r'charged[:\s]+\$?\s*([\d,]+\.\d{2})',
        # HTML span patterns (Amazon style)
        r'currency-value["\']?>\s*([\d,]+\.\d{2})',
    ]

    amounts = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match.replace(',', ''))
                if 0.01 <= amount <= 50000:  # Reasonable range
                    amounts.append(amount)
            except:
                continue

    if amounts:
        # Return the largest amount (usually the total)
        return max(amounts)
    return None

def extract_amazon_order_total(text, html_text):
    """Special extraction for Amazon orders."""
    # Amazon order totals are often in specific patterns
    patterns = [
        r'Order\s*Total[:\s]*\$?\s*([\d,]+\.\d{2})',
        r'Grand\s*Total[:\s]*\$?\s*([\d,]+\.\d{2})',
        r'Item\s*Subtotal[:\s]*\$?\s*([\d,]+\.\d{2})',
        r'currency-value["\']?[^>]*>\s*([\d,]+\.\d{2})',
    ]

    combined = f"{text} {html_text}"
    amounts = []

    for pattern in patterns:
        matches = re.findall(pattern, combined, re.IGNORECASE)
        for match in matches:
            try:
                amount = float(match.replace(',', ''))
                if 0.01 <= amount <= 10000:
                    amounts.append(amount)
            except:
                continue

    if amounts:
        return max(amounts)
    return None

def parse_date(date_str):
    """Parse email date to YYYY-MM-DD format."""
    try:
        # Handle various date formats
        for fmt in ['%a, %d %b %Y %H:%M:%S %z', '%d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z']:
            try:
                dt = datetime.strptime(date_str.split(' (')[0].strip(), fmt)
                return dt.strftime('%Y-%m-%d')
            except:
                continue
        # Fallback - try to extract date
        match = re.search(r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})', date_str)
        if match:
            day, month, year = match.groups()
            months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                     'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
            return f"{year}-{months[month]}-{day.zfill(2)}"
    except:
        pass
    return None

def get_vendor_from_email(from_addr, subject):
    """Extract vendor name from email address or subject."""
    # Known vendor mappings
    vendor_map = {
        'anthropic': 'Anthropic',
        'stripe.com': 'Stripe',
        'paypal': 'PayPal',
        'apple': 'Apple',
        'amazon': 'Amazon',
        'chase': 'Chase',
        'americanexpress': 'American Express',
        'venmo': 'Venmo',
        'google': 'Google',
        'netflix': 'Netflix',
        'spotify': 'Spotify',
        'uber': 'Uber',
        'lyft': 'Lyft',
        'doordash': 'DoorDash',
        'grubhub': 'Grubhub',
        'instacart': 'Instacart',
        'target': 'Target',
        'walmart': 'Walmart',
        'costco': 'Costco',
        'homedepot': 'Home Depot',
        'lowes': "Lowe's",
        'bestbuy': 'Best Buy',
        'openrouter': 'OpenRouter',
        'railway': 'Railway',
        'vercel': 'Vercel',
        'cloudflare': 'Cloudflare',
        'figma': 'Figma',
        'notion': 'Notion',
        'slack': 'Slack',
        'zoom': 'Zoom',
        'dropbox': 'Dropbox',
        'adobe': 'Adobe',
        'microsoft': 'Microsoft',
        'github': 'GitHub',
        'digitalocean': 'DigitalOcean',
        'aws': 'AWS',
        'heroku': 'Heroku',
        'twilio': 'Twilio',
        'sendgrid': 'SendGrid',
        'mailchimp': 'Mailchimp',
        'airtable': 'Airtable',
        'zapier': 'Zapier',
        'calendly': 'Calendly',
        'canva': 'Canva',
        'squarespace': 'Squarespace',
        'wix': 'Wix',
        'shopify': 'Shopify',
        'etsy': 'Etsy',
        'ebay': 'eBay',
        'frontier': 'Frontier',
        'nipsco': 'NIPSCO',
        'aep': 'I&M Power',
        'indiana michigan': 'I&M Power',
        'progressive': 'Progressive',
        'mazda': 'Mazda Financial',
        'landart': 'LandArt',
        'paddle': 'Paddle',
        'gumroad': 'Gumroad',
        'lemon squeezy': 'Lemon Squeezy',
        'clay': 'Clay Labs',
        'x.com': 'X (Twitter)',
        'obsidian': 'Obsidian',
        '1password': '1Password',
        'bitwarden': 'Bitwarden',
        'nordvpn': 'NordVPN',
        'expressvpn': 'ExpressVPN',
        'openai': 'OpenAI',
        'midjourney': 'Midjourney',
        'cursor': 'Cursor',
        'xai': 'xAI',
        'bladehq': 'BladeHQ',
        'dlttrading': 'DLT Trading',
        'smkw': 'SMKW',
        'smoky mountain': 'SMKW',
        'knifecenter': 'KnifeCenter',
        'nvidia': 'NVIDIA',
        'affirm': 'Affirm',
        'curb': 'Curb',
        'gocurb': 'Curb',
        'nintendo': 'Nintendo',
        'carhartt': 'Carhartt',
        'hexclad': 'HexClad',
        'aliexpress': 'AliExpress',
        'monport': 'Monport Laser',
    }

    from_lower = from_addr.lower()
    subject_lower = subject.lower()

    for key, vendor in vendor_map.items():
        if key in from_lower or key in subject_lower:
            return vendor

    # Try to extract from email address
    match = re.search(r'[\w.-]+@([\w.-]+)', from_addr)
    if match:
        domain = match.group(1).split('.')[0]
        return domain.title()

    return 'Unknown'

def categorize_transaction(vendor, description):
    """Assign category based on vendor/description."""
    vendor_lower = vendor.lower()
    desc_lower = description.lower()

    # Software/SaaS
    if any(x in vendor_lower for x in ['anthropic', 'openai', 'openrouter', 'xai', 'cursor', 'midjourney',
                                        'figma', 'notion', 'slack', 'zoom', 'adobe', 'github', 'vercel',
                                        'railway', 'cloudflare', 'digitalocean', 'heroku', 'airtable',
                                        'zapier', '1password', 'obsidian', 'clay', 'paddle', 'x (twitter)']):
        return 'Software Subscriptions'

    # Utilities
    if any(x in vendor_lower for x in ['frontier', 'nipsco', 'i&m', 'power', 'electric', 'gas', 'water']):
        return 'Utilities'

    # Auto
    if any(x in vendor_lower for x in ['mazda', 'honda', 'toyota', 'ford', 'progressive', 'geico', 'auto']):
        return 'Auto'

    # Food/Dining
    if any(x in vendor_lower for x in ['doordash', 'grubhub', 'ubereats', 'instacart', 'restaurant', 'cafe']):
        return 'Food & Dining'

    # Shopping
    if any(x in vendor_lower for x in ['amazon', 'target', 'walmart', 'costco', 'bestbuy', 'etsy', 'ebay',
                                        'bladehq', 'dlt trading', 'smkw', 'knifecenter', 'hexclad', 'carhartt']):
        return 'Shopping'

    # Home
    if any(x in vendor_lower for x in ['landart', 'home depot', 'lowes', 'menards']):
        return 'Home Services'

    # Entertainment
    if any(x in vendor_lower for x in ['netflix', 'spotify', 'hulu', 'disney', 'hbo', 'apple', 'nintendo']):
        return 'Entertainment'

    # Travel
    if any(x in vendor_lower for x in ['uber', 'lyft', 'airline', 'hotel', 'airbnb', 'curb']):
        return 'Travel'

    # Tech Hardware
    if any(x in vendor_lower for x in ['nvidia', 'monport']):
        return 'Tech Hardware'

    return 'Other'

def get_all_body_parts(payload, bodies=None):
    """Recursively extract all body parts from email payload."""
    if bodies is None:
        bodies = {'plain': '', 'html': ''}

    if 'parts' in payload:
        for part in payload['parts']:
            get_all_body_parts(part, bodies)
    else:
        mime_type = payload.get('mimeType', '')
        body_data = payload.get('body', {}).get('data', '')

        if body_data:
            decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
            if mime_type == 'text/plain':
                bodies['plain'] += decoded
            elif mime_type == 'text/html':
                bodies['html'] += decoded

    return bodies

def get_message_body(service, msg_id):
    """Get the body text of an email (both plain and HTML)."""
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

        # Get headers
        headers = message['payload'].get('headers', [])
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
        from_addr = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')

        # Get all body parts
        bodies = get_all_body_parts(message['payload'])

        # Convert HTML to text if we have it
        html_text = ''
        if bodies['html']:
            html_text = html_to_text(bodies['html'])

        # Also include snippet
        snippet = message.get('snippet', '')

        return {
            'subject': subject,
            'from': from_addr,
            'date': date,
            'body': bodies['plain'],
            'html': bodies['html'],
            'html_text': html_text,
            'snippet': snippet,
            'id': msg_id
        }
    except Exception as e:
        print(f"  Error getting message {msg_id}: {e}")
        return None

def main():
    print("Gmail Transaction Parser (Enhanced)")
    print("=" * 60)

    service = get_gmail_service()
    if not service:
        return

    all_messages = []
    seen_ids = set()

    # Search for messages
    for query in SEARCH_QUERIES:
        print(f"\nSearching: {query[:60]}...")
        try:
            results = service.users().messages().list(userId='me', q=query, maxResults=500).execute()
            messages = results.get('messages', [])

            # Handle pagination
            while 'nextPageToken' in results:
                results = service.users().messages().list(
                    userId='me', q=query, maxResults=500,
                    pageToken=results['nextPageToken']
                ).execute()
                messages.extend(results.get('messages', []))

            for msg in messages:
                if msg['id'] not in seen_ids:
                    all_messages.append(msg)
                    seen_ids.add(msg['id'])

            print(f"  Found {len(messages)} messages")
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nTotal unique messages: {len(all_messages)}")
    print("\nParsing messages...")

    transactions = []

    for i, msg in enumerate(all_messages):
        if i % 50 == 0:
            print(f"  Processing {i}/{len(all_messages)}...")

        data = get_message_body(service, msg['id'])
        if not data:
            continue

        # Parse date
        date = parse_date(data['date'])
        if not date:
            continue

        # Extract vendor
        vendor = get_vendor_from_email(data['from'], data['subject'])

        # Extract amount - try multiple sources
        full_text = f"{data['subject']} {data['snippet']} {data['body']} {data['html_text']}"

        # Special handling for Amazon
        if 'amazon' in vendor.lower():
            amount = extract_amazon_order_total(data['body'], data['html_text'])
        else:
            amount = extract_amount(full_text)

        # Skip if no amount found
        if not amount:
            continue

        # Create description
        description = data['subject'][:100]

        # Categorize
        category = categorize_transaction(vendor, description)

        transactions.append({
            'Date': date,
            'Description': description,
            'Amount': -abs(amount),  # Expenses are negative
            'Transaction Type': 'Expense',
            'Vendor/Customer': vendor,
            'Category': category,
            'Notes': f"Gmail ID: {data['id'][:20]}",
        })

    print(f"\nExtracted {len(transactions)} transactions with amounts")

    # Sort by date
    transactions.sort(key=lambda x: x['Date'], reverse=True)

    # Remove duplicates (same vendor, date, amount)
    seen = set()
    unique_transactions = []
    for t in transactions:
        key = (t['Date'], t['Vendor/Customer'], t['Amount'])
        if key not in seen:
            seen.add(key)
            unique_transactions.append(t)

    print(f"After deduplication: {len(unique_transactions)} transactions")

    # Write CSV
    print(f"\nWriting to {OUTPUT_FILE}...")

    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Date', 'Description', 'Amount', 'Transaction Type', 'Vendor/Customer', 'Category', 'Notes'])
        writer.writeheader()
        writer.writerows(unique_transactions)

    print(f"\nDone! Created {OUTPUT_FILE}")
    print(f"Total transactions: {len(unique_transactions)}")

    # Summary by category
    print("\nSummary by Category:")
    print("-" * 40)
    categories = {}
    for t in unique_transactions:
        cat = t['Category']
        if cat not in categories:
            categories[cat] = {'count': 0, 'total': 0}
        categories[cat]['count'] += 1
        categories[cat]['total'] += abs(t['Amount'])

    for cat, data in sorted(categories.items(), key=lambda x: -x[1]['total']):
        print(f"  {cat:<25} {data['count']:>4} txns  ${data['total']:>10,.2f}")

if __name__ == "__main__":
    main()
