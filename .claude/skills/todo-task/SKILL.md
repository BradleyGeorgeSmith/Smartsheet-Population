---
name: todo-task
description: Expand one short To Do or Todoist entry into a full task brief, then build its Word document, write-back text and Claude Code prompt. Use when the user gives a brief task entry or an idea in a few words, or asks to expand, brief or build out a task.
argument-hint: [the entry text, or a Todoist task id]
---

# Expand one entry into a brief

The entry: `$ARGUMENTS`

If no entry was given, ask for it. If it is a Todoist task id or link, read the task with
the Todoist connector and use its content as the entry and its description as the notes.
Keep the entry exactly as written, mistakes included. It is never edited.

## Steps

1. **Start the task folder.** From `todo-task/`:

   ```bash
   python -m todotask new "<the entry, word for word>" --source "<Todoist | Microsoft To Do | Manual>" \
     --notes "<notes already on the task>" --task-id "<id if known>" --date <capture date> --out ../briefs
   ```

   This prints the folder it made, holding `brief.json` with the entry and an empty brief.

2. **Write the brief.** Read `todo-task/spec/expand-json-prompt.txt` and follow its rules
   exactly. Read `todo-task/spec/examples/tomato-timelapse.json` for the layout, length and
   tone only. Fill in `task_type`, `brief` and `writeback` in the folder's `brief.json`.
   Work only from the entry and its notes. Do not use anything else you know about the owner
   unless the owner asked you to in this conversation.

3. **Check it.** Run `python -m todotask check <folder>/brief.json` and fix what it lists.
   Then ask the `brief-checker` agent to review the brief against the entry. Fix every
   medium or high failure it reports. One round is enough.

4. **Build the files.** Run `python -m todotask render <folder>/brief.json`. This writes the
   Word document, `prompt.md` (the text for a Claude Code session) and `writeback.txt`.

5. **Hand it over.** Show the title, the description line, anything marked "(to confirm)"
   and what is needed from the owner. Give the path of the Word document and send the file
   if you can. Do not change the task in Todoist and do not start a session unless the owner
   asks; `/todo-task-sweep` does both.

## Rules

- `briefs/` is git-ignored. Never commit a brief, a Word document or an entry.
- If `python -c "import docx"` fails, run `pip install python-docx` first.
- An errand (buy, pay, book, call, reply) or an unreadable entry gets a short brief whose plan
  says no Claude session is needed. That is a correct result, not a failure.
- End with: Completed; Waiting on; Next action; Completion evidence.
