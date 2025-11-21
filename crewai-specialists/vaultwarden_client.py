#!/usr/bin/env python3
"""
Vaultwarden Client for CrewAI Specialists
Access API credentials stored in Vaultwarden on DGX Spark
"""
import sqlite3
import json
from pathlib import Path

VAULTWARDEN_DB = "~/vaultwarden/data/db.sqlite3"
USER_EMAIL = "mike.finneran@gmail.com"

class VaultwardenClient:
    def __init__(self, db_path=None, ssh_host=None):
        """
        Initialize Vaultwarden client
        
        Args:
            db_path: Path to local Vaultwarden database
            ssh_host: SSH host (e.g., 'mikefinneran@192.168.68.88') for remote access
        """
        self.db_path = db_path or VAULTWARDEN_DB
        self.ssh_host = ssh_host
        
    def get_credential(self, name):
        """
        Get a credential by name
        
        Args:
            name: Name of the credential (e.g., "OpenAI API Key", "Anthropic")
            
        Returns:
            dict with 'username' and 'password' fields
        """
        if self.ssh_host:
            return self._get_credential_ssh(name)
        else:
            return self._get_credential_local(name)
    
    def _get_credential_local(self, name):
        """Get credential from local database"""
        db_path = Path(self.db_path).expanduser()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Find user
        cursor.execute("SELECT uuid FROM users WHERE email = ?", (USER_EMAIL,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"User {USER_EMAIL} not found")
        
        user_uuid = result[0]
        
        # Find cipher by name (case-insensitive partial match)
        cursor.execute("""
            SELECT name, data 
            FROM ciphers 
            WHERE user_uuid = ? AND lower(name) LIKE lower(?)
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_uuid, f"%{name}%"))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise ValueError(f"Credential '{name}' not found")
        
        cipher_name, data = result
        login_data = json.loads(data)
        
        return {
            'name': cipher_name,
            'username': login_data.get('username', ''),
            'password': login_data.get('password', '')
        }
    
    def _get_credential_ssh(self, name):
        """Get credential from remote database via SSH"""
        import subprocess
        
        # Query via SSH
        cmd = f'''ssh {self.ssh_host} "sqlite3 {self.db_path} \\"
            SELECT name, data 
            FROM ciphers 
            WHERE user_uuid = (SELECT uuid FROM users WHERE email = '{USER_EMAIL}')
            AND lower(name) LIKE lower('%{name}%')
            ORDER BY created_at DESC
            LIMIT 1
            \\""'''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise ValueError(f"SSH query failed: {result.stderr}")
        
        lines = result.stdout.strip().split('|')
        if len(lines) < 2:
            raise ValueError(f"Credential '{name}' not found")
        
        cipher_name = lines[0]
        data = json.loads(lines[1])
        
        return {
            'name': cipher_name,
            'username': data.get('username', ''),
            'password': data.get('password', '')
        }
    
    def list_credentials(self):
        """List all available credentials"""
        if self.ssh_host:
            return self._list_credentials_ssh()
        else:
            return self._list_credentials_local()
    
    def _list_credentials_local(self):
        """List credentials from local database"""
        db_path = Path(self.db_path).expanduser()
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name 
            FROM ciphers 
            WHERE user_uuid = (SELECT uuid FROM users WHERE email = ?)
            ORDER BY name
        """, (USER_EMAIL,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [r[0] for r in results]
    
    def _list_credentials_ssh(self):
        """List credentials from remote database via SSH"""
        import subprocess
        
        cmd = f'''ssh {self.ssh_host} "sqlite3 {self.db_path} \\"
            SELECT name 
            FROM ciphers 
            WHERE user_uuid = (SELECT uuid FROM users WHERE email = '{USER_EMAIL}')
            ORDER BY name
            \\""'''
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n')


# Convenience functions
def get_api_key(service_name):
    """
    Quick access to API keys
    
    Usage:
        openai_key = get_api_key("OpenAI")
        anthropic_key = get_api_key("Anthropic")
        perplexity_key = get_api_key("Perplexity")
    """
    client = VaultwardenClient(ssh_host="mikefinneran@192.168.68.88")
    cred = client.get_credential(service_name)
    return cred['password']


if __name__ == "__main__":
    # Example usage
    client = VaultwardenClient(ssh_host="mikefinneran@192.168.68.88")
    
    print("Available credentials:")
    for name in client.list_credentials():
        print(f"  - {name}")
    
    print("\nTesting credential retrieval:")
    cred = client.get_credential("OpenAI")
    print(f"  OpenAI API Key: {cred['password'][:20]}...")
