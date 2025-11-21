#!/bin/bash
# Remote/tmux Layout: Local Claude | Remote tmux session
# Usage: ./iterm-layout-remote.sh [user@host]

REMOTE_HOST="$1"

if [ -z "$REMOTE_HOST" ]; then
    echo "Usage: $0 user@host"
    echo "Example: $0 ubuntu@192.168.1.100"
    exit 1
fi

# AppleScript to create Remote layout in iTerm2
osascript << EOF
tell application "iTerm"
    create window with default profile
    tell current session of current window
        set name to "Claude Code (Local)"
        write text "clear"
        write text "echo '=== Remote Development Mode ==='"
        write text "echo 'Local Claude Code (Left) | Remote tmux (Right)'"
        write text "claude"

        -- Split vertically for remote session
        tell (split vertically with default profile)
            set name to "Remote: $REMOTE_HOST"
            write text "clear"
            write text "echo '=== Connecting to $REMOTE_HOST ==='"
            write text "echo 'Using tmux integration mode (-CC)'"
            write text "echo 'Your session will survive disconnects!'"
            write text "echo ''"

            -- Connect with tmux integration
            write text "ssh $REMOTE_HOST -t 'tmux -CC new -A -s dev'"
        end tell
    end tell
end tell
EOF

echo "Remote layout created for: $REMOTE_HOST"
echo "tmux integration mode (-CC) keeps your session alive through disconnects"
