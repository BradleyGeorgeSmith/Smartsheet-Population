# Agents

Each file is a complete specification: role, trigger, inputs, tools,
procedure, outputs, guardrails, and a run prompt you can paste into Claude
Code, Claude Cowork, a cloud scheduled task, or another agent runtime
(OpenClaw, Manus, n8n with an LLM node).

| # | Agent | CODE stage | Cadence | Writes to |
|---|---|---|---|---|
| 01 | Capture | Capture | Daily | `00_Inbox` |
| 02 | Organise (PARA router) | Organise | Weekly | PARA folders, Todoist projects |
| 03 | Distil | Distil | On touch, monthly sweep | the note itself |
| 04 | Express | Express | Weekly | `10_Projects/*/packets`, drafts |
| 05 | Pinterest to Dropbox | Capture | Weekly | Dropbox Inspiration, manifests |
| 06 | Quote and Image Curator | Capture, Express | Weekly | Inspiration/Quotes, cards |
| 07 | Marketing Material Capture | Capture | Daily batch | Marketing-Swipe-File |
| 08 | To-do Triage | Organise | Weekly | `todo-prompts/`, Todoist |
| 09 | Journal | Capture, Distil | Daily | `20_Areas/Journal` |
| 10 | Weekly Review | Organise | Sunday | review report, Todoist |

How they chain: Capture and Journal feed `00_Inbox` every day. Organise and
To-do Triage empty it on Sunday inside the Weekly Review. Distil runs on
notes you reopen. Express pulls from Projects to make packets. Pinterest,
Quote and Marketing capture agents are specialised Capture agents with their
own sources.

Activation: none of these are live. `routines/schedules.md` shows the exact
`/schedule` commands and cron lines. Activate the Weekly Review first, then
Journal, then the rest one at a time.
