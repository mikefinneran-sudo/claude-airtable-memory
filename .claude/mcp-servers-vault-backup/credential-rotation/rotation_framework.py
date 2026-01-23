#!/usr/bin/env python3
"""
Automated Credential Rotation Framework
Handles automatic rotation of API keys and credentials with 1Password integration
"""

import json
import subprocess
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
import hashlib


class RotationAudit:
    """Manages rotation audit log"""

    def __init__(self, audit_file: Path):
        self.audit_file = audit_file
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)

    def log_rotation(self, service: str, status: str, details: str = ""):
        """Log a rotation attempt"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "status": status,
            "details": details
        }

        # Append to audit log
        with open(self.audit_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def get_last_rotation(self, service: str) -> Optional[datetime]:
        """Get last successful rotation timestamp for a service"""
        if not self.audit_file.exists():
            return None

        last_rotation = None
        with open(self.audit_file, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry['service'] == service and entry['status'] == 'success':
                        last_rotation = datetime.fromisoformat(entry['timestamp'])
                except:
                    continue

        return last_rotation

    def needs_rotation(self, service: str, rotation_days: int) -> bool:
        """Check if a service needs rotation based on policy"""
        last = self.get_last_rotation(service)
        if last is None:
            return True

        return datetime.now() - last > timedelta(days=rotation_days)


class OnePasswordManager:
    """Handles 1Password CLI operations"""

    @staticmethod
    def read(reference: str) -> str:
        """Read a value from 1Password"""
        result = subprocess.run(
            ['op', 'read', reference],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    @staticmethod
    def update(item_name: str, field: str, value: str, vault: str = "API_Keys") -> bool:
        """Update a field in 1Password"""
        try:
            subprocess.run(
                ['op', 'item', 'edit', item_name, f'{field}={value}', '--vault', vault],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def get_item(item_name: str, vault: str = "API_Keys") -> Dict:
        """Get full item details from 1Password"""
        result = subprocess.run(
            ['op', 'item', 'get', item_name, '--vault', vault, '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)


class CredentialRotator(ABC):
    """Base class for service-specific credential rotators"""

    def __init__(self, service_name: str, op_item: str, rotation_days: int = 90):
        self.service_name = service_name
        self.op_item = op_item
        self.rotation_days = rotation_days
        self.op = OnePasswordManager()
        self.logger = logging.getLogger(f'rotation.{service_name}')

    @abstractmethod
    def generate_new_credential(self) -> Tuple[bool, str, str]:
        """
        Generate new credential via API
        Returns: (success, new_credential, message)
        """
        pass

    @abstractmethod
    def revoke_old_credential(self, old_credential: str) -> Tuple[bool, str]:
        """
        Revoke old credential via API
        Returns: (success, message)
        """
        pass

    def rotate(self, audit: RotationAudit) -> bool:
        """Execute full rotation process"""
        try:
            self.logger.info(f"Starting rotation for {self.service_name}")

            # Step 1: Get current credential
            current_credential = self.op.read(f'op://API_Keys/{self.op_item}/credential')

            # Step 2: Generate new credential
            success, new_credential, message = self.generate_new_credential()
            if not success:
                audit.log_rotation(self.service_name, 'failed', f'Generation failed: {message}')
                self.logger.error(f"Failed to generate new credential: {message}")
                return False

            # Step 3: Update 1Password
            if not self.op.update(self.op_item, 'credential', new_credential):
                audit.log_rotation(self.service_name, 'failed', 'Failed to update 1Password')
                self.logger.error("Failed to update 1Password")
                return False

            # Step 4: Test new credential
            if not self.test_credential(new_credential):
                # Rollback
                self.op.update(self.op_item, 'credential', current_credential)
                audit.log_rotation(self.service_name, 'failed', 'New credential test failed, rolled back')
                self.logger.error("New credential test failed, rolled back")
                return False

            # Step 5: Revoke old credential
            revoke_success, revoke_message = self.revoke_old_credential(current_credential)
            if not revoke_success:
                self.logger.warning(f"Failed to revoke old credential: {revoke_message}")
                # Don't fail rotation if revocation fails

            audit.log_rotation(self.service_name, 'success', f'Rotated successfully')
            self.logger.info("Rotation completed successfully")
            return True

        except Exception as e:
            audit.log_rotation(self.service_name, 'failed', str(e))
            self.logger.exception("Rotation failed with exception")
            return False

    def test_credential(self, credential: str) -> bool:
        """
        Test if credential works (override in subclasses)
        Default: always return True
        """
        return True


class RotationScheduler:
    """Manages rotation schedule and execution"""

    def __init__(self, config_file: Path, audit_file: Path):
        self.config_file = config_file
        self.audit = RotationAudit(audit_file)
        self.rotators: List[CredentialRotator] = []
        self.logger = logging.getLogger('rotation.scheduler')

    def register_rotator(self, rotator: CredentialRotator):
        """Register a credential rotator"""
        self.rotators.append(rotator)

    def check_and_rotate(self, force: bool = False) -> Dict[str, bool]:
        """Check all services and rotate if needed"""
        results = {}

        for rotator in self.rotators:
            needs_rotation = force or self.audit.needs_rotation(
                rotator.service_name,
                rotator.rotation_days
            )

            if needs_rotation:
                self.logger.info(f"Rotating {rotator.service_name}")
                results[rotator.service_name] = rotator.rotate(self.audit)
            else:
                last = self.audit.get_last_rotation(rotator.service_name)
                days_since = (datetime.now() - last).days if last else None
                self.logger.info(
                    f"Skipping {rotator.service_name} (last rotation: {days_since} days ago)"
                )

        return results

    def get_rotation_status(self) -> Dict[str, Dict]:
        """Get rotation status for all services"""
        status = {}

        for rotator in self.rotators:
            last = self.audit.get_last_rotation(rotator.service_name)
            needs = self.audit.needs_rotation(rotator.service_name, rotator.rotation_days)

            status[rotator.service_name] = {
                'last_rotation': last.isoformat() if last else 'never',
                'needs_rotation': needs,
                'rotation_policy_days': rotator.rotation_days,
                'days_until_rotation': rotator.rotation_days - (datetime.now() - last).days if last else 0
            }

        return status


def setup_logging(log_dir: Path):
    """Setup logging configuration"""
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'rotation.log'),
            logging.StreamHandler()
        ]
    )
