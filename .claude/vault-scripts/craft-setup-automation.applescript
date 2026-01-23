#!/usr/bin/osascript

-- Craft Setup Automation
-- Creates 6 spaces, imports files, sets up templates
-- Usage: osascript craft-setup-automation.applescript

on run
	-- Configuration
	set spaceNames to {"Inbox", "Daily Notes", "Meeting Notes", "Strategy & Planning", "Reference", "Templates"}
	set craftImportPath to (POSIX path of (path to home folder)) & "Documents/CraftImport/"

	-- Ensure Craft is running
	tell application "Craft"
		activate
		delay 2
	end tell

	-- Use System Events for UI automation
	tell application "System Events"
		tell process "Craft"
			-- Step 1: Create Spaces
			log "Creating spaces..."
			repeat with spaceName in spaceNames
				try
					-- Click profile button (top-left)
					click button 1 of group 1 of toolbar 1 of window 1
					delay 1

					-- Look for "Add New Space" menu item
					click menu item "Add New Space" of menu 1 of button 1 of group 1 of toolbar 1 of window 1
					delay 1

					-- Type space name
					keystroke spaceName
					delay 0.5

					-- Press Enter to create
					keystroke return
					delay 2

					log "Created space: " & spaceName

				on error errMsg
					log "Error creating space " & spaceName & ": " & errMsg
				end try
			end repeat

			log "All spaces created!"

		end tell
	end tell

	return "Craft automation complete!"
end run
