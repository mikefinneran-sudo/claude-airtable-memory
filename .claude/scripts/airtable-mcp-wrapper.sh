#!/bin/bash
# Wrapper for Airtable MCP server with daily auth

export AIRTABLE_API_KEY=$(/Users/mikefinneran/.claude/scripts/airtable-daily-auth.sh)

if [[ -z "$AIRTABLE_API_KEY" || "$AIRTABLE_API_KEY" == ERROR* ]]; then
    echo "Airtable auth failed. Run: op signin" >&2
    exit 1
fi

exec npx -y airtable-mcp-server "$@"
