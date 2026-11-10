# Schedules: cron lines and activation commands

| Routine | Agent | Cron (Pacific/Auckland) | `/schedule` command (run in a Claude Code session on this repo) |
|---|---|---|---|
| Morning plan | 09 Journal | `CRON_TZ=Pacific/Auckland 7 6 * * 1-6` | `/schedule every day except Sunday at 6:07am NZ, run the Journal Agent morning pass as described in second-brain/agents/09-journal-agent.md` |
| Capture daily | 01 Capture | `CRON_TZ=Pacific/Auckland 37 6 * * *` | `/schedule daily at 6:37am NZ, run second-brain/agents/01-capture-agent.md with the Todoist connector read-only` |
| Daily shutdown | 09 Journal | `CRON_TZ=Pacific/Auckland 37 17 * * 1-5` | `/schedule weekdays at 5:37pm NZ, run the Journal Agent evening pass per second-brain/agents/09-journal-agent.md` |
| Marketing capture | 07 Marketing | `CRON_TZ=Pacific/Auckland 7 18 * * 1-5` | `/schedule weekdays at 6:07pm NZ, run second-brain/agents/07-marketing-capture-agent.md read-only on Dropbox and HubSpot` |
| Express weekly | 04 Express | `CRON_TZ=Pacific/Auckland 7 14 * * 5` | `/schedule Fridays at 2:07pm NZ, run second-brain/agents/04-express-agent.md, drafts only` |
| Pinterest sync | 05 Pinterest | `CRON_TZ=Pacific/Auckland 7 9 * * 6` | `/schedule Saturdays at 9:07am NZ, run second-brain/agents/05-pinterest-dropbox-agent.md (needs PINTEREST_ACCESS_TOKEN and DROPBOX_ACCESS_TOKEN as network secrets)` |
| Weekly review | 10 Weekly Review | `CRON_TZ=Pacific/Auckland 7 16 * * 0` | `/schedule Sundays at 4:07pm NZ, run second-brain/agents/10-weekly-review-agent.md with Todoist and Google Calendar read-only` |
| Weekly reflection | 09 Journal | `CRON_TZ=Pacific/Auckland 7 17 * * 0` | `/schedule Sundays at 5:07pm NZ, run the Journal Agent weekly reflection` |
| Quotes weekly | 06 Quotes | `CRON_TZ=Pacific/Auckland 7 7 * * 1` | `/schedule Mondays at 7:07am NZ, run second-brain/agents/06-quote-image-curator-agent.md` |
| Distil monthly | 03 Distil | `CRON_TZ=Pacific/Auckland 7 15 1-7 * 0` | `/schedule first Sunday of each month at 3:07pm NZ, run second-brain/agents/03-distil-agent.md monthly pattern pass` |
| PARA re-sort | 02 Organise, 08 Triage | `CRON_TZ=Pacific/Auckland 7 10 1 * *` | `/schedule on the 1st of each month at 10:07am NZ, run second-brain/routines/monthly-para-resort.md` |
| Archive sweep | 02 Organise | `CRON_TZ=Pacific/Auckland 7 10 1 1,4,7,10 *` | `/schedule quarterly on the 1st of Jan, Apr, Jul, Oct at 10:07am NZ, run second-brain/routines/quarterly-archive-sweep.md` |

## Session loops (while you are working)

```text
/loop 30m run the Capture Agent on anything new in second-brain/00_Inbox and the Todoist Inbox, read-only on Todoist
/loop 2h run the Distil Agent weekly pass on notes changed today
/loop                 (bare: uses .claude/loop.md, which keeps the repo and PR healthy)
```

## Limits that matter

- Cloud scheduled tasks: minimum interval one hour, 100 scheduled runs per
  hour per account, runs use your connectors as you. Remove connectors a
  task does not need in its settings.
- Session loops: minimum one minute, expire after seven days, only fire while
  the session is open and idle.
- Scheduled runs count against your Claude usage. Start with the weekly
  review and the two journal runs, measure for a week, then add more.

Source: Claude Code docs, https://code.claude.com/docs/en/scheduled-tasks and
https://code.claude.com/docs/en/routines.
