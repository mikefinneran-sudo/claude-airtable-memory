#!/bin/bash
# Restore from S3 - Restore Claude backups from S3

set -e

S3_BUCKET="${S3_BACKUP_BUCKET}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if S3 bucket is configured
if [ -z "$S3_BUCKET" ]; then
    echo "❌ S3_BACKUP_BUCKET not set"
    exit 1
fi

# Check if AWS CLI is available
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}              S3 Restore - Available Backups${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# List available backups
echo "📋 Fetching backups from s3://$S3_BUCKET/claude-backups/..."
echo ""

backups=$(aws s3 ls "s3://$S3_BUCKET/claude-backups/" | grep "backup-" | sort -r)

if [ -z "$backups" ]; then
    echo "❌ No backups found in S3"
    exit 1
fi

# Display backups with numbers
echo "Available backups:"
echo ""
echo "$backups" | nl -w2 -s'. '
echo ""

# Get user selection
read -p "Select backup number to restore (or 'q' to quit): " selection

if [ "$selection" = "q" ]; then
    echo "Aborted"
    exit 0
fi

# Get the selected backup filename
backup_file=$(echo "$backups" | sed -n "${selection}p" | awk '{print $4}')

if [ -z "$backup_file" ]; then
    echo "❌ Invalid selection"
    exit 1
fi

echo ""
echo "Selected: $backup_file"
echo ""
echo "⚠️  WARNING: This will restore the following:"
echo "   - Session archives"
echo "   - Project workspaces"
echo "   - Memory files"
echo "   - Configuration"
echo ""
echo "Current files will be backed up to ~/.claude/pre-restore-backup/"
echo ""
read -p "Continue with restore? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted"
    exit 0
fi

# Backup current state first
echo ""
echo "💾 Backing up current state..."
BACKUP_DIR="$HOME/.claude/pre-restore-backup-$(date '+%Y%m%d-%H%M%S')"
mkdir -p "$BACKUP_DIR"

for dir in session-archive projects; do
    if [ -d "$HOME/.claude/$dir" ]; then
        cp -R "$HOME/.claude/$dir" "$BACKUP_DIR/"
    fi
done

for file in SESSION-MEMORY.md WORKING-CONTEXT.md CLAUDE.md; do
    if [ -f "$HOME/.claude/$file" ]; then
        cp "$HOME/.claude/$file" "$BACKUP_DIR/"
    fi
done

echo "   ✅ Current state backed up to $BACKUP_DIR"

# Download from S3
echo ""
echo "☁️  Downloading from S3..."
RESTORE_DIR="$HOME/.claude/s3-restore"
mkdir -p "$RESTORE_DIR"

aws s3 cp "s3://$S3_BUCKET/claude-backups/$backup_file" "$RESTORE_DIR/$backup_file"

if [ $? -ne 0 ]; then
    echo "❌ Download failed"
    exit 1
fi

echo "   ✅ Downloaded successfully"

# Extract backup
echo ""
echo "📦 Extracting backup..."
cd "$RESTORE_DIR"
tar -xzf "$backup_file"

BACKUP_FOLDER=$(basename "$backup_file" .tar.gz)

if [ ! -d "$BACKUP_FOLDER" ]; then
    echo "❌ Backup extraction failed"
    exit 1
fi

echo "   ✅ Extracted successfully"

# Show manifest
if [ -f "$BACKUP_FOLDER/MANIFEST.txt" ]; then
    echo ""
    echo "📋 Backup Manifest:"
    cat "$BACKUP_FOLDER/MANIFEST.txt"
    echo ""
fi

# Restore files
echo ""
echo "📥 Restoring files..."

# Restore session archives
if [ -d "$BACKUP_FOLDER/session-archives" ]; then
    mkdir -p "$HOME/.claude/session-archive"
    cp -R "$BACKUP_FOLDER/session-archives"/* "$HOME/.claude/session-archive/" 2>/dev/null || true
    echo "   ✅ Session archives restored"
fi

# Restore projects
if [ -d "$BACKUP_FOLDER/projects" ]; then
    mkdir -p "$HOME/.claude/projects"
    cp -R "$BACKUP_FOLDER/projects"/* "$HOME/.claude/projects/" 2>/dev/null || true
    echo "   ✅ Project workspaces restored"
fi

# Restore memory files
if [ -d "$BACKUP_FOLDER/memory" ]; then
    cp "$BACKUP_FOLDER/memory"/* "$HOME/.claude/" 2>/dev/null || true
    echo "   ✅ Memory files restored"
fi

# Restore documentation
if [ -d "$BACKUP_FOLDER/docs" ]; then
    cp "$BACKUP_FOLDER/docs"/* "$HOME/.claude/" 2>/dev/null || true
    echo "   ✅ Documentation restored"
fi

# Restore utilities (optional)
if [ -d "$BACKUP_FOLDER/utilities" ]; then
    read -p "Restore utilities repository? (y/N): " restore_utils
    if [[ "$restore_utils" =~ ^[Yy]$ ]]; then
        mkdir -p "$HOME/.claude/projects/utilities-repo-setup"
        cp -R "$BACKUP_FOLDER/utilities"/* "$HOME/.claude/projects/utilities-repo-setup/" 2>/dev/null || true
        echo "   ✅ Utilities restored"
    fi
fi

# Cleanup
echo ""
echo "🧹 Cleaning up..."
rm -rf "$RESTORE_DIR"
echo "   ✅ Cleanup complete"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              Restore Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Restored from: $backup_file"
echo "Pre-restore backup: $BACKUP_DIR"
echo ""
echo "You can now resume work with restored data."
echo ""
