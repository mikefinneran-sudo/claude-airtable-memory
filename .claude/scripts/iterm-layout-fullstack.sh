#!/bin/bash
# Full Stack Layout: Claude Code | Dev Server | Tests
# Usage: ./iterm-layout-fullstack.sh [project-directory]

PROJECT_DIR="${1:-$(pwd)}"
cd "$PROJECT_DIR" || exit 1

# AppleScript to create Full Stack layout in iTerm2
osascript << EOF
tell application "iTerm"
    create window with default profile
    tell current session of current window
        set name to "Claude Code"
        write text "cd \"$PROJECT_DIR\""
        write text "clear"
        write text "echo '=== Full Stack Mode ==='"
        write text "echo 'Claude Code (Left) | Dev Server (Top Right) | Tests (Bottom Right)'"
        write text "claude"

        -- Split vertically for right column
        tell (split vertically with default profile)
            set name to "Dev Server"
            write text "cd \"$PROJECT_DIR\""
            write text "clear"
            write text "echo '=== Development Server ==='"

            -- Try to detect and start dev server
            write text "if [ -f package.json ] && grep -q '\"dev\"' package.json; then"
            write text "  npm run dev"
            write text "elif [ -f manage.py ]; then"
            write text "  python manage.py runserver"
            write text "elif [ -f Cargo.toml ]; then"
            write text "  cargo run"
            write text "else"
            write text "  echo 'No dev server detected. Start your server here.'"
            write text "fi"

            -- Split horizontally for tests
            tell (split horizontally with default profile)
                set name to "Tests"
                write text "cd \"$PROJECT_DIR\""
                write text "clear"
                write text "echo '=== Test Watcher ==='"

                -- Try to detect and start test watcher
                write text "if [ -f package.json ] && grep -q '\"test\"' package.json; then"
                write text "  npm run test:watch 2>/dev/null || npm test -- --watch 2>/dev/null"
                write text "elif [ -f pytest.ini ] || [ -f setup.py ]; then"
                write text "  pytest-watch 2>/dev/null || pytest --watch 2>/dev/null"
                write text "elif [ -f Cargo.toml ]; then"
                write text "  cargo watch -x test 2>/dev/null"
                write text "else"
                write text "  echo 'Configure test watcher here'"
                write text "fi"
            end tell
        end tell
    end tell
end tell
EOF

echo "Full Stack layout created for: $PROJECT_DIR"
