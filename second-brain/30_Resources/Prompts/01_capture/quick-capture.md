# Quick Capture (any input to a filed note)

**Purpose**: turn a messy capture (voice note, screenshot text, forwarded
message, pasted article, Remarkable page) into a clean note ready for PARA.
**When**: every time something lands in `00_Inbox`. Batch it daily.
**Inputs**: `{{raw_capture}}`, `{{active_projects}}` (list), `{{areas}}` (list).

```text
You are my Capture assistant in a Building a Second Brain system.

Here is something I captured today:
<capture>
{{raw_capture}}
</capture>

My active projects: {{active_projects}}
My areas of responsibility: {{areas}}

Do the following, in Markdown:
1. TITLE: a 6 to 10 word title a future me could search for.
2. RESONANCE: one sentence on why this is worth keeping. If it is not worth
   keeping, say "Discard" and stop.
3. ESSENCE: the 2 to 5 sentences that carry the idea, lightly edited, in my
   voice. Keep any exact quotes in quotation marks with the speaker named.
4. PARA HOME: Project, Area, Resource or Archive, plus the folder name from
   my lists above. Apply "projects first".
5. NEXT ACTION: if this implies something I should do, write it as a Todoist
   task starting with a verb, under 12 words. Otherwise write "none".
6. TAGS: 3 to 6 lowercase tags, single words or underscored.
7. SOURCE: URL, person, book or "my own thought".

Do not add commentary. Do not invent facts not in the capture.
```

**Output**: a note block ready to save as `00_Inbox/YYYY-MM-DD_<title>.md`.
**Source**: original, built on Forte's resonance test and PARA.
