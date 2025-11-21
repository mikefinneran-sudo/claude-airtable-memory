#!/bin/bash
# Claude Code Project Memory Initializer
# Usage: init-project-memory.sh [project-path]
# If no path provided, uses current directory

set -e

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"
PROJECT_NAME=$(basename "$(pwd)")

# Create .claude directory if it doesn't exist
mkdir -p .claude

# Check if CLAUDE.md already exists
if [ -f ".claude/CLAUDE.md" ]; then
    echo "⚠️  CLAUDE.md already exists in this project"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted. Existing CLAUDE.md preserved."
        exit 0
    fi
fi

# Detect project type
PROJECT_TYPE="Unknown"
TECH_STACK=""

if [ -f "package.json" ]; then
    PROJECT_TYPE="Node.js/JavaScript"
    if grep -q "\"react\"" package.json 2>/dev/null; then
        TECH_STACK="React"
    fi
    if grep -q "\"next\"" package.json 2>/dev/null; then
        TECH_STACK="Next.js"
    fi
    if grep -q "\"typescript\"" package.json 2>/dev/null; then
        TECH_STACK="$TECH_STACK TypeScript"
    fi
elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="Python"
    if [ -f "pyproject.toml" ]; then
        TECH_STACK="Python (modern packaging)"
    fi
elif [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="Rust"
elif [ -f "go.mod" ]; then
    PROJECT_TYPE="Go"
elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
    PROJECT_TYPE="Java"
fi

# Check for git
if [ -d ".git" ]; then
    GIT_REMOTE=$(git remote get-url origin 2>/dev/null || echo "No remote configured")
else
    GIT_REMOTE="Not a git repository"
fi

# Generate CLAUDE.md
cat > .claude/CLAUDE.md << EOF
# Project: $PROJECT_NAME

## Overview
[Add a brief description of what this project does]

## Project Type
- **Type**: $PROJECT_TYPE
- **Tech Stack**: $TECH_STACK
- **Repository**: $GIT_REMOTE

## Architecture
[Describe the project structure, key directories, and how components interact]

## Key Files & Directories
[List important files and what they do]
- \`src/\` -
- \`tests/\` -
- \`README.md\` -

## Coding Standards
[Add project-specific coding conventions]
-
-
-

## Development Commands
[List common commands used in this project]
- Build:
- Test:
- Run:
- Deploy:

## Dependencies & Setup
[Note any special setup requirements]
-
-

## Business Context
[Add any domain knowledge, business logic, or important context]
-
-

## Current Work
[Track what you're currently working on or planning]
-
-

---
*Auto-generated on $(date +%Y-%m-%d)*
*Update this file as the project evolves*
EOF

echo "✅ Created .claude/CLAUDE.md for project: $PROJECT_NAME"
echo "📝 Edit .claude/CLAUDE.md to customize the project memory"
echo ""
echo "Next steps:"
echo "  1. Fill in the [bracketed] sections with project details"
echo "  2. Add this to git: git add .claude/CLAUDE.md"
echo "  3. Claude will automatically load this context in future sessions"
