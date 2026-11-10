# Substack or LinkedIn Post from Notes

**Purpose**: write a publishable post in Brad's voice from captured notes and
journal entries. Serves the "write my journey to Substack and LinkedIn" tasks.
**When**: weekly, from the week's best notes.
**Inputs**: `{{notes}}`, `{{theme}}`, `{{platform}}` (Substack or LinkedIn),
`{{voice_sample}}` (two or three paragraphs Brad has already written).

```text
You are helping me publish on {{platform}}. Write in my voice, which you can
hear in this sample:
<voice>
{{voice_sample}}
</voice>

Theme for this piece: {{theme}}

Raw material (notes, journal lines, quotes I saved):
<notes>
{{notes}}
</notes>

Write the post.
- Substack: 600 to 900 words, a title under 10 words, a one-line subtitle,
  3 to 5 short sections with plain headings, one concrete story from the
  notes, one practical takeaway the reader can do today.
- LinkedIn: under 1,300 characters, first line is a hook that stands alone,
  short paragraphs, no hashtags in the body, three hashtags at the end.
Rules: no cliches, no "In a world", no "game-changer". Keep exact quotes
attributed. If a fact is not in the notes, do not add it. Finish with a
one-line author note: who I am and what I am building, in my words.
Then list 3 alternative titles.
```

**Output**: a draft for review; file under `10_Projects/Substack/drafts/`.
**Source**: original.
