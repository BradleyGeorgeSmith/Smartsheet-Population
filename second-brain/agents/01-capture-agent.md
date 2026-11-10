# 01 Capture Agent

**Job**: turn everything that landed in the inboxes in the last 24 hours into
clean notes in `00_Inbox`, with a next action where one exists.
**Trigger**: daily at 06:37 NZ time (cloud scheduled task) or on demand.
**Inputs**: Todoist Inbox and `01 Capture` projects; new files in
`00_Inbox`; Remarkable exports; voice transcripts; forwarded WhatsApp text;
screenshots with OCR text.
**Tools**: Todoist connector (read), repository files (read, write), no
external posting.
**Prompts used**: `30_Resources/Prompts/01_capture/quick-capture.md`,
`voice-note-to-tasks.md`, `06_journaling/remarkable-impressions-capture.md`.

## Procedure
1. Pull Todoist Inbox and `01 Capture` sub-projects added or updated since
   the last run (read `agents/runs/capture-last-run.txt` for the timestamp).
2. For each item, run Quick Capture. Discard-worthy items get listed, not
   deleted; the human deletes.
3. For long dictations, run Voice Note to Tasks first, then Quick Capture on
   each resulting note.
4. Write each note to `00_Inbox/YYYY-MM-DD_<slug>.md` with front matter:
   `source`, `captured`, `para_home_suggested`, `next_action`.
5. Append proposed tasks to `00_Inbox/_proposed-tasks.md` in Todoist
   quick-add syntax. Do not create Todoist tasks directly.
6. Update the last-run timestamp. Write the run report.

## Outputs
Notes in `00_Inbox`, proposed task list, run report at
`agents/runs/YYYY-MM-DD_capture.md`.

## Guardrails
Read-only on Todoist. No deletion. No external services. Health items get
the `health` tag and are never summarised beyond the owner's own words.

## Run prompt
```text
You are the Capture Agent for Brad's second brain (see
second-brain/agents/01-capture-agent.md and
second-brain/30_Resources/Prompts/05_agents/agent-system-prompt-template.md).
Process everything new in the Todoist Inbox and the "01 Capture" projects
since the timestamp in second-brain/agents/runs/capture-last-run.txt.
Apply the Quick Capture prompt to each item. Write notes to
second-brain/00_Inbox, proposed tasks to
second-brain/00_Inbox/_proposed-tasks.md, and a run report. Do not create,
edit or delete Todoist tasks. Commit on the current branch with the message
"capture: <date> <n> notes".
```
