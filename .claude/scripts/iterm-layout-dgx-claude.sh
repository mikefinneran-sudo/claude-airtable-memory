#!/bin/bash
# Launch DGX Spark Claude Code environment
# Layout: Claude Code (Left) | GPU Monitor (Right)

osascript << 'EOF'
tell application "iTerm"
    create window with default profile
    tell current session of current window
        set name to "DGX Claude Code"

        -- Connect to DGX with tmux integration
        write text "ssh mikefinneran@192.168.68.88 -t 'tmux -CC new -A -s dgx-claude'"
        delay 3

        -- Navigate to projects and launch Claude
        write text "cd ~/projects 2>/dev/null || mkdir -p ~/projects && cd ~/projects"
        write text "clear"
        write text "~/dgx-launch-claude.sh"

        -- Split vertically for GPU monitoring
        tell (split vertically with default profile)
            set name to "GPU Monitor"
            write text "ssh mikefinneran@192.168.68.88"
            delay 2
            write text "clear"
            write text "watch -n 2 -c 'nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv,noheader,nounits'"
        end tell
    end tell
end tell
EOF

echo "DGX Spark Claude Code layout launched"
echo "Left: Claude Code | Right: GPU Monitor"
