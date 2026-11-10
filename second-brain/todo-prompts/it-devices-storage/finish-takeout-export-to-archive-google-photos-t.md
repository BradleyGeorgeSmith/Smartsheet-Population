# Finish Takeout export to archive Google Photos to Google Drive so an automatic publishing loop (Claude plus personal Instagram) can be set up

| Field | Value |
|---|---|
| Todoist | [6hPr4JPJJvG9HVf7](https://app.todoist.com/app/task/6hPr4JPJJvG9HVf7) |
| Project | Inbox |
| Priority | p4 |
| Due | 2026-08-31 |
| Category | IT, devices, accounts and storage |
| PARA home | `20_Areas/IT-Devices-and-Storage` |
| Sensitivity | normal |

## As captured
Finish Takeout export to archive Google Photos to Google Drive so an automatic publishing loop (Claude plus personal Instagram) can be set up


## Context
Most of these trace back to one root cause: files spread over OneDrive, NAS, external drives and three laptops, plus a managed-device policy from work. Every fix should move toward one PARA tree on the NAS with verified backups.

## Prompt (paste into Claude, ChatGPT or an agent run)
```text
This is an IT, device, account or storage item:
Task: Finish Takeout export to archive Google Photos to Google Drive so an automatic publishing loop (Claude plus personal Instagram) can be set up
Notes: (none)
From Todoist project: Inbox. Due: 2026-08-31.

1. Restate as a single verifiable outcome.
2. Diagnose: list the two or three most likely causes or prerequisites, in order of likelihood.
3. Give the exact steps for Windows 11 (or the named device), including menu paths or commands, under 10 steps. Mark anything that needs admin rights or IT (OneHQ, UBT) approval.
4. Data-safety check: what must be backed up or verified before any delete, de-sync or reinstall. Never propose deleting data that has not been verified on the NAS and one other place.
5. If this relates to Streamline, group policy or "managed by your organisation", explain in two sentences what is likely happening and what the owner can and cannot change on a device they own.
6. PARA home: 20_Areas/IT-Devices-and-Storage/<device or service>.
7. Passwords: recommend unique generated passwords in 1Password, never a shared base password.
```

## Next steps
1. Due date 2026-08-31 has passed: reschedule or archive at the next review.
2. Back up or verify before changing anything.
3. Do the steps; if blocked by policy, raise a OneHQ ticket with the exact error.
4. Record the fix in 20_Areas/IT-Devices-and-Storage/runbook.md.

## Session suggestion
Run this together with the other items in `todo-prompts/it-devices-storage/` (one Claude Code
session per category, oldest first). Related agent: see `second-brain/agents/README.md`.
