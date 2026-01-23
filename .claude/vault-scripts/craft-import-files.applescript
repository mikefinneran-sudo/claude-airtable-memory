#!/usr/bin/osascript

-- Import files to Craft via drag-and-drop automation

on run
	set dailyFolder to POSIX file "/Users/mikefinneran/Documents/CraftImport/Daily"
	set strategyFolder to POSIX file "/Users/mikefinneran/Documents/CraftImport/Strategy"

	tell application "Finder"
		-- Get all markdown files from Daily folder
		set dailyFiles to every file of folder dailyFolder whose name extension is "md"

		-- Get all markdown files from Strategy folder
		set strategyFiles to every file of folder strategyFolder whose name extension is "md"
	end tell

	tell application "Craft"
		activate
		delay 1
	end tell

	tell application "System Events"
		tell process "Craft"

			-- Import Daily Notes
			log "Importing daily files..."

			-- Click Daily folder
			keystroke "f" using command down
			delay 0.3
			keystroke "Daily"
			keystroke return
			delay 0.5

			-- For each file, import it
			repeat with theFile in dailyFiles
				try
					-- Open file picker
					keystroke "o" using command down
					delay 0.8

					-- Navigate using Cmd+Shift+G
					keystroke "g" using {command down, shift down}
					delay 0.5

					-- Type full file path
					set filePath to POSIX path of (theFile as alias)
					keystroke filePath
					keystroke return
					delay 0.5

					-- Press Return to open
					keystroke return
					delay 1

					log "Imported: " & (name of theFile)
				on error errMsg
					log "Error importing file: " & errMsg
				end try
			end repeat

			-- Import Strategy Files
			log "Importing strategy files..."

			-- Click Projects folder
			keystroke "f" using command down
			delay 0.3
			keystroke "Projects"
			keystroke return
			delay 0.5

			-- For each file, import it
			repeat with theFile in strategyFiles
				try
					-- Open file picker
					keystroke "o" using command down
					delay 0.8

					-- Navigate using Cmd+Shift+G
					keystroke "g" using {command down, shift down}
					delay 0.5

					-- Type full file path
					set filePath to POSIX path of (theFile as alias)
					keystroke filePath
					keystroke return
					delay 0.5

					-- Press Return to open
					keystroke return
					delay 1

					log "Imported: " & (name of theFile)
				on error errMsg
					log "Error importing file: " & errMsg
				end try
			end repeat

		end tell
	end tell

	return "✅ All files imported"
end run
