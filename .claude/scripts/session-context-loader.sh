#!/bin/bash
# Load working context at session start
# Outputs context as a message for Claude to see

WORKING_CONTEXT="$HOME/.claude/WORKING-CONTEXT.md"

if [ -f "$WORKING_CONTEXT" ]; then
    # Get last updated timestamp
    LAST_UPDATED=$(head -5 "$WORKING_CONTEXT" | grep "Last Updated" | cut -d':' -f2- | xargs)

    # Get current project and status
    PROJECT=$(grep "^\*\*Project\*\*:" "$WORKING_CONTEXT" | head -1 | cut -d':' -f2- | xargs)
    STATUS=$(grep "^\*\*Status\*\*:" "$WORKING_CONTEXT" | head -1 | cut -d':' -f2- | xargs)

    # Get active projects table (if exists)
    ACTIVE=$(grep -A5 "## Active Projects" "$WORKING_CONTEXT" 2>/dev/null | tail -3)

    echo "{\"message\": \"📋 Last session ($LAST_UPDATED): $PROJECT - $STATUS. Say 'show full context' for details.\"}"
else
    echo "{\"message\": \"No WORKING-CONTEXT.md found. Starting fresh session.\"}"
fi
