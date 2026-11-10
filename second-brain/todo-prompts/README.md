# To-do prompts

One Markdown file per open Todoist task, generated from the export in
`../scripts/data/` by `../scripts/todoist_prompt_generator.py`. Start with
`index.md`, then `_sessions.md` for the hand-picked high-leverage groups.

Each file holds: the task as captured, its Todoist link, project, priority,
due date, category, PARA home, a context note, a ready-to-paste prompt
tailored to the task type, and next steps.

## How to work a category as one session

Open Claude Code on this repository and say, for example:

```text
Work through second-brain/todo-prompts/ai-agents-automation/ oldest first.
For each file run its prompt, write the result into the PARA home it names
(create the folder if missing), and append a one-line outcome to
second-brain/todo-prompts/_sessions-log.md. Do not touch Todoist.
```

## Reports

- `_reports/duplicates.md`: near-identical titles to merge.
- `_reports/stale.md`: due dates more than 60 days past.
- `_reports/by-project.md`: counts per Todoist project.
- `_proposed-moves.md`: Todoist clean-ups for you to approve before any
  session applies them.

## Privacy choices made in the export

- Tasks flagged `(private)` get a minimal prompt that organises without
  elaborating.
- Contact-list projects (about 120 personal names and 15 doctor and expert
  names) are represented by one aggregate row each; the names stay in
  Todoist.
- Long supplement and medication shopping lists are collapsed into one row
  per Todoist list.
- Descriptions that were previous Claude elaborations are shortened to a
  line; the full text remains in Todoist.

## Regenerate

```bash
python second-brain/scripts/todoist_prompt_generator.py
```

Re-export first if Todoist has changed (the To-do Triage Agent does this).
