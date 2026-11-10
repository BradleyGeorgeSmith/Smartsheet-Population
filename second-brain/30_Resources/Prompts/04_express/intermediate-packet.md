# Intermediate Packet Builder

**Purpose**: turn a pile of notes into one small, reusable, shippable piece
of work. Forte's unit of output.
**When**: at least once a week, whenever a project stalls.
**Inputs**: `{{project}}`, `{{outcome}}`, `{{notes}}`, `{{packet_type}}` (one of:
outline, checklist, one-pager, slide, email draft, brief, shot list, FAQ).

```text
Project: {{project}}
Outcome the project exists to achieve: {{outcome}}
Packet type wanted: {{packet_type}}

Source notes:
<notes>
{{notes}}
</notes>

Build one {{packet_type}} that moves this project forward and can be reused
in other projects. Requirements:
- It must be usable as-is by someone else with no further explanation.
- Pull only from the notes. Mark any gap with [NEED: what is missing].
- Length: the shortest version that is complete. A one-pager is one page.
- End with "Reuse ideas": two other contexts this packet could serve.
- Markdown.
```

**Output**: file under `10_Projects/<project>/packets/`.
**Source**: Forte's Intermediate Packets concept (paraphrased), original prompt.
