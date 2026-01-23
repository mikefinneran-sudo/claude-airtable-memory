#!/usr/bin/env python3
"""
Gmail OAuth Quick Start
Handles one-time OAuth authorization for Gmail API

Run this ONCE to authorize access, then use fetch-subscription-invoices.py

Setup Time: 15-20 minutes (including Google Cloud Console)
Schedule: Run once, then never again (until token expires in ~7 days of inactivity)
"""

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def setup_oauth():
    """
    One-time OAuth setup for Gmail API
    """
    print("🔐 Gmail OAuth Setup")
    print("=" * 60)

    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(script_dir, 'credentials.json')
    token_path = os.path.join(script_dir, 'token.pickle')

    # Check for credentials file
    if not os.path.exists(creds_path):
        print("\n❌ credentials.json not found!")
        print("\nSetup Required:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create new project (or select existing)")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Download as 'credentials.json'")
        print(f"6. Save to: {creds_path}")
        print("\n📖 Full guide: GMAIL_OAUTH_COMPLETE_GUIDE.md")
        return False

    print(f"✅ Found credentials.json")
    print(f"📁 Token will be saved to: {token_path}\n")

    # Check if token already exists
    if os.path.exists(token_path):
        print("⚠️  Token already exists!")
        response = input("Re-authorize? This will overwrite existing token (y/N): ")
        if response.lower() != 'y':
            print("\n✅ Using existing token")
            return True

    try:
        # Run OAuth flow
        print("\n🌐 Starting OAuth flow...")
        print("Your browser will open automatically.")
        print("If you see 'unverified app' warning, click 'Advanced' → 'Go to [app] (unsafe)'")
        print("\nWaiting for authorization...\n")

        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)

        # Save token
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

        print("\n✅ Authorization successful!")
        print(f"✅ Token saved to: {token_path}")

        # Test the connection
        print("\n🔍 Testing Gmail API connection...")
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()

        print(f"✅ Connected to: {profile.get('emailAddress')}")
        print(f"📧 Total messages: {profile.get('messagesTotal')}")

        print("\n" + "=" * 60)
        print("🎉 OAuth setup complete!")
        print("\n📋 Next Steps:")
        print("1. Token is saved and will auto-refresh")
        print("2. Run: python3 fetch-subscription-invoices.py")
        print("3. Or run: ./run-all-trackers.sh")
        print("\n💡 Token expires after ~7 days of inactivity")
        print("   Just re-run this script if needed")

        return True

    except Exception as e:
        print(f"\n❌ OAuth setup failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check credentials.json is valid")
        print("2. Verify Gmail API is enabled in Cloud Console")
        print("3. Try deleting token.pickle and re-running")
        print("4. See GMAIL_OAUTH_COMPLETE_GUIDE.md for full instructions")
        return False

def main():
    success = setup_oauth()

    if success:
        print("\n✅ Ready to fetch invoices!")
        print("\nRun: python3 fetch-subscription-invoices.py")
    else:
        print("\n❌ Setup incomplete")
        print("Follow instructions above and try again")

if __name__ == '__main__':
    main()
