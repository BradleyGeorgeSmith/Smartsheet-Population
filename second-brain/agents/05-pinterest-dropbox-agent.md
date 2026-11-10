# 05 Pinterest to Dropbox Agent

**Job**: mirror every pin image on Brad's Pinterest boards into Dropbox
under a PARA-aligned Inspiration tree, with a manifest and tags, so the
inspiration library lives where the design tools can reach it.
**Trigger**: weekly, Saturday 09:07 NZ time, or on demand.
**Inputs**: Pinterest account (OAuth token with `boards:read`, `pins:read`),
Dropbox token (`files.content.write`, `files.metadata.read`), optional board
filter.
**Tools**: `scripts/pinterest_to_dropbox.py` (Pinterest API v5, Dropbox
API v2), repository files. Tokens come from environment variables only.
**Prompts used**: `09_visual-inspiration/pinterest-to-dropbox-run.md`,
`pin-board-audit.md`.

## Procedure
1. Dry run: list boards, pin counts, target paths.
2. Real run with `--since-last-run`: download original-size images, upload
   to `/Brad Smith/30_Resources/Inspiration/Pinterest/<Board>/<pin-id>_<slug>.jpg`,
   skipping files that already exist (hash check).
3. Write the manifest JSON (pin id, title, description, link, board, dropbox
   path, sha256) to `30_Resources/Inspiration/Pinterest/_manifests/`.
4. Run the Pin Board Audit on new pins; save the tagging table beside the
   manifest.
5. Run report: counts, failures, boards that look like they belong under
   Architecture, Manufacturing, Branding or Innovation and should be
   re-homed (proposal only).

## Guardrails
Never deletes from Pinterest or Dropbox. Only Brad's own boards. Respects
Pinterest rate limits (the script sleeps on 429). Image copyright stays with
the original creators; this is a private reference library, not for
republishing.

## Setup (one time)
1. Create a Pinterest app at https://developers.pinterest.com/apps/ and
   complete OAuth for scopes `boards:read pins:read`. Store the access token
   as `PINTEREST_ACCESS_TOKEN`.
2. Create a Dropbox app (scoped, full Dropbox or an app folder) at
   https://www.dropbox.com/developers/apps with `files.content.write` and
   `files.metadata.read`. Generate a token, store as `DROPBOX_ACCESS_TOKEN`.
   For the Hydralada team account also set `DROPBOX_PATH_ROOT_NS` to the
   root namespace id so paths resolve inside the team space.
3. `pip install -r second-brain/scripts/requirements.txt`.
4. `python second-brain/scripts/pinterest_to_dropbox.py --dry-run`.

## Run prompt
See `30_Resources/Prompts/09_visual-inspiration/pinterest-to-dropbox-run.md`.
