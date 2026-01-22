#!/bin/bash
# Airtable Daily Auth Helper
# Caches token for one day, then requires re-auth from 1Password

CACHE_FILE="/tmp/.airtable_token_$(date +%Y%m%d)"
TOKEN_NAME="AirTable Personal Token"
VAULT="API_Keys"

# Check if today's cache exists
if [[ -f "$CACHE_FILE" ]]; then
    cat "$CACHE_FILE"
    exit 0
fi

# Clean up old cache files
rm -f /tmp/.airtable_token_* 2>/dev/null

# Get token from 1Password
TOKEN=$(op item get "$TOKEN_NAME" --vault "$VAULT" --reveal --fields label=credential 2>/dev/null)

if [[ -z "$TOKEN" || "$TOKEN" == *"error"* ]]; then
    echo "ERROR: Failed to get Airtable token from 1Password" >&2
    echo "Run: op signin" >&2
    exit 1
fi

# Cache for today
echo "$TOKEN" > "$CACHE_FILE"
chmod 600 "$CACHE_FILE"

echo "$TOKEN"
