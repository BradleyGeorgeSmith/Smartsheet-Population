# Delegation Brief (to a person or an agent)

**Purpose**: write tasks "as though I had thirty agents or staff" (Brad's own
instruction). Turns a one-line to-do into a brief someone else can execute.
**When**: any task you will not do yourself this week.
**Inputs**: `{{task}}`, `{{context}}`, `{{who}}` (person, OpenClaw agent,
Claude scheduled task, Fiverr), `{{deadline}}`.

```text
Task as I wrote it: {{task}}
Context: {{context}}
Delegate to: {{who}}
Deadline: {{deadline}}

Write a delegation brief in Markdown:
- OUTCOME: one sentence, what exists when this is done.
- WHY IT MATTERS: one sentence linking to a project or area.
- INPUTS: files, links, logins needed (name them; never include passwords;
  say "in 1Password under X").
- STEPS: numbered, each one action, each under 15 words.
- DECISIONS RESERVED FOR ME: what they must ask before doing.
- DONE CHECKLIST: 3 to 5 verifiable checks.
- REPORT BACK: format and where (Todoist comment, Slack, email, repo file).
- ESTIMATE: time and cost if any.
If {{who}} is an AI agent, add a RUN PROMPT block they can be given verbatim.
```

**Output**: attach as the Todoist task description or `agents/runs/<task>.md`.
**Source**: original.
