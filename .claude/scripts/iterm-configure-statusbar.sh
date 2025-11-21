#!/bin/bash
# Configure iTerm2 Status Bar
# Adds useful components for development workflow

echo "=== iTerm2 Status Bar Configuration ==="
echo ""
echo "This script will guide you through setting up a useful status bar."
echo ""
echo "Recommended components:"
echo "  1. Current Directory - Shows working directory"
echo "  2. Git Branch - Shows current git branch and status"
echo "  3. CPU Utilization - Monitor system load"
echo "  4. Memory Utilization - Track memory usage"
echo "  5. Network Throughput - See network activity"
echo "  6. Clock - Current time"
echo ""
echo "Manual setup required:"
echo "  1. iTerm2 > Settings > Profiles > Session"
echo "  2. Check 'Status bar enabled'"
echo "  3. Click 'Configure Status Bar'"
echo "  4. Drag components from bottom to top bar:"
echo "     - Current Directory (left)"
echo "     - Git Branch (left)"
echo "     - CPU % (right)"
echo "     - Memory (right)"
echo "     - Clock (right)"
echo "  5. Click 'Auto-Rainbow' for automatic colors"
echo ""

# Enable status bar in preferences
defaults write com.googlecode.iterm2 "ShowStatusBar" -bool true

# Status bar configuration (manual import required)
cat > /tmp/iterm2-statusbar-config.json << 'EOF'
{
  "components": [
    {
      "class": "iTermStatusBarWorkingDirectoryComponent",
      "configuration": {
        "knobs": {
          "base": 0,
          "maxrenderwidth": 0.3,
          "minwidth": 0.1,
          "path": "path"
        }
      }
    },
    {
      "class": "iTermStatusBarGitComponent",
      "configuration": {
        "knobs": {
          "base": 0,
          "maxrenderwidth": 0.25,
          "minwidth": 0.1
        }
      }
    },
    {
      "class": "iTermStatusBarCPUUtilizationComponent",
      "configuration": {
        "knobs": {
          "base": 1,
          "maxrenderwidth": 0.1,
          "minwidth": 0.05
        }
      }
    },
    {
      "class": "iTermStatusBarMemoryUtilizationComponent",
      "configuration": {
        "knobs": {
          "base": 1,
          "maxrenderwidth": 0.1,
          "minwidth": 0.05
        }
      }
    },
    {
      "class": "iTermStatusBarClockComponent",
      "configuration": {
        "knobs": {
          "base": 1,
          "format": 0,
          "maxrenderwidth": 0.15,
          "minwidth": 0.1
        }
      }
    }
  ],
  "advanced configuration": {
    "font": "Monaco 12",
    "algorithm": 0
  }
}
EOF

echo "Status bar configuration created: /tmp/iterm2-statusbar-config.json"
echo ""
echo "To apply: iTerm2 > Settings > Profiles > Session > Configure Status Bar"
echo ""
echo "Status bar is now enabled. Restart iTerm2 to see changes."
