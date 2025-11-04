#!/bin/bash
# Start Session Memory
# Run when starting work on a project

set -e

# Check/create 1Password session (24-hour authorization)
if [ -f "$HOME/.claude/scripts/check-1password-session.sh" ]; then
    source "$HOME/.claude/scripts/check-1password-session.sh"
fi

# Get project name from argument or prompt
if [ -z "$1" ]; then
    echo "Usage: start-session.sh [project-name]"
    echo ""
    echo "Available projects:"
    cat ~/.claude/PROJECT-REGISTRY.md | grep "^\|" | grep -v "Project" | grep -v "^---"
    echo ""
    read -p "Enter project name: " PROJECT_NAME
else
    PROJECT_NAME="$1"
fi

# Normalize project name
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_SLUG"

# Check if project workspace exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "⚠️  Project workspace not found: $PROJECT_DIR"
    echo ""
    read -p "Create new project workspace? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdir -p "$PROJECT_DIR"
        echo "✅ Created $PROJECT_DIR"
        echo "   Run: ~/.claude/init-project-memory.sh $PROJECT_DIR"
        exit 0
    else
        exit 1
    fi
fi

# Determine project location from README
if [ -f "$PROJECT_DIR/README.md" ]; then
    LOCATION=$(grep "^**Main Location**:" "$PROJECT_DIR/README.md" | cut -d: -f2- | xargs || echo "$PROJECT_DIR")
else
    LOCATION="$PROJECT_DIR"
fi

# Create new session memory
SESSION_FILE="$HOME/.claude/SESSION-MEMORY.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

cat > "$SESSION_FILE" << EOF
# Current Session Memory

**Session Started**: $TIMESTAMP
**Project**: $PROJECT_NAME
**Location**: $LOCATION

---

## User's Request

[Add what you're working on this session]

---

## What I'm Building This Session

[List goals for this session]

---

## Actions Taken This Session

### ✅ Completed


### 🔄 In Progress


### ⏭️ Next


---

## Decisions Made

[Track key decisions as session progresses]

---

## Files Modified

[Will be updated as session progresses]

---

## Context for Next Action

[Current state and what you're about to do]

---

**Last Updated**: $TIMESTAMP
EOF

echo "✅ Session started: $PROJECT_NAME"
echo "📝 Session memory: $SESSION_FILE"
echo ""
echo "Quick reference:"
echo "  - Project workspace: $PROJECT_DIR"
echo "  - README: cat $PROJECT_DIR/README.md"
echo "  - Status: cat $PROJECT_DIR/STATUS.md"
echo "  - Recent sessions: cat $PROJECT_DIR/SESSIONS.md | tail -50"
echo ""
echo "When done, run: ~/.claude/scripts/save-session-memory.sh"
