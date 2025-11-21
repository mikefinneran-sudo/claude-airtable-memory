#!/bin/bash
# TDD Layout: Claude Code | Test Watcher
# Usage: ./iterm-layout-tdd.sh [project-directory]

PROJECT_DIR="${1:-$(pwd)}"
cd "$PROJECT_DIR" || exit 1

# AppleScript to create TDD layout in iTerm2
osascript << EOF
tell application "iTerm"
    create window with default profile
    tell current session of current window
        write text "cd \"$PROJECT_DIR\""
        write text "clear"
        write text "echo '=== TDD Mode: Claude Code (Left) | Tests (Right) ==='"
        write text "echo 'Starting Claude Code...'"
        write text "claude"

        -- Split vertically for test watcher
        tell (split vertically with default profile)
            write text "cd \"$PROJECT_DIR\""
            write text "clear"
            write text "echo '=== Test Watcher ==='"

            -- Try to detect and start appropriate test watcher
            write text "if [ -f package.json ] && grep -q '\"test\"' package.json; then"
            write text "  npm run test:watch 2>/dev/null || npm test -- --watch 2>/dev/null || npm test"
            write text "elif [ -f pytest.ini ] || [ -f setup.py ]; then"
            write text "  pytest-watch 2>/dev/null || pytest --watch 2>/dev/null || pytest"
            write text "elif [ -f Cargo.toml ]; then"
            write text "  cargo watch -x test 2>/dev/null || cargo test"
            write text "else"
            write text "  echo 'No test framework detected. Supported: npm/pytest/cargo'"
            write text "  echo 'Configure your test watcher here.'"
            write text "fi"
        end tell
    end tell
end tell
EOF

echo "TDD layout created for: $PROJECT_DIR"
