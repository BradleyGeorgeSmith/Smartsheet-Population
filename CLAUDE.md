# Working in this repository

This repo holds Brad Smith's second-brain system under `second-brain/`, plus
quote-card image folders (`cards/`, `album02/`) used as a transfer bucket for
Metricool.

## Orientation

- Read `second-brain/README.md` first, then `second-brain/00_Brief/00_master-prompt.md`.
- Methods: Tiago Forte's PARA (`10_Projects`, `20_Areas`, `30_Resources`,
  `40_Archives`, with `00_Inbox` in front) and CODE (Capture, Organise,
  Distil, Express). File by actionability: projects first.
- Agents live in `second-brain/agents/`, routines in `second-brain/routines/`,
  prompts in `second-brain/30_Resources/Prompts/`.
- `second-brain/todo-prompts/` is generated. Edit the generator
  (`second-brain/scripts/todoist_prompt_generator.py`) or the TSV exports in
  `second-brain/scripts/data/`, then re-run; do not hand-edit generated files.

## Rules for any session here

- Private data: health, finance, family and faith material is present. Never
  paste personal identifiers into external services. Keep health items in
  `20_Areas/Health`.
- Connectors (Todoist, Dropbox, HubSpot, Smartsheet, Notion, Google) are
  read-only unless the owner has approved a specific moves file or asked for
  the write in the current conversation.
- Never delete; archive. Never post, send, publish or spend.
- Scheduled tasks and loops are defined in `second-brain/routines/schedules.md`
  but are not activated by default. Activate only when the owner asks.
- Scripts read tokens from environment variables only. Do not write secrets
  to files.
- Commit messages: short, present tense, prefixed by the agent or area, for
  example `capture: 2026-11-10 7 notes`.

## Bare `/loop`

`.claude/loop.md` defines the default maintenance loop: process new inbox
files, tend the open PR, add summaries to today's changed notes. It never
writes to connectors.
