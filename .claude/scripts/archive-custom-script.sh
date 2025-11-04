#!/bin/bash
# Archive Custom Script to GitHub
# Automatically documents and commits custom scripts to utilities-repo-setup

SCRIPTS_REPO="$HOME/.claude/projects/utilities-repo-setup"
SCRIPT_FILE="$1"
SCRIPT_NAME=$(basename "$SCRIPT_FILE")
PROJECT_NAME="$2"
DESCRIPTION="$3"

if [ -z "$SCRIPT_FILE" ] || [ ! -f "$SCRIPT_FILE" ]; then
    echo "Usage: archive-custom-script.sh <script-file> <project-name> <description>"
    echo ""
    echo "Example:"
    echo "  archive-custom-script.sh ./fix-passkey-complete.sh waltersignal 'Google passkey automation'"
    exit 1
fi

# Check if utilities repo exists
if [ ! -d "$SCRIPTS_REPO" ]; then
    echo "📦 Utilities repo not found. Creating..."
    mkdir -p "$SCRIPTS_REPO"
    cd "$SCRIPTS_REPO"
    git init

    # Create structure
    mkdir -p {automation,fixes,utilities,project-specific}

    cat > README.md << 'EOFREADME'
# Custom Scripts Repository

Collection of custom scripts from various projects, automatically archived by Claude Code.

## Structure

```
utilities-repo-setup/
├── automation/        # Automation and workflow scripts
├── fixes/            # Problem-solving scripts (bugs, issues)
├── utilities/        # General utility scripts
├── project-specific/ # Scripts tied to specific projects
└── archive/          # Historical scripts
```

## Scripts Catalog

See `CATALOG.md` for full list with descriptions.

---

*Auto-maintained by Claude Code script archival system*
EOFREADME

    # Create catalog
    cat > CATALOG.md << 'EOFCAT'
# Scripts Catalog

Auto-generated index of all archived scripts.

---

## Quick Reference

| Script | Category | Project | Description | Date Added |
|--------|----------|---------|-------------|------------|
EOFCAT

    git add .
    git commit -m "Initial commit: Utilities repo structure"

    echo "✅ Created utilities repo at: $SCRIPTS_REPO"
fi

cd "$SCRIPTS_REPO"

# Determine category based on script name and description
CATEGORY="utilities"
if [[ "$SCRIPT_NAME" == *"fix-"* ]] || [[ "$DESCRIPTION" == *"fix"* ]]; then
    CATEGORY="fixes"
elif [[ "$SCRIPT_NAME" == *"automate"* ]] || [[ "$DESCRIPTION" == *"automat"* ]]; then
    CATEGORY="automation"
elif [ -n "$PROJECT_NAME" ] && [ "$PROJECT_NAME" != "general" ]; then
    CATEGORY="project-specific/$PROJECT_NAME"
    mkdir -p "$CATEGORY"
fi

# Copy script
DEST="$SCRIPTS_REPO/$CATEGORY/$SCRIPT_NAME"
cp "$SCRIPT_FILE" "$DEST"
chmod +x "$DEST"

echo "📝 Creating documentation..."

# Create/update documentation
DOC_FILE="$SCRIPTS_REPO/$CATEGORY/${SCRIPT_NAME%.sh}.md"

cat > "$DOC_FILE" << EOFDOC
# $SCRIPT_NAME

**Category**: $CATEGORY
**Project**: ${PROJECT_NAME:-General}
**Date Added**: $(date '+%Y-%m-%d')

---

## Description

${DESCRIPTION:-Custom script from $PROJECT_NAME}

## Location

\`$CATEGORY/$SCRIPT_NAME\`

## Usage

\`\`\`bash
$CATEGORY/$SCRIPT_NAME [options]
\`\`\`

## Source

Created during: $PROJECT_NAME project
Original location: $SCRIPT_FILE

## Dependencies

$(head -20 "$SCRIPT_FILE" | grep -E "^# Requires:|^# Dependencies:" || echo "None documented")

## Last Updated

$(date '+%Y-%m-%d %H:%M:%S')

---

## Script Content

\`\`\`bash
$(cat "$SCRIPT_FILE")
\`\`\`

---

*Auto-archived by Claude Code*
EOFDOC

# Update catalog
CATALOG="$SCRIPTS_REPO/CATALOG.md"
DATE=$(date '+%Y-%m-%d')

# Add entry to catalog (if not already there)
if ! grep -q "$SCRIPT_NAME" "$CATALOG"; then
    echo "| \`$SCRIPT_NAME\` | $CATEGORY | ${PROJECT_NAME:-General} | ${DESCRIPTION:-N/A} | $DATE |" >> "$CATALOG"
fi

# Git commit
git add .
git commit -m "Add script: $SCRIPT_NAME from $PROJECT_NAME

Category: $CATEGORY
Description: $DESCRIPTION
Date: $DATE"

echo ""
echo "✅ Script archived!"
echo "   Location: $DEST"
echo "   Docs: $DOC_FILE"
echo "   Category: $CATEGORY"
echo ""
echo "📋 To push to GitHub:"
echo "   cd $SCRIPTS_REPO"
echo "   git remote add origin <your-github-repo-url>"
echo "   git push -u origin main"
