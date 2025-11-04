#!/bin/bash
# Install Claude Code Warp Project Manager
# Author: Claude Code
# Usage: ./install.sh

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}   Claude Code Warp Project Manager${NC}"
echo -e "${BLUE}   Installation Script${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

# Check if Warp is installed
if [ ! -d "/Applications/Warp.app" ]; then
    echo -e "${RED}❌ Warp terminal not found${NC}"
    echo -e "${YELLOW}📥 Please install Warp from: https://www.warp.dev${NC}\n"
    exit 1
fi

echo -e "${GREEN}✅ Warp terminal found${NC}\n"

# Check directories exist
echo -e "${BLUE}📂 Checking directories...${NC}"

CLAUDE_DIR="$HOME/.claude"
SCRIPTS_DIR="$CLAUDE_DIR/scripts"
TEMPLATES_DIR="$CLAUDE_DIR/templates"
PROJECTS_DIR="$CLAUDE_DIR/projects"
WARP_CONFIGS="$HOME/.warp/launch_configurations"

if [ ! -d "$SCRIPTS_DIR" ]; then
    echo -e "${YELLOW}⚠️  Scripts directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Directories verified${NC}\n"

# Make all scripts executable
echo -e "${BLUE}🔧 Setting script permissions...${NC}"
chmod +x "$SCRIPTS_DIR"/*.sh
echo -e "${GREEN}✅ Scripts are executable${NC}\n"

# Generate Warp configurations
echo -e "${BLUE}⚙️  Generating Warp configurations...${NC}"
"$SCRIPTS_DIR/generate-warp-configs.sh"
echo ""

# Check shell configuration
SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

ALIAS_LINE="source ~/.claude/scripts/setup-aliases.sh"

if grep -q "$ALIAS_LINE" "$SHELL_RC" 2>/dev/null; then
    echo -e "${GREEN}✅ Shell aliases already configured${NC}\n"
else
    echo -e "${BLUE}📝 Adding aliases to $SHELL_RC...${NC}"
    echo "" >> "$SHELL_RC"
    echo "# Claude Code Project Manager" >> "$SHELL_RC"
    echo "$ALIAS_LINE" >> "$SHELL_RC"
    echo -e "${GREEN}✅ Aliases added${NC}\n"
fi

# Load aliases for current session
source "$SCRIPTS_DIR/setup-aliases.sh"

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}\n"

# Test context manager
if "$SCRIPTS_DIR/context-manager.sh" status > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Context manager working${NC}"
else
    echo -e "${RED}❌ Context manager failed${NC}"
fi

# Test Warp configs exist
config_count=$(find "$WARP_CONFIGS" -name "claude-*.yaml" 2>/dev/null | wc -l)
if [ "$config_count" -gt 0 ]; then
    echo -e "${GREEN}✅ Warp configurations created ($config_count configs)${NC}"
else
    echo -e "${RED}❌ No Warp configurations found${NC}"
fi

echo -e "\n${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}   Installation Complete! 🎉${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}\n"

echo -e "${BLUE}📖 Quick Start:${NC}\n"
echo -e "${YELLOW}1. Reload your shell:${NC}"
echo -e "   source $SHELL_RC\n"

echo -e "${YELLOW}2. Open a project:${NC}"
echo -e "   cproject\n"

echo -e "${YELLOW}3. Start Claude Code:${NC}"
echo -e "   claude\n"

echo -e "${YELLOW}4. Load project context:${NC}"
echo -e "   \"Continue [project-name]\"\n"

echo -e "${BLUE}📚 Documentation:${NC}"
echo -e "   Quick Start: ${GREEN}cat ~/.claude/WARP-QUICKSTART.md${NC}"
echo -e "   Full Guide:  ${GREEN}cat ~/.claude/WARP-PROJECT-MANAGER.md${NC}\n"

echo -e "${BLUE}💡 Commands:${NC}"
echo -e "   ${GREEN}cproject${NC}   - Open project in new Warp tab"
echo -e "   ${GREEN}cresearch${NC}  - Research with Perplexity Pro"
echo -e "   ${GREEN}ccontext${NC}   - Manage context"
echo -e "   ${GREEN}cwarp${NC}      - Regenerate Warp configs\n"

echo -e "${YELLOW}⚠️  Don't forget to reload your shell!${NC}"
echo -e "   source $SHELL_RC\n"
