#!/bin/bash
# Initialize a Claude Code Project Session in Warp
# Author: Claude Code
# Usage: ./init-project-session.sh [project-name]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Paths
CLAUDE_DIR="$HOME/.claude"
CLAUDE_PROJECTS_DIR="$CLAUDE_DIR/projects"
VAULT_PROJECTS_DIR="$HOME/Documents/ObsidianVault/Projects"
REGISTRY_FILE="$CLAUDE_DIR/PROJECT-REGISTRY.md"
WORKING_CONTEXT="$CLAUDE_DIR/WORKING-CONTEXT.md"

# Function to create new project
create_new_project() {
    echo -e "${BLUE}📝 Creating new project...${NC}\n"
    
    # Get project name
    echo -e "${BLUE}Enter project name:${NC} "
    read -r project_name
    
    if [ -z "$project_name" ]; then
        echo -e "${RED}❌ Project name cannot be empty${NC}"
        exit 1
    fi
    
    # Choose location
    echo -e "\n${BLUE}Where would you like to create the project?${NC}"
    echo -e "${GREEN}  1. Claude projects (~/.claude/projects)${NC}"
    echo -e "${GREEN}  2. Obsidian Vault (~/Documents/ObsidianVault/Projects)${NC}"
    echo -e "${BLUE}Enter choice (1 or 2):${NC} "
    read -r location_choice
    
    case $location_choice in
        1)
            project_path="$CLAUDE_PROJECTS_DIR/$project_name"
            ;;
        2)
            project_path="$VAULT_PROJECTS_DIR/$project_name"
            ;;
        *)
            echo -e "${RED}❌ Invalid choice${NC}"
            exit 1
            ;;
    esac
    
    # Check if project already exists
    if [ -d "$project_path" ]; then
        echo -e "${RED}❌ Project already exists: $project_path${NC}"
        exit 1
    fi
    
    # Create project directory
    mkdir -p "$project_path"
    echo -e "${GREEN}✅ Created directory: $project_path${NC}"
    
    # Initialize git repository
    echo -e "${BLUE}Initialize git repository? (y/n):${NC} "
    read -r init_git
    
    if [[ "$init_git" =~ ^[Yy]$ ]]; then
        cd "$project_path"
        git init
        echo -e "${GREEN}✅ Initialized git repository${NC}"
    fi
    
    # Create README.md
    echo -e "${BLUE}Create README.md? (y/n):${NC} "
    read -r create_readme
    
    if [[ "$create_readme" =~ ^[Yy]$ ]]; then
        cat > "$project_path/README.md" << EOF
# $project_name

## Description

Add your project description here.

## Setup

Add setup instructions here.

## Usage

Add usage instructions here.
EOF
        echo -e "${GREEN}✅ Created README.md${NC}"
    fi
    
    echo -e "\n${GREEN}🎉 Project created successfully!${NC}\n"
    echo -e "${BLUE}📂 Location: $project_path${NC}\n"
    echo -e "${BLUE}Next steps:${NC}"
    echo -e "   1. Run: ${YELLOW}cproject $project_name${NC}"
    echo -e "   2. Start working on your project!\n"
}

