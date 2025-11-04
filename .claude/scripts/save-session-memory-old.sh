#!/bin/bash
# Save Session Memory - Auto-run on session exit
# Captures session summary and updates WORKING-CONTEXT

set -e

SESSION_FILE="$HOME/.claude/SESSION-MEMORY.md"
WORKING_CONTEXT="$HOME/.claude/WORKING-CONTEXT.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Check if session memory exists
if [ ! -f "$SESSION_FILE" ]; then
    echo "No active session memory found"
    exit 0
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

# Optionally archive the session memory
ARCHIVE_DIR="$HOME/.claude/session-archive"
mkdir -p "$ARCHIVE_DIR"
cp "$SESSION_FILE" "$ARCHIVE_DIR/session-$(date '+%Y%m%d-%H%M%S').md"

echo "✅ Session archived"
echo ""
echo "To resume this work: Reference $PROJECT_DIR/SESSIONS.md"
