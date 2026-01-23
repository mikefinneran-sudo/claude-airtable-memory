#!/usr/bin/env python3
"""
Subscription Invoice Fetcher
Pulls subscription invoices from Gmail to verify actual tech stack costs
"""

import os
import pickle
import base64
import re
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import email

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Services to search for
SERVICES = [
    'Claude',
    'Anthropic',
    'Perplexity',
    'Cursor',
    'Figma',
    'Gamma',
    'GitHub',
    'Vercel',
    'OpenAI',
    'Google Workspace',
    'Make.com',
    'Zapier',
    'n8n',
    'Airtable',
    'Notion',
    'Canva',
    'Smartproxy',
    'Clay',
]

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_dir, 'gmail_token.pickle')
    creds_path = os.path.join(script_dir, 'gmail_credentials.json')

    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print(f"\n❌ Error: Gmail credentials not found at {creds_path}")
                print("\n📋 To set up Gmail API access:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing")
                print("3. Enable Gmail API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download credentials.json")
                print(f"6. Save as: {creds_path}")
                print("\nThen run this script again.")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def get_message_body(msg):
    """Extract email body from message"""
    try:
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            data = msg['payload']['body'].get('data')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    except Exception as e:
        print(f"Error extracting body: {e}")
    return ""

def extract_cost(body, subject):
    """Extract cost from invoice email"""
    # Common patterns for costs
    patterns = [
        r'\$\s*([\d,]+\.\d{2})',  # $XX.XX
        r'USD\s*([\d,]+\.\d{2})',  # USD XX.XX
        r'Total[:\s]+\$\s*([\d,]+\.\d{2})',  # Total: $XX.XX
        r'Amount[:\s]+\$\s*([\d,]+\.\d{2})',  # Amount: $XX.XX
        r'(\d+\.\d{2})\s*USD',  # XX.XX USD
    ]

    text = subject + " " + body

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Return first match, cleaned
            amount = matches[0].replace(',', '')
            return float(amount)

    return None

def search_invoices(service, query, service_name):
    """Search for invoices from a specific service"""
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=5  # Last 5 invoices
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return []

        invoices = []

        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Get headers
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')

            # Parse date
            try:
                date_obj = email.utils.parsedate_to_datetime(date_str)
                date = date_obj.strftime('%Y-%m-%d')
            except:
                date = 'Unknown'

            # Get body
            body = get_message_body(msg)

            # Extract cost
            cost = extract_cost(body, subject)

            if cost:
                invoices.append({
                    'service': service_name,
                    'date': date,
                    'cost': cost,
                    'subject': subject,
                    'from': from_email
                })

        return invoices

    except Exception as e:
        print(f"Error searching {service_name}: {e}")
        return []

def main():
    print("🔍 Fetching Subscription Invoices from Gmail...\n")

    service = get_gmail_service()
    if not service:
        return

    print("✅ Connected to Gmail\n")

    # Calculate date range (last 60 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    date_query = f"after:{start_date.strftime('%Y/%m/%d')}"

    all_invoices = []

    # Search queries for each service
    queries = {
        'Claude/Anthropic': f'(from:anthropic.com OR from:claude.ai) (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Perplexity': f'from:perplexity.ai (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Cursor': f'from:cursor.sh (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Figma': f'from:figma.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Gamma': f'from:gamma.app (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'GitHub': f'from:github.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Vercel': f'from:vercel.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'OpenAI': f'from:openai.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Make.com': f'from:make.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Zapier': f'from:zapier.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'n8n': f'from:n8n.io (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Airtable': f'from:airtable.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Notion': f'from:notion.so (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Canva': f'from:canva.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
        'Smartproxy': f'from:smartproxy.com (subject:invoice OR subject:receipt OR subject:payment) {date_query}',
    }

    for service_name, query in queries.items():
        print(f"Searching {service_name}...", end=' ')
        invoices = search_invoices(service, query, service_name)

        if invoices:
            print(f"✅ Found {len(invoices)} invoice(s)")
            all_invoices.extend(invoices)
        else:
            print("❌ No invoices")

    print(f"\n📊 Total Invoices Found: {len(all_invoices)}\n")

    if not all_invoices:
        print("No subscription invoices found in the last 60 days.")
        return

    # Sort by date (newest first)
    all_invoices.sort(key=lambda x: x['date'], reverse=True)

    # Generate markdown report
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, '../subscription-invoices.md')

    with open(output_file, 'w') as f:
        f.write("# Subscription Invoices (Last 60 Days)\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Invoices:** {len(all_invoices)}\n\n")

        # Calculate monthly costs
        services_costs = {}
        for invoice in all_invoices:
            service = invoice['service']
            if service not in services_costs:
                services_costs[service] = []
            services_costs[service].append(invoice['cost'])

        f.write("## Monthly Costs Summary\n\n")
        f.write("| Service | Last Invoice | Avg Cost | Status |\n")
        f.write("|---------|--------------|----------|--------|\n")

        total_monthly = 0
        for service, costs in sorted(services_costs.items()):
            last_cost = costs[0]
            avg_cost = sum(costs) / len(costs)
            total_monthly += avg_cost

            f.write(f"| {service} | ${last_cost:.2f} | ${avg_cost:.2f}/mo | Active |\n")

        f.write(f"| **TOTAL** | | **${total_monthly:.2f}/mo** | |\n\n")

        f.write(f"**Estimated Annual Cost:** ${total_monthly * 12:.2f}/year\n\n")

        # Detailed invoice list
        f.write("## Invoice Details\n\n")
        f.write("| Date | Service | Amount | Subject |\n")
        f.write("|------|---------|--------|----------|\n")

        for invoice in all_invoices:
            subject_short = invoice['subject'][:60] + '...' if len(invoice['subject']) > 60 else invoice['subject']
            f.write(f"| {invoice['date']} | {invoice['service']} | ${invoice['cost']:.2f} | {subject_short} |\n")

    print(f"\n✅ Report generated: {output_file}")
    print(f"\n💰 Estimated Monthly Cost: ${total_monthly:.2f}/mo")
    print(f"💰 Estimated Annual Cost: ${total_monthly * 12:.2f}/year")

if __name__ == '__main__':
    main()
