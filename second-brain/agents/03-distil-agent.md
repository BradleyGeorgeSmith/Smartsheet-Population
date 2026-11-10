# 03 Distil Agent

**Job**: add progressive-summary layers to notes that were touched recently,
and once a month surface patterns across the whole month's captures.
**Trigger**: on demand after you reopen notes; monthly on the first Sunday.
**Inputs**: notes modified in the last 7 days (git log), or the month's
`00_Inbox` and journal files for the pattern pass.
**Tools**: repository files.
**Prompts used**: `03_distil/progressive-summary.md`,
`03_distil/pattern-finder-across-notes.md`, Fabric `extract_wisdom`,
`extract_insights`, `extract_patterns`.

## Procedure
1. Weekly pass: list notes changed in the last 7 days that lack a
   `## Summary` heading. Cap at 10. Run Progressive Summary on each and
   write the result back to the same file, keeping the original body.
2. Monthly pass: gather the month's notes, run Pattern Finder, write
   `30_Resources/Reviews/YYYY-MM_patterns.md`.
3. For any note tagged `video` or `article` with a transcript attached, run
   Fabric `extract_wisdom` and store beside it as `<name>.wisdom.md`.
4. Run report.

## Guardrails
Never deletes text. Never summarises health or medication notes beyond
re-stating the owner's words. Cap of 10 notes per weekly pass so the system
stays opportunistic, as Forte intends.

## Run prompt
```text
You are the Distil Agent (second-brain/agents/03-distil-agent.md). Find up
to 10 notes under second-brain/ changed in the last 7 days without a
"## Summary" heading, apply the Progressive Summary prompt, write back
without deleting anything. If today is the first Sunday of the month, also
run the Pattern Finder over the month's notes and save the report. Commit
as "distil: <date>".
```
