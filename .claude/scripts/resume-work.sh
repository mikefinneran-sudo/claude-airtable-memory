#!/bin/bash
# Resume Work - Load memory and context for new session
# Usage: resume-work.sh [project-name]
#   Or just: resume

set -e

CLAUDE_DIR="$HOME/.claude"
WORKING_CONTEXT="$CLAUDE_DIR/WORKING-CONTEXT.md"
SESSION_MEMORY="$CLAUDE_DIR/SESSION-MEMORY.md"
PROJECT_REGISTRY="$CLAUDE_DIR/PROJECT-REGISTRY.md"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear

# Check/create 1Password session (24-hour authorization)
if [ -f "$HOME/.claude/scripts/check-1password-session.sh" ]; then
    source "$HOME/.claude/scripts/check-1password-session.sh"
fi

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}                   CLAUDE CODE - RESUME WORK                        ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Show current week focus
if [ -f "$WORKING_CONTEXT" ]; then
    echo -e "${BLUE}📅 Current Week Focus:${NC}"
    grep -A 2 "## Current Week Focus" "$WORKING_CONTEXT" | tail -2 | sed 's/^/   /'
    echo ""
fi

# Show recent activity
if [ -f "$WORKING_CONTEXT" ]; then
    echo -e "${BLUE}📊 Recent Activity (Last 3 Sessions):${NC}"
    grep "^###" "$WORKING_CONTEXT" | grep -E "^### [0-9]{4}-" | head -3 | sed 's/###/   →/'
    echo ""
fi

# Show active projects
if [ -f "$PROJECT_REGISTRY" ]; then
    echo -e "${BLUE}🎯 Active Projects:${NC}"
    grep "^|" "$PROJECT_REGISTRY" | grep -v "Project" | grep -v "^---" | grep "🟢\|🟡" | head -5 | sed 's/^/   /'
    echo ""
fi

# Show this week's goals
if [ -f "$WORKING_CONTEXT" ]; then
    echo -e "${BLUE}✅ This Week's Goals:${NC}"
    sed -n '/## This Week'"'"'s Goals/,/^---/p' "$WORKING_CONTEXT" | grep "^-" | sed 's/^/   /'
    echo ""
fi

# Show current blockers
if [ -f "$WORKING_CONTEXT" ]; then
    echo -e "${YELLOW}⚠️  Current Blockers:${NC}"
    sed -n '/## Current Blockers/,/^---/p' "$WORKING_CONTEXT" | grep -E "^\*\*|^-" | sed 's/^/   /' || echo "   None"
    echo ""
fi

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# If project name provided, start that project
if [ ! -z "$1" ]; then
    PROJECT_NAME="$1"
    echo -e "${GREEN}▶ Loading project: $PROJECT_NAME${NC}"
    echo ""
    ~/.claude/scripts/start-session.sh "$PROJECT_NAME"
    exit 0
fi

# Interactive project selection
echo -e "${BLUE}Select a project to continue:${NC}"
echo ""
echo "  1) WalterSignal"
echo "  2) FlyFlat"
echo "  3) SpecialAgentStanny"
echo "  4) LifeHub 2.0"
echo "  5) Other (specify)"
echo "  6) Just show memory (no new session)"
echo ""
read -p "Enter choice (1-6): " choice

case $choice in
    1)
        PROJECT="waltersignal"
        ;;
    2)
        PROJECT="flyflat"
        ;;
    3)
        PROJECT="specialagentstanny"
        ;;
    4)
        PROJECT="lifehub-2.0"
        ;;
    5)
        read -p "Enter project name: " PROJECT
        ;;
    6)
        echo ""
        echo -e "${GREEN}✅ Memory loaded. Ready to work!${NC}"
        echo ""
        echo "To start a specific project later, use:"
        echo "  ~/.claude/scripts/start-session.sh [project-name]"
        echo ""
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}▶ Starting session for: $PROJECT${NC}"
echo ""
~/.claude/scripts/start-session.sh "$PROJECT"
