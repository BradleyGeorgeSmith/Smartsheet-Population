# ToDo Task

Turns a short To Do entry into a full brief, a Word document, the text for the task list,
and a prompt that starts the work in a Claude Code session.

    To Do or Todoist entry  →  brief (Word document)  →  Claude Code session  →  finished content

**Start with the playbook: [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md).**

## What is here

| Path | What it is |
|------|------------|
| `docs/PLAYBOOK.md` | How the whole procedure works, and how to set it up. |
| `templates/` | The blank Word template, as `.docx` and `.dotx`. |
| `word-skill/` | The green prompt packaged as a Claude skill, for Claude for Word. |
| `app/` | The ToDo Task Builder page (a Claude artifact). |
| `spec/` | The wording everything else is built from. Edit wording here only. |
| `todotask/` | The Python package behind `python -m todotask`. |
| `automation/` | The scheduled-task prompt and the project instructions. |
| `scripts/` | PowerShell scripts for Windows. |
| `config.json` | Limits for the daily sweep. |

The Claude Code skills, agents and saved workflow are in `../.claude/`.

## Try it

```bash
cd todo-task
python -m pip install python-docx
python -m todotask new "garden timelapse vid?? 30 days tomatoes.. phone on tripod.. music"
```

That prints the Word document it made, under `briefs/`. Open it, and send the green prompt
to Claude in Word. In Claude Code, `/todo-task <entry>` does the whole expansion.

## Checks

```bash
python -m pytest -q                    # the Python package
node --test tests/app_core.test.js     # the page's brief logic (needs the docx package)
```

After changing anything in `spec/` or `app/src/`, rebuild:

```bash
python -m todotask template && python -m todotask app && python -m todotask wordskill
```

## Privacy

This repository is public. Entries, briefs, Word documents and finished content are never
committed: `briefs/` and `private/` are git-ignored.
