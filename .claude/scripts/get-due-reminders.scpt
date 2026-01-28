-- get-due-reminders.scpt
-- Extracts due and overdue reminders, outputs as markdown checkboxes
-- Usage: osascript get-due-reminders.scpt

use AppleScript version "2.4"
use scripting additions

on run
    set today to current date
    set endOfToday to today - (time of today) + (24 * 60 * 60) - 1

    set dueTodayList to {}
    set overdueList to {}

    tell application "Reminders"
        set allLists to every list
        repeat with aList in allLists
            set listName to name of aList
            try
                set incompleteReminders to (every reminder of aList whose completed is false)
                repeat with rem in incompleteReminders
                    set remName to name of rem
                    set remDueDate to due date of rem

                    if remDueDate is not missing value then
                        if remDueDate ≤ endOfToday then
                            -- Check if overdue (before today)
                            set startOfToday to today - (time of today)
                            if remDueDate < startOfToday then
                                set end of overdueList to {name:remName, dueDate:remDueDate, listName:listName}
                            else
                                set end of dueTodayList to {name:remName, dueDate:remDueDate, listName:listName}
                            end if
                        end if
                    end if
                end repeat
            on error errMsg
                -- Skip lists that cause errors
            end try
        end repeat
    end tell

    -- Build markdown output
    set mdOutput to ""

    -- Overdue section
    if (count of overdueList) > 0 then
        set mdOutput to mdOutput & "### Overdue" & linefeed
        repeat with rem in overdueList
            set mdOutput to mdOutput & "- [ ] " & name of rem & " (" & listName of rem & ")" & linefeed
        end repeat
        set mdOutput to mdOutput & linefeed
    end if

    -- Due today section
    if (count of dueTodayList) > 0 then
        set mdOutput to mdOutput & "### Due Today" & linefeed
        repeat with rem in dueTodayList
            set mdOutput to mdOutput & "- [ ] " & name of rem & " (" & listName of rem & ")" & linefeed
        end repeat
    end if

    if mdOutput = "" then
        return "- No tasks due today"
    else
        return mdOutput
    end if
end run
