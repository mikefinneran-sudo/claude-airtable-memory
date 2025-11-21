#!/bin/bash
# Optimize browser windows and vertical display bottom

echo "🔧 Optimizing browser and vertical display..."

# ============================================
# RIGHT THIRD - Comet Browser Windows
# ============================================

# Make Comet windows easier to read and switch between
# Top window - Full width, better height for web content
osascript <<'EOF'
tell application "System Events"
    tell process "Comet"
        try
            -- Get all windows
            set allWindows to every window
            if (count of allWindows) ≥ 2 then
                -- Top window (first visible)
                set position of window 1 to {2285, 25}
                set size of window 1 to {1155, 710}

                -- Bottom window (second visible)
                set position of window 2 to {2285, 735}
                set size of window 2 to {1155, 705}
            else if (count of allWindows) = 1 then
                -- Only one window, make it full height
                set position of window 1 to {2285, 25}
                set size of window 1 to {1155, 1415}
            end if
        end try
    end tell
end tell
EOF

# ============================================
# VERTICAL DISPLAY - Bottom (Granola)
# ============================================

# Granola - Optimize for meeting notes readability
osascript <<'EOF'
tell application "System Events"
    tell process "Granola"
        try
            set allWindows to every window whose visible is true
            if (count of allWindows) > 0 then
                set position of window 1 to {3440, 1280}
                set size of window 1 to {1080, 640}
            end if
        on error
            -- Granola might not have a main window, try to activate it
            tell application "Granola" to activate
            delay 1
            set position of window 1 to {3440, 1280}
            set size of window 1 to {1080, 640}
        end try
    end tell
end tell
EOF

echo "✅ Browser and vertical display optimized!"
echo ""
echo "Changes made:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Comet Browser (Right third):"
echo "  - Optimized for web content readability"
echo "  - Windows stacked and aligned"
echo "  - Size: 1155px width (comfortable for most sites)"
echo ""
echo "Granola (Vertical bottom):"
echo "  - Positioned at bottom of vertical display"
echo "  - Size: 1080x640px (optimal for notes)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
