#!/usr/bin/env python3
"""
Airtable API Key Rotator
Automatically rotates Airtable personal access tokens
"""

import requests
from typing import Tuple
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from rotation_framework import CredentialRotator


class AirtableRotator(CredentialRotator):
    """
    Rotates Airtable Personal Access Tokens

    Note: Airtable API tokens must be created via the web UI
    This rotator assists with the process but requires manual token creation
    """

    def __init__(self):
        super().__init__(
            service_name="Airtable",
            op_item="Airtable WalterSignal",
            rotation_days=90
        )
        self.base_url = "https://api.airtable.com/v0"

    def generate_new_credential(self) -> Tuple[bool, str, str]:
        """
        Airtable tokens must be created manually via web UI
        This method provides instructions for manual rotation
        """
        instructions = """
        Airtable tokens must be created manually:

        1. Go to: https://airtable.com/create/tokens
        2. Click 'Create new token'
        3. Name: 'WalterSignal API Token - [DATE]'
        4. Scopes:
           - data.records:read
           - data.records:write
           - schema.bases:read
        5. Access: Select your WalterSignal base
        6. Copy the token
        7. Update 1Password manually:
           op item edit 'Airtable WalterSignal' api_key='YOUR_NEW_TOKEN'
        8. Test the token
        9. Revoke the old token: https://airtable.com/account
        """

        return False, "", instructions

    def revoke_old_credential(self, old_credential: str) -> Tuple[bool, str]:
        """
        Airtable tokens must be revoked manually via web UI
        https://airtable.com/account -> API -> Personal access tokens
        """
        return False, "Manual revocation required at https://airtable.com/account"

    def test_credential(self, credential: str) -> bool:
        """Test if the Airtable token works"""
        try:
            base_id = self.op.read('op://API_Keys/Airtable WalterSignal/base_id')

            headers = {
                'Authorization': f'Bearer {credential}',
                'Content-Type': 'application/json'
            }

            # Try to list bases (read-only test)
            response = requests.get(
                f'{self.base_url}/meta/bases',
                headers=headers,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            self.logger.error(f"Credential test failed: {e}")
            return False


if __name__ == "__main__":
    # Manual rotation helper
    print("Airtable API Token Rotation Helper")
    print("=" * 50)

    rotator = AirtableRotator()
    success, _, instructions = rotator.generate_new_credential()
    print(instructions)

    print("\nAfter creating the new token, test it:")
    print("python modules/airtable_rotator.py test <NEW_TOKEN>")

    if len(sys.argv) > 2 and sys.argv[1] == "test":
        token = sys.argv[2]
        if rotator.test_credential(token):
            print("✅ Token works!")
        else:
            print("❌ Token failed testing")
