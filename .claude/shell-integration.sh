# Claude Code Shell Integration
# Add this to your ~/.zshrc or ~/.bashrc

# Initialize Claude memory for a project
claude-init() {
    ~/.claude/init-project-memory.sh "$@"
}

# Auto-initialize Claude memory when entering a git repo (optional)
# Uncomment the following to enable automatic initialization:
#
# auto_claude_init() {
#     if [ -d .git ] && [ ! -f .claude/CLAUDE.md ]; then
#         echo "📋 New git project detected. Initialize Claude memory? (y/N)"
#         read -q && echo && claude-init
#     fi
# }
#
# # Hook into directory change
# chpwd_functions+=(auto_claude_init)

# Quick command to edit project memory
claude-edit() {
    if [ -f .claude/CLAUDE.md ]; then
        ${EDITOR:-nano} .claude/CLAUDE.md
    else
        echo "No .claude/CLAUDE.md found in current directory"
        echo "Run 'claude-init' to create one"
    fi
}

# View current project memory
claude-show() {
    if [ -f .claude/CLAUDE.md ]; then
        cat .claude/CLAUDE.md
    else
        echo "No .claude/CLAUDE.md found in current directory"
    fi
}
