# Activation log

Scheduled tasks created in the claude.ai cloud (each firing starts a fresh
session in the Default environment, clones the repository and runs the
agent prompt). Manage them from the claude.ai scheduled-tasks page or with
`list_triggers` / `update_trigger` in a Claude Code session.

## 2026-11-10: owner approved "start all requests"

| Routine | Cron (Pacific/Auckland) | Trigger id | First run (UTC) |
|---|---|---|---|
| Weekly Review | `7 16 * * 0` | trig_01ELwHfXKtzENtHaCjbWUrpH | 2026-11-15 03:07 |
| Journal morning pages | `7 6 * * 1-6` | trig_012MAjn5YCpDfnFwrp23ogqq | 2026-11-11 17:07 |
| Capture daily | `37 6 * * *` | trig_01LQzKL7zRfERc1Y2JxsdJXh | 2026-11-11 17:37 |
| Journal evening shutdown | `37 17 * * 1-5` | trig_01Xk6GPNADwyPyEppsEPWKrh | 2026-11-11 04:37 |
| Marketing capture | `7 18 * * 1-5` | trig_01SYFinbKP1ouL884ADrY2a4 | 2026-11-11 05:07 |
| Express weekly | `7 14 * * 5` | trig_015SJTL69AWyw9FcWHjubstA | 2026-11-13 01:07 |
| Pinterest to Dropbox sync | `7 9 * * 6` | trig_01NSGivqFcia959Q6RY44xZi | 2026-11-13 20:07 |
| Weekly reflection | `7 17 * * 0` | trig_017jv4VuhqzZVk9hVjBCHREV | 2026-11-15 04:07 |
| Quotes and cards weekly | `7 7 * * 1` | trig_01XZPi8Sv7yWtQac5innQf3p | 2026-11-15 18:07 |
| Distil monthly pattern pass | `7 15 1-7 * 0` | trig_019Y4rLvJDTq28Z2kjUFwjBM | 2026-11-15 02:07 |
| Monthly PARA re-sort | `7 10 1 * *` | trig_01NgRah7wrrZybjUrKHVEhxn | 2026-11-30 21:07 |
| Quarterly archive sweep | `7 10 1 1,4,7,10 *` | trig_01AKAgvFH5kDZuz4UvCp326J | 2026-12-31 21:07 |

## Known limits of this activation

- **No connectors on the fired sessions.** The scheduled tasks were created
  from a Claude Code session, and this organisation does not allow passing
  connector grants through that route. Fired sessions therefore run with
  the repository, the network proxy and its secrets, but without Todoist,
  Google Calendar, Dropbox or HubSpot tools. Every prompt says "if the
  connector is available", so the runs still produce their files from what
  is in the repository. To give a routine its connectors, recreate it from
  the claude.ai scheduled-tasks page and tick the connectors there.
- **Pinterest and Dropbox API tokens.** Network secrets were saved for
  api.pinterest.com and api.dropboxapi.com on 2026-11-10, but both services
  rejected them (Pinterest 401, Dropbox `invalid_access_token`) when tested
  from this session. Until the values are replaced with valid tokens (and a
  token added for content.dropboxapi.com for uploads), the Saturday sync will
  stop at the dry run and write a note under `agents/runs/`.
- **Branch.** Until PR #1 merges, each run checks out `ccr-796462b2-dk3ic5`.
  After the merge they work on `main`.

## Dropbox PARA tree

Created 2026-11-10 under `/Brad Smith/` (namespace 447843443) with the
Dropbox connector: the five PARA roots, three inbox sub-folders, eight
project folders, eleven area folders, thirteen resource folders (including
Inspiration/{Architecture, Manufacturing, Innovation, Branding, Pinterest,
Quotes, Quote-Cards}) and three archive year folders. Nothing was moved or
deleted. Any folder can be removed again from Dropbox if unwanted.
