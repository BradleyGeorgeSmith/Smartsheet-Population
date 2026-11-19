# ToDo Task

This repository holds the ToDo Task pipeline. It turns a short To Do entry into a full
brief, a Word document, the text written back to the task list, and a prompt that starts
the work in a Claude Code session.

    To Do or Todoist entry  →  brief (Word document)  →  Claude Code session  →  finished content

The owner captures entries on a phone, often in a few misspelt words. Nothing stays a
one-line entry: every entry gets a brief, and every brief that Claude can act on gets a session.

## This repository is public

Never commit a person's entries, briefs, Word documents or finished content. They go in
`private/` or `briefs/` (both git-ignored), back onto the task in Todoist, or to a private
store the owner has named. The only example brief that may be committed is the neutral one
in `todo-task/spec/examples/`. Before any commit, check that `git status` shows nothing
personal. The folders `album02/` and `cards/` belong to a different job; leave them alone.

## Where things are

| Path | What it is |
|------|------------|
| `todo-task/spec/` | The single source of wording: working rules, the green Word prompt, the expansion rules, the brief schema, the example. Change wording here and nowhere else. |
| `todo-task/todotask/` | Python package. `python -m todotask` builds the Word documents, the session prompt and the write-back text. |
| `todo-task/app/` | The ToDo Task Builder page. `src/` is edited; `todo-task-builder.html` is built by `python -m todotask app`. |
| `todo-task/templates/` | The blank Word template (`.docx` and `.dotx`), built by `python -m todotask template`. |
| `todo-task/automation/` | The scheduled-task prompt, the project instructions and the Power Automate recipes. |
| `todo-task/scripts/` | PowerShell scripts for Windows. |
| `todo-task/docs/` | The playbook. |
| `.claude/skills/` | `todo-task` (expand one entry), `todo-task-sweep` (every new entry), `todo-task-run` (carry out a brief). |
| `.claude/agents/` | The subagents those skills use. |

Run commands from `todo-task/`: `python -m pytest -q` and `node --test tests/app_core.test.js`.
After changing anything in `spec/` or `app/src/`, rebuild with `python -m todotask template`
and `python -m todotask app`, then run both test suites.

## The brief

Six parts, always in this order (full rules in `todo-task/spec/brief-structure.md`):

1. **Working rules for Claude**: a fixed paragraph, never reworded.
2. **Title**: starts with an action word.
3. **Description, Status, Calendar date** on one line.
4. **[Topic] Context**: one to four short first-person paragraphs.
5. **Information Needed and Next Actions**: numbered; item 1 starts "Next action:".
6. **Execution Plan for Claude**: Output, Steps, Tools, Rhythm, Done when.

It closes with the original entry, word for word, so the brief works as a prompt on its own.

## Rules that never bend

- The original entry is never edited.
- Stay with the motive of the entry. Do not swap in a tidier idea.
- Invent nothing. Unknown things are "Not supplied". Guesses carry "(to confirm)".
- Write as the owner, plainly. No judgement, no cautions or limits the owner did not write.
- Health: organise information and questions for the clinician. No diagnosis, no treatment advice.
- Do not contact anyone, post anything or spend money for the owner unless the brief asks for it.
- Report what was actually done. End every update with: Completed; Waiting on; Next action;
  Completion evidence.

## Stages and Todoist labels

`Captured` → `Briefed` → `In session` → `Waiting on me` → `Done`

Labels: `briefed`, `in-session`, `waiting-on-me`, `content-done`. A task labelled `skip-ai`
is never touched. When updating a Todoist task, send its existing labels as well as the new
one, because the labels field replaces the whole list.

## When a message starts with "Working rules for Claude:"

That message is a brief. Carry it out by following `.claude/skills/todo-task-run/SKILL.md`.
