#!/bin/bash

# FlyFlat Weekly Update Generator
# Runs every Friday at 12 PM ET
# Generates update email for Omar

set -e

# Paths
VAULT_PATH="/Users/mikefinneran/Documents/ObsidianVault"
FLYFLAT_DIR="$VAULT_PATH/Projects/FlyFlat"
UPDATES_DIR="$FLYFLAT_DIR/Weekly-Updates"
TODAY=$(date +%Y-%m-%d)
WEEK_NUM=$(date +%U)
UPDATE_FILE="$UPDATES_DIR/$TODAY-Week-$WEEK_NUM-Update.md"

# Create directory if needed
mkdir -p "$UPDATES_DIR"

# Get last 7 days of activity
LAST_WEEK=$(date -v-7d +%Y-%m-%d)

# Generate update
cat > "$UPDATE_FILE" <<EOF
---
type: weekly-update
date: $TODAY
week: $WEEK_NUM
recipient: Omar
project: FlyFlat
status: draft
---

# FlyFlat Weekly Update - Week $WEEK_NUM
**Date:** $(date +"%B %d, %Y")
**To:** Omar
**From:** Mike Finneran

---

## 📊 Executive Summary

**This Week's Focus:**
- [Add primary focus area]

**Key Metrics:**
- Hours worked: [X hours]
- Deliverables completed: [X]
- Client meetings: [X]
- Revenue impact: [\$X]

**Status:** 🟢 On Track / 🟡 Attention Needed / 🔴 Blocked

---

## ✅ Completed This Week

### Major Accomplishments
- [ ] [Accomplishment 1]
- [ ] [Accomplishment 2]
- [ ] [Accomplishment 3]

### Client Work
- **[Client Name]**: [What was delivered]
- **[Client Name]**: [What was delivered]

### Internal Projects
- [Project updates]

---

## 🎯 In Progress

### This Week
- [ ] [Active task 1]
- [ ] [Active task 2]
- [ ] [Active task 3]

### Blocked/Waiting On
- [Any blockers or dependencies]

---

## 📅 Next Week's Plan

### Priorities (Week $(date -v+7d +%U))
1. [Top priority]
2. [Second priority]
3. [Third priority]

### Scheduled Meetings
- [Date/Time]: [Meeting description]

### Expected Deliverables
- [Deliverable 1] - Due [date]
- [Deliverable 2] - Due [date]

---

## 💰 Financial Update

**This Week:**
- Billable hours: [X]
- Non-billable hours: [X]
- Revenue generated: \$[X]

**Month to Date:**
- Total hours: [X]
- Total revenue: \$[X]
- Budget vs. actual: [status]

---

## 🚨 Issues & Concerns

### Blockers
- [None / List any blockers]

### Risks
- [None / List any risks]

### Requests
- [Any support needed from Omar]

---

## 📈 Metrics & KPIs

| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| Client satisfaction | [X/10] | [X/10] | ⬆️/⬇️/➡️ |
| On-time delivery | [X%] | [X%] | ⬆️/⬇️/➡️ |
| Utilization rate | [X%] | [X%] | ⬆️/⬇️/➡️ |

---

## 💡 Opportunities

- [New opportunity 1]
- [New opportunity 2]

---

## 📝 Notes

**Feedback from last week:**
- [Any follow-up from previous update]

**Additional context:**
- [Any other relevant information]

---

**Next Update:** $(date -v+7d +"%B %d, %Y")

---

*Generated automatically - Edit before sending*
*Save final version to: Projects/FlyFlat/Weekly-Updates/*
EOF

# Open in default editor
echo "✅ FlyFlat Weekly Update created: $UPDATE_FILE"
echo ""
echo "📝 Opening in Obsidian..."

# Log
echo "$(date): Created FlyFlat update for week $WEEK_NUM" >> "$VAULT_PATH/.scripts/flyflat-updates.log"

# Auto-sync to Notion (if configured)
if [ -f "$VAULT_PATH/.scripts/sync_to_notion.py" ]; then
    echo ""
    echo "🔄 Syncing to Notion..."
    python3 "$VAULT_PATH/.scripts/sync_to_notion.py" --folder "Projects/FlyFlat/Weekly-Updates" 2>&1 | tee -a "$VAULT_PATH/.scripts/flyflat-updates.log"
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo "✅ Synced to Notion"
    else
        echo "⚠️  Notion sync failed (check logs)"
    fi
fi

exit 0
