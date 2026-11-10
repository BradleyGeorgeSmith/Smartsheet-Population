# Migrate OneDrive Business to NAS

| Field | Value |
|---|---|
| Todoist | [6h7FFRf4XqVjFGpR](https://app.todoist.com/app/task/6h7FFRf4XqVjFGpR) |
| Project | Every Day Practising/Stop/Start/Keep |
| Priority | p4 |
| Due | 2026-01-29 |
| Category | IT, devices, accounts and storage |
| PARA home | `20_Areas/IT-Devices-and-Storage` |
| Sensitivity | normal |

## As captured
Migrate OneDrive Business to NAS


## Context
Most of these trace back to one root cause: files spread over OneDrive, NAS, external drives and three laptops, plus a managed-device policy from work. Every fix should move toward one PARA tree on the NAS with verified backups.

## Prompt (paste into Claude, ChatGPT or an agent run)
```text
This is an IT, device, account or storage item:
Task: Migrate OneDrive Business to NAS
Notes: (none)
From Todoist project: Every Day Practising/Stop/Start/Keep. Due: 2026-01-29.

1. Restate as a single verifiable outcome.
2. Diagnose: list the two or three most likely causes or prerequisites, in order of likelihood.
3. Give the exact steps for Windows 11 (or the named device), including menu paths or commands, under 10 steps. Mark anything that needs admin rights or IT (OneHQ, UBT) approval.
4. Data-safety check: what must be backed up or verified before any delete, de-sync or reinstall. Never propose deleting data that has not been verified on the NAS and one other place.
5. If this relates to Streamline, group policy or "managed by your organisation", explain in two sentences what is likely happening and what the owner can and cannot change on a device they own.
6. PARA home: 20_Areas/IT-Devices-and-Storage/<device or service>.
7. Passwords: recommend unique generated passwords in 1Password, never a shared base password.
```

## Next steps
1. Due date 2026-01-29 has passed: reschedule or archive at the next review.
2. Back up or verify before changing anything.
3. Do the steps; if blocked by policy, raise a OneHQ ticket with the exact error.
4. Record the fix in 20_Areas/IT-Devices-and-Storage/runbook.md.

## Session suggestion
Run this together with the other items in `todo-prompts/it-devices-storage/` (one Claude Code
session per category, oldest first). Related agent: see `second-brain/agents/README.md`.
