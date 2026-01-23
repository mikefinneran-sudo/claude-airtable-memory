-- AppleScript to automate UTM VM creation for macOS
-- This script automates the GUI interaction to create a macOS VM

tell application "System Events"
    tell process "UTM"
        -- Wait for UTM to be ready
        repeat until exists window 1
            delay 0.5
        end repeat

        -- Click the "+" button to create new VM
        click button 1 of window 1
        delay 1

        -- Select "Virtualize" option
        click button "Virtualize" of window 1
        delay 1

        -- Select "macOS 12+" option
        click button "macOS 12+" of window 1
        delay 1

        -- Configure RAM to 8GB (8192 MB)
        -- Configure CPU to 4 cores
        -- Configure storage to 64 GB
        -- These specifics depend on UTM's UI layout

        -- Click "Continue" or "Next" buttons as needed
        -- (UI navigation will depend on UTM version)

    end tell
end tell
