#!/bin/bash
# Automated prevention of code in vault
# Add this to crontab: 0 */6 * * * ~/.claude/scripts/prevent-code-in-vault.sh

LOG_FILE="$HOME/.claude/logs/vault-purity.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date): Running vault purity check..." >> "$LOG_FILE"

if ! ~/.claude/scripts/check-vault-purity.sh >> "$LOG_FILE" 2>&1; then
    echo "$(date): ❌ VIOLATIONS DETECTED - Sending alert" >> "$LOG_FILE"

    # Send notification (macOS)
    osascript -e 'display notification "Code detected in vault! Check ~/.claude/logs/vault-purity.log" with title "Vault Purity Violation"'

    exit 1
else
    echo "$(date): ✅ Vault is pure" >> "$LOG_FILE"
    exit 0
fi
