#!/bin/bash
# Load email template and copy to clipboard

VAULT="/Users/mikefinneran/Documents/ObsidianVault"
TEMPLATES_DIR="${VAULT}/Templates/Email"

if [ -z "$1" ]; then
    echo "Usage: $0 <template-name>"
    echo ""
    echo "Available templates:"
    if [ -d "$TEMPLATES_DIR" ]; then
        ls "$TEMPLATES_DIR" 2>/dev/null | sed 's/.md//' || echo "  (No templates yet)"
    else
        echo "  (Templates directory not created yet)"
        echo "  Create templates in: $TEMPLATES_DIR"
    fi
    exit 1
fi

TEMPLATE_NAME="$1"
TEMPLATE_FILE="${TEMPLATES_DIR}/${TEMPLATE_NAME}.md"

if [ -f "$TEMPLATE_FILE" ]; then
    # Copy to clipboard
    cat "$TEMPLATE_FILE" | pbcopy

    echo "✓ Template copied to clipboard:"
    echo "  ${TEMPLATE_NAME}"
    echo ""
    echo "Paste in Superhuman with ⌘V"
    echo ""
    echo "Template preview:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    head -10 "$TEMPLATE_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "❌ Template not found: ${TEMPLATE_NAME}"
    echo ""
    echo "Create it at: ${TEMPLATE_FILE}"
    exit 1
fi
