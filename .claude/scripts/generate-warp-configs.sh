#!/bin/bash
# Generate Warp Launch Configurations for Claude Code Projects
# Author: Claude Code
# Usage: ./generate-warp-configs.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
CLAUDE_DIR="$HOME/.claude"
CLAUDE_PROJECTS_DIR="$CLAUDE_DIR/projects"
VAULT_PROJECTS_DIR="$HOME/Documents/ObsidianVault/Projects"
TEMPLATE_FILE="$CLAUDE_DIR/templates/launch-config.yaml"
WARP_CONFIGS_DIR="$HOME/.warp/launch_configurations"

# Warp color options: red, green, yellow, blue, magenta, cyan
COLORS=("blue" "green" "magenta" "cyan" "yellow" "red")

echo -e "${BLUE}🚀 Warp Launch Configuration Generator${NC}"
echo -e "${BLUE}=======================================${NC}\n"

# Create warp configs directory if it doesn't exist
mkdir -p "$WARP_CONFIGS_DIR"

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${YELLOW}⚠️  Template not found at $TEMPLATE_FILE${NC}"
    exit 1
fi

# Counter for color selection
color_index=0

# Function to generate config for a project
generate_config() {
    local project_dir="$1"
    local project_name=$(basename "$project_dir")

    # Skip certain directories
    if [ "$project_name" = "archive" ] || [[ "$project_name" == -Users-* ]]; then
        return
    fi

    local project_title=$(echo "$project_name" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
    local project_path="$project_dir"
    local project_color="${COLORS[$color_index]}"

    # Cycle through colors
    color_index=$(( (color_index + 1) % ${#COLORS[@]} ))

    # Generate config file
    local config_file="$WARP_CONFIGS_DIR/claude-${project_name}.yaml"

    # Replace template variables
    sed -e "s|{{PROJECT_NAME}}|$project_name|g" \
        -e "s|{{PROJECT_TITLE}}|$project_title|g" \
        -e "s|{{PROJECT_PATH}}|$project_path|g" \
        -e "s|{{PROJECT_COLOR}}|$project_color|g" \
        "$TEMPLATE_FILE" > "$config_file"

    echo -e "${GREEN}✅ Generated config for: $project_title${NC}"
    echo -e "   📄 File: $config_file"
    echo -e "   📂 Path: $project_path"
    echo -e "   🎨 Color: $project_color\n"
}

# Generate configs for Claude projects directory
if [ -d "$CLAUDE_PROJECTS_DIR" ]; then
    echo -e "${BLUE}📂 Scanning ~/.claude/projects/${NC}\n"
    for project_dir in "$CLAUDE_PROJECTS_DIR"/*; do
        if [ -d "$project_dir" ]; then
            generate_config "$project_dir"
        fi
    done
fi

# Generate configs for Obsidian Vault projects
if [ -d "$VAULT_PROJECTS_DIR" ]; then
    echo -e "${BLUE}📂 Scanning ~/Documents/ObsidianVault/Projects/${NC}\n"
    for project_dir in "$VAULT_PROJECTS_DIR"/*; do
        if [ -d "$project_dir" ]; then
            generate_config "$project_dir"
        fi
    done
fi

echo -e "${GREEN}✨ Configuration generation complete!${NC}\n"
echo -e "${BLUE}📖 How to use:${NC}"
echo -e "   1. Open Warp terminal"
echo -e "   2. Press Cmd+P (Command Palette)"
echo -e "   3. Type 'Launch Configuration'"
echo -e "   4. Select your project\n"
echo -e "${BLUE}💡 Or from command line:${NC}"
echo -e "   open 'warp://action/new_tab?path=$PROJECTS_DIR/[project-name]'\n"
