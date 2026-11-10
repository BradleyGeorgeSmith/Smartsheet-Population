# Quote Card Generator (copy and layout spec)

**Purpose**: produce the copy, layout spec and alt text for quote cards in
the style already used in this repository's `cards/` and `album02/` folders
(4:5 for Metricool scheduling).
**When**: after the Quote Curator run, in batches of 8 to 16.
**Inputs**: `{{card_lines}}`, `{{brand}}` (Good Measure, Hydralada, NEXUS,
personal), `{{palette}}`, `{{font}}`.

```text
Brand: {{brand}}  Palette: {{palette}}  Font: {{font}}
Card lines:
<lines>
{{card_lines}}
</lines>

For each card output:
- FILENAME: NN_two-word-slug.png (zero-padded, lowercase, hyphenated)
- HEADLINE: the quote, line breaks marked with /, max 3 lines of 28 chars
- ATTRIBUTION: name, small caps
- LAYOUT: one of: centred, left-stack, bottom-band, split-image; and why
- IMAGE: the image direction from the curator, or "typographic only"
- ALT TEXT: one sentence for accessibility and SEO
- CAPTION: a 1 to 2 sentence social caption in my voice, no hashtags
- HASHTAGS: 3, relevant to the theme
Then an ordering for a 2-week schedule, 1 card per weekday, alternating
themes, with suggested posting times from Metricool's best-time data if I
paste it: {{best_times}}
Markdown table.
```

**Output**: a spec sheet the design step (Adobe Express or Canva) follows;
PNGs land in `cards/` then Dropbox `30_Resources/Inspiration/Quote-Cards/`.
**Source**: original.
