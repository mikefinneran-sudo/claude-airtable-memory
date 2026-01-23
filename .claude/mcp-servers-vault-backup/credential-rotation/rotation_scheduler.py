#!/usr/bin/env python3
"""
Automated Credential Rotation Scheduler
Runs periodically to check and rotate credentials as needed
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add modules to path
sys.path.append(str(Path(__file__).parent))
from rotation_framework import RotationScheduler, RotationAudit, setup_logging
from modules.cloudflare_rotator import CloudflareRotator


def send_notification(title: str, message: str):
    """Send macOS notification"""
    try:
        import subprocess
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        subprocess.run(['osascript', '-e', script], check=False)
    except:
        pass


def main():
    """Main scheduler execution"""
    base_dir = Path(__file__).parent
    logs_dir = base_dir / "logs"
    config_file = base_dir / "config" / "rotation_config.json"

    # Setup logging
    setup_logging(logs_dir)

    # Initialize scheduler
    audit = RotationAudit(logs_dir / "audit.jsonl")
    scheduler = RotationScheduler(config_file, logs_dir / "audit.jsonl")

    # Register automated rotators
    # Only Cloudflare supports full automation currently
    cloudflare = CloudflareRotator()
    scheduler.register_rotator(cloudflare)

    print("=" * 60)
    print("Credential Rotation Scheduler")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Check rotation status
    status = scheduler.get_rotation_status()

    print("Rotation Status:")
    print("-" * 60)
    for service, info in status.items():
        print(f"\n{service}:")
        print(f"  Last Rotation: {info['last_rotation']}")
        print(f"  Needs Rotation: {info['needs_rotation']}")
        print(f"  Policy: Every {info['rotation_policy_days']} days")

    # Perform rotations if needed
    print("\n" + "=" * 60)
    print("Checking for rotations...")
    print("=" * 60)

    results = scheduler.check_and_rotate(force=False)

    if results:
        print("\nRotation Results:")
        print("-" * 60)
        success_count = 0
        failed_count = 0

        for service, success in results.items():
            status_emoji = "✅" if success else "❌"
            print(f"{status_emoji} {service}: {'Success' if success else 'Failed'}")

            if success:
                success_count += 1
            else:
                failed_count += 1

        # Send summary notification
        if success_count > 0:
            send_notification(
                "Credential Rotation",
                f"Rotated {success_count} credential(s)"
            )

        if failed_count > 0:
            send_notification(
                "Credential Rotation Failed",
                f"{failed_count} rotation(s) failed - check logs"
            )
    else:
        print("\n✅ No rotations needed at this time")

    # Check for services that need manual rotation
    manual_services = [
        "Perplexity Pro",
        "Gamma API",
        "Airtable",
        "Google OAuth - MCP",
        "Google OAuth - Parser",
        "TMDB API"
    ]

    print("\n" + "=" * 60)
    print("Manual Rotation Needed:")
    print("=" * 60)

    needs_manual = False
    for service in manual_services:
        if audit.needs_rotation(service, 90):  # Default 90 days
            last = audit.get_last_rotation(service)
            last_str = last.strftime('%Y-%m-%d') if last else "Never"
            print(f"⚠️  {service} (last: {last_str})")
            needs_manual = True

    if not needs_manual:
        print("✅ No manual rotations needed")
    else:
        send_notification(
            "Manual Credential Rotation Needed",
            "Some credentials need manual rotation"
        )

    print("\n" + "=" * 60)
    print("Scheduler execution complete")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
        send_notification("Credential Rotation Error", str(e))
        sys.exit(1)
