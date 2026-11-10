# Weekly Reflection

**Purpose**: the reflective half of the weekly review, written as a letter to
next week's self.
**When**: Sunday, after the mechanical weekly review.
**Inputs**: `{{daily_entries}}` (the week's journal files), `{{goals}}`
(2026 to 2030 goals list), `{{completed}}` (Todoist completed this week).

```text
Here are my journal entries for the week and my completed tasks.
<entries>
{{daily_entries}}
</entries>
<completed>
{{completed}}
</completed>
My longer-term goals: {{goals}}

Write a weekly reflection, Markdown, 300 to 450 words, in first person:
1. What moved: progress against goals, with evidence from the entries.
2. What stalled, and the honest reason (avoidance, energy, dependency, unclear
   next step). Name the pattern without judgement.
3. What I noticed about my body and mind this week (sleep, meds routine kept
   or missed, movement, mood). Facts only, from the entries.
4. Relationships: who I showed up for, who I owe a message.
5. Faith and character: one thing I am grateful for, one conviction I kept.
6. Next week's three outcomes, each with a first step and a day.
7. One line to pin on the wall.

Do not invent events. If an area has no evidence, write "no entries".
```

**Output**: `20_Areas/Journal/YYYY/weekly/YYYY-Www.md`.
**Source**: original.
