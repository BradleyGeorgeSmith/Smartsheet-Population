# Brad's Second Brain

An AI-operated personal knowledge and productivity system built on Tiago
Forte's PARA and CODE methods, run by Claude Code agents and routines.

Start here: `00_Brief/00_master-prompt.md` is the brief this was built from.
`00_Brief/01_sources.md` lists every source used.

## Layout

```
00_Brief/        the rewritten brief, sources, (later) the master life prompt
00_Inbox/        single capture point; emptied weekly
10_Projects/     short-term efforts with an end; one folder each
20_Areas/        ongoing responsibilities; one folder each
30_Resources/    prompt library, frameworks, inspiration, swipe file, templates, reviews
40_Archives/     inactive material, never deleted
agents/          ten agent specifications with paste-ready run prompts
routines/        daily, weekly, monthly, quarterly routines with cron and /schedule commands
scripts/         Pinterest to Dropbox sync, quote fetcher, PARA scaffolder, to-do prompt generator
todo-prompts/    one contextual prompt per open Todoist task, grouped by category, with index and reports
```

## How it runs

1. **Capture** all day into Todoist, Pinterest, Remarkable and dictation.
   The Capture Agent turns it into notes in `00_Inbox` each morning.
2. **Organise** on Sunday: the Weekly Review Agent empties the inbox into
   PARA and hands you a 30-minute checklist.
3. **Distil** whenever you reopen a note: progressive summary layers.
4. **Express** on Fridays: one packet per focus project and one draft post.

Specialised capture agents handle Pinterest (to Dropbox), quotes and images
(to quote cards), and marketing material (to the swipe file). The Journal
Agent writes morning and evening pages from dictation. The To-do Triage
Agent regenerates `todo-prompts/` from a Todoist export.

## First week

1. Read `routines/README.md` and activate the Weekly Review scheduled task.
2. Dictate a morning page tomorrow and run the Journal Agent on it.
3. Open `todo-prompts/index.md`, pick one category, and run it as one
   session: "work through todo-prompts/ai-agents-automation/, oldest first".
4. Review `todo-prompts/_proposed-moves.md` and approve a first batch of
   Todoist clean-ups.
5. Set Pinterest and Dropbox tokens and run the sync in dry-run mode.

## Mirroring the structure elsewhere

`scripts/para_scaffold.py --print` shows the tree. Use `--target` for a
local drive, NAS or OneDrive folder, `--dropbox "/Brad Smith"` for Dropbox.
Keep the same names everywhere: Todoist, Notion, bookmarks, YouTube
playlists, Remarkable folders.

## Privacy

This repository holds health, financial and personal material from the
Todoist export. Keep it private. Agents are written to never send personal
identifiers to external services and to keep health items inside
`20_Areas/Health`. Individual names from contact-list projects were left
out of the generated files on purpose.
