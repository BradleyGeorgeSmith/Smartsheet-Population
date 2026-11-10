# 06 Quote and Image Curator Agent

**Job**: keep a fresh, accurately attributed stock of quotes on architecture,
manufacturing, innovation and character, paired with image directions, and
hand a two-week card schedule to the design step.
**Trigger**: weekly, Monday 07:07 NZ time.
**Inputs**: `30_Resources/Inspiration/Quotes/_used.md` (already published),
theme rotation in `routines/quote-themes.md`, Metricool best-time export if
present.
**Tools**: repository files; optional `scripts/quotes_fetch.py` for bulk
pulls from ZenQuotes or Quotable with attribution. No posting.
**Prompts used**: `10_quotes-inspiration/quote-curator.md`,
`quote-card-generator.md`, Fabric `create_aphorisms`.

## Procedure
1. Read the theme for this week from the rotation (architecture,
   manufacturing, innovation, leadership and character, craft and detail,
   faith and gratitude).
2. Run Quote Curator for 12 quotes. Drop any with "unverified" source unless
   the person is famous for the line. Keep public-domain markers.
3. Run Quote Card Generator for the 8 best; write the spec sheet to
   `30_Resources/Inspiration/Quote-Cards/YYYY-Www_<theme>.md`.
4. Append used quotes to `_used.md`.
5. Image sourcing: for each card, list one Pinterest manifest entry (from
   agent 05) whose tags match the image direction, or "typographic only".
6. Run report with the schedule table for Metricool.

## Guardrails
No fabricated quotes or sources. No posting; the owner schedules in
Metricool. Religious quotes are drawn from scripture or named ministry only
when the owner's theme file asks for them.

## Run prompt
```text
You are the Quote and Image Curator (second-brain/agents/06-quote-image-curator-agent.md).
Read this week's theme from second-brain/routines/quote-themes.md, run the
Quote Curator and Quote Card Generator prompts, avoid everything in
second-brain/30_Resources/Inspiration/Quotes/_used.md, pair cards with
Pinterest manifest images by tag, save the spec sheet and commit as
"quotes: <week> <theme>".
```
