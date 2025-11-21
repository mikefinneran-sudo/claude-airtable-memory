#!/bin/bash

# Knowledge Base Sync Script
# Syncs to Google Drive, Spark, and Airtable

LOG_FILE="$HOME/.claude/logs/knowledge-base-sync.log"
KB_PATH="$HOME/Documents/ObsidianVault/Knowledge-Base"
GDRIVE_PATH="$HOME/Library/CloudStorage/GoogleDrive-mike.finneran@gmail.com/My Drive/Knowledge-Base"
SPARK_HOST="mikefinneran@192.168.68.62"

echo "=== Knowledge Base Sync Started: $(date) ===" >> "$LOG_FILE"

# 1. Sync to Google Drive
echo "Syncing to Google Drive..." >> "$LOG_FILE"
rsync -av "$KB_PATH/" "$GDRIVE_PATH/" >> "$LOG_FILE" 2>&1

# 2. Sync to Spark
echo "Syncing to Spark..." >> "$LOG_FILE"
rsync -avz -e "ssh -o StrictHostKeyChecking=no" \
  "$KB_PATH/" "$SPARK_HOST:~/Knowledge-Base/" >> "$LOG_FILE" 2>&1

# 3. Update Airtable index
echo "Updating Airtable index..." >> "$LOG_FILE"
python3 "$HOME/.claude/scripts/index-knowledge-base.py" >> "$LOG_FILE" 2>&1

echo "=== Sync Completed: $(date) ===" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

