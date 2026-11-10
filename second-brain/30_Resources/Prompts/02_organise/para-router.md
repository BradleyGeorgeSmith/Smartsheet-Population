# PARA Router (file anything to the right folder)

**Purpose**: decide where a note, file, bookmark or task belongs under PARA
using Forte's actionability rule. Works for one item or a batch.
**When**: weekly review, or any time `00_Inbox` has more than 20 items.
**Inputs**: `{{items}}` (one per line: title plus one-line summary),
`{{projects}}`, `{{areas}}`, `{{resources}}`.

```text
You are the Organise step of a Building a Second Brain system that uses PARA.

Current folders:
PROJECTS (active, each has an end): {{projects}}
AREAS (ongoing responsibilities): {{areas}}
RESOURCES (topics of interest): {{resources}}
ARCHIVES: anything inactive.

Items to file:
<items>
{{items}}
</items>

For each item output one table row:
| # | Item | PARA category | Folder | Why (under 12 words) | Next action or "none" |

Rules, in order:
1. If an active project needs it, file it there, even if a topic folder also fits.
2. Else if it maintains a standard in an area, file it there.
3. Else if it is interesting but uncommitted, file it under a resource.
4. Else archive it.
5. If you need a folder that does not exist, propose it with the prefix NEW:
   and only if at least three items would land in it.
6. Flag anything that looks like a duplicate of another item in the batch.
7. Flag anything that reads as a goal or value statement rather than a task,
   and suggest it goes to 20_Areas/Vision-Mission-Values.

After the table, list proposed NEW folders and the duplicates found.
```

**Output**: a routing table you can act on in one pass.
**Source**: Forte's "organise by actionability" (paraphrased), original prompt.
