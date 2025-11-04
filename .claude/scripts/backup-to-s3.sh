#!/bin/bash
# Backup to S3 - Intelligent Session and Project Archival
# Backs up session archives, project files, and Airtable exports

set -e

S3_BUCKET="${S3_BACKUP_BUCKET}"
TIMESTAMP=$(date '+%Y-%m-%d-%H%M%S')
BACKUP_ROOT="$HOME/.claude/s3-backups"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if S3 bucket is configured
if [ -z "$S3_BUCKET" ]; then
    echo "❌ S3_BACKUP_BUCKET not set"
    echo "   Run: ~/.claude/scripts/setup-s3-integration.sh"
    exit 1
fi

# Check if AWS CLI is available
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found"
    echo "   Run: ~/.claude/scripts/setup-s3-integration.sh"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}              S3 Backup - Starting${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Create temporary backup directory
mkdir -p "$BACKUP_ROOT"
BACKUP_DIR="$BACKUP_ROOT/backup-$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup in: $BACKUP_DIR"
echo ""

# Backup 1: Session Archives
if [ -d "$HOME/.claude/session-archive" ]; then
    echo "📝 Backing up session archives..."
    session_count=$(find "$HOME/.claude/session-archive" -type f -name "*.md" | wc -l | xargs)

    mkdir -p "$BACKUP_DIR/session-archives"
    cp -R "$HOME/.claude/session-archive"/* "$BACKUP_DIR/session-archives/" 2>/dev/null || true

    echo "   ✅ $session_count session files"
fi

# Backup 2: Project Workspaces
if [ -d "$HOME/.claude/projects" ]; then
    echo "📁 Backing up project workspaces..."
    project_count=$(find "$HOME/.claude/projects" -maxdepth 1 -type d | tail -n +2 | wc -l | xargs)

    mkdir -p "$BACKUP_DIR/projects"
    cp -R "$HOME/.claude/projects"/* "$BACKUP_DIR/projects/" 2>/dev/null || true

    echo "   ✅ $project_count projects"
fi

# Backup 3: Working Context and Memory
echo "🧠 Backing up memory files..."
mkdir -p "$BACKUP_DIR/memory"

for file in SESSION-MEMORY.md WORKING-CONTEXT.md CLAUDE.md; do
    if [ -f "$HOME/.claude/$file" ]; then
        cp "$HOME/.claude/$file" "$BACKUP_DIR/memory/"
    fi
done

echo "   ✅ Memory files backed up"

# Backup 4: Configuration Files
echo "⚙️  Backing up configuration..."
mkdir -p "$BACKUP_DIR/config"

for file in setup-aliases.sh init-project-memory.sh; do
    if [ -f "$HOME/.claude/scripts/$file" ]; then
        cp "$HOME/.claude/scripts/$file" "$BACKUP_DIR/config/"
    fi
done

# Backup .zshrc (for aliases and environment variables)
if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" "$BACKUP_DIR/config/zshrc-backup"
fi

echo "   ✅ Config files backed up"

# Backup 5: Custom Scripts (from utilities repo)
if [ -d "$HOME/.claude/projects/utilities-repo-setup" ]; then
    echo "🛠  Backing up utilities repository..."

    mkdir -p "$BACKUP_DIR/utilities"
    cp -R "$HOME/.claude/projects/utilities-repo-setup"/* "$BACKUP_DIR/utilities/" 2>/dev/null || true

    echo "   ✅ Utilities backed up"
fi

# Backup 6: Documentation
echo "📚 Backing up documentation..."
mkdir -p "$BACKUP_DIR/docs"

for doc in MEMORY-OPTIMIZATION-COMPLETE.md SCRIPTS-ARCHIVAL-SYSTEM.md ACTIVITY-TRACKING-SYSTEM.md; do
    if [ -f "$HOME/.claude/$doc" ]; then
        cp "$HOME/.claude/$doc" "$BACKUP_DIR/docs/"
    fi
done

echo "   ✅ Documentation backed up"

# Create backup manifest
cat > "$BACKUP_DIR/MANIFEST.txt" <<EOF
Claude Code Backup
Created: $(date '+%Y-%m-%d %H:%M:%S')
Bucket: $S3_BUCKET
Host: $(hostname)

Contents:
- Session Archives: $session_count files
- Projects: $project_count workspaces
- Memory Files: SESSION-MEMORY.md, WORKING-CONTEXT.md
- Configuration: aliases, scripts, .zshrc
- Utilities: Custom scripts repository
- Documentation: System guides

Backup Size: $(du -sh "$BACKUP_DIR" | cut -f1)
EOF

echo ""
echo "📊 Backup Summary:"
cat "$BACKUP_DIR/MANIFEST.txt" | grep -v "^$"
echo ""

# Compress backup
echo "🗜  Compressing backup..."
cd "$BACKUP_ROOT"
tar -czf "backup-$TIMESTAMP.tar.gz" "backup-$TIMESTAMP"
COMPRESSED_SIZE=$(du -sh "backup-$TIMESTAMP.tar.gz" | cut -f1)
echo "   ✅ Compressed to $COMPRESSED_SIZE"
echo ""

# Upload to S3
echo "☁️  Uploading to S3..."
aws s3 cp "backup-$TIMESTAMP.tar.gz" "s3://$S3_BUCKET/claude-backups/backup-$TIMESTAMP.tar.gz" \
    --storage-class STANDARD_IA \
    --metadata "type=claude-backup,timestamp=$TIMESTAMP"

if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ Uploaded successfully${NC}"
    echo ""
    echo "S3 Location:"
    echo "   s3://$S3_BUCKET/claude-backups/backup-$TIMESTAMP.tar.gz"
else
    echo "   ❌ Upload failed"
    exit 1
fi

# Cleanup local backup
echo ""
echo "🧹 Cleaning up local files..."
rm -rf "$BACKUP_DIR"
rm "backup-$TIMESTAMP.tar.gz"
echo "   ✅ Local backup removed"

# List recent backups
echo ""
echo "📋 Recent backups in S3:"
aws s3 ls "s3://$S3_BUCKET/claude-backups/" --recursive | tail -5

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}              Backup Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Backup: s3://$S3_BUCKET/claude-backups/backup-$TIMESTAMP.tar.gz"
echo "Size: $COMPRESSED_SIZE"
echo ""
