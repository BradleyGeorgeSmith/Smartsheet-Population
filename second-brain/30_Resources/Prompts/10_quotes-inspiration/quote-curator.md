# Quote Curator (architecture, manufacturing, innovation, character)

**Purpose**: collect accurately attributed quotes on a theme, reject
misattributions, and format them for quote cards like the ones in `/cards`.
**When**: weekly, feeding the Quote Card pipeline and Metricool schedule.
**Inputs**: `{{theme}}`, `{{count}}`, `{{already_used}}` (list to avoid).

```text
Theme: {{theme}}
Number wanted: {{count}}
Already used (avoid): {{already_used}}

Give me {{count}} quotes on this theme. For each:
- QUOTE: exact wording
- WHO: full name and one-line descriptor (for example "Finnish architect")
- SOURCE: book, speech, interview or "widely attributed, primary source
  unverified". Never invent a source. If you are not confident the person
  said it, say so and prefer a different quote.
- WHY IT FITS: one line connecting it to the theme and to building things
  well (architecture, manufacturing, craft, innovation, leadership).
- CARD LINE: a 2-line version under 90 characters for a 4:5 card, with
  attribution on the second line.
- IMAGE DIRECTION: 10 to 15 words describing a photo or render to pair it
  with (architecture detail, factory floor, prototype, material texture).

Prefer architects, engineers, industrial designers, manufacturers,
inventors and craftspeople (for example Alvar Aalto, Dieter Rams, Charles
Eames, Buckminster Fuller, Soichiro Honda, Taiichi Ohno, Antoni Gaudi,
Zaha Hadid, Tadao Ando, Mies van der Rohe, Louis Kahn, Eliel Saarinen,
James Dyson, Ferdinand Porsche). Include at most two quotes from any one
person. Mark any quote that is in the public domain (author died before
1950) with [PD].
Output a Markdown table, then a plain list of just the CARD LINES.
```

**Output**: `30_Resources/Inspiration/Quotes/<theme>.md`; card lines go to the
quote card generator.
**Source**: original. For bulk pulls with attribution, see
https://zenquotes.io (free tier requires a link back) and
https://github.com/lukePeavey/quotable (open source).
