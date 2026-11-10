# Remarkable Impressions Capture

**Purpose**: convert handwriting-to-text exports from the Remarkable (church
notes, impressions, sketches of Toop plans, meeting notes) into filed notes
and tasks. Serves "use Remarkable for impressions, set up a system for
capturing and remembering" and "put all my Remarkable notes into Claude".
**When**: after each export (weekly at minimum).
**Inputs**: `{{ocr_text}}`, `{{notebook_name}}`, `{{date_range}}`.

```text
Below is OCR text from my Remarkable notebook "{{notebook_name}}", pages
written between {{date_range}}. Handwriting recognition is imperfect.

<ocr>
{{ocr_text}}
</ocr>

1. Clean the text lightly: fix obvious OCR errors, keep my phrasing, mark
   unreadable parts as [illegible].
2. Split into entries by date or heading. For each entry give a title.
3. Classify each entry: Impression (faith or reflection), Meeting note,
   Idea, Sketch description, Task list, Quote, Other.
4. For each entry: PARA home (Project, Area or Resource and folder).
5. Extract all tasks as "verb-first task [Project]".
6. Extract quotes and scripture references exactly, with speaker or reference.
7. End with "Themes this period": 3 to 5 bullets.

Markdown. Preserve every entry; do not summarise them away.
```

**Output**: one file per notebook export in `00_Inbox`, then routed.
**Source**: original.
