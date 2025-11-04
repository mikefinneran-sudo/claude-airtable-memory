#!/bin/bash
# Save Session Memory - Auto-run on session exit
# Captures session summary and updates WORKING-CONTEXT
# ENHANCED with validation checks

set -e

SESSION_FILE="$HOME/.claude/SESSION-MEMORY.md"
WORKING_CONTEXT="$HOME/.claude/WORKING-CONTEXT.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Check if session memory exists
if [ ! -f "$SESSION_FILE" ]; then
    echo "No active session memory found"
    exit 0
fi

# VALIDATION: Check file structure
validate_session_file() {
    local errors=0

    if ! grep -q "^**Session Started**:" "$SESSION_FILE"; then
        echo "⚠️  SESSION-MEMORY.md is malformed (missing 'Session Started')"
        errors=$((errors + 1))
    fi

    if ! grep -q "^**Project**:" "$SESSION_FILE"; then
        echo "⚠️  SESSION-MEMORY.md is malformed (missing 'Project')"
        errors=$((errors + 1))
    fi

    # Check file isn't empty or too small
    local line_count=$(wc -l < "$SESSION_FILE")
    if [ "$line_count" -lt 10 ]; then
        echo "⚠️  SESSION-MEMORY.md seems incomplete ($line_count lines, expected 10+)"
        errors=$((errors + 1))
    fi

    # Check for required sections
    if ! grep -q "## Actions Taken" "$SESSION_FILE"; then
        echo "⚠️  SESSION-MEMORY.md missing 'Actions Taken' section"
        errors=$((errors + 1))
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ Validation failed with $errors error(s)"
        echo "Session memory preserved but not saved to project"
        return 1
    fi

    return 0
}

# Run validation
if ! validate_session_file; then
    exit 1
fi

# Extract key session data
SESSION_DATE=$(grep "Session Started" "$SESSION_FILE" | head -1 | cut -d: -f2- | xargs)
PROJECT=$(grep "^**Project**:" "$SESSION_FILE" | head -1 | cut -d: -f2 | xargs)
LOCATION=$(grep "^**Location**:" "$SESSION_FILE" | head -1 | cut -d: -f2- | xargs)

# Create session summary
echo ""
echo "=== Session Completed ==="
echo "Project: $PROJECT"
echo "Time: $SESSION_DATE"
echo ""

# Check if project workspace exists
PROJECT_SLUG=$(echo "$PROJECT" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_SLUG"

if [ -d "$PROJECT_DIR" ]; then
    # Append session summary to project sessions log
    SESSIONS_LOG="$PROJECT_DIR/SESSIONS.md"

    echo "" >> "$SESSIONS_LOG"
    echo "---" >> "$SESSIONS_LOG"
    echo "" >> "$SESSIONS_LOG"
    echo "## Session: $SESSION_DATE" >> "$SESSIONS_LOG"
    echo "" >> "$SESSIONS_LOG"

    # Extract completed actions
    sed -n '/### ✅ Completed/,/### /p' "$SESSION_FILE" | grep -v "^###" >> "$SESSIONS_LOG" || true

    # Extract decisions
    echo "" >> "$SESSIONS_LOG"
    echo "**Decisions Made:**" >> "$SESSIONS_LOG"
    sed -n '/## Decisions Made/,/##/p' "$SESSION_FILE" | grep "^[0-9]" >> "$SESSIONS_LOG" || true

    # Extract files modified
    echo "" >> "$SESSIONS_LOG"
    echo "**Files Modified:**" >> "$SESSIONS_LOG"
    sed -n '/## Files Modified/,/##/p' "$SESSION_FILE" | grep -E "^\*|^-" >> "$SESSIONS_LOG" || true

    echo "" >> "$SESSIONS_LOG"
    echo "*Session auto-saved by save-session-memory.sh*" >> "$SESSIONS_LOG"

    echo "✅ Session summary saved to: $PROJECT_DIR/SESSIONS.md"
else
    echo "⚠️  Project workspace not found: $PROJECT_DIR"
    echo "   Session memory preserved in: $SESSION_FILE"
fi

# Update WORKING-CONTEXT with latest session
if [ -f "$WORKING_CONTEXT" ]; then
    # Update the session log section
    echo "" >> "$WORKING_CONTEXT"
    echo "---" >> "$WORKING_CONTEXT"
    echo "**Session Completed**: $TIMESTAMP" >> "$WORKING_CONTEXT"
    echo "**Project**: $PROJECT" >> "$WORKING_CONTEXT"
    echo "**Location**: $LOCATION" >> "$WORKING_CONTEXT"
    echo "" >> "$WORKING_CONTEXT"
fi

echo "✅ WORKING-CONTEXT updated"

# Archive the session memory
ARCHIVE_DIR="$HOME/.claude/session-archive"
mkdir -p "$ARCHIVE_DIR"
ARCHIVE_FILE="$ARCHIVE_DIR/session-$(date '+%Y%m%d-%H%M%S').md"
cp "$SESSION_FILE" "$ARCHIVE_FILE"

echo "✅ Session archived to: $ARCHIVE_FILE"

# Check for custom scripts created during session
check_for_custom_scripts() {
    echo ""
    echo "🔍 Checking for custom scripts created this session..."

    # Extract files created from session memory
    local scripts_found=0
    while IFS= read -r file; do
        if [[ "$file" == *.sh ]] || [[ "$file" == *.py ]]; then
            if [ -f "$file" ] && [ -x "$file" ]; then
                scripts_found=$((scripts_found + 1))
                echo "  ✓ Found script: $(basename "$file")"

                # Ask user if they want to archive it
                echo -n "    Archive to GitHub utilities repo? (y/N): "
                read -r archive_reply
                if [[ "$archive_reply" =~ ^[Yy]$ ]]; then
                    # Extract description from session memory or use default
                    desc=$(grep -A 3 "$(basename "$file")" "$SESSION_FILE" | grep -v "^#" | head -1 | sed 's/^[^:]*://' | xargs)
                    desc="${desc:-Custom script from $PROJECT}"

                    "$HOME/.claude/scripts/archive-custom-script.sh" "$file" "$PROJECT" "$desc"
                fi
            fi
        fi
    done < <(sed -n '/## Files Modified/,/##/p' "$SESSION_FILE" | grep -E "^\*\*Created|^-" | sed 's/^.*` //' | sed 's/`$//')

    if [ $scripts_found -eq 0 ]; then
        echo "  No executable scripts found in session"
    fi
}

# Only check for scripts if PROJECT_DIR exists (completed project)
if [ -d "$PROJECT_DIR" ]; then
    check_for_custom_scripts
fi

echo ""
echo "To resume this work: Reference $PROJECT_DIR/SESSIONS.md"

# Log activity to Airtable for summaries
if [ -f "$HOME/.claude/scripts/log-activity-to-airtable.sh" ]; then
    if [ -n "$AIRTABLE_TOKEN" ] && [ -n "$AIRTABLE_BASE_ID" ]; then
        "$HOME/.claude/scripts/log-activity-to-airtable.sh"
    fi
fi
