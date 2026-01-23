#!/usr/bin/osascript

-- Full Craft Automation - NO MANUAL STEPS
-- Imports all files, creates templates, enables sync

on run
	set craftImportPath to (POSIX path of (path to home folder)) & "Documents/CraftImport/"
	set dailyPath to craftImportPath & "Daily"
	set strategyPath to craftImportPath & "Strategy"

	tell application "Craft"
		activate
		delay 2
	end tell

	tell application "System Events"
		tell process "Craft"

			-- Import Daily Notes
			log "Importing daily notes..."
			try
				-- Switch to Daily Notes space (click in sidebar)
				click static text "Daily Notes" of group 1 of splitter group 1 of window 1
				delay 1

				-- Click 3-dot menu
				click button 3 of toolbar 1 of window 1
				delay 0.5

				-- Click Import
				click menu item "Import" of menu 1 of button 3 of toolbar 1 of window 1
				delay 1

				-- File picker appears - navigate to Daily folder
				keystroke "g" using {command down, shift down}
				delay 0.5
				keystroke dailyPath
				keystroke return
				delay 1

				-- Select all files
				keystroke "a" using command down
				delay 0.5

				-- Click Open
				click button "Open" of sheet 1 of window 1
				delay 3

				log "Daily notes imported"
			on error errMsg
				log "Error importing daily notes: " & errMsg
			end try

			-- Import Strategy Docs
			log "Importing strategy docs..."
			try
				-- Switch to Strategy & Planning space
				click static text "Strategy & Planning" of group 1 of splitter group 1 of window 1
				delay 1

				-- Click 3-dot menu
				click button 3 of toolbar 1 of window 1
				delay 0.5

				-- Click Import
				click menu item "Import" of menu 1 of button 3 of toolbar 1 of window 1
				delay 1

				-- File picker - navigate to Strategy folder
				keystroke "g" using {command down, shift down}
				delay 0.5
				keystroke strategyPath
				keystroke return
				delay 1

				-- Select all files
				keystroke "a" using command down
				delay 0.5

				-- Click Open
				click button "Open" of sheet 1 of window 1
				delay 3

				log "Strategy docs imported"
			on error errMsg
				log "Error importing strategy docs: " & errMsg
			end try

			-- Create Daily Note Template
			log "Creating daily note template..."
			try
				-- Switch to Templates space
				click static text "Templates" of group 1 of splitter group 1 of window 1
				delay 1

				-- Create new doc (Cmd+N)
				keystroke "n" using command down
				delay 1

				-- Type template content
				keystroke "# {{date:YYYY-MM-DD}}"
				keystroke return
				keystroke return
				keystroke "## Today's Focus"
				keystroke return
				keystroke "- [ ] Priority 1"
				keystroke return
				keystroke "- [ ] Priority 2"
				keystroke return
				keystroke "- [ ] Priority 3"
				keystroke return
				keystroke return
				keystroke "## Notes"
				keystroke return
				keystroke return
				keystroke return
				keystroke "## Tasks Completed"
				keystroke return
				keystroke "-"
				keystroke return
				keystroke return
				keystroke "## Ideas & Thoughts"
				keystroke return
				keystroke return
				keystroke return
				keystroke "## Tomorrow's Priorities"
				keystroke return
				keystroke "-"
				keystroke return
				keystroke "-"
				keystroke return
				keystroke "-"

				-- Rename to "Daily Note Template"
				keystroke "r" using command down
				delay 0.5
				keystroke "Daily Note Template"
				keystroke return
				delay 1

				log "Daily template created"
			on error errMsg
				log "Error creating daily template: " & errMsg
			end try

			-- Enable iCloud Sync
			log "Enabling iCloud sync..."
			try
				-- Open preferences (Cmd+,)
				keystroke "," using command down
				delay 1

				-- Click General tab
				click button "General" of toolbar 1 of window 1
				delay 0.5

				-- Check "Enable iCloud sync"
				click checkbox "Enable iCloud sync" of group 1 of window 1
				delay 0.5

				-- Close preferences
				keystroke "w" using command down

				log "iCloud sync enabled"
			on error errMsg
				log "Error enabling iCloud: " & errMsg
			end try

		end tell
	end tell

	return "✅ Craft fully automated setup complete!"
end run
