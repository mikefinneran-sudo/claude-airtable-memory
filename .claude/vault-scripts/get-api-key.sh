#!/bin/bash
# Retrieve API key from 1Password CLI

if [ -z "$1" ]; then
    echo "Usage: $0 <item-name>"
    echo "Example: $0 'Anthropic API'"
    exit 1
fi

ITEM_NAME="$1"

if command -v op >/dev/null 2>&1; then
    # Try to read the credential
    if op read "op://Private/${ITEM_NAME}/credential" 2>/dev/null; then
        :
    else
        echo "Error: Could not find item '${ITEM_NAME}' in 1Password vault 'Private'" >&2
        echo "Available vaults:" >&2
        op vault list 2>/dev/null || echo "  (Not signed in)" >&2
        exit 1
    fi
else
    echo "Error: 1Password CLI not installed" >&2
    exit 1
fi
