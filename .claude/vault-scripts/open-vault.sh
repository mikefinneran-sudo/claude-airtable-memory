#!/bin/bash
# Open ObsidianVault in Obsidian app

VAULT_PATH="$HOME/Documents/ObsidianVault"

if [ -d "/Applications/Obsidian.app" ]; then
    open -a "Obsidian" "$VAULT_PATH"
else
    echo "Error: Obsidian not installed"
    exit 1
fi
