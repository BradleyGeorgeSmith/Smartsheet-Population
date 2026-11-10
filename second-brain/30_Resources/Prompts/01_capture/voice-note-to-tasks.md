# Voice Note to Tasks and Notes

**Purpose**: split a rambling voice transcript (Whisper Flow, WhatsApp voice,
TalkerACR, phone memo) into tasks, notes, calendar items and ideas.
**When**: after any dictation session.
**Inputs**: `{{transcript}}`, `{{today}}`.

```text
Below is a transcript of me thinking aloud. Today is {{today}}.

<transcript>
{{transcript}}
</transcript>

Separate it into these sections, Markdown, nothing else:

## Tasks
One per line, verb first, under 12 words, with a suggested Todoist project
in brackets and a due date if I implied one. Example:
- Order creatine from Xplosive Supplements [PHYSIQUE] (due Fri)

## Calendar
Anything with a date or time, as "YYYY-MM-DD HH:MM Title (who)".

## Notes and ideas
Each a 1 to 3 sentence note with a title line. These go to 00_Inbox.

## People mentioned
Name: what I said about them or owe them.

## Open questions
Things I asked myself and did not answer.

Rules: keep my wording where it is clear, fix grammar where it is not, never
add items I did not say, mark anything uncertain with (?).
```

**Output**: five sections; paste the Tasks block into Todoist, file the rest.
**Source**: original.
