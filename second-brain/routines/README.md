# Routines and Loops

Routines are the heartbeat of the system. Each file defines what happens,
when, and the exact command to activate it in three ways:

1. **Cloud scheduled task** (runs without your machine): `/schedule` in any
   Claude Code session on this repository, or the web form at
   https://claude.ai/code/routines. Minimum interval one hour. Connectors
   you include are usable by the run. See `schedules.md`.
2. **Session loop** (while a Claude Code session is open): `/loop <interval>
   <prompt>` or bare `/loop`, which uses `.claude/loop.md` at the repo root.
   Session loops expire after seven days.
3. **Desktop scheduled task** (runs on your Windows machine with local file
   access): Claude Desktop, Scheduled tasks, paste the same prompt.

Nothing here is activated yet. Activate in this order and live with each for
a week before adding the next:

1. `weekly-review.md` (Sunday)
2. `daily-shutdown.md` then `morning-plan.md`
3. `capture-daily.md`
4. `quotes-weekly.md`, `pinterest-weekly.md`, `marketing-daily.md`
5. `monthly-para-resort.md`, `quarterly-archive-sweep.md`

Timezone: all times are NZ local (Pacific/Auckland). Cron lines are written
with `CRON_TZ=Pacific/Auckland` for cloud tasks. Minutes are off the hour on
purpose, because on-the-hour runs can start late.
