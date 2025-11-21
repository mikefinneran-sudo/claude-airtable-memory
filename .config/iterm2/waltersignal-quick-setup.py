#!/usr/bin/env python3
"""
WalterSignal iTerm2 Quick Setup
Uses iTerm2 Python API to configure profile automatically
"""

import iterm2
import sys

async def main(connection):
    app = await iterm2.async_get_app(connection)

    # Get or create WalterSignal profile
    profile = None
    all_profiles = await iterm2.PartialProfile.async_query(connection)

    for p in all_profiles:
        if p.name == "WalterSignal Development":
            profile = p
            print("✓ Found existing WalterSignal profile")
            break

    if profile is None:
        # Create new profile
        profile = await iterm2.Profile.async_create(
            connection,
            "WalterSignal Development"
        )
        print("✓ Created new WalterSignal profile")

    # Configure colors
    await profile.async_set_background_color(
        iterm2.Color(0, 0, 0)  # Black
    )
    await profile.async_set_foreground_color(
        iterm2.Color(255, 255, 255)  # White
    )
    await profile.async_set_cursor_color(
        iterm2.Color(139, 92, 246)  # Purple
    )
    await profile.async_set_selection_color(
        iterm2.Color(139, 92, 246, alpha=77)  # Purple 30% alpha
    )

    # Set badge
    await profile.async_set_badge_text("WS")
    await profile.async_set_badge_color(
        iterm2.Color(139, 92, 246, alpha=128)  # Purple 50% alpha
    )

    # Set working directory
    await profile.async_set_custom_directory(
        "/Users/mikefinneran/.claude/command-center/erp-dashboard"
    )
    await profile.async_set_use_custom_directory(True)

    print("✓ Configured colors and badge")
    print("✓ Set working directory")

    # Add triggers (requires manual setup in UI currently)
    print("")
    print("⚠️  Triggers must be configured manually:")
    print("   1. Go to Preferences → Profiles → Advanced → Triggers")
    print("   2. Click 'Edit' and add:")
    print("")
    print("   Regex: (Error|Failed|error)")
    print("   Action: Highlight Text")
    print("   Parameters: Red background")
    print("")
    print("   Regex: (✓ Compiled|Success)")
    print("   Action: Highlight Text")
    print("   Parameters: Green background")
    print("")
    print("   Regex: ✓ Ready in")
    print("   Action: Post Notification")
    print("   Parameters: 'Dashboard Ready'")
    print("")

    print("✓ WalterSignal profile configured!")
    print("")
    print("Open new window with: Cmd+N → Select 'WalterSignal Development'")

iterm2.run_until_complete(main)
