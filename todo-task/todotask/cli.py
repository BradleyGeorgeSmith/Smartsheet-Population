"""Command line for the ToDo Task pipeline.

    python -m todotask template                 build the blank Word template
    python -m todotask new "entry text"         start a document for one To Do entry
    python -m todotask render brief.json        build the finished document, prompt and write-back
    python -m todotask prompt brief.json        print the Claude Code session prompt
    python -m todotask check brief.json         list anything that breaks the brief structure
    python -m todotask app                      build the ToDo Task Builder page from the spec
    python -m todotask wordskill                package the green prompt as a Claude skill for Word
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from . import __version__, render as rendering
from .models import Entry, TaskBrief, slugify

DEFAULT_OUT = Path("briefs")
TEMPLATE_NAME = "ToDo-Task-Brief-TEMPLATE"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="todotask",
        description="Turn a short To Do entry into a Word brief and a Claude Code prompt.",
    )
    parser.add_argument("--version", action="version", version=f"todotask {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    p = commands.add_parser("template", help="Build the blank Word template (.docx and .dotx).")
    p.add_argument("--out", type=Path, default=Path("templates"), help="Folder to write into.")
    p.set_defaults(run=cmd_template)

    p = commands.add_parser("new", help="Start a document for one To Do entry.")
    p.add_argument("entry", nargs="?", default="", help="The To Do entry, exactly as captured. Use '-' to read it from standard input.")
    p.add_argument("--from-json", type=Path, default=None, metavar="FILE",
                   help="Read the entry from a JSON file with text, notes, source, list, task_id and captured_on. "
                        "Safest when the entry holds quotes or line breaks.")
    p.add_argument("--notes", default="", help="Anything already in the task's notes.")
    p.add_argument("--source", default="Manual", help="Microsoft To Do, Todoist or Manual.")
    p.add_argument("--list", default="", dest="list_name", help="The list or project the task is in.")
    p.add_argument("--task-id", default="", help="Task id or link.")
    p.add_argument("--labels", default="", help="Labels already on the task, separated by commas.")
    p.add_argument("--date", default="", help="Capture date as YYYY-MM-DD. Defaults to today.")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Folder that holds one sub-folder per task.")
    p.set_defaults(run=cmd_new)

    p = commands.add_parser("render", help="Build the finished document, prompt and write-back from a brief.")
    p.add_argument("brief", type=Path, help="Path to brief.json.")
    p.add_argument("--out", type=Path, default=None, help="Folder to write into. Defaults to the brief's folder.")
    p.add_argument("--force", action="store_true", help="Render even if the brief has structure problems.")
    p.set_defaults(run=cmd_render)

    p = commands.add_parser("prompt", help="Print the Claude Code session prompt for a brief.")
    p.add_argument("brief", type=Path)
    p.set_defaults(run=cmd_prompt)

    p = commands.add_parser("check", help="List anything that breaks the brief structure.")
    p.add_argument("brief", type=Path)
    p.set_defaults(run=cmd_check)

    p = commands.add_parser("app", help="Build the ToDo Task Builder page from the spec.")
    p.add_argument("--out", type=Path, default=None, help="Folder to write into. Defaults to app/.")
    p.set_defaults(run=cmd_app)

    p = commands.add_parser("wordskill", help="Package the green prompt as a Claude skill for Word.")
    p.add_argument("--out", type=Path, default=None, help="Folder to write into. Defaults to word-skill/.")
    p.set_defaults(run=cmd_wordskill)

    p = commands.add_parser("playbook", help="Build the Word copy of the playbook from docs/PLAYBOOK.md.")
    p.add_argument("--out", type=Path, default=None)
    p.set_defaults(run=cmd_playbook)

    _register_connected_commands(commands)

    args = parser.parse_args(argv)
    try:
        return int(args.run(args) or 0)
    except (FileNotFoundError, ValueError) as error:
        print(f"todotask: {error}", file=sys.stderr)
        return 2


def _register_connected_commands(commands) -> None:
    """Commands that talk to Todoist, Microsoft To Do and Claude live in their own module."""
    try:
        from . import connected
    except ImportError:
        return
    connected.register(commands)


# --------------------------------------------------------------------------- #

def cmd_template(args) -> int:
    for suffix in (".docx", ".dotx"):
        path = rendering.render(None, args.out / f"{TEMPLATE_NAME}{suffix}")
        print(path)
    return 0


def cmd_new(args) -> int:
    given: dict = {}
    if args.from_json:
        # utf-8-sig: Windows PowerShell writes a byte-order mark at the start of UTF-8 files.
        given = json.loads(args.from_json.read_text(encoding="utf-8-sig"))
        if not isinstance(given, dict):
            raise ValueError(f"{args.from_json} must hold one JSON object.")
    text = str(given.get("text") or (sys.stdin.read() if args.entry == "-" else args.entry))
    if not text.strip():
        raise ValueError("The entry is empty.")
    task = TaskBrief(entry=Entry(
        text=text.strip(),
        notes=str(given.get("notes") or args.notes).strip(),
        source=str(given.get("source") or args.source),
        list=str(given.get("list") or args.list_name),
        task_id=str(given.get("task_id") or args.task_id),
        captured_on=str(given.get("captured_on") or args.date or dt.date.today().isoformat())[:10],
        labels=[str(label).strip() for label in (given.get("labels") or args.labels.split(",")) if str(label).strip()],
    ))
    folder = task_folder(args.out, task)
    task.save(folder / "brief.json")
    print(rendering.render(task, folder / f"{folder.name}.docx"))
    print(folder / "brief.json")
    return 0


def cmd_render(args) -> int:
    task = TaskBrief.load(args.brief)
    problems = task.problems()
    if problems and not args.force:
        _report(problems)
        print("Nothing was written. Fix the brief, or add --force.", file=sys.stderr)
        return 1
    for line in write_outputs(task, args.out or args.brief.parent):
        print(line)
    if problems:
        _report(problems)
    return 0


def cmd_prompt(args) -> int:
    sys.stdout.write(rendering.brief_prompt(TaskBrief.load(args.brief)))
    return 0


def cmd_check(args) -> int:
    problems = TaskBrief.load(args.brief).problems()
    if not problems:
        print("The brief follows the structure.")
        return 0
    _report(problems)
    return 1


def cmd_playbook(args) -> int:
    from .playbook import build_playbook
    print(build_playbook(args.out))
    return 0


def cmd_wordskill(args) -> int:
    from .wordskill import build_word_skill
    print(build_word_skill(args.out))
    return 0


def cmd_app(args) -> int:
    from .appbuild import build_app
    print(build_app(args.out))
    return 0


# --------------------------------------------------------------------------- #

def task_folder(root: Path, task: TaskBrief) -> Path:
    """One folder per task: ``<capture date>-<a few words>``."""
    name_source = task.writeback.title or task.brief.title or task.entry.text
    date = task.entry.captured_on or dt.date.today().isoformat()
    return Path(root) / f"{date}-{slugify(name_source)}"


def write_outputs(task: TaskBrief, folder: Path) -> list[Path]:
    """Write the Word document, the session prompt and the write-back text."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    name = folder.name if folder.name not in ("", ".") else "brief"
    written = [rendering.render(task, folder / f"{name}.docx")]
    prompt = folder / "prompt.md"
    prompt.write_text(rendering.brief_prompt(task), encoding="utf-8")
    writeback = folder / "writeback.txt"
    writeback.write_text(
        f"TITLE\n{task.writeback.title}\n\nDESCRIPTION\n{rendering.writeback_note(task)}\n", encoding="utf-8"
    )
    link = folder / "session-link.txt"
    link.write_text(rendering.session_link(task) + "\n", encoding="utf-8")
    row = folder / "app-row.json"
    row.write_text(json.dumps(app_row(task), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return written + [prompt, writeback, link, row]


def app_row(task: TaskBrief, stage: str = "Briefed") -> dict:
    """The brief as one row of the ToDo Task Builder page's ``briefs`` collection."""
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    data = task.to_dict()
    return {"title": task.brief.title, **data, "stage": stage, "session_url": "", "created_at": now, "updated_at": now}


def app_row_id(task: TaskBrief, folder: Path) -> str:
    """A stable id for the row: the task id when there is one, else the folder name."""
    raw = f"{slugify(task.entry.source or 'task', 2)}-{task.entry.task_id}" if task.entry.task_id else Path(folder).name
    return "".join(ch if ch.isalnum() or ch in "_-.~" else "-" for ch in raw)[:120] or "task"


def _report(problems: list[str]) -> None:
    for problem in problems:
        print(f"  - {problem}", file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
