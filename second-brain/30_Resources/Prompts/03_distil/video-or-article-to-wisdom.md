# Video or Article to Wisdom (Fabric extract_wisdom wrapper)

**Purpose**: run Fabric's `extract_wisdom` pattern on a YouTube transcript,
podcast, or article and file the result. Serves Brad's "rewatch videos that
improve productivity" and "set up what videos to watch in Fabric" tasks.
**When**: after any long-form content worth keeping.
**Inputs**: `{{transcript}}`, `{{source_url}}`, `{{speaker}}`.

Use the verbatim pattern in `../fabric-patterns/extract_wisdom.md` as the
system prompt, then add this user message:

```text
Source: {{source_url}}
Speaker(s): {{speaker}}

<input>
{{transcript}}
</input>

After the standard sections, add:
## PARA FILING
Project, Area or Resource this belongs to, and why, in one line.
## ACTIONS FOR ME
Up to 5 tasks, verb first, under 12 words, that follow from the content.
```

With the Fabric CLI the equivalent is:

```bash
yt --transcript "{{source_url}}" | fabric --pattern extract_wisdom > "00_Inbox/$(date +%F)_wisdom.md"
```

**Output**: a wisdom note ready for `00_Inbox`, then PARA.
**Source**: Daniel Miessler, Fabric, MIT licence. Wrapper is original.
