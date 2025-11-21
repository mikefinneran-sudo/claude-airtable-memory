#!/bin/bash
# Optimize window sizes for readability - keeps positions, improves sizes

echo "🎯 Optimizing window sizes for readability..."

# ============================================
# LEFT THIRD - Obsidian & Superhuman
# ============================================

# Obsidian - Top half, optimized for note reading (1147x720)
osascript <<EOF
tell application "System Events"
    tell process "Obsidian"
        set position of front window to {0, 25}
        set size of front window to {1147, 710}
    end tell
end tell
EOF

# Superhuman - Bottom half, optimized for email list + preview (1147x710)
osascript <<EOF
tell application "System Events"
    tell process "Superhuman"
        set position of front window to {0, 735}
        set size of front window to {1147, 705}
    end tell
end tell
EOF

# ============================================
# MIDDLE THIRD - iTerm2 (already perfect!)
# ============================================
echo "✓ iTerm2 already optimized"

# ============================================
# RIGHT THIRD - Comet Browser
# ============================================

# Comet main windows - Stacked for easy switching
# Top window - Workona (1155x710)
osascript <<EOF
tell application "System Events"
    tell process "Comet"
        try
            set win1 to window "Workona - Comet"
            set position of win1 to {2285, 25}
            set size of win1 to {1155, 710}
        end try
    end tell
end tell
EOF

# Bottom window - Gemini (1155x705)
osascript <<EOF
tell application "System Events"
    tell process "Comet"
        try
            set win2 to window "Google Gemini - Comet"
            set position of win2 to {2285, 735}
            set size of win2 to {1155, 705}
        end try
    end tell
end tell
EOF

# ============================================
# VERTICAL DISPLAY - Slack, WhatsApp, Granola
# ============================================

# Slack - Top third (1080x640)
osascript <<EOF
tell application "System Events"
    tell process "Slack"
        set position of front window to {3440, 0}
        set size of front window to {1080, 640}
    end tell
end tell
EOF

# WhatsApp - Middle third (1080x640)
osascript <<EOF
tell application "System Events"
    tell process "WhatsApp"
        set position of front window to {3440, 640}
        set size of front window to {1080, 640}
    end tell
end tell
EOF

# Granola - Bottom third (1080x640)
osascript <<EOF
tell application "System Events"
    tell process "Granola"
        set position of front window to {3440, 1280}
        set size of front window to {1080, 640}
    end tell
end tell
EOF

echo "✅ Workspace optimized for readability!"
echo ""
echo "Optimized Layout:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Ultrawide Left (1147px):"
echo "  Top: Obsidian (710px) - Note reading"
echo "  Bottom: Superhuman (705px) - Email list + preview"
echo ""
echo "Ultrawide Middle (1147px):"
echo "  iTerm2 (full height) - Terminal work"
echo ""
echo "Ultrawide Right (1155px):"
echo "  Top: Comet/Workona (710px) - Tab management"
echo "  Bottom: Comet/Gemini (705px) - AI assistant"
echo ""
echo "Vertical Portrait (1080px):"
echo "  Top: Slack (640px) - Team chat"
echo "  Middle: WhatsApp (640px) - Messages"
echo "  Bottom: Granola (640px) - Meeting notes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
