#!/usr/bin/env python3
"""
Add workspace launch button to Stream Deck programmatically
"""

import json
import shutil
import uuid
from pathlib import Path

# Paths
PROFILE_DIR = Path.home() / "Library/Application Support/HotSpot/StreamDock/profiles"
PROFILE_ID = "GIS40GLS-EI01-0F1A-C549-Q5WG5HCO6R33.sdProfile"
PROFILE_PATH = PROFILE_DIR / PROFILE_ID
MANIFEST_PATH = PROFILE_PATH / "manifest.json"
IMAGES_DIR = PROFILE_PATH / "Images"
ICON_SOURCE = Path.home() / ".claude/stream-deck-icons/launch-workspace.png"

# Read current manifest
with open(MANIFEST_PATH, 'r') as f:
    manifest = json.load(f)

# Copy icon to Images directory
icon_filename = "launch_workspace_icon.png"
icon_dest = IMAGES_DIR / icon_filename
shutil.copy2(ICON_SOURCE, icon_dest)
print(f"✓ Copied icon to: {icon_dest}")

# Find first empty button position (check positions 0,0 through 5,2)
empty_position = None
for row in range(6):
    for col in range(3):
        pos = f"{row},{col}"
        if pos not in manifest["Actions"]:
            empty_position = pos
            break
    if empty_position:
        break

if not empty_position:
    print("❌ No empty button positions available!")
    exit(1)

print(f"✓ Using position: {empty_position}")

# Create new button action for shell script
action_id = str(uuid.uuid4())
new_button = {
    "ActionID": action_id,
    "Controller": "",
    "Name": "Launch Workspace",
    "Settings": {
        "Timeout": 0,
        "Argument": "",
        "Path": "/bin/bash",
        "Args": [
            "/Users/mikefinneran/.claude/scripts/launch-workspace.sh"
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

# Add button to manifest
manifest["Actions"][empty_position] = new_button

# Write back to manifest
with open(MANIFEST_PATH, 'w') as f:
    json.dump(manifest, f, indent=4)

print(f"✅ Added workspace button at position {empty_position}!")
print("\nButton Details:")
print(f"  Position: {empty_position}")
print(f"  Name: Launch Workspace")
print(f"  Icon: {icon_filename}")
print(f"  Script: /Users/mikefinneran/.claude/scripts/launch-workspace.sh")
print("\nRestart Stream Controller to see the changes, or they may appear automatically.")
