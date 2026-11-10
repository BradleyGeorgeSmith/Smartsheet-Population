# Progressive Summary (layers 2 to 4)

**Purpose**: apply Forte's progressive summarisation to one note so a future
reader gets the value in ten seconds.
**When**: whenever you reopen a note for a real reason. Never in bulk.
**Inputs**: `{{note}}` (layer 1 text, your captured excerpts).

```text
Apply Progressive Summarisation to this note. Keep every word of the
original; add layers on top.

<note>
{{note}}
</note>

Return the note in Markdown with:
- LAYER 4 at the top: an executive summary of 2 to 4 sentences in plain
  first-person language, as if I am explaining it to myself next year.
- LAYER 2 and 3 inside the body: wrap the key passages in **bold** (no more
  than a third of the text), and wrap the best of the bold in ==highlight==
  marks (no more than a third of the bold).
- A final line "Why I kept this:" with one sentence.

Rules: do not paraphrase the body, do not delete anything, do not add
information that is not in the note. Bold full phrases, not single words.
```

**Output**: the same note with layers added; replace the original file.
**Source**: Tiago Forte, Progressive Summarisation (paraphrased rules).
