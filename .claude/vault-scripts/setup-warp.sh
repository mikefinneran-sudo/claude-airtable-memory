#!/bin/bash
# Setup Warp terminal integration with ObsidianVault

echo "🚀 Setting up Warp integration..."
echo ""

VAULT="/Users/mikefinneran/Documents/ObsidianVault"
WARP_DIR="$HOME/.warp"
ZSHRC="$HOME/.zshrc"

# 1. Create Warp directories
mkdir -p "$WARP_DIR/workflows"
mkdir -p "$WARP_DIR/themes"
mkdir -p "$WARP_DIR/launch_configurations"

echo "✓ Created Warp directories"

# 2. Add aliases to .zshrc if not present
if ! grep -q "# ObsidianVault aliases for Warp" "$ZSHRC" 2>/dev/null; then
    cat >> "$ZSHRC" <<'EOF'

# ObsidianVault aliases for Warp
alias vault='cd ~/Documents/ObsidianVault'
alias vopen='open -a Obsidian ~/Documents/ObsidianVault'
alias vdaily='python3 ~/Documents/ObsidianVault/.scripts/update_daily_note.py && open "obsidian://open?vault=ObsidianVault&file=Daily/$(date +%Y-%m-%d).md"'
alias vmorning='~/Documents/ObsidianVault/.scripts/morning-routine.sh'
alias vevening='~/Documents/ObsidianVault/.scripts/evening-routine.sh'
alias vgranola='~/Documents/ObsidianVault/.scripts/granola-export.sh'
alias vscreenshot='~/Documents/ObsidianVault/.scripts/daily-screenshot.sh'
alias vgit='cd ~/Documents/ObsidianVault && git status'
alias vpush='cd ~/Documents/ObsidianVault && git add . && git commit -m "Updates $(date +%Y-%m-%d)" && git push'

EOF
    echo "✓ Added aliases to .zshrc"
else
    echo "ℹ️  Aliases already in .zshrc"
fi

# 3. Create Warp workflows
cat > "$WARP_DIR/workflows/vault-ops.yaml" <<'EOF'
name: Vault Operations
description: Quick ObsidianVault operations

commands:
  open:
    name: Open Vault
    command: cd ~/Documents/ObsidianVault && open -a Obsidian .

  daily:
    name: Daily Note
    command: python3 ~/Documents/ObsidianVault/.scripts/update_daily_note.py

  morning:
    name: Morning Routine
    command: ~/Documents/ObsidianVault/.scripts/morning-routine.sh

  evening:
    name: Evening Routine
    command: ~/Documents/ObsidianVault/.scripts/evening-routine.sh

  status:
    name: Git Status
    command: cd ~/Documents/ObsidianVault && git status
EOF

echo "✓ Created vault-ops.yaml workflow"

# 4. Reload shell config
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Warp setup complete!"
echo ""
echo "New aliases available:"
echo "  vault      - Navigate to vault"
echo "  vopen      - Open vault in Obsidian"
echo "  vdaily     - Create/open daily note"
echo "  vmorning   - Morning routine"
echo "  vevening   - Evening routine"
echo "  vgranola   - Export Granola meetings"
echo "  vgit       - Vault git status"
echo "  vpush      - Quick git push"
echo ""
echo "Reload shell: source ~/.zshrc"
echo "Or restart Warp terminal"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
