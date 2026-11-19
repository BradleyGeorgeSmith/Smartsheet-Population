---
name: todo-task-sweep
description: Find every new Todoist task that has no brief yet, expand each into a brief, write the new title and description back to the task, and start a Claude Code session for the ones Claude can act on.
argument-hint: [dry-run] [days=3] [limit=10]
disable-model-invocation: true
---

# Sweep: every new entry gets a brief

Arguments: `$ARGUMENTS`. `dry-run` means write nothing to Todoist and start no sessions.
`days=N` and `limit=N` override the settings.

This skill changes tasks in the owner's Todoist and starts sessions that use the owner's
plan. Run it only when the owner or their scheduled task asked for it.

## Settings

Read `todo-task/config.json`. If `todo-task/config.local.json` exists, its values win.

| Setting | Meaning |
|---------|---------|
| `filter` | The Todoist filter that finds candidates. `{days}` is replaced by the window. |
| `skip_labels` | A task carrying any of these labels is left alone. Checked after the search, not in the filter. |
| `window_days` | How far back to look. |
| `max_briefs_per_run` | Most entries to expand in one run. |
| `max_sessions_per_run` | Most sessions to start in one run. |
| `write_back` | Update the task's title and description. |
| `keep_description_over` | A task whose own description is longer than this many characters keeps it; only the title changes and the brief goes in a comment. |
| `comment_brief` | Add the full brief to the task as a comment. |
| `start_sessions` | Start a Claude Code session for briefs that need one. |
| `session_model` | Model for the sessions. Empty means the default. |
| `app_url` | The link of the owner's ToDo Task Builder page. Set it in `config.local.json` or in the request, never in `config.json`. |

## Steps

1. **Find the entries.** Call the Todoist `find-tasks` tool with the filter and a limit of
   100, following the cursor until there are no more pages. Drop any task that has one of the `skip_labels`
   (`from-email` tasks were written by another automation and already carry their own
   detail), and any recurring task. If a task's description is longer than 2,000
   characters, give the writer the first 2,000 and say it was cut. Sort newest first and keep
   `max_briefs_per_run`. If more were found than you kept, say how many were left for the
   next run.

2. **Make sure the labels exist.** Call `find-labels`. Add any of `briefed`, `in-session`,
   `waiting-on-me`, `content-done` and `skip-ai` that is missing with `add-labels`.

3. **Expand each entry.** For each task, give one `brief-writer` agent the task's content as
   the entry, its description as the notes, its id, its labels and its `addedAt` date. Run them in
   parallel. Each returns the path of a finished `brief.json`. For five or more entries, run
   the saved workflow `todo-task-expand` with the list of entries as its `args` instead; it
   expands and checks every entry and returns the same paths.

4. **Check each brief.** Give each `brief.json` to a `brief-checker` agent. Where it reports
   a medium or high failure, send the failures back to a `brief-writer` once. If the brief
   still fails, leave that task untouched and list it in the report.

5. **Build the files.** For each brief that passed, from `todo-task/`:
   `python -m todotask render <folder>/brief.json`.

6. **Write back** (skip on `dry-run` or when `write_back` is false). For each brief, call
   `update-tasks` with the task id, `content` set to the write-back title, `description` set
   to the DESCRIPTION block of `writeback.txt` (the new description followed by the original
   entry and the original notes), and `labels` set to the task's existing labels plus
   `briefed`. The labels field replaces the whole list, so always send the existing ones too.
   If the task's own description is longer than `keep_description_over` characters, leave the
   description as it is: send only `content` and `labels`. If `comment_brief` is true,
   add the contents of `prompt.md` to the task with `add-comments` and `notifyUsers` set to
   `["none"]`.

7. **Start sessions** (skip on `dry-run` or when `start_sessions` is false). A brief needs a
   session unless its plan output starts "No Claude session needed" (errands, reflections
   and unclear entries never get one). Start at most
   `max_sessions_per_run`, newest first, with the `create_session` tool of the Claude Code
   Remote connector:
   - `prompt`: the contents of `prompt.md`, then a blank line, then
     `Task record: Todoist task <id>. Post the results there as a comment.`
   - `title`: `ToDo Task: <brief title>`
   - `tags`: `["todo-task"]`
   - `model`: `session_model`, if set
   - `source_url`: this repository, so the session loads these skills

   Then add the label `in-session` to the task. If the tool is not available, say so in the
   report and give the path of each `prompt.md` instead.

8. **List the briefs on the phone page** (skip on `dry-run`, or when no `app_url` was given
   in the settings or the request). With the ArtifactData tool, write each brief's
   `app-row.json` to the page's `briefs` collection: `set`, with the document id
   `todoist-<task id>` and `file_path` pointing at the file. Use one `batch` for several.
   If the task now has a session, add `"stage": "In session"` and the session link as
   `session_url` with an `update`.

9. **Report.** One row per entry: original entry, new title, type, what was written back,
   and the session started or the reason none was. Then list what was skipped and why.
   End with: Completed; Waiting on; Next action; Completion evidence. The evidence is the
   task ids updated and the session ids started, not a statement that it was done.

## Rules

- Never touch a task labelled `skip-ai`, a task assigned to someone else, or a completed task.
- Never commit anything under `briefs/`. This repository is public.
- If a Todoist call fails, stop writing, report what was and was not changed, and do not
  retry a write blindly: read the task first to see whether the change went through.
- An entry that cannot be read gets a short brief asking the owner what was meant, and no
  session. That is the correct outcome.
