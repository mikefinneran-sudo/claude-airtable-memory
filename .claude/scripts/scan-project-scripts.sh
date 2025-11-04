#!/bin/bash
# Scan Projects for Custom Scripts
# Finds all custom scripts across projects and catalogs them

SCRIPTS_FOUND=0
SCRIPTS_TO_ARCHIVE=()

echo "🔍 Scanning for custom scripts across projects..."
echo ""

# Function to check if script should be archived
should_archive() {
    local file="$1"
    local basename=$(basename "$file")

    # Skip if already in utilities repo
    if [[ "$file" == *"utilities-repo-setup"* ]]; then
        return 1
    fi

    # Skip common system files
    if [[ "$basename" == "package.json" ]] || \
       [[ "$basename" == "setup.py" ]] || \
       [[ "$basename" == "Makefile" ]] || \
       [[ "$basename" == "Dockerfile" ]]; then
        return 1
    fi

    # Include shell scripts and Python scripts
    if [[ "$file" == *.sh ]] || [[ "$file" == *.py ]]; then
        # Check if it's a custom script (has shebang and is executable)
        if head -1 "$file" | grep -q "#!" && [ -x "$file" ]; then
            return 0
        fi
    fi

    return 1
}

# Scan ObsidianVault projects
echo "📁 Scanning ObsidianVault projects..."
if [ -d "$HOME/Documents/ObsidianVault/Projects" ]; then
    while IFS= read -r script; do
        if should_archive "$script"; then
            SCRIPTS_FOUND=$((SCRIPTS_FOUND + 1))
            SCRIPTS_TO_ARCHIVE+=("$script")

            # Get project name from path
            PROJECT=$(echo "$script" | sed 's|.*/Projects/||' | cut -d'/' -f1)
            SCRIPT_NAME=$(basename "$script")

            echo "  ✓ Found: $SCRIPT_NAME (in $PROJECT)"
        fi
    done < <(find "$HOME/Documents/ObsidianVault/Projects" -type f \( -name "*.sh" -o -name "*.py" \) 2>/dev/null)
fi

# Scan .scripts directory
echo ""
echo "📁 Scanning .scripts directory..."
if [ -d "$HOME/Documents/ObsidianVault/.scripts" ]; then
    while IFS= read -r script; do
        if should_archive "$script"; then
            SCRIPTS_FOUND=$((SCRIPTS_FOUND + 1))
            SCRIPTS_TO_ARCHIVE+=("$script")

            SCRIPT_NAME=$(basename "$script")
            echo "  ✓ Found: $SCRIPT_NAME (in .scripts)"
        fi
    done < <(find "$HOME/Documents/ObsidianVault/.scripts" -maxdepth 1 -type f \( -name "*.sh" -o -name "*.py" \) -executable 2>/dev/null)
fi

# Scan .claude scripts
echo ""
echo "📁 Scanning .claude scripts..."
if [ -d "$HOME/.claude/scripts" ]; then
    while IFS= read -r script; do
        SCRIPTS_FOUND=$((SCRIPTS_FOUND + 1))
        SCRIPTS_TO_ARCHIVE+=("$script")

        SCRIPT_NAME=$(basename "$script")
        echo "  ✓ Found: $SCRIPT_NAME (in .claude/scripts)"
    done < <(find "$HOME/.claude/scripts" -maxdepth 1 -type f \( -name "*.sh" -o -name "*.py" \) -executable 2>/dev/null)
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "📊 Scan Results"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Total scripts found: $SCRIPTS_FOUND"
echo ""

if [ ${#SCRIPTS_TO_ARCHIVE[@]} -eq 0 ]; then
    echo "No scripts to archive."
    exit 0
fi

# Ask user if they want to archive all
echo "Would you like to archive all these scripts? (y/N): "
read -r REPLY

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted. To archive individual scripts, use:"
    echo "  archive-custom-script.sh <script-file> <project> <description>"
    exit 0
fi

# Archive all scripts
echo ""
echo "📦 Archiving scripts..."
echo ""

for script in "${SCRIPTS_TO_ARCHIVE[@]}"; do
    # Extract project name and create description
    if [[ "$script" == *"/Projects/"* ]]; then
        PROJECT=$(echo "$script" | sed 's|.*/Projects/||' | cut -d'/' -f1)
        SUBDIR=$(echo "$script" | sed 's|.*/Projects/[^/]*/||' | sed 's|/[^/]*$||')
        DESC="Script from $PROJECT project"
        if [ -n "$SUBDIR" ] && [ "$SUBDIR" != "$SCRIPT_NAME" ]; then
            DESC="$DESC ($SUBDIR)"
        fi
    elif [[ "$script" == *"/.scripts/"* ]]; then
        PROJECT="obsidian-vault"
        DESC="Obsidian vault automation script"
    elif [[ "$script" == *"/.claude/"* ]]; then
        PROJECT="claude-code"
        DESC="Claude Code utility script"
    else
        PROJECT="general"
        DESC="Utility script"
    fi

    SCRIPT_NAME=$(basename "$script")

    echo "  → Archiving: $SCRIPT_NAME"
    "$HOME/.claude/scripts/archive-custom-script.sh" "$script" "$PROJECT" "$DESC" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "    ✓ Archived successfully"
    else
        echo "    ✗ Failed to archive"
    fi
done

echo ""
echo "✅ Scan and archive complete!"
echo ""
echo "📋 To push to GitHub:"
echo "   cd ~/.claude/projects/utilities-repo-setup"
echo "   gh repo create utilities-repo-setup --public --source=. --remote=origin --push"
echo ""
echo "Or manually:"
echo "   cd ~/.claude/projects/utilities-repo-setup"
echo "   git remote add origin git@github.com:YOUR-USERNAME/utilities-repo-setup.git"
echo "   git push -u origin main"
