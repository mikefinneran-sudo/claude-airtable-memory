#!/bin/bash
# Log Session Activity to Airtable
# Captures session work for on-demand summaries

set -e

SESSION_FILE="$HOME/.claude/SESSION-MEMORY.md"
AIRTABLE_TOKEN="${AIRTABLE_TOKEN}"
BASE_ID="${AIRTABLE_BASE_ID:-appActivityTracking}"
TABLE_NAME="Daily Activity Log"

# Check if session file exists
if [ ! -f "$SESSION_FILE" ]; then
    echo "No session memory found"
    exit 0
fi

# Check for Airtable credentials
if [ -z "$AIRTABLE_TOKEN" ]; then
    echo "⚠️  AIRTABLE_TOKEN not set. Set it with:"
    echo "   export AIRTABLE_TOKEN='your_token_here'"
    exit 0
fi

# Extract session data
extract_session_data() {
    local project=$(grep "^**Project**:" "$SESSION_FILE" | head -1 | cut -d: -f2 | xargs)
    local session_date=$(grep "Session Started" "$SESSION_FILE" | head -1 | cut -d: -f2- | xargs)
    local location=$(grep "^**Location**:" "$SESSION_FILE" | head -1 | cut -d: -f2- | xargs)

    # Extract completed actions (count and summary)
    local completed_count=$(sed -n '/### ✅ Completed/,/###/p' "$SESSION_FILE" | grep -c "^- \[x\]" || echo "0")
    local completed_items=$(sed -n '/### ✅ Completed/,/###/p' "$SESSION_FILE" | grep "^- \[x\]" | sed 's/^- \[x\] //' | head -10 | paste -sd "," -)

    # Extract decisions
    local decisions=$(sed -n '/## Decisions Made/,/##/p' "$SESSION_FILE" | grep "^[0-9]" | head -5 | paste -sd "," -)

    # Extract files created/modified
    local files_created=$(sed -n '/### Created/,/###/p' "$SESSION_FILE" | grep -c "^-" || echo "0")
    local files_modified=$(sed -n '/### Modified/,/###/p' "$SESSION_FILE" | grep -c "^-" || echo "0")

    # Extract any blockers
    local blockers=$(sed -n '/## Blockers/,/##/p' "$SESSION_FILE" | grep "^-" | head -3 | paste -sd "," -)

    # Create JSON payload
    cat <<EOF
{
  "fields": {
    "Date": "$(date -u +"%Y-%m-%d")T$(date -u +"%H:%M:%S").000Z",
    "Project": "$project",
    "Session Start": "$session_date",
    "Location": "$location",
    "Completed Tasks": $completed_count,
    "Task Details": "$completed_items",
    "Decisions Made": "$decisions",
    "Files Created": $files_created,
    "Files Modified": $files_modified,
    "Blockers": "$blockers",
    "Session Type": "Development",
    "Status": "Completed"
  }
}
EOF
}

# Send to Airtable
log_to_airtable() {
    local payload=$(extract_session_data)

    response=$(curl -s -X POST "https://api.airtable.com/v0/$BASE_ID/$TABLE_NAME" \
        -H "Authorization: Bearer $AIRTABLE_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "\"id\""; then
        echo "✅ Activity logged to Airtable"
        # Extract record ID for reference
        record_id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        echo "   Record ID: $record_id"
    else
        echo "⚠️  Failed to log to Airtable:"
        echo "$response" | head -3
    fi
}

# Main execution
echo "📊 Logging session activity to Airtable..."
log_to_airtable

# Optional: Clean up old session after logging
# rm "$SESSION_FILE"
