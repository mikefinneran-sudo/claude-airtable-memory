tell application "iTerm"
    activate
    create window with default profile
    tell current session of current window
        split horizontally with default profile
        write text "# Tests will run here"
    end tell
    tell first session of current window
        write text "# Claude Code here"
    end tell
end tell
