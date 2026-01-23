#!/usr/bin/env python3
"""
Life Hub Setup Wizard
Easy one-click OAuth setup for Gmail and Google Calendar
"""

import os
import sys
import json
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

# Add script directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from google.auth.transport.requests import Request
    import pickle
except ImportError:
    print("⚠️  Google libraries not installed yet.")
    print("Run: pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

from oauth_server import LocalOAuthServer

# Paths
VAULT_PATH = Path.home() / "Documents" / "ObsidianVault"
SCRIPT_PATH = VAULT_PATH / ".scripts"
CONFIG_DIR = Path.home() / ".lifehub"
CONFIG_DIR.mkdir(exist_ok=True)

# OAuth Configuration
# TODO: Replace with your actual OAuth credentials from Google Cloud Console
OAUTH_CONFIG = {
    "installed": {
        "client_id": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "client_secret": "YOUR_CLIENT_SECRET",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["http://localhost"]
    }
}

# Scopes for each service
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def check_oauth_config():
    """Check if OAuth credentials are configured"""
    if OAUTH_CONFIG["installed"]["client_id"].startswith("YOUR_CLIENT_ID"):
        print("❌ OAuth credentials not configured yet.\n")
        print("Please follow setup instructions:")
        print("1. Get OAuth credentials from Google Cloud Console")
        print("2. Update OAUTH_CONFIG in setup_wizard.py")
        print("\nSee: /Users/mikefinneran/Documents/ObsidianVault/Resources/Sync Setup Guide.md")
        return False
    return True


def connect_service(service_name, scopes):
    """
    Connect a service using OAuth 2.0

    Args:
        service_name: Name of the service (e.g., "gmail", "calendar")
        scopes: List of OAuth scopes required

    Returns:
        bool: True if successful, False otherwise
    """

    print(f"\n{'='*60}")
    print(f"🔐 Connecting {service_name.title()} to Life Hub")
    print(f"{'='*60}\n")

    # Check if already connected
    token_file = CONFIG_DIR / f"{service_name}_token.json"
    if token_file.exists():
        print(f"⚠️  {service_name.title()} is already connected.")
        response = input("Do you want to reconnect? (y/N): ").strip().lower()
        if response != 'y':
            print("✅ Keeping existing connection")
            return True
        token_file.unlink()

    try:
        # Start local OAuth server
        print("🚀 Starting local OAuth server...")
        server = LocalOAuthServer()
        port = server.start()
        redirect_uri = f"http://localhost:{port}"

        print(f"✅ Server running on port {port}\n")

        # Create OAuth flow
        oauth_config = OAUTH_CONFIG.copy()
        oauth_config["installed"]["redirect_uris"] = [redirect_uri]

        # Save temp config
        temp_config = CONFIG_DIR / "temp_oauth_config.json"
        with open(temp_config, 'w') as f:
            json.dump(oauth_config, f)

        flow = Flow.from_client_secrets_file(
            str(temp_config),
            scopes=scopes,
            redirect_uri=redirect_uri
        )

        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )

        print("🌐 Opening browser for authentication...")
        print(f"   If the browser doesn't open, visit this URL:\n   {auth_url}\n")

        # Open browser
        webbrowser.open(auth_url)

        # Wait for callback
        print("⏳ Waiting for you to complete authorization in browser...")
        print("   (This usually takes 10-30 seconds)\n")

        try:
            code = server.wait_for_code(timeout=120)
            print("✅ Authorization received!\n")
        except TimeoutError:
            print("❌ Timeout waiting for authorization.")
            print("   Please try again and complete the authorization within 2 minutes.")
            server.stop()
            temp_config.unlink(missing_ok=True)
            return False

        # Exchange code for credentials
        print("🔄 Exchanging authorization code for credentials...")
        flow.fetch_token(code=code)
        creds = flow.credentials

        # Save credentials
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }

        with open(token_file, 'w') as f:
            json.dump(token_data, f, indent=2)

        # Set secure permissions
        os.chmod(token_file, 0o600)

        print(f"✅ {service_name.title()} connected successfully!")
        print(f"   Token saved to: {token_file}\n")

        # Cleanup
        server.stop()
        temp_config.unlink(missing_ok=True)

        # Also save in old pickle format for backward compatibility
        pickle_file = SCRIPT_PATH / f"{service_name}_token.pickle"
        with open(pickle_file, 'wb') as f:
            pickle.dump(creds, f)

        return True

    except Exception as e:
        print(f"\n❌ Error connecting {service_name}: {e}")
        print("\nPlease check:")
        print("1. OAuth credentials are correct")
        print("2. Gmail/Calendar API is enabled in Google Cloud Console")
        print("3. Your email is added as a test user")
        return False


