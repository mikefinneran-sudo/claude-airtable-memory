#!/bin/bash

# Enhanced Daily Note Creator for LifeHub 2.0
# Creates daily note with basic structure that can be enhanced in Obsidian

VAULT_PATH="$HOME/Documents/ObsidianVault"
DAILY_DIR="$VAULT_PATH/Daily"
TODAY=$(date +%Y-%m-%d)
DAY_NAME=$(date +%A)
FULL_DATE=$(date +"%A, %B %d %Y")
DAILY_NOTE="$DAILY_DIR/$TODAY.md"

# Ensure Daily directory exists
mkdir -p "$DAILY_DIR"

# Check if today's note already exists
if [ -f "$DAILY_NOTE" ]; then
    echo "✅ Daily note for $TODAY already exists"
    open "obsidian://open?vault=ObsidianVault&file=Daily/$TODAY"
    exit 0
fi

# Create enhanced daily note
cat > "$DAILY_NOTE" << 'TEMPLATE'
---
date: DATEVAR
type: daily-note
day-of-week: DAYVAR
week: WEEKVAR
month: MONTHVAR
energy-level:
mood:
---

# 📅 FULLDATEVAR

[[Daily/YESTERDAYVAR|← Yesterday]] | [[Daily/TOMORROWVAR|Tomorrow →]]

---

## 🌅 Morning Setup

### Today's Intention
_What's my primary focus for today?_

### Top 3 Priorities
1. [ ]
2. [ ]
3. [ ]

### Energy Level: ___ /10
### Mood: ___

---

## 📋 Tasks

### Must Do Today
_High priority tasks with deadlines_

- [ ]

### Active Projects Check-in
_Current projects I'm working on_

**LifeHub 2.0:**
- [ ]

**Other Projects:**
- [ ]

---

## 💰 Business Metrics

### Revenue Today
- Amount: $
- Source:
- Notes:

### Customer Activity
- New leads:
- Conversations:
- Sales calls:

---

## 📧 Communications

### Emails
- Inbox zero? [ ]
- Priority responses: [ ]
- Follow-ups needed:

### Meetings
-

---

## 🎯 Habit Tracker

- [ ] Morning routine
- [ ] Exercise
- [ ] Deep work (2+ hours)
- [ ] Learning (30+ min)
- [ ] Writing
- [ ] Reach out to 1 person
- [ ] Review finances
- [ ] Evening planning

---

## ⏰ Time Log

### Morning


### Afternoon


### Evening


---

## 💡 Captures & Ideas

### Quick Notes
-

### Ideas for Later
-

---

## 🏆 Wins Today

### Small Wins
-

### Big Win
-

---

## 🌙 Evening Reflection

### What Went Well?
-

### What Could Be Better?
-

### Tomorrow's Focus
1.
2.
3.

### Gratitude
1.
2.
3.

---

## 📊 Daily Stats

**Energy Level**: ___ /10
**Productivity**: ___ /10
**Satisfaction**: ___ /10

---

## 🔗 Related

- [[Dashboard]]
- [[Projects/LifeHub/lifehub-overview|LifeHub 2.0]]

---

*Created: TIMESTAMPVAR*
*Template: Daily Note Enhanced v2.0*
TEMPLATE

# Replace placeholders
YESTERDAY=$(date -v-1d +%Y-%m-%d)
TOMORROW=$(date -v+1d +%Y-%m-%d)
WEEK=$(date +%Y-W%U)
MONTH=$(date +%Y-%m)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

sed -i '' "s/DATEVAR/$TODAY/g" "$DAILY_NOTE"
sed -i '' "s/DAYVAR/$DAY_NAME/g" "$DAILY_NOTE"
sed -i '' "s/FULLDATEVAR/$FULL_DATE/g" "$DAILY_NOTE"
sed -i '' "s/YESTERDAYVAR/$YESTERDAY/g" "$DAILY_NOTE"
sed -i '' "s/TOMORROWVAR/$TOMORROW/g" "$DAILY_NOTE"
sed -i '' "s/WEEKVAR/$WEEK/g" "$DAILY_NOTE"
sed -i '' "s/MONTHVAR/$MONTH/g" "$DAILY_NOTE"
sed -i '' "s/TIMESTAMPVAR/$TIMESTAMP/g" "$DAILY_NOTE"

echo "✨ Created daily note for $TODAY"
echo "📝 Opening in Obsidian..."

# Open in Obsidian
open "obsidian://open?vault=ObsidianVault&file=Daily/$TODAY"

exit 0
