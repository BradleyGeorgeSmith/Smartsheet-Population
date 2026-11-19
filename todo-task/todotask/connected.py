"""Commands that talk to Todoist and to the Claude API.

These give a way to run the pipeline with no Claude Code session at all, for example from
Windows Task Scheduler:

    python -m todotask todoist-pull           start a brief for every new Todoist entry
    python -m todotask expand brief.json      have Claude write the brief
    python -m todotask todoist-writeback ...  put the title and description on the task
    python -m todotask sweep                  all of the above, for every new entry

Two secrets are read from the environment and never written anywhere:

    TODOIST_API_TOKEN   Todoist: Settings, Integrations, Developer, "Copy API token"
    ANTHROPIC_API_KEY   only for ``expand`` and ``sweep``

Inside Claude Code none of this is needed: the skills use the Todoist connector instead.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Callable

from . import render as rendering
from . import spec
from .models import TASK_TYPES, Entry, TaskBrief, model_example

TODOIST_API = "https://api.todoist.com/api/v1"
DEFAULT_MODEL = "claude-fable-5-2"
CONFIG_DIR = Path(__file__).resolve().parent.parent

# Limits Todoist publishes for a task name, a description and a comment.
TITLE_LIMIT, DESCRIPTION_LIMIT, COMMENT_LIMIT = 500, 16383, 15000
NOTES_CUT = 2000

DEFAULTS: dict[str, Any] = {
    "filter": "#Inbox & created after: -{days} days & !recurring",
    "skip_labels": [spec.LABEL_BRIEFED, spec.LABEL_SKIP, "from-email"],
    "window_days": 3,
    "max_briefs_per_run": 10,
    "write_back": True,
    "comment_brief": True,
    "keep_description_over": 500,
}


class ConnectionProblem(RuntimeError):
    """Something outside this program refused or failed, explained in plain words."""


def load_config(folder: Path = CONFIG_DIR) -> dict[str, Any]:
    """Defaults, then ``config.json``, then ``config.local.json`` (which is never committed)."""
    config = dict(DEFAULTS)
    for name in ("config.json", "config.local.json"):
        path = folder / name
        if path.exists():
            config.update(json.loads(path.read_text(encoding="utf-8")))
    return config


# --------------------------------------------------------------------------- #
# Todoist
# --------------------------------------------------------------------------- #

class Todoist:
    """The few Todoist API calls the pipeline needs. Standard library only."""

    def __init__(self, token: str | None = None, *, send: Callable | None = None, sleep: Callable = time.sleep):
        self.token = token or os.environ.get("TODOIST_API_TOKEN", "")
        if not self.token:
            raise ConnectionProblem(
                "No Todoist token. In Todoist open Settings, Integrations, Developer, copy the API token, "
                "and set it as the environment variable TODOIST_API_TOKEN."
            )
        self._send = send or urllib.request.urlopen
        self._sleep = sleep

    def _call(self, method: str, path: str, *, params: dict | None = None, body: dict | None = None) -> Any:
        url = TODOIST_API + path
        if params:
            # The filter holds #, & and spaces, so it must be encoded, never pasted into the address.
            url += "?" + urllib.parse.urlencode(params)
        headers = {"Authorization": f"Bearer {self.token}"}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
            headers["X-Request-Id"] = str(uuid.uuid4())
        for attempt in range(3):
            request = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with self._send(request, timeout=30) as response:
                    text = response.read().decode("utf-8")
                    return json.loads(text) if text.strip() else None
            except urllib.error.HTTPError as error:
                detail = _error_detail(error)
                if error.code in (429, 500, 502, 503, 504) and attempt < 2:
                    self._sleep(min(float(detail.get("retry_after") or 2 * (attempt + 1)), 30))
                    continue
                raise ConnectionProblem(_todoist_message(error.code, detail)) from error
            except urllib.error.URLError as error:
                raise ConnectionProblem(f"Todoist could not be reached: {error.reason}") from error
        raise ConnectionProblem("Todoist did not answer after three tries.")

    def filter_tasks(self, query: str) -> list[dict]:
        """Every active task matching a Todoist filter, following the paging cursor."""
        tasks: list[dict] = []
        cursor = None
        while True:
            params = {"query": query, "limit": 200}
            if cursor:
                params["cursor"] = cursor
            page = self._call("GET", "/tasks/filter", params=params) or {}
            tasks.extend(page.get("results") or [])
            cursor = page.get("next_cursor")
            if not cursor:
                return tasks

    def get_task(self, task_id: str) -> dict:
        return self._call("GET", f"/tasks/{urllib.parse.quote(task_id, safe='')}")

    def update_task(self, task_id: str, **fields: Any) -> dict:
        # Todoist updates with POST. Only the fields sent are changed.
        return self._call("POST", f"/tasks/{urllib.parse.quote(task_id, safe='')}", body=fields)

    def add_comment(self, task_id: str, content: str) -> dict:
        return self._call("POST", "/comments", body={"task_id": task_id, "content": content})

    def label_names(self) -> set[str]:
        names: set[str] = set()
        cursor = None
        while True:
            page = self._call("GET", "/labels", params={"limit": 200, **({"cursor": cursor} if cursor else {})}) or {}
            names.update(label.get("name", "") for label in page.get("results") or [])
            cursor = page.get("next_cursor")
            if not cursor:
                return names

    def ensure_labels(self, wanted: list[str]) -> list[str]:
        """Create any missing label. Returns the names that were created."""
        missing = [name for name in wanted if name not in self.label_names()]
        for name in missing:
            self._call("POST", "/labels", body={"name": name})
        return missing


def _error_detail(error: urllib.error.HTTPError) -> dict:
    try:
        body = json.loads(error.read().decode("utf-8"))
    except Exception:  # noqa: BLE001 - an unreadable error body is still an error
        body = {}
    extra = body.get("error_extra") if isinstance(body, dict) else None
    return {
        "message": body.get("error", "") if isinstance(body, dict) else "",
        "retry_after": (extra or {}).get("retry_after") or error.headers.get("Retry-After"),
    }


def _todoist_message(code: int, detail: dict) -> str:
    if code == 401:
        return "Todoist refused the token. Copy a fresh one from Settings, Integrations, Developer."
    if code == 410:
        return "Todoist says this address is retired. This program needs updating."
    said = f" Todoist said: {detail['message']}" if detail.get("message") else ""
    return f"Todoist answered with error {code}.{said}"


def new_entries(todoist: Todoist, config: dict, *, days: int | None = None, limit: int | None = None) -> tuple[list[dict], int]:
    """New tasks without a brief, newest first, and how many more were left for next time.

    Labels are checked here, not in the filter, because Todoist is changing how filters
    write labels (``@label`` to ``%label``).
    """
    window = days or int(config["window_days"])
    found = todoist.filter_tasks(str(config["filter"]).replace("{days}", str(window)))
    skip = set(config["skip_labels"])
    keep = [
        task for task in found
        if not task.get("checked")
        and not skip.intersection(task.get("labels") or [])
        and not (task.get("due") or {}).get("is_recurring")
        and str(task.get("content") or "").strip()
    ]
    keep.sort(key=lambda task: str(task.get("added_at") or ""), reverse=True)
    most = limit or int(config["max_briefs_per_run"])
    return keep[:most], max(0, len(keep) - most)


def entry_from_task(task: dict) -> Entry:
    notes = str(task.get("description") or "").strip()
    if len(notes) > NOTES_CUT:
        notes = notes[:NOTES_CUT].rstrip() + f"\n\n[The note was cut here. It continues for about {len(notes) - NOTES_CUT} more characters.]"
    return Entry(
        text=str(task["content"]).strip(), notes=notes, source="Todoist",
        list=str(task.get("project_id") or ""), task_id=str(task["id"]),
        captured_on=str(task.get("added_at") or "")[:10],
        labels=[str(label) for label in task.get("labels") or []],
    )


def existing_brief(root: Path, task_id: str) -> Path | None:
    """The brief already started for this task, if there is one."""
    for path in sorted(Path(root).glob("*/brief.json")):
        try:
            if json.loads(path.read_text(encoding="utf-8")).get("entry", {}).get("task_id") == task_id:
                return path
        except (OSError, ValueError):
            continue
    return None


def write_back(todoist: Todoist, task: TaskBrief, config: dict, *, dry_run: bool = False) -> dict:
    """Put the title and description on the Todoist task. Returns what was, or would be, sent."""
    if task.entry.source != "Todoist" or not task.entry.task_id:
        raise ValueError("This brief did not come from Todoist, so there is no task to write back to.")
    problems = task.problems()
    if problems:
        raise ValueError("The brief is not ready to write back: " + problems[0])

    current = todoist.get_task(task.entry.task_id)
    labels = list(dict.fromkeys([*(current.get("labels") or []), spec.LABEL_BRIEFED]))  # the field replaces the whole list
    change: dict[str, Any] = {"content": task.writeback.title[:TITLE_LIMIT], "labels": labels}

    note = rendering.writeback_note(task)
    own_description = str(current.get("description") or "")
    if len(own_description) <= int(config["keep_description_over"]) and len(note) <= DESCRIPTION_LIMIT:
        change["description"] = note
    comment = rendering.brief_prompt(task)[:COMMENT_LIMIT] if config.get("comment_brief") else ""

    if not dry_run:
        todoist.ensure_labels([spec.LABEL_BRIEFED])
        todoist.update_task(task.entry.task_id, **change)
        if comment:
            todoist.add_comment(task.entry.task_id, comment)
    return {"task_id": task.entry.task_id, "was": current.get("content", ""), "change": change, "comment": bool(comment), "sent": not dry_run}


# --------------------------------------------------------------------------- #
# Claude
# --------------------------------------------------------------------------- #

_TEXT = {"type": "string"}
_LIST = {"type": "array", "items": {"type": "string"}}

BRIEF_FORMAT = {
    "type": "object",
    "additionalProperties": False,
    "required": ["task_type", "brief", "writeback"],
    "properties": {
        "task_type": {"type": "string", "enum": list(TASK_TYPES)},
        "brief": {
            "type": "object",
            "additionalProperties": False,
            "required": ["title", "description", "status", "calendar_date", "context_heading", "context", "actions", "plan"],
            "properties": {
                "title": _TEXT, "description": _TEXT, "status": _TEXT, "calendar_date": _TEXT,
                "context_heading": _TEXT, "context": _LIST, "actions": _LIST,
                "plan": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["output", "steps", "tools", "rhythm", "done_when"],
                    "properties": {"output": _TEXT, "steps": _LIST, "tools": _TEXT, "rhythm": _TEXT, "done_when": _TEXT},
                },
            },
        },
        "writeback": {
            "type": "object",
            "additionalProperties": False,
            "required": ["title", "description"],
            "properties": {"title": _TEXT, "description": _TEXT},
        },
    },
}


def expansion_request(entry: Entry) -> str:
    """The instruction sent to Claude: the shared rules, the example, then this entry."""
    example = model_example()
    shown = {key: example.to_dict()[key] for key in ("task_type", "brief", "writeback")}
    template = (spec.SPEC_DIR / "expand-json-prompt.txt").read_text(encoding="utf-8").strip()
    values = {
        "EXAMPLE_ENTRY": example.entry.text,
        "EXAMPLE_JSON": json.dumps(shown, indent=2, ensure_ascii=False),
        "TODAY": entry.captured_on or "Not supplied",
        "ENTRY": entry.text,
        "NOTES": entry.notes or "None",
    }
    # One pass, so an entry that happens to contain "{{NOTES}}" is left exactly as written.
    return re.sub(r"\{\{(" + "|".join(values) + r")\}\}", lambda match: values[match.group(1)], template)


def expand_entry(task: TaskBrief, *, client: Any = None, model: str | None = None) -> TaskBrief:
    """Have Claude write the brief for one entry. The entry itself is never changed."""
    if client is None:
        try:
            import anthropic
        except ImportError as error:
            raise ConnectionProblem("The Claude library is missing. Run: python -m pip install anthropic") from error
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY, or an `ant auth login` profile

    # Streaming, because a careful brief can take longer than an ordinary request allows.
    # If the first model declines, Anthropic's recommended fallback answers in the same call.
    with client.beta.messages.stream(
        model=model or os.environ.get("TODOTASK_MODEL") or DEFAULT_MODEL,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": BRIEF_FORMAT}},
        messages=[{"role": "user", "content": expansion_request(task.entry)}],
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == "refusal":
        category = getattr(getattr(message, "stop_details", None), "category", None)
        raise ConnectionProblem(f"Claude declined to expand this entry{f' ({category})' if category else ''}. Reword it, or expand it by hand.")
    if message.stop_reason == "max_tokens":
        raise ConnectionProblem("The reply was cut off before the brief was finished. Try again.")
    text = next((block.text for block in message.content if block.type == "text"), "")
    try:
        written = json.loads(text)
    except ValueError as error:
        raise ConnectionProblem("The reply could not be read as a brief. Try again.") from error
    return TaskBrief.from_dict({**written, "entry": task.to_dict()["entry"]})


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #

def register(commands) -> None:
    from pathlib import Path as _Path

    p = commands.add_parser("todoist-pull", help="Start a brief for every new Todoist entry.")
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--out", type=_Path, default=_Path("briefs"))
    p.set_defaults(run=cmd_pull)

    p = commands.add_parser("expand", help="Have Claude write the brief for an entry (needs ANTHROPIC_API_KEY).")
    p.add_argument("brief", type=_Path)
    p.add_argument("--model", default=None)
    p.set_defaults(run=cmd_expand)

    p = commands.add_parser("todoist-writeback", help="Put a finished brief's title and description on its Todoist task.")
    p.add_argument("brief", type=_Path)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(run=cmd_writeback)

    p = commands.add_parser("sweep", help="Pull, expand, build and write back every new Todoist entry.")
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--out", type=_Path, default=_Path("briefs"))
    p.add_argument("--model", default=None)
    p.add_argument("--dry-run", action="store_true", help="Write the briefs, but change nothing in Todoist.")
    p.set_defaults(run=cmd_sweep)


def _guard(run: Callable) -> Callable:
    def wrapped(args) -> int:
        try:
            return run(args)
        except ConnectionProblem as problem:
            print(f"todotask: {problem}", file=sys.stderr)
            return 3
    return wrapped


def _pull(args, todoist: Todoist, config: dict) -> list[Path]:
    from .cli import task_folder

    tasks, left = new_entries(todoist, config, days=args.days, limit=args.limit)
    paths: list[Path] = []
    for item in tasks:
        path = existing_brief(args.out, str(item["id"]))
        if path is None:
            task = TaskBrief(entry=entry_from_task(item))
            folder = task_folder(args.out, task)
            path = task.save(folder / "brief.json")
            rendering.render(task, folder / f"{folder.name}.docx")
        paths.append(path)
    if left:
        print(f"{left} more new entries were left for the next run.", file=sys.stderr)
    return paths


@_guard
def cmd_pull(args) -> int:
    for path in _pull(args, Todoist(), load_config()):
        print(path)
    return 0


@_guard
def cmd_expand(args) -> int:
    from .cli import write_outputs

    task = expand_entry(TaskBrief.load(args.brief), model=args.model)
    task.save(args.brief)
    problems = task.problems()
    for line in write_outputs(task, args.brief.parent):
        print(line)
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)
    return 1 if problems else 0


@_guard
def cmd_writeback(args) -> int:
    result = write_back(Todoist(), TaskBrief.load(args.brief), load_config(), dry_run=args.dry_run)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


@_guard
def cmd_sweep(args) -> int:
    from .cli import write_outputs

    config, todoist = load_config(), Todoist()
    report = []
    for path in _pull(args, todoist, config):
        task = TaskBrief.load(path)
        row: dict[str, Any] = {"entry": task.entry.text[:80], "brief": str(path)}
        try:
            if not task.is_expanded:
                task = expand_entry(task, model=args.model)
                task.save(path)
            problems = task.problems()
            if problems:
                row["left_alone"] = problems[0]
            else:
                write_outputs(task, path.parent)
                row["title"] = task.brief.title
                if config.get("write_back"):
                    row["todoist"] = write_back(todoist, task, config, dry_run=args.dry_run)["sent"]
        except (ConnectionProblem, ValueError) as problem:
            row["left_alone"] = str(problem)
        report.append(row)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0
