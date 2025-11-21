#!/bin/bash
# Optimize browser window for bottom third of vertical display

echo "🔧 Optimizing browser for vertical display bottom..."

# ============================================
# VERTICAL DISPLAY - Bottom third (Comet)
# ============================================

# Place a Comet window at bottom of vertical display
# Bottom third: 1080x640px at position (3440, 1280)
osascript <<'EOF'
tell application "System Events"
    tell process "Comet"
        try
            -- Find a suitable Comet window (preferably Meet or a secondary window)
            set allWindows to every window
            if (count of allWindows) ≥ 3 then
                -- Use third window for vertical bottom
                set position of window 3 to {3440, 1280}
                set size of window 3 to {1080, 640}
            else if (count of allWindows) = 2 then
                -- Create space by using second window
                set position of window 2 to {3440, 1280}
                set size of window 2 to {1080, 640}
            end if
        end try
    end tell
end tell
EOF

echo "✅ Browser optimized for vertical display!"
echo ""
echo "Layout:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Vertical Display (1080x1920):"
echo "  Top: Slack (1080x640)"
echo "  Middle: WhatsApp (1080x640)"
echo "  Bottom: Comet Browser (1080x640)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
