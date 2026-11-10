# Scripts

| Script | Purpose | Needs |
|---|---|---|
| `pinterest_to_dropbox.py` | Mirror all pin images from your Pinterest boards into Dropbox under the PARA Inspiration tree, with a JSON manifest. Dry-run mode. Never deletes. | `PINTEREST_ACCESS_TOKEN`, `DROPBOX_ACCESS_TOKEN`, optional `DROPBOX_PATH_ROOT_NS` |
| `quotes_fetch.py` | Pull a raw batch of attributed quotes by theme from free APIs for the Quote Curator to verify. | network |
| `para_scaffold.py` | Create the PARA folder tree on a local drive, NAS, OneDrive folder, or in Dropbox. Folders only. | optional `DROPBOX_ACCESS_TOKEN` |
| `todoist_prompt_generator.py` | Turn the Todoist export in `data/todoist_tasks.tsv` into one contextual prompt file per task under `todo-prompts/`, plus index, dedupe and stale reports. | none |

Install: `pip install -r requirements.txt` (Python 3.10 or newer).

Tokens are read from environment variables only. For cloud scheduled tasks,
store them as network secrets on the environment, not as plain variables.

When a token is stored as a network secret, the environment's proxy injects
it into requests to that host and no environment variable holds it. Run the
scripts with placeholder values (`PINTEREST_ACCESS_TOKEN=proxy-injected
DROPBOX_ACCESS_TOKEN=proxy-injected`) so they do not skip the work; the proxy
overwrites the Authorization header. Dropbox needs secrets for both
`api.dropboxapi.com` (metadata, folders) and `content.dropboxapi.com`
(uploads). For the Hydralada team account set
`DROPBOX_PATH_ROOT_NS=2661730259` so `/Brad Smith/...` paths resolve.

## Pinterest token (one-time)
1. https://developers.pinterest.com/apps/ create an app (standard access is
   enough for your own boards).
2. Redirect URI can be `https://localhost/`. Scopes: `boards:read pins:read`.
3. Complete the OAuth flow once (the Pinterest docs "Authentication" page has
   the two curl calls) and keep the refresh token in 1Password.

## Dropbox token (one-time)
1. https://www.dropbox.com/developers/apps create a scoped app, "Full Dropbox".
2. Permissions: `files.metadata.read`, `files.content.write`, `files.content.read`.
3. Generate an access token (or set up refresh tokens for long-lived use).
4. Team account: find your root namespace id with `/2/users/get_current_account`
   (`root_info.root_namespace_id`) and set `DROPBOX_PATH_ROOT_NS`.
