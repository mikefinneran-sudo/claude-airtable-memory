#!/bin/bash
# Open Project in Code Editor
# Quick launcher for VS Code, Cursor, or Windsurf

EDITOR="${1:-code}"
PROJECT_PATH="${2:-.}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Normalize editor name
case "$EDITOR" in
    vscode|vs|code)
        EDITOR_CMD="code"
        EDITOR_NAME="VS Code"
        ;;
    cursor|ai|ai-code)
        EDITOR_CMD="cursor"
        EDITOR_NAME="Cursor (AI)"
        ;;
    windsurf|surf|ws)
        EDITOR_CMD="windsurf"
        EDITOR_NAME="Windsurf"
        ;;
    *)
        echo -e "${YELLOW}Unknown editor: $EDITOR${NC}"
        echo ""
        echo "Available editors:"
        echo "  code, vscode, vs    → VS Code"
        echo "  cursor, ai, ai-code → Cursor (AI-powered)"
        echo "  windsurf, surf, ws  → Windsurf"
        echo ""
        echo "Usage: open-in-editor <editor> [path]"
        echo "Example: open-in-editor cursor ~/Projects/myapp"
        exit 1
        ;;
esac

# Check if editor is installed
if ! command -v "$EDITOR_CMD" &> /dev/null; then
    echo -e "${YELLOW}$EDITOR_NAME not found${NC}"
    echo "Install with: brew install --cask ${EDITOR_CMD}"
    exit 1
fi

# Resolve path
if [ "$PROJECT_PATH" = "." ]; then
    PROJECT_PATH="$(pwd)"
fi

# Open in editor
echo -e "${BLUE}Opening in $EDITOR_NAME...${NC}"
echo "Path: $PROJECT_PATH"
echo ""

$EDITOR_CMD "$PROJECT_PATH"

echo -e "${GREEN}✅ Opened in $EDITOR_NAME${NC}"
