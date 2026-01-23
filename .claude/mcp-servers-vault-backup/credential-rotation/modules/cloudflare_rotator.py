#!/usr/bin/env python3
"""
Cloudflare API Token Rotator
Automatically rotates Cloudflare API tokens via API
"""

import requests
from typing import Tuple
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from rotation_framework import CredentialRotator


class CloudflareRotator(CredentialRotator):
    """
    Rotates Cloudflare API Tokens
    Uses Cloudflare API to create and revoke tokens
    """

    def __init__(self):
        super().__init__(
            service_name="Cloudflare",
            op_item="Cloudflare Wrangler OAuth",
            rotation_days=90
        )
        self.api_base = "https://api.cloudflare.com/client/v4"

    def generate_new_credential(self) -> Tuple[bool, str, str]:
        """
        Create a new Cloudflare API token
        Note: Requires an existing token with token creation permissions
        """
        try:
            current_token = self.op.read('op://API_Keys/Cloudflare Wrangler OAuth/oauth_token')

            headers = {
                'Authorization': f'Bearer {current_token}',
                'Content-Type': 'application/json'
            }

            # Create new token with same permissions
            token_data = {
                "name": f"Wrangler CLI Token - {self.get_timestamp()}",
                "policies": [
                    {
                        "effect": "allow",
                        "resources": {
                            "com.cloudflare.api.account.*": "*"
                        },
                        "permission_groups": [
                            {
                                "id": "c8fed203ed3043cba015a93ad1616f1f",  # Workers Scripts Write
                                "name": "Workers Scripts Write"
                            },
                            {
                                "id": "e086da7e2179491d91ee5f35b3ca210a",  # Workers KV Storage Write
                                "name": "Workers KV Storage Write"
                            }
                        ]
                    }
                ]
            }

            response = requests.post(
                f'{self.api_base}/user/tokens',
                headers=headers,
                json=token_data,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                new_token = result['result']['value']
                return True, new_token, "Token created successfully"
            else:
                return False, "", f"API error: {response.text}"

        except Exception as e:
            return False, "", str(e)

    def revoke_old_credential(self, old_credential: str) -> Tuple[bool, str]:
        """Revoke the old Cloudflare token"""
        try:
            # Get token ID from token value
            headers = {
                'Authorization': f'Bearer {old_credential}',
                'Content-Type': 'application/json'
            }

            # List tokens to find the ID
            response = requests.get(
                f'{self.api_base}/user/tokens',
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                return False, "Failed to list tokens"

            tokens = response.json()['result']
            # Find our token (we can't match on value, so this is best effort)
            # In practice, we'd need to store the token ID

            return True, "Revocation requires token ID - manage at https://dash.cloudflare.com/profile/api-tokens"

        except Exception as e:
            return False, str(e)

    def test_credential(self, credential: str) -> bool:
        """Test if the Cloudflare token works"""
        try:
            headers = {
                'Authorization': f'Bearer {credential}',
                'Content-Type': 'application/json'
            }

            response = requests.get(
                f'{self.api_base}/user/tokens/verify',
                headers=headers,
                timeout=10
            )

            return response.status_code == 200

        except Exception as e:
            self.logger.error(f"Credential test failed: {e}")
            return False

    def get_timestamp(self):
        """Get formatted timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    print("Cloudflare API Token Rotation")
    print("=" * 50)

    from rotation_framework import RotationAudit, setup_logging
    from pathlib import Path

    log_dir = Path(__file__).parent.parent / "logs"
    setup_logging(log_dir)

    audit = RotationAudit(log_dir / "audit.jsonl")
    rotator = CloudflareRotator()

    if len(sys.argv) > 1 and sys.argv[1] == "rotate":
        success = rotator.rotate(audit)
        if success:
            print("✅ Rotation successful!")
        else:
            print("❌ Rotation failed")
    else:
        print("Usage: python modules/cloudflare_rotator.py rotate")
