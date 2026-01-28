-- get-calendar-events.scpt
-- Extracts today's calendar events and outputs as markdown list
-- Usage: osascript get-calendar-events.scpt

use AppleScript version "2.4"
use scripting additions
use framework "Foundation"

on run
    set today to current date
    set startOfDay to today - (time of today)
    set endOfDay to startOfDay + (24 * 60 * 60) - 1

    set eventList to {}

    tell application "Calendar"
        set calendarList to every calendar
        repeat with cal in calendarList
            set calName to name of cal
            -- Skip holidays and birthdays calendars
            if calName is not "Holidays" and calName is not "Birthdays" then
                try
                    set dayEvents to (every event of cal whose start date ≥ startOfDay and start date ≤ endOfDay)
                    repeat with evt in dayEvents
                        set eventStart to start date of evt
                        set eventSummary to summary of evt

                        -- Format time as HH:MM
                        set eventHour to hours of eventStart
                        set eventMinute to minutes of eventStart
                        if eventHour < 10 then set eventHour to "0" & eventHour
                        if eventMinute < 10 then set eventMinute to "0" & eventMinute
                        set timeStr to (eventHour as text) & ":" & (eventMinute as text)

                        -- Add to list with sortable timestamp
                        set sortKey to (eventHour as number) * 60 + (eventMinute as number)
                        set end of eventList to {sortKey:sortKey, timeStr:timeStr, summary:eventSummary, calendar:calName}
                    end repeat
                on error errMsg
                    -- Skip calendars that cause errors
                end try
            end if
        end repeat
    end tell

    -- Sort by time (simple bubble sort)
    set listCount to count of eventList
    repeat with i from 1 to listCount - 1
        repeat with j from 1 to listCount - i
            if sortKey of item j of eventList > sortKey of item (j + 1) of eventList then
                set temp to item j of eventList
                set item j of eventList to item (j + 1) of eventList
                set item (j + 1) of eventList to temp
            end if
        end repeat
    end repeat

    -- Output as markdown
    if (count of eventList) = 0 then
        return "- No events scheduled"
    else
        set mdOutput to ""
        repeat with evt in eventList
            set mdOutput to mdOutput & "- **" & timeStr of evt & "** - " & summary of evt & " (" & calendar of evt & ")" & linefeed
        end repeat
        return mdOutput
    end if
end run
