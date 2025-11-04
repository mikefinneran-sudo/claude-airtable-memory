---
description: Add item to backlog and close tab
---

You are helping the user add an item to their backlog and maintain a tidy workspace.

## Your Task

1. **Identify the correct backlog file:**
   - If the conversation is about FlyFlat: `/Users/mikefinneran/Documents/ObsidianVault/BACKLOG-FlyFlat.md`
   - If the conversation is about WalterSignal or general work: `/Users/mikefinneran/Documents/ObsidianVault/BACKLOG.md`
   - If unclear, ask the user which backlog to use

2. **Read the backlog file** to understand the current structure and find the right section

3. **Add the new item** in the appropriate priority section:
   - Critical Priority (🔥) - Blocking revenue, SLA misses, customer complaints
   - High Priority (🚀) - Clear ROI, team productivity, customer experience
   - Medium Priority (📊) - Good idea, needs validation, longer timeline

4. **Format the entry** using this template:
   ```markdown
   ### [Number]. [Task Name]
   **Status:** [Planning/Ready/In Progress/Blocked]
   **Owner:** [Name]
   **Created:** [Today's date]
   **From:** [Source - e.g., "User request", "L10 Meeting", etc.]

   **Concept:** [One-line description]

   **Problem:**
   - [Key pain points]

   **Solution:**
   - [Proposed approach]

   **Impact:**
   - [Expected outcomes]

   **Next Steps:**
   1. [Action item 1]
   2. [Action item 2]
   ```

5. **Update backlog stats** at the bottom of the file:
   - Total Items count
   - Priority breakdown
   - Last Review date (today)

6. **Inform the user** what was added and confirm the tab will close

## Important Notes

- Keep the entry concise but informative
- Use the existing backlog style and formatting
- Increment the item number correctly
- If this relates to work already done, mark status as "Ready" or "Complete"
- Always update the "Last Updated" date at the top of the file

## After Completion

Tell the user:
"✅ Added to [FlyFlat/Main] backlog as [Priority] #[Number]

You can close this tab now - everything is saved in the backlog!"

Do NOT actually close the tab - the user will do that manually. Just give them confirmation that it's safe to close.
