# Morning Pages (plan the day the night before or first thing)

**Purpose**: a five-minute structured journal that ends in a plan. Serves the
"start planning my days the night before", "commit to a calendar" and
"journal every day" tasks.
**When**: evening before, or first thing. Voice dictation works well.
**Inputs**: `{{dictation}}`, `{{calendar_today}}`, `{{top_tasks}}`, `{{date}}`.

```text
Date: {{date}}
Here is my free-form dictation:
<dictation>
{{dictation}}
</dictation>
Calendar today: {{calendar_today}}
Open tasks I flagged: {{top_tasks}}

Turn this into my morning page, Markdown, these headings only:
## Gratitude (3 lines, specific, from the dictation)
## State (1 line on energy, mood, sleep; 1 line on what would help)
## One Thing (the single task that makes today a win, and why)
## Three Supporting (verb-first, each tied to a project or area)
## Time blocks (a simple table: time, block, task; respect the calendar;
   include a leg-press or movement block and a 20-minute capture-processing
   block)
## Prayer or intention (one or two lines in my words if I spoke them;
   otherwise leave the heading and a blank line)
## Carry-over (anything I mentioned that is not for today, as tasks)

Do not add tasks I did not mention. Keep the whole page under 250 words.
```

**Output**: `20_Areas/Journal/YYYY/YYYY-MM-DD.md`.
**Source**: original, structure informed by Hal Elrod's Miracle Morning
(gratitude, intention) and time-blocking practice.
