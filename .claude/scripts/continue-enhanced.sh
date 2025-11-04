#!/bin/bash
# Enhanced Continue Function - Smart project continuation with context preview

# Check/create 1Password session (24-hour authorization)
if [ -f "$HOME/.claude/scripts/check-1password-session.sh" ]; then
    source "$HOME/.claude/scripts/check-1password-session.sh"
fi

continue_project() {
    local project="${1:-waltersignal}"
    local project_dir="$HOME/.claude/projects/$project"

    if [ ! -d "$project_dir" ]; then
        echo "❌ Project not found: $project"
        echo ""
        echo "Available projects:"
        ls -1 "$HOME/.claude/projects/" | grep -v "^-" | grep -v "^\." | sed 's/^/  - /'
        return 1
    fi

    clear
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  📂 Loading $project context...                               "
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Show project README summary
    if [ -f "$project_dir/README.md" ]; then
        echo "📋 Project Overview:"
        head -10 "$project_dir/README.md" | grep -v "^#" | sed 's/^/   /'
        echo ""
    fi

    # Show recent activity
    if [ -f "$project_dir/SESSIONS.md" ]; then
        echo "🕒 Last session:"
        tail -30 "$project_dir/SESSIONS.md" | head -20 | sed 's/^/   /'
        echo ""
    fi

    # Show current blockers
    if [ -f "$project_dir/STATUS.md" ]; then
        echo "⚠️  Current blockers:"
        sed -n '/## Current Blockers/,/^##/p' "$project_dir/STATUS.md" | grep -v "^##" | grep -v "^---" | grep -v "^$" | sed 's/^/   /'
        echo ""
    fi

    # Show next tasks
    if [ -f "$project_dir/BACKLOG.md" ]; then
        echo "✅ Next tasks:"
        grep "^- \[ \]" "$project_dir/BACKLOG.md" | head -5 | sed 's/^/   /'
        echo ""
    fi

    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  Ready to work on $project                                     "
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""

    # Start new session
    "$HOME/.claude/scripts/start-session.sh" "$project"
}

# Export function for use in shell
if [ -n "$BASH_VERSION" ]; then
    export -f continue_project
fi

# If called directly, execute
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    continue_project "$@"
fi
