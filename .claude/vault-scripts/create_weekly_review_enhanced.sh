#!/bin/bash

# Enhanced Weekly Review Creator for LifeHub 2.0
# Creates weekly review note every Sunday

VAULT_PATH="$HOME/Documents/ObsidianVault"
WEEKLY_DIR="$VAULT_PATH/Weekly"
WEEK=$(date +%Y-W%U)
WEEK_NOTE="$WEEKLY_DIR/$WEEK.md"
WEEK_START=$(date -v-sun +%Y-%m-%d)
WEEK_END=$(date -v+sat +%Y-%m-%d)
YEAR=$(date +%Y)
WEEK_NUM=$(date +%U)

# Ensure Weekly directory exists
mkdir -p "$WEEKLY_DIR"

# Check if this week's review already exists
if [ -f "$WEEK_NOTE" ]; then
    echo "✅ Weekly review for $WEEK already exists"
    open "obsidian://open?vault=ObsidianVault&file=Weekly/$WEEK"
    exit 0
fi

# Create weekly review note
cat > "$WEEK_NOTE" << 'TEMPLATE'
---
week: WEEKVAR
year: YEARVAR
week-number: WEEKNUMVAR
date-range: STARTVAR to ENDVAR
type: weekly-review
status: in-progress
---

# 📅 Weekly Review - Week WEEKNUMVAR (YEARVAR)

**Period**: STARTVAR to ENDVAR

---

## 🎯 Week Overview

### Theme of the Week
_What was this week about?_

### Overall Rating
- **Productivity**: ___ /10
- **Balance**: ___ /10
- **Satisfaction**: ___ /10

---

## ✅ Accomplishments

### Major Wins
1.
2.
3.

### Tasks Completed
-
-
-

### Projects Advanced
**LifeHub 2.0:**
-

**Other Projects:**
-

---

## 📊 Metrics & Progress

### Business Metrics
- **Revenue this week**: $
- **New customers**:
- **Customer conversations**:
- **Proposals sent**:

### Productivity Metrics
- **Deep work hours**:
- **Tasks completed**:
- **Projects active**:
- **Goals achieved**: ___ / ___

---

## 🎓 Learnings

### What Worked Well
1.
2.
3.

### What Didn't Work
1.
2.
3.

### Key Insights
-
-
-

---

## 🚧 Challenges

### Obstacles Faced
1.
2.
3.

### How I Overcame Them
-
-

### Still Blocked On
-

---

## 💡 Ideas & Captures

### New Ideas This Week
-
-
-

### To Explore Further
-
-

---

## 🎯 Next Week Planning

### Week's Theme
_What will next week be about?_

### Top 3 Goals
1. [ ]
2. [ ]
3. [ ]

### Projects to Focus On
- [ ] **LifeHub 2.0**:
- [ ] **Other**:

### Important Deadlines
-

### Time Blocks
- **Monday**:
- **Tuesday**:
- **Wednesday**:
- **Thursday**:
- **Friday**:

---

## 🎯 Habit Tracker

### Daily Habits (Days Completed)
- Morning routine: ___ / 7
- Exercise: ___ / 7
- Deep work: ___ / 7
- Learning: ___ / 7
- Writing: ___ / 7
- Evening reflection: ___ / 7

### Streaks
- **Current streak**: ___ days
- **Longest streak**: ___ days

---

## 💬 Reflections

### Energy & Wellbeing
- **Average energy**: ___ /10
- **Sleep quality**: ___ /10
- **Stress level**: ___ /10

### Work-Life Balance
_How was the balance this week?_

### Gratitude
1.
2.
3.

---

## 🔗 Related

- [[Weekly/PREVWEEKVAR|← Previous Week]]
- [[Weekly/NEXTWEEKVAR|Next Week →]]
- [[Dashboard]]
- [[Monthly/MONTHVAR|This Month]]

---

*Created: TIMESTAMPVAR*
*Template: Weekly Review Enhanced v2.0*
TEMPLATE

# Calculate previous and next week
PREV_WEEK=$(date -v-7d +%Y-W%U)
NEXT_WEEK=$(date -v+7d +%Y-W%U)
MONTH=$(date +%Y-%m)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")

# Replace placeholders
sed -i '' "s/WEEKVAR/$WEEK/g" "$WEEK_NOTE"
sed -i '' "s/YEARVAR/$YEAR/g" "$WEEK_NOTE"
sed -i '' "s/WEEKNUMVAR/$WEEK_NUM/g" "$WEEK_NOTE"
sed -i '' "s/STARTVAR/$WEEK_START/g" "$WEEK_NOTE"
sed -i '' "s/ENDVAR/$WEEK_END/g" "$WEEK_NOTE"
sed -i '' "s/PREVWEEKVAR/$PREV_WEEK/g" "$WEEK_NOTE"
sed -i '' "s/NEXTWEEKVAR/$NEXT_WEEK/g" "$WEEK_NOTE"
sed -i '' "s/MONTHVAR/$MONTH/g" "$WEEK_NOTE"
sed -i '' "s/TIMESTAMPVAR/$TIMESTAMP/g" "$WEEK_NOTE"

echo "✨ Created weekly review for week $WEEK_NUM"
echo "📝 Opening in Obsidian..."

# Open in Obsidian
open "obsidian://open?vault=ObsidianVault&file=Weekly/$WEEK"

exit 0
