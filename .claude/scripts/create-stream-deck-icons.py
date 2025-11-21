#!/usr/bin/env python3
"""
Create custom Stream Deck icons with clear labels
Resolution: 144x144 pixels (standard Stream Deck size)
"""

from PIL import Image, ImageDraw, ImageFont
import os

ICON_SIZE = 144
OUTPUT_DIR = os.path.expanduser("~/.claude/stream-deck-icons")

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_icon(filename, bg_color, emoji, label, label_color="#FFFFFF"):
    """Create a Stream Deck icon with emoji and label"""
    img = Image.new('RGB', (ICON_SIZE, ICON_SIZE), bg_color)
    draw = ImageDraw.Draw(img)

    # Try to use system fonts
    try:
        emoji_font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 60)
        label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        emoji_font = ImageFont.load_default()
        label_font = ImageFont.load_default()

    # Draw emoji in center-top
    emoji_bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    emoji_height = emoji_bbox[3] - emoji_bbox[1]
    emoji_x = (ICON_SIZE - emoji_width) // 2
    emoji_y = 20
    draw.text((emoji_x, emoji_y), emoji, font=emoji_font, fill=label_color)

    # Draw label at bottom
    label_bbox = draw.textbbox((0, 0), label, font=label_font)
    label_width = label_bbox[2] - label_bbox[0]
    label_x = (ICON_SIZE - label_width) // 2
    label_y = ICON_SIZE - 30
    draw.text((label_x, label_y), label, font=label_font, fill=label_color)

    # Save
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    print(f"✓ Created: {filename}")
    return filepath

# Main workspace launcher
create_icon("launch-workspace.png", "#2E3440", "🚀", "WORKSPACE", "#88C0D0")

# Rectangle Pro - Window Management
create_icon("window-left.png", "#3B4252", "◀️", "LEFT HALF", "#81A1C1")
create_icon("window-right.png", "#3B4252", "▶️", "RIGHT HALF", "#81A1C1")
create_icon("window-maximize.png", "#3B4252", "⬜", "MAXIMIZE", "#81A1C1")
create_icon("window-center.png", "#3B4252", "🎯", "CENTER", "#81A1C1")
create_icon("window-top-left.png", "#434C5E", "↖️", "TOP LEFT", "#88C0D0")
create_icon("window-top-right.png", "#434C5E", "↗️", "TOP RIGHT", "#88C0D0")
create_icon("window-bottom-left.png", "#434C5E", "↙️", "BOTTOM LEFT", "#88C0D0")
create_icon("window-bottom-right.png", "#434C5E", "↘️", "BOTTOM RIGHT", "#88C0D0")

# WhisperFlow / Wispr Flow
create_icon("whisper-record.png", "#BF616A", "🎙️", "RECORD", "#ECEFF4")
create_icon("whisper-stop.png", "#D08770", "⏹️", "STOP", "#ECEFF4")
create_icon("whisper-open.png", "#5E81AC", "🗣️", "WISPR FLOW", "#ECEFF4")

# Project Switching
create_icon("project-waltersignal.png", "#8FBCBB", "🚀", "WALTER\nSIGNAL", "#2E3440")
create_icon("project-vault.png", "#A3BE8C", "📝", "OBSIDIAN", "#2E3440")
create_icon("project-research.png", "#B48EAD", "🔬", "RESEARCH", "#2E3440")
create_icon("project-admin.png", "#EBCB8B", "📧", "ADMIN", "#2E3440")

# iTerm2 Layouts
create_icon("iterm-tdd.png", "#4C566A", "⚡", "TDD LAYOUT", "#88C0D0")
create_icon("iterm-fullstack.png", "#4C566A", "🔥", "FULL STACK", "#88C0D0")

# Quick Actions
create_icon("context-load.png", "#5E81AC", "🧠", "CONTEXT", "#ECEFF4")
create_icon("session-save.png", "#81A1C1", "💾", "SAVE", "#ECEFF4")
create_icon("daily-note.png", "#88C0D0", "📅", "DAILY NOTE", "#2E3440")
create_icon("airtable-sync.png", "#A3BE8C", "🔄", "AT SYNC", "#2E3440")
create_icon("s3-backup.png", "#8FBCBB", "☁️", "BACKUP", "#2E3440")

# System actions
create_icon("close-apps.png", "#BF616A", "❌", "CLOSE ALL", "#ECEFF4")
create_icon("refresh.png", "#EBCB8B", "🔃", "REFRESH", "#2E3440")

print("\n✅ All icons created!")
print(f"Location: {OUTPUT_DIR}")
print("\nTo use in Stream Controller:")
print("1. Right-click Stream Deck button")
print("2. Select 'Custom Image' or 'Icon'")
print(f"3. Browse to: {OUTPUT_DIR}")
print("4. Select the appropriate icon")
