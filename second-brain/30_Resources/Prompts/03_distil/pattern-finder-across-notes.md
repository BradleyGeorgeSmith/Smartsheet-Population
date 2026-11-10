# Pattern Finder Across Notes

**Purpose**: read many captures at once and surface the recurring themes,
contradictions and the few ideas that keep returning. Pairs with Fabric's
`extract_patterns`.
**When**: monthly review, or before writing anything long.
**Inputs**: `{{notes}}` (10 to 40 notes, each with title and body).

```text
Below are notes I captured over the last month.

<notes>
{{notes}}
</notes>

1. THEMES: list 5 to 12 themes that appear in three or more notes. For each,
   name the notes (by title) that support it.
2. TENSIONS: pairs of notes that pull in opposite directions. One line each.
3. THE ONE THING: the single idea that, if acted on, would make the most of
   the others unnecessary. Explain in 3 sentences.
4. NEGLECTED: my twelve favourite problems that got no new material this
   month (I will paste them below if available): {{twelve_problems}}
5. EXPRESS: three Intermediate Packets I could produce from this material
   this week (a post outline, a checklist, a slide, a one-pager). Title and
   three bullets each.

Markdown only. Quote notes rather than inventing.
```

**Output**: a monthly themes report filed under `30_Resources/Reviews/`.
**Source**: original; Fabric `extract_patterns` for a stricter variant.
