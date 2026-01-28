#!/bin/bash
# route-inbox-tasks.sh
# Routes tasks from Reminders Inbox to appropriate lists based on tags
# Runs via LaunchAgent every 15 minutes
#
# Routing Rules:
#   #ws     -> Work
#   #personal -> Personal
#   #grocery -> Grocery
#   #followup -> Creates calendar follow-up
#   No tag  -> Stays in Inbox for manual triage

set -euo pipefail

LOG_FILE="$HOME/.claude/logs/task-router.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "Starting task routing..."

# AppleScript to route tasks
osascript << 'EOF'
use AppleScript version "2.4"
use scripting additions

tell application "Reminders"
    -- Get or create required lists
    set listNames to {"Inbox", "Work", "Personal", "Grocery"}
    repeat with listName in listNames
        if not (exists list listName) then
            make new list with properties {name:listName}
        end if
    end repeat

    set inboxList to list "Inbox"
    set workList to list "Work"
    set personalList to list "Personal"
    set groceryList to list "Grocery"

    set movedCount to 0

    -- Get all incomplete reminders from Inbox
    set inboxReminders to (every reminder of inboxList whose completed is false)

    repeat with rem in inboxReminders
        set remName to name of rem
        set targetList to missing value
        set newName to remName

        -- Check for tags and determine destination
        if remName contains "#ws" then
            set targetList to workList
            set newName to my replaceText(remName, "#ws", "")
        else if remName contains "#work" then
            set targetList to workList
            set newName to my replaceText(remName, "#work", "")
        else if remName contains "#personal" then
            set targetList to personalList
            set newName to my replaceText(remName, "#personal", "")
        else if remName contains "#grocery" then
            set targetList to groceryList
            set newName to my replaceText(remName, "#grocery", "")
        else if remName contains "#groceries" then
            set targetList to groceryList
            set newName to my replaceText(remName, "#groceries", "")
        end if

        -- Move if we found a tag
        if targetList is not missing value then
            -- Clean up the name (trim spaces)
            set newName to my trimText(newName)

            -- Create new reminder in target list
            set newRem to make new reminder at targetList with properties {name:newName, body:body of rem}

            -- Copy due date if exists
            try
                set due date of newRem to due date of rem
            end try

            -- Copy priority if exists
            try
                set priority of newRem to priority of rem
            end try

            -- Delete from Inbox
            delete rem

            set movedCount to movedCount + 1
        end if
    end repeat

    return movedCount & " tasks routed"
end tell

on replaceText(sourceText, findText, replaceWith)
    set AppleScript's text item delimiters to findText
    set textItems to text items of sourceText
    set AppleScript's text item delimiters to replaceWith
    set resultText to textItems as text
    set AppleScript's text item delimiters to ""
    return resultText
end replaceText

on trimText(theText)
    -- Remove leading/trailing spaces
    set theText to theText as text
    repeat while theText starts with " "
        set theText to text 2 thru -1 of theText
    end repeat
    repeat while theText ends with " "
        set theText to text 1 thru -2 of theText
    end repeat
    return theText
end trimText
EOF

RESULT=$?
if [[ $RESULT -eq 0 ]]; then
    log "Task routing completed successfully"
else
    log "Task routing failed with exit code $RESULT"
fi
