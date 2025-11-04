#!/bin/bash
# Claude Code Context Management Utilities
# Author: Claude Code
# Usage: ./context-manager.sh [command]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Paths
CLAUDE_DIR="$HOME/.claude"
WORKING_CONTEXT="$CLAUDE_DIR/WORKING-CONTEXT.md"
PROJECTS_DIR="$CLAUDE_DIR/projects"

# Function to show context status
show_status() {
    echo -e "${BLUE}📊 Context Status${NC}\n"

    if [ -f "$WORKING_CONTEXT" ]; then
        local current_project=$(grep "^\*\*Current Project\*\*:" "$WORKING_CONTEXT" | tail -1 | sed 's/\*\*Current Project\*\*: //')
        local last_session=$(grep "^\*\*Session Started\*\*:" "$WORKING_CONTEXT" | tail -1 | sed 's/\*\*Session Started\*\*: //')

        if [ -n "$current_project" ]; then
            echo -e "${GREEN}🎯 Current Focus:${NC} $current_project"
        else
            echo -e "${YELLOW}⚠️  No active project${NC}"
        fi

        if [ -n "$last_session" ]; then
            echo -e "${GREEN}🕐 Last Session:${NC} $last_session"
        fi

        # Count total lines
        local total_lines=$(wc -l < "$WORKING_CONTEXT")
        echo -e "${GREEN}📄 Context Size:${NC} $total_lines lines"

        # Estimate token usage (rough estimate: ~4 chars per token)
        local file_size=$(wc -c < "$WORKING_CONTEXT")
        local estimated_tokens=$((file_size / 4))
        echo -e "${GREEN}🎫 Estimated Tokens:${NC} ~$estimated_tokens"

        if [ $estimated_tokens -gt 5000 ]; then
            echo -e "${YELLOW}⚠️  Consider compacting context (>5000 tokens)${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Working context not found${NC}"
    fi
    echo ""
}

# Function to archive current context
archive_context() {
    local archive_date=$(date '+%Y-%m-%d')
    local archive_file="$CLAUDE_DIR/archive/working-context-${archive_date}.md"

    mkdir -p "$CLAUDE_DIR/archive"

    if [ -f "$WORKING_CONTEXT" ]; then
        cp "$WORKING_CONTEXT" "$archive_file"
        echo -e "${GREEN}✅ Context archived to:${NC}"
        echo -e "   $archive_file\n"
    else
        echo -e "${YELLOW}⚠️  No context to archive${NC}"
    fi
}

# Function to reset context
reset_context() {
    local backup_date=$(date '+%Y-%m-%d-%H%M%S')
    local backup_file="$CLAUDE_DIR/archive/working-context-backup-${backup_date}.md"

    mkdir -p "$CLAUDE_DIR/archive"

    if [ -f "$WORKING_CONTEXT" ]; then
        # Backup first
        cp "$WORKING_CONTEXT" "$backup_file"
        echo -e "${GREEN}📦 Backed up to:${NC} $backup_file\n"

        # Create fresh context
        cat > "$WORKING_CONTEXT" << EOF
# Working Context

**Week of**: $(date '+%Y-%m-%d')
**Last Updated**: $(date '+%Y-%m-%d %H:%M')

## Current Focus
No active project

## This Week
-

## Session Log
---
**Context Reset**: $(date '+%Y-%m-%d %H:%M')

EOF
        echo -e "${GREEN}✅ Context reset to clean slate${NC}\n"
    else
        echo -e "${YELLOW}⚠️  No context file found${NC}"
    fi
}

# Function to switch project context
switch_project() {
    local project_name="$1"

    if [ -z "$project_name" ]; then
        echo -e "${RED}❌ Project name required${NC}"
        echo -e "${YELLOW}Usage: $0 switch [project-name]${NC}"
        exit 1
    fi

    if [ ! -d "$PROJECTS_DIR/$project_name" ]; then
        echo -e "${RED}❌ Project not found: $project_name${NC}"
        exit 1
    fi

    if [ -f "$WORKING_CONTEXT" ]; then
        echo -e "\n---\n" >> "$WORKING_CONTEXT"
        echo -e "**Project Switch**: $(date '+%Y-%m-%d %H:%M')" >> "$WORKING_CONTEXT"
        echo -e "**Switched to**: $project_name\n" >> "$WORKING_CONTEXT"

        echo -e "${GREEN}✅ Context updated to: $project_name${NC}"
        echo -e "${BLUE}💡 Reminder: Run ${YELLOW}/clear${NC} ${BLUE}in Claude Code to avoid context pollution${NC}\n"
    else
        echo -e "${YELLOW}⚠️  Working context not found${NC}"
    fi
}

# Function to show context tips
show_tips() {
    echo -e "${BLUE}💡 Context Management Tips${NC}\n"
    echo -e "${GREEN}1. Clear Between Tasks${NC}"
    echo -e "   Run ${YELLOW}/clear${NC} in Claude Code after completing a major task\n"

    echo -e "${GREEN}2. Compact at 70%${NC}"
    echo -e "   Check context meter (bottom right in Claude Code)"
    echo -e "   Run ${YELLOW}/compact${NC} when it hits 70%\n"

    echo -e "${GREEN}3. Separate Sessions${NC}"
    echo -e "   Open new Warp tabs for different projects"
    echo -e "   Each tab maintains its own Claude Code context\n"

    echo -e "${GREEN}4. Weekly Reset${NC}"
    echo -e "   Run ${YELLOW}$0 reset${NC} every Monday to start fresh\n"

    echo -e "${GREEN}5. Project-Specific Context${NC}"
    echo -e "   Create ${YELLOW}CLAUDE.md${NC} in project directories"
    echo -e "   Claude will load it automatically\n"

    echo -e "${BLUE}📚 Learn More:${NC}"
    echo -e "   • Check context: ${YELLOW}/context${NC}"
    echo -e "   • Disable MCP servers: ${YELLOW}@server-name disable${NC}"
    echo -e "   • Manage memory: Check ~/.claude/CLAUDE.md\n"
}

# Main script
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}      Context Management Utilities${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

command="${1:-status}"

case "$command" in
    status)
        show_status
        ;;
    archive)
        archive_context
        ;;
    reset)
        echo -e "${YELLOW}⚠️  This will reset your working context!${NC}"
        echo -e "${YELLOW}A backup will be created first.${NC}\n"
        echo -e "Continue? (y/N): "
        read -r confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            reset_context
        else
            echo -e "${BLUE}Cancelled${NC}"
        fi
        ;;
    switch)
        switch_project "$2"
        ;;
    tips)
        show_tips
        ;;
    *)
        echo -e "${YELLOW}Usage:${NC}"
        echo -e "  ${GREEN}$0 status${NC}         - Show current context status"
        echo -e "  ${GREEN}$0 archive${NC}        - Archive current context"
        echo -e "  ${GREEN}$0 reset${NC}          - Reset context to clean slate"
        echo -e "  ${GREEN}$0 switch [name]${NC}  - Switch to different project"
        echo -e "  ${GREEN}$0 tips${NC}           - Show context management tips\n"
        ;;
esac
