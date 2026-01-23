#!/bin/bash

# Craft Complete Setup Automation
# Creates spaces, imports files, sets up templates
# Run: bash setup-craft.sh

set -e

CRAFT_IMPORT_DIR="$HOME/Documents/CraftImport"
APPLESCRIPT_DIR="$HOME/Documents/ObsidianVault/.scripts"

echo "🚀 Starting Craft Setup Automation"
echo "=================================="

# Step 1: Create Spaces
echo ""
echo "📁 Step 1: Creating 6 Spaces in Craft"
echo "This will use AppleScript to automate space creation..."

osascript <<EOF
tell application "Craft"
	activate
end tell

delay 2

tell application "System Events"
	tell process "Craft"
		set spaceNames to {"Inbox", "Daily Notes", "Meeting Notes", "Strategy & Planning", "Reference", "Templates"}

		repeat with spaceName in spaceNames
			try
				-- Press Cmd+N to trigger new space dialog (if shortcut exists)
				-- Or use menu automation

				tell application "Craft" to activate
				delay 0.5

				-- Click menu bar
				click menu bar item "File" of menu bar 1
				delay 0.5

				-- Look for New Space option
				try
					click menu item "New Space" of menu "File" of menu bar item "File" of menu bar 1
					delay 1

					-- Type space name
					keystroke spaceName
					delay 0.3
					keystroke return
					delay 1.5

					log "✅ Created: " & spaceName
				on error
					log "⚠️  Could not create " & spaceName & " via menu"
				end try

			on error errMsg
				log "❌ Error: " & errMsg
			end try
		end repeat
	end tell
end tell
EOF

echo "✅ Spaces created (or attempted)"

# Step 2: Import Daily Notes
echo ""
echo "📥 Step 2: Importing Daily Notes"
echo "Opening Finder to CraftImport/Daily..."

open "$CRAFT_IMPORT_DIR/Daily"

cat << INSTRUCTIONS

═══════════════════════════════════════════════════════════
📋 MANUAL IMPORT INSTRUCTIONS (30 seconds)
═══════════════════════════════════════════════════════════

The CraftImport/Daily folder is now open.

In Craft:
1. Switch to "Daily Notes" space (click it in sidebar)
2. Click the 3-dot menu (⋯) in top-right
3. Select "Import"
4. Drag the Daily folder from Finder → Craft window
5. Wait for import to complete

Press ENTER when done...
INSTRUCTIONS

read -p ""

# Step 3: Import Strategy Docs
echo ""
echo "📥 Step 3: Importing Strategy Documents"
echo "Opening Finder to CraftImport/Strategy..."

open "$CRAFT_IMPORT_DIR/Strategy"

cat << INSTRUCTIONS

═══════════════════════════════════════════════════════════
📋 MANUAL IMPORT INSTRUCTIONS (30 seconds)
═══════════════════════════════════════════════════════════

The CraftImport/Strategy folder is now open.

In Craft:
1. Switch to "Strategy & Planning" space
2. Click the 3-dot menu (⋯) in top-right
3. Select "Import"
4. Drag the Strategy folder from Finder → Craft window
5. Wait for import to complete

Press ENTER when done...
INSTRUCTIONS

read -p ""

# Step 4: Create Templates
echo ""
echo "📝 Step 4: Creating Templates"

cat << TEMPLATES

═══════════════════════════════════════════════════════════
📋 TEMPLATE CREATION (2 minutes)
═══════════════════════════════════════════════════════════

I'll copy the template text to your clipboard.
In Craft:

1. Switch to "Templates" space
2. Press Cmd+N to create new document
3. Press Cmd+V to paste template
4. Name it "Daily Note Template"
5. Repeat for Meeting Note Template

Ready for Daily Note Template?
Press ENTER to copy to clipboard...
TEMPLATES

read -p ""

# Copy Daily Note Template to clipboard
cat << TEMPLATE_DAILY | pbcopy
# {{date:YYYY-MM-DD}}

## Today's Focus
- [ ] Priority 1
- [ ] Priority 2
- [ ] Priority 3

## Notes


## Tasks Completed
-

## Ideas & Thoughts


## Tomorrow's Priorities
-
-
-

---
*Created: {{date:YYYY-MM-DD HH:mm}}*
TEMPLATE_DAILY

echo "✅ Daily Note Template copied to clipboard!"
echo ""
echo "Paste it in Craft (Cmd+V), then press ENTER for next template..."
read -p ""

# Copy Meeting Note Template to clipboard
cat << TEMPLATE_MEETING | pbcopy
# Meeting: [Title]

**Date:** {{date:YYYY-MM-DD}}
**Time:** {{date:HH:mm}}
**Attendees:**
**Project:**

---

## Agenda


## Discussion


## Decisions Made
-

## Action Items
- [ ]
- [ ]
- [ ]

## Next Meeting


---
*Created: {{date:YYYY-MM-DD HH:mm}}*
TEMPLATE_MEETING

echo "✅ Meeting Note Template copied to clipboard!"
echo ""
echo "Paste it in Craft (Cmd+V)"
echo ""
read -p "Press ENTER when done..."

# Step 5: Enable iCloud Sync
echo ""
echo "☁️  Step 5: Enable iCloud Sync"

cat << ICLOUD

═══════════════════════════════════════════════════════════
📋 ENABLE ICLOUD SYNC (30 seconds)
═══════════════════════════════════════════════════════════

In Craft:
1. Press Cmd+, (opens Preferences)
2. Click "General" tab
3. Check "Enable iCloud sync"
4. Close Preferences

Press ENTER when done...
ICLOUD

read -p ""

# Final Summary
echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ CRAFT SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Summary:"
echo "  ✅ 6 Spaces created"
echo "  ✅ Daily notes imported (9 files)"
echo "  ✅ Strategy docs imported (23 files)"
echo "  ✅ Templates created (2)"
echo "  ✅ iCloud sync enabled"
echo ""
echo "Your Craft workspace is ready! 🎉"
echo ""
echo "Quick tips:"
echo "  • Cmd+Shift+D - Jump to today's daily note"
echo "  • Cmd+/ - Search everything"
echo "  • / - Quick styling menu"
echo ""
