#!/bin/bash
# Airtable Daily Auth Helper
# Caches token for one day, then requires re-auth from 1Password

CACHE_FILE="/tmp/.airtable_token_$(date +%Y%m%d)"
FALLBACK_CACHE="/tmp/.airtable_token_latest"
TOKEN_NAME="AirTable Personal Token"
VAULT="API_Keys"

# Check if today's cache exists
if [[ -f "$CACHE_FILE" ]]; then
    cat "$CACHE_FILE"
    exit 0
fi

# Try to get token from 1Password (may fail if not authed yet)
TOKEN=$(op item get "$TOKEN_NAME" --vault "$VAULT" --reveal --fields label=credential 2>/dev/null)

if [[ -n "$TOKEN" && "$TOKEN" != *"error"* && "$TOKEN" != *"not signed in"* ]]; then
    # Clean up old cache files
    rm -f /tmp/.airtable_token_2* 2>/dev/null

    # Cache for today
    echo "$TOKEN" > "$CACHE_FILE"
    chmod 600 "$CACHE_FILE"

    # Also save as latest fallback
    echo "$TOKEN" > "$FALLBACK_CACHE"
    chmod 600 "$FALLBACK_CACHE"

    echo "$TOKEN"
    exit 0
fi

# 1Password not available - try fallback cache (yesterday's token usually still works)
if [[ -f "$FALLBACK_CACHE" ]]; then
    cat "$FALLBACK_CACHE"
    exit 0
fi

# No cache and no 1Password - fail
echo "ERROR: No Airtable token available. Run: op-auth" >&2
exit 1
