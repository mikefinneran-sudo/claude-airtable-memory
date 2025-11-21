#!/bin/bash
# Toggle Wispr Flow on/off

# Check if Wispr Flow is running
if pgrep -x "Wispr Flow" > /dev/null; then
    echo "🛑 Stopping Wispr Flow..."
    osascript -e 'quit app "Wispr Flow"'
    sleep 0.5
    # Force kill if still running
    killall "Wispr Flow" 2>/dev/null
    echo "✓ Wispr Flow stopped"
else
    echo "🎙️ Starting Wispr Flow..."
    open -a "Wispr Flow"
    echo "✓ Wispr Flow started"
fi