# Function to list available projects
list_projects() {
    echo -e "${BLUE}📚 Available Projects:${NC}\n"
    local index=1

    # List projects from Claude directory
    if [ -d "$CLAUDE_PROJECTS_DIR" ]; then
        for project_dir in "$CLAUDE_PROJECTS_DIR"/*; do
            if [ -d "$project_dir" ]; then
                project_name=$(basename "$project_dir")
                # Skip unwanted directories
                if [ "$project_name" != "archive" ] && [[ "$project_name" != -Users-* ]]; then
                    echo -e "${GREEN}  $index. $project_name${NC}"
                    ((index++))
                fi
            fi
        done
    fi

    # List projects from Vault directory
    if [ -d "$VAULT_PROJECTS_DIR" ]; then
        for project_dir in "$VAULT_PROJECTS_DIR"/*; do
            if [ -d "$project_dir" ]; then
                project_name=$(basename "$project_dir")
                echo -e "${GREEN}  $index. $project_name${NC}"
                ((index++))
            fi
        done
    fi

    echo ""
}

# Function to find project path
find_project_path() {
    local project_name="$1"

    # Check Claude projects directory
    if [ -d "$CLAUDE_PROJECTS_DIR/$project_name" ]; then
        echo "$CLAUDE_PROJECTS_DIR/$project_name"
        return 0
    fi

    # Check Vault projects directory
    if [ -d "$VAULT_PROJECTS_DIR/$project_name" ]; then
        echo "$VAULT_PROJECTS_DIR/$project_name"
        return 0
    fi

    return 1
}

# Function to open project in new Warp tab
open_project() {
    local project_name="$1"
    local project_path=$(find_project_path "$project_name")

    if [ -z "$project_path" ]; then
        echo -e "${RED}❌ Project not found: $project_name${NC}"
        echo -e "${YELLOW}💡 Run without arguments to see available projects${NC}"
        exit 1
    fi

    echo -e "${BLUE}🚀 Initializing project session...${NC}\n"
    echo -e "${GREEN}📍 Project: $project_name${NC}"
    echo -e "${GREEN}📂 Location: $project_path${NC}\n"

    # Update working context
    if [ -f "$WORKING_CONTEXT" ]; then
        echo -e "\n---\n**Session Started**: $(date '+%Y-%m-%d %H:%M')" >> "$WORKING_CONTEXT"
        echo -e "**Current Project**: $project_name" >> "$WORKING_CONTEXT"
        echo -e "**Project Path**: $project_path\n" >> "$WORKING_CONTEXT"
    fi

    # Open in new Warp tab using URI scheme
    echo -e "${BLUE}🪟 Opening new Warp tab...${NC}"
    open "warp://action/new_tab?path=$(echo "$project_path" | sed 's/ /%20/g')"

    echo -e "\n${GREEN}✅ Project session initialized!${NC}\n"
    echo -e "${BLUE}📖 Next steps:${NC}"
    echo -e "   1. Wait for new Warp tab to open"
    echo -e "   2. In the new tab, run: ${YELLOW}claude${NC}"
    echo -e "   3. Say: ${YELLOW}\"Continue $project_name\"${NC}"
    echo -e "   4. Claude will load project context automatically\n"
    echo -e "${BLUE}💡 Tips:${NC}"
    echo -e "   • Use ${YELLOW}@ symbol${NC} to reference project files"
    echo -e "   • Run ${YELLOW}/clear${NC} when switching focus areas"
    echo -e "   • Use ${YELLOW}/compact${NC} when context hits 70%\n"
}

# Function to display interactive menu
interactive_menu() {
    list_projects

    echo -e "${BLUE}Enter project number or name (or 'new' to create):${NC} "
    read -r selection
    
    # Check if user wants to create new project
    if [[ "$selection" == "new" ]]; then
        create_new_project
        return
    fi

    # Check if input is a number
    if [[ "$selection" =~ ^[0-9]+$ ]]; then
        # Get project by index
        local index=1
        local found=false

        # Check Claude projects directory
        if [ -d "$CLAUDE_PROJECTS_DIR" ]; then
            for project_dir in "$CLAUDE_PROJECTS_DIR"/*; do
                if [ -d "$project_dir" ]; then
                    project_name=$(basename "$project_dir")
                    if [ "$project_name" != "archive" ] && [[ "$project_name" != -Users-* ]]; then
                        if [ "$index" -eq "$selection" ]; then
                            open_project "$project_name"
                            return
                        fi
                        ((index++))
                    fi
                fi
            done
        fi

        # Check Vault projects directory
        if [ -d "$VAULT_PROJECTS_DIR" ]; then
            for project_dir in "$VAULT_PROJECTS_DIR"/*; do
                if [ -d "$project_dir" ]; then
                    project_name=$(basename "$project_dir")
                    if [ "$index" -eq "$selection" ]; then
                        open_project "$project_name"
                        return
                    fi
                    ((index++))
                fi
            done
        fi

        echo -e "${RED}❌ Invalid selection${NC}"
        exit 1
    else
        # Treat as project name
        open_project "$selection"
    fi
}

# Main script
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}   Claude Code Project Session Manager${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

if [ $# -eq 0 ]; then
    # No arguments - show interactive menu
    interactive_menu
else
    # Project name provided
    open_project "$1"
fi
