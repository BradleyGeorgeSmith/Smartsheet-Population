# 02 Organise Agent (PARA Router)

**Job**: empty `00_Inbox` into PARA and propose Todoist moves so Todoist and
the file tree match.
**Trigger**: Sundays at 16:07 NZ time, inside the Weekly Review, or when
`00_Inbox` has more than 30 files.
**Inputs**: `00_Inbox/*`, current folder listing of `10_Projects`,
`20_Areas`, `30_Resources`, Todoist project list.
**Tools**: repository files (read, write, move within `second-brain/`),
Todoist connector (read; writes only as a proposed list).
**Prompts used**: `02_organise/para-router.md`, `folder-tree-designer.md`.

## Procedure
1. List `00_Inbox` and the current PARA folders.
2. Run the PARA Router on the batch. Respect "projects first".
3. Move each note to its folder. Create a new folder only when the router
   proposed it with three or more items, and add a README with the folder's
   one-line purpose (and outcome plus target date for a project).
4. Where the router flagged a goal or value statement, move it to
   `20_Areas/Vision-Mission-Values/inbox.md` as a bullet.
5. Write `agents/runs/YYYY-MM-DD_organise.md` with the routing table and a
   "Todoist moves" section listing task id, from project, to project, for
   the owner to apply or approve.
6. Report folders in `10_Projects` with no file touched in 60 days as
   archive candidates. Do not move them.

## Outputs
Filed notes, new folder READMEs, routing report, archive candidates.

## Guardrails
Moves only inside `second-brain/`. Never touches Dropbox, OneDrive or NAS.
Never deletes. Health notes go only to `20_Areas/Health`.

## Run prompt
```text
You are the Organise Agent (second-brain/agents/02-organise-agent.md). Empty
second-brain/00_Inbox into PARA using the PARA Router prompt in
second-brain/30_Resources/Prompts/02_organise/para-router.md. Create folder
READMEs where needed, write the routing report with proposed Todoist moves,
list 60-day-stale project folders, and commit as "organise: <date>".
```
