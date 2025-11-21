tell application "iTerm"
    activate
    create window with default profile
    tell current session of current window
        split horizontally with default profile
        split vertically with default profile
    end tell
    tell first session of current window
        write text "# Claude Code here"
    end tell
    tell second session of current window
        write text "# Dev Server here"
    end tell
    tell third session of current window
        write text "# Tests here"
    end tell
end tell
