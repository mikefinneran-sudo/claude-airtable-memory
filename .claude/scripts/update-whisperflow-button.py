#!/usr/bin/env python3
"""
Update the round black button (bottom right) to toggle WhisperFlow
"""

import json
import shutil
from pathlib import Path

# Paths
PROFILE_DIR = Path.home() / "Library/Application Support/HotSpot/StreamDock/profiles"
PROFILE_ID = "GIS40GLS-EI01-0F1A-C549-Q5WG5HCO6R33.sdProfile"
PROFILE_PATH = PROFILE_DIR / PROFILE_ID
MANIFEST_PATH = PROFILE_PATH / "manifest.json"
IMAGES_DIR = PROFILE_PATH / "Images"
ICON_SOURCE = Path.home() / ".claude/stream-deck-icons/whisper-record.png"

# Read current manifest
with open(MANIFEST_PATH, 'r') as f:
    manifest = json.load(f)

# Copy icon to Images directory
icon_filename = "whisper_toggle_icon.png"
icon_dest = IMAGES_DIR / icon_filename
shutil.copy2(ICON_SOURCE, icon_dest)
print(f"✓ Copied WhisperFlow icon to: {icon_dest}")

# Bottom right button position (5,2)
button_position = "5,2"

# Create WhisperFlow toggle button
whisperflow_button = {
    "ActionID": manifest["Actions"].get(button_position, {}).get("ActionID", "whisperflow-toggle-001"),
    "Controller": "",
    "Name": "Toggle Wispr Flow",
    "Settings": {
        "Timeout": 0,
        "Argument": "",
        "Path": "/bin/bash",
        "Args": [
            "/Users/mikefinneran/.claude/scripts/toggle-whisperflow.sh"
        ]
    },
    "State": 0,
    "States": [
        {
            "Image": icon_filename
        }
    ],
    "UUID": "com.hotspot.streamdock.system.shellscript"
}

# Update button at position 5,2
manifest["Actions"][button_position] = whisperflow_button

# Backup and write
backup_path = MANIFEST_PATH.with_suffix('.json.backup')
shutil.copy2(MANIFEST_PATH, backup_path)

with open(MANIFEST_PATH, 'w') as f:
    json.dump(manifest, f, indent=4)

print(f"✅ Updated bottom-right button (position {button_position})!")
print("\nButton Details:")
print(f"  Position: {button_position} (bottom right)")
print(f"  Name: Toggle Wispr Flow")
print(f"  Icon: 🎙️ Whisper Record")
print(f"  Script: /Users/mikefinneran/.claude/scripts/toggle-whisperflow.sh")
print(f"  Backup: {backup_path}")
print("\nPress the round black button to toggle WhisperFlow on/off!")
print("Changes may appear immediately or after restarting Stream Controller.")
