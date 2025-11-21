#!/bin/bash
# Sync Google Drive data to DGX Spark external storage

GDRIVE_PATH="$HOME/Library/CloudStorage/GoogleDrive-mike.finneran@gmail.com/My Drive"
DGX_HOST="mikefinneran@192.168.68.62"
DGX_PATH="/mnt/models/google-drive-archive"

echo "=== Google Drive → DGX Spark Sync ==="
echo ""
echo "Source: $GDRIVE_PATH"
echo "Destination: $DGX_HOST:$DGX_PATH"
echo ""

# Create destination directory on DGX
echo "Creating destination directory..."
ssh $DGX_HOST "mkdir -p $DGX_PATH"

# Sync with rsync (resume-capable, shows progress)
echo ""
echo "Starting sync (this will take a while for 250GB)..."
echo "Press Ctrl+C to pause. Re-run this script to resume."
echo ""

rsync -avhP --stats \
  --exclude '.DS_Store' \
  --exclude '.Trash' \
  --exclude '.tmp' \
  "$GDRIVE_PATH/" \
  "$DGX_HOST:$DGX_PATH/"

echo ""
echo "=== Sync Complete ==="
ssh $DGX_HOST "du -sh $DGX_PATH"
