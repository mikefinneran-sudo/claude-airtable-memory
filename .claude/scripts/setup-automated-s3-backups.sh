#!/bin/bash
# Setup Automated Daily S3 Backups via cron or launchd

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           Automated S3 Backup Scheduler Setup                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "Choose backup schedule:"
echo "1. Daily (recommended) - 2 AM every day"
echo "2. Weekly - Sunday 2 AM"
echo "3. Custom cron schedule"
echo ""
read -p "Enter choice (1-3): " schedule_choice

BACKUP_SCRIPT="$HOME/.claude/scripts/backup-to-s3.sh"

if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo "❌ Backup script not found: $BACKUP_SCRIPT"
    exit 1
fi

# macOS uses launchd instead of cron
echo ""
echo "Setting up launchd job for macOS..."

PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$PLIST_DIR/com.claude.s3backup.plist"

mkdir -p "$PLIST_DIR"

case $schedule_choice in
    1)
        # Daily at 2 AM
        cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.s3backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>$BACKUP_SCRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/.claude/logs/s3-backup.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.claude/logs/s3-backup-error.log</string>
</dict>
</plist>
EOF
        echo "✅ Daily backup scheduled for 2:00 AM"
        ;;

    2)
        # Weekly on Sunday at 2 AM
        cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.s3backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>$BACKUP_SCRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/.claude/logs/s3-backup.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.claude/logs/s3-backup-error.log</string>
</dict>
</plist>
EOF
        echo "✅ Weekly backup scheduled for Sunday 2:00 AM"
        ;;

    3)
        echo ""
        echo "For custom schedules, edit the plist file manually:"
        echo "   $PLIST_FILE"
        echo ""
        echo "Creating basic daily template..."

        cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.s3backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>$BACKUP_SCRIPT</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/.claude/logs/s3-backup.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.claude/logs/s3-backup-error.log</string>
</dict>
</plist>
EOF
        echo "✅ Template created (daily at 2 AM)"
        echo "   Edit $PLIST_FILE to customize"
        ;;

    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Create logs directory
mkdir -p "$HOME/.claude/logs"

# Load the launch agent
echo ""
echo "📥 Loading launch agent..."
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Launch agent loaded successfully"
else
    echo "⚠️  Launch agent load failed (may need to restart)"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║               Automated Backups Configured!                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Configuration:"
echo "   Plist: $PLIST_FILE"
echo "   Script: $BACKUP_SCRIPT"
echo "   Logs: $HOME/.claude/logs/"
echo ""
echo "Commands:"
echo "   View status: launchctl list | grep claude"
echo "   Unload: launchctl unload $PLIST_FILE"
echo "   Reload: launchctl load $PLIST_FILE"
echo "   Test now: $BACKUP_SCRIPT"
echo ""
echo "Logs:"
echo "   tail -f ~/.claude/logs/s3-backup.log"
echo ""
