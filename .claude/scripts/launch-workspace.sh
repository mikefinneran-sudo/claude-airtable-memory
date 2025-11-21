#!/bin/bash
# Master Workspace Layout - One Button Launch
# Displays: 3440x1440 Ultrawide | 1080x1920 Vertical | Laptop (blank)

echo "🚀 Launching Master Workspace..."

# ============================================
# ULTRAWIDE DISPLAY (3440x1440) - Main Monitor
# ============================================

# LEFT THIRD TOP - Obsidian (1147x710)
echo "📝 Opening Obsidian..."
open -a "Obsidian"
sleep 2
osascript <<'EOF'
tell application "System Events"
    tell process "Obsidian"
        set position of front window to {0, 25}
        set size of front window to {1147, 710}
    end tell
end tell
EOF

# LEFT THIRD BOTTOM - Superhuman (1147x705)
echo "📧 Opening Superhuman..."
open -a "Superhuman"
sleep 2
osascript <<'EOF'
tell application "System Events"
    tell process "Superhuman"
        set position of front window to {0, 735}
        set size of front window to {1147, 705}
    end tell
end tell
EOF

# MIDDLE THIRD - iTerm2 (1147x1415 full height)
echo "💻 Opening iTerm2..."
open -a "iTerm"
sleep 2
osascript <<'EOF'
tell application "System Events"
    tell process "iTerm2"
        set position of front window to {1147, 25}
        set size of front window to {1147, 1415}
    end tell
end tell
EOF

# RIGHT THIRD - Comet Browser windows (1155px width)
echo "🌐 Opening Comet Browser..."
open -a "Comet"
sleep 3
osascript <<'EOF'
tell application "System Events"
    tell process "Comet"
        try
            set allWindows to every window
            if (count of allWindows) ≥ 1 then
                -- Main browser window - top half
                set position of window 1 to {2285, 25}
                set size of window 1 to {1155, 710}
            end if
            if (count of allWindows) ≥ 2 then
                -- Second browser window - bottom half
                set position of window 2 to {2285, 735}
                set size of window 2 to {1155, 705}
            end if
        end try
    end tell
end tell
EOF

# ============================================
# VERTICAL DISPLAY (1080x1920) - Portrait
# ============================================

# TOP - Slack (1080x640)
echo "💬 Opening Slack..."
open -a "Slack"
sleep 2
osascript <<'EOF'
tell application "System Events"
    tell process "Slack"
        set position of front window to {3440, 0}
        set size of front window to {1080, 640}
    end tell
end tell
EOF

# MIDDLE - WhatsApp Business (1080x640)
echo "📱 Opening WhatsApp..."
open -a "WhatsApp"
sleep 2
osascript <<'EOF'
tell application "System Events"
    tell process "WhatsApp"
        set position of front window to {3440, 640}
        set size of front window to {1080, 640}
    end tell
end tell
EOF

# BOTTOM - Comet Browser (1080x640)
echo "🌐 Positioning Comet on vertical display..."
sleep 2
osascript <<'EOF'
tell application "System Events"
    tell process "Comet"
        try
            set allWindows to every window
            if (count of allWindows) ≥ 3 then
                -- Use third window for vertical bottom
                set position of window 3 to {3440, 1280}
                set size of window 3 to {1080, 640}
            end if
        end try
    end tell
end tell
EOF

echo ""
echo "✅ Workspace Ready!"
echo ""
echo "Layout Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ultrawide (3440x1440):"
echo "  Left Top: Obsidian (1147x710)"
echo "  Left Bottom: Superhuman (1147x705)"
echo "  Middle: iTerm2 (1147x1415)"
echo "  Right Top: Comet (1155x710)"
echo "  Right Bottom: Comet (1155x705)"
echo ""
echo "Vertical (1080x1920):"
echo "  Top: Slack (1080x640)"
echo "  Middle: WhatsApp (1080x640)"
echo "  Bottom: Comet (1080x640)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