def check_connection(service_name):
    """Check if a service is connected"""
    token_file = CONFIG_DIR / f"{service_name}_token.json"
    return token_file.exists()


def test_connection(service_name):
    """Test if a connection works"""
    from googleapiclient.discovery import build

    token_file = CONFIG_DIR / f"{service_name}_token.json"

    if not token_file.exists():
        print(f"❌ {service_name.title()} is not connected yet")
        return False

    try:
        # Load credentials
        with open(token_file, 'r') as f:
            token_data = json.load(f)

        creds = Credentials(
            token=token_data['token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=token_data['scopes']
        )

        # Refresh if needed
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

            # Save updated token
            token_data['token'] = creds.token
            with open(token_file, 'w') as f:
                json.dump(token_data, f, indent=2)

        # Test API call
        if service_name == 'gmail':
            service = build('gmail', 'v1', credentials=creds)
            service.users().labels().list(userId='me').execute()
        elif service_name == 'calendar':
            service = build('calendar', 'v3', credentials=creds)
            service.calendarList().list().execute()

        print(f"✅ {service_name.title()} connection working!")
        return True

    except Exception as e:
        print(f"❌ {service_name.title()} connection test failed: {e}")
        return False


def show_status():
    """Show connection status for all services"""
    print("\n" + "="*60)
    print("Life Hub - Connection Status")
    print("="*60 + "\n")

    services = [
        ('gmail', 'Gmail'),
        ('calendar', 'Google Calendar')
    ]

    for service_id, service_name in services:
        connected = check_connection(service_id)
        status = "✅ Connected" if connected else "❌ Not connected"
        print(f"{service_name:20} {status}")

    print()


def main():
    """Main setup wizard"""

    if len(sys.argv) < 2:
        print("Life Hub Setup Wizard\n")
        print("Usage:")
        print("  obs-setup gmail         Connect Gmail")
        print("  obs-setup calendar      Connect Google Calendar")
        print("  obs-setup all           Connect all services")
        print("  obs-setup status        Show connection status")
        print("  obs-setup test <service> Test a connection")
        print()
        show_status()
        return

    command = sys.argv[1].lower()

    # Check OAuth config first
    if command not in ['status', 'test'] and not check_oauth_config():
        sys.exit(1)

    if command == 'gmail':
        success = connect_service('gmail', GMAIL_SCOPES)
        if success:
            print("💡 Tip: Run 'obs-sync-email' to sync your inbox now!")

    elif command == 'calendar':
        success = connect_service('calendar', CALENDAR_SCOPES)
        if success:
            print("💡 Tip: Run 'obs-sync-cal' to sync your calendar now!")

    elif command == 'all':
        print("Setting up all services...\n")
        gmail_ok = connect_service('gmail', GMAIL_SCOPES)
        calendar_ok = connect_service('calendar', CALENDAR_SCOPES)

        print("\n" + "="*60)
        print("Setup Complete!")
        print("="*60)
        print(f"Gmail: {'✅' if gmail_ok else '❌'}")
        print(f"Calendar: {'✅' if calendar_ok else '❌'}\n")

        if gmail_ok and calendar_ok:
            print("💡 Try these commands:")
            print("   obs-sync-email    Sync Gmail inbox")
            print("   obs-sync-cal      Sync calendar")
            print("   obs-sync-all      Sync everything")

    elif command == 'status':
        show_status()

    elif command == 'test':
        if len(sys.argv) < 3:
            print("Usage: obs-setup test <service>")
            print("Example: obs-setup test gmail")
            return
        service = sys.argv[2].lower()
        test_connection(service)

    else:
        print(f"Unknown command: {command}")
        print("Run 'obs-setup' without arguments to see usage")


if __name__ == "__main__":
    main()
