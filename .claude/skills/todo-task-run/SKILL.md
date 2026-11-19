---
name: todo-task-run
description: Carry out a ToDo Task brief. Use when a message starts with "Working rules for Claude:" or the user pastes a task brief and asks for the work to begin.
argument-hint: [the brief, or the path of its prompt.md]
---

# Carry out a brief

The brief is the whole instruction. Its first paragraph, "Working rules for Claude", wins
over anything here if the two ever disagree.

## Steps

1. **Read the brief once, fully.** Find: the Outcome in the Description; the numbered
   actions; the Execution Plan (Output, Steps, Tools, Rhythm, Done when); the original entry
   at the end; and a "Task record" line, if there is one.

2. **Stop early when that is the right answer.** If the plan output starts "No Claude
   session needed", confirm that in one line, list anything marked "Not supplied", and stop.

3. **Sort the steps.** Steps that do not depend on the owner are done now. Steps that start
   "When I supply" wait. Never fill a gap with an invented fact to get a waiting step moving.

4. **Do the work with the right agent.** Use one agent per output where the outputs are
   separate, and run them at the same time:
   - `content-writer` for written pieces, plans, worksheets, question lists and learning notes
   - `video-ideas` for video ideas, titles, opening lines, outlines and shot lists
   - `researcher` for background that needs sources

   Give each agent the whole brief, because an agent sees nothing else. Keep the outcome
   simple: writing, a plan, video ideas or learning notes. If the entry asked for a format
   by name, such as Excel or Word, deliver that format.

5. **Save the outputs.** Put every file in `briefs/<task folder>/output/`, or
   `briefs/<date>-<short name>/output/` if the folder does not exist yet. Write Markdown
   first. Where a Word document is wanted, convert with `pandoc file.md -o file.docx`.
   `briefs/` is git-ignored: never commit outputs, because this repository is public.

6. **Check before reporting.** Give the brief and the outputs to the `evidence-checker`
   agent. Fix what it finds. It checks that each item in "Done when" can be shown, that
   nothing was invented, and that the health rule was kept.

7. **Deliver.** Send the files to the owner. If the brief has a "Task record" line naming a
   Todoist task, add one comment to that task with a short summary and the main output in
   full (`add-comments`, `notifyUsers` set to `["none"]`), then set its labels: the existing
   labels plus `waiting-on-me` if anything still depends on the owner, or `content-done` if
   everything in "Done when" is met. Remove `in-session` in the same update.

8. **Keep the brief current.** Add the decisions made and lessons learned to the brief's
   folder as `decisions.md`, so the next session builds on them.

9. **Report.** End with exactly these four lines, each filled in:

   ```
   Completed: what was actually produced, by name
   Waiting on: what the owner has to supply or decide
   Next action: the single next step and who takes it
   Completion evidence: file paths, task ids and session ids that show it
   ```

## Rules

- Do not contact anyone, post anything or spend money for the owner unless the brief asks.
- Health topics: organise information and questions for the clinician. No diagnosis, no
  advice on treatment, medicines, supplements or doses.
- Personal, family, money and faith topics: write plainly, without judgement, and keep to
  what the owner wrote.
- Say "not done" when something was not done. An update without evidence is not finished.
