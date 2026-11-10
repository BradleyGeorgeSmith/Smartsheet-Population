# Pinterest to Dropbox Sync (agent run prompt)

**Purpose**: the prompt an agent or a Claude Code session uses to run the
sync script, verify results, and file the audit.
**When**: weekly, or after a pinning session.
**Inputs**: environment variables `PINTEREST_ACCESS_TOKEN`,
`DROPBOX_ACCESS_TOKEN`; optional `--board` filter.

```text
Run the Pinterest to Dropbox sync for my boards.

1. First run `python scripts/pinterest_to_dropbox.py --dry-run` and show me
   the boards found, pin counts, and the Dropbox target paths it would use
   under /Brad Smith/30_Resources/Inspiration/Pinterest/<board>/.
2. If the dry run lists no errors, run it for real with `--since-last-run`
   so only new pins download.
3. Report: pins downloaded, skipped as duplicates, failed (with reasons).
4. Save the run manifest (JSON) the script writes to
   30_Resources/Inspiration/Pinterest/_manifests/.
5. Feed the new pins' titles and descriptions to the Pin Board Audit prompt
   and save the tagging table beside the manifest.
6. Never delete anything in Dropbox. Never store tokens in files.
```

**Output**: images in Dropbox, manifest and tagging table in the repo.
**Source**: original. API references: Pinterest API v5
(https://developers.pinterest.com/docs/api/v5/), Dropbox API v2
(https://www.dropbox.com/developers/documentation/http/documentation).
