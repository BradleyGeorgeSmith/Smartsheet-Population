# NCH Software invoice sent

| Field | Value |
|---|---|
| Todoist | [6h7FFRQRwcjhpmp2](https://app.todoist.com/app/task/6h7FFRQRwcjhpmp2) |
| Project | Every Day Practising/Stop/Start/Keep |
| Priority | p4 |
| Due | 2026-01-29 |
| Category | Finance, subscriptions and admin |
| PARA home | `20_Areas/Finance-and-Subscriptions` |
| Sensitivity | normal |

## As captured
NCH Software invoice sent


## Context
Subscriptions have been leaking money (four Lovable top-ups in one day, renewals on tools no longer used). The weekly review's transactions step is where this gets caught.

## Prompt (paste into Claude, ChatGPT or an agent run)
```text
This is a finance, subscription or admin item:
Task: NCH Software invoice sent
Notes: (none)
From Todoist project: Every Day Practising/Stop/Start/Keep. Due: 2026-01-29.

1. Restate as a decision or an action with a deadline.
2. List what I need to see first: account, last charge, renewal date, who pays (me, Hydralada, Caleb), where the invoice lives.
3. If it is a subscription: give the keep/cancel/downgrade test (used in the last 30 days? duplicates another tool? needed for an active project?) and a recommendation with the reason.
4. If it is a payment or refund: the exact steps and the message to send, under 60 words.
5. Add a line for 20_Areas/Finance-and-Subscriptions/subscriptions.md (name, cost, cycle, renewal, decision).
6. Calendar line for the renewal or follow-up in Morgen.
No financial advice beyond organising the decision.
```

## Next steps
1. Due date 2026-01-29 has passed: reschedule or archive at the next review.
2. Find the last invoice or charge and the renewal date.
3. Decide keep, cancel or downgrade; act the same day.
4. Record it in 20_Areas/Finance-and-Subscriptions/subscriptions.md.

## Session suggestion
Run this together with the other items in `todo-prompts/finance-admin/` (one Claude Code
session per category, oldest first). Related agent: see `second-brain/agents/README.md`.
