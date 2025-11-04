#!/bin/bash
# Memory Search - Search across all memory files
# Usage: memory-search "authentication"

QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: memory-search <query>"
    echo ""
    echo "Examples:"
    echo "  memory-search authentication"
    echo "  memory-search \"passkey fix\""
    echo "  memory-search WalterFetch"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🔍 Searching memory for: $QUERY                              "
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if ripgrep is installed
if ! command -v rg &> /dev/null; then
    echo "⚠️  ripgrep (rg) not installed. Using grep instead..."
    echo ""

    # Fallback to grep
    echo "📁 Project files:"
    grep -r -i --color=always "$QUERY" "$HOME/.claude/projects/" 2>/dev/null | head -20
    echo ""

    echo "📄 Global files:"
    grep -i --color=always "$QUERY" "$HOME/.claude/"*.md 2>/dev/null | head -10
else
    # Use ripgrep for better output
    echo "📁 Project workspace files:"
    rg -i --heading --color=always \
       --glob '*.md' \
       --glob '!node_modules' \
       --glob '!.git' \
       --max-count 5 \
       "$QUERY" \
       "$HOME/.claude/projects/" 2>/dev/null

    echo ""
    echo "📄 Global memory files:"
    rg -i --heading --color=always \
       --glob '*.md' \
       --max-count 5 \
       "$QUERY" \
       "$HOME/.claude/"*.md 2>/dev/null

    echo ""
    echo "📦 Session archives:"
    rg -i --heading --color=always \
       --glob '*.md' \
       --max-count 3 \
       "$QUERY" \
       "$HOME/.claude/session-archive/" 2>/dev/null
fi

echo ""
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
