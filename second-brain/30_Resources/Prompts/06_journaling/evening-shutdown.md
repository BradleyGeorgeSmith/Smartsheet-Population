# Evening Shutdown and Short Accounts

**Purpose**: close the day, capture wins and loose ends, keep short accounts.
Serves "review my day and plan ahead", "keep short accounts", "everyday
reporting: achievements, apologies, wins, gratitude".
**When**: end of the work day, five minutes.
**Inputs**: `{{dictation}}`, `{{completed_tasks}}`, `{{date}}`.

```text
Date: {{date}}
Completed today (from Todoist): {{completed_tasks}}
My dictation:
<dictation>
{{dictation}}
</dictation>

Write my shutdown entry, Markdown, under 200 words:
## Wins (up to 5, one line each, include small ones)
## Short accounts (anything to apologise for, repair, or say tomorrow; name
   the person; one line each; or "clear")
## Open loops (unfinished items, each as a task with a project in brackets)
## Learned (one or two sentences; something I will do differently)
## Gratitude (one line)
## Tomorrow's One Thing (one line)

Then output a second block titled TODOIST with the open loops formatted one
per line as "content #Project @label p2" so I can paste them in.
```

**Output**: append to the day's journal file; paste TODOIST block into Todoist.
**Source**: original; Forte's "decide, don't do" and Brad's reporting list.
