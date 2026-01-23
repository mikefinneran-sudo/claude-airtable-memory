#!/bin/bash
# Automated check to ensure vault contains NO code
# Run this as a cron job or git pre-commit hook

VAULT_PATH="$HOME/Documents/ObsidianVault"
VIOLATIONS=()

echo "🔍 Checking vault purity..."

# Check for node_modules
if find "$VAULT_PATH" -type d -name "node_modules" 2>/dev/null | grep -q .; then
    VIOLATIONS+=("❌ node_modules found in vault")
fi

# Check for venv
if find "$VAULT_PATH" -type d -name "venv" 2>/dev/null | grep -q .; then
    VIOLATIONS+=("❌ venv found in vault")
fi

# Check for .next
if find "$VAULT_PATH" -type d -name ".next" 2>/dev/null | grep -q .; then
    VIOLATIONS+=("❌ .next found in vault")
fi

# Check for __pycache__
if find "$VAULT_PATH" -type d -name "__pycache__" 2>/dev/null | grep -q .; then
    VIOLATIONS+=("❌ __pycache__ found in vault")
fi

# Check for .claude folders in vault
if find "$VAULT_PATH" -type d -name ".claude" 2>/dev/null | grep -q .; then
    VIOLATIONS+=("❌ .claude folders found in vault")
fi

# Check for package.json (usually indicates code)
PACKAGE_COUNT=$(find "$VAULT_PATH" -name "package.json" 2>/dev/null | wc -l)
if [ "$PACKAGE_COUNT" -gt 0 ]; then
    VIOLATIONS+=("❌ Found $PACKAGE_COUNT package.json files")
fi

# Check for .py files (should be in ~/.claude/scripts/ or ~/Code/)
PY_COUNT=$(find "$VAULT_PATH" -name "*.py" 2>/dev/null | wc -l)
if [ "$PY_COUNT" -gt 0 ]; then
    VIOLATIONS+=("❌ Found $PY_COUNT Python files")
fi

# Check for .js/.ts files (should be in ~/Code/) - exclude .obsidian plugins
JS_COUNT=$(find "$VAULT_PATH" -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" 2>/dev/null | grep -v "\.obsidian/plugins" | wc -l)
if [ "$JS_COUNT" -gt 0 ]; then
    VIOLATIONS+=("❌ Found $JS_COUNT JavaScript/TypeScript files (excluding Obsidian plugins)")
fi

# Report results
if [ ${#VIOLATIONS[@]} -eq 0 ]; then
    echo "✅ Vault is pure - no code detected"
    exit 0
else
    echo "🚨 VAULT PURITY VIOLATIONS:"
    for violation in "${VIOLATIONS[@]}"; do
        echo "   $violation"
    done
    echo ""
    echo "Action required: Move code to ~/Code/"
    exit 1
fi
