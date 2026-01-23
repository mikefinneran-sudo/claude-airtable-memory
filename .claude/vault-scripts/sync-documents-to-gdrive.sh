#!/bin/bash

# LifeHub - Documents Folder Full Sync to Google Drive
# Syncs entire /Users/mikefinneran/Documents to Google Drive
# Excludes: .DS_Store, symlinks to avoid recursion

set -e  # Exit on error

# Paths
DOCS_PATH="/Users/mikefinneran/Documents"
GDRIVE_PATH="$HOME/Library/CloudStorage/GoogleDrive-mike.finneran@gmail.com/My Drive/Documents"
LOG_FILE="$DOCS_PATH/ObsidianVault/.scripts/gdrive-docs-sync.log"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✓ $1" >> "$LOG_FILE"
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ! $1" >> "$LOG_FILE"
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✗ $1" >> "$LOG_FILE"
    echo -e "${RED}[✗]${NC} $1"
}

# Header
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Documents Folder → Google Drive Full Sync"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

log "Starting full Documents sync..."

# Check source exists
if [ ! -d "$DOCS_PATH" ]; then
    log_error "Documents folder not found: $DOCS_PATH"
    exit 1
fi

# Create Google Drive destination if needed
if [ ! -d "$GDRIVE_PATH" ]; then
    log "Creating Google Drive Documents folder..."
    mkdir -p "$GDRIVE_PATH"
    log_success "Created: $GDRIVE_PATH"
fi

log_success "Google Drive available"

# Full sync using rsync
log "Syncing entire Documents folder..."
echo ""

rsync -av \
    --delete \
    --exclude='.DS_Store' \
    --exclude='*.log' \
    --exclude='GOOGLE_DRIVE_DOCUMENTS' \
    --exclude='.Trash' \
    --exclude='*.tmp' \
    --exclude='.TemporaryItems' \
    "$DOCS_PATH/" "$GDRIVE_PATH/" 2>&1 | tee -a "$LOG_FILE"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log_success "Documents sync completed successfully"
else
    log_error "Some issues during sync (check log)"
fi

# Get stats
TOTAL_SIZE=$(du -sh "$GDRIVE_PATH" 2>/dev/null | awk '{print $1}')
FILE_COUNT=$(find "$GDRIVE_PATH" -type f 2>/dev/null | wc -l | tr -d ' ')

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Sync Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
log_success "Full Documents folder synced to Google Drive"

echo ""
echo "Synced to: $GDRIVE_PATH"
echo "Total size: $TOTAL_SIZE"
echo "Total files: $FILE_COUNT"
echo ""
echo "What's included:"
echo "  ✓ ObsidianVault/ (complete - including .git, .obsidian, .scripts)"
echo "  ✓ .claude/ (Claude Code settings)"
echo "  ✓ claude-code-resources/"
echo "  ✓ All other files and folders in Documents/"
echo ""
echo "Excluded:"
echo "  ✗ .DS_Store (Mac system files)"
echo "  ✗ GOOGLE_DRIVE_DOCUMENTS (symlink to avoid recursion)"
echo "  ✗ .Trash, temp files"
echo ""

# Log file location
echo "Full log: $LOG_FILE"
echo ""

# Exit successfully
exit 0
