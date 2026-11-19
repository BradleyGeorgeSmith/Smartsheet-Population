"""The data behind one brief, plus the checks that keep briefs consistent."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from . import spec

TASK_TYPES = (
    "content", "plan", "learning", "idea", "health",
    "errand", "appointment", "purchase", "person", "reflection", "unclear",
)

TITLE_MAX = 120
WRITEBACK_TITLE_MAX = 90
WRITEBACK_DESCRIPTION_MAX = 600


@dataclass
class Entry:
    """The raw capture. ``text`` is never corrected."""

    text: str
    notes: str = ""
    source: str = "Manual"
    list: str = ""
    task_id: str = ""
    captured_on: str = ""
    # ``list`` above is a field name here, so the built-in is not available as a factory.
    labels: list[str] = field(default_factory=lambda: [])  # labels the task carried when captured


@dataclass
class Plan:
    output: str = ""
    steps: list[str] = field(default_factory=list)
    tools: str = ""
    rhythm: str = ""
    done_when: str = ""


@dataclass
class Brief:
    title: str = ""
    description: str = ""
    status: str = ""
    calendar_date: str = "Not supplied"
    context_heading: str = "Context"
    context: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    plan: Plan = field(default_factory=Plan)


@dataclass
class Writeback:
    title: str = ""
    description: str = ""


@dataclass
class TaskBrief:
    entry: Entry
    brief: Brief = field(default_factory=Brief)
    writeback: Writeback = field(default_factory=Writeback)
    task_type: str = "idea"

    # ---- loading and saving -------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskBrief":
        if not isinstance(data, dict):
            raise ValueError("A brief must be a JSON object.")
        entry_data = data.get("entry")
        if not isinstance(entry_data, dict) or not str(entry_data.get("text", "")).strip():
            raise ValueError("A brief needs entry.text: the original To Do entry.")
        brief_data = dict(data.get("brief") or {})
        plan = Plan(**_known(Plan, brief_data.pop("plan", None) or {}))
        return cls(
            entry=Entry(**_known(Entry, entry_data)),
            brief=Brief(plan=plan, **_known(Brief, brief_data, skip=("plan",))),
            writeback=Writeback(**_known(Writeback, data.get("writeback") or {})),
            task_type=str(data.get("task_type") or "idea"),
        )

    @classmethod
    def load(cls, path: str | Path) -> "TaskBrief":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry": asdict(self.entry),
            "task_type": self.task_type,
            "brief": asdict(self.brief),
            "writeback": asdict(self.writeback),
        }

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    # ---- checks -------------------------------------------------------------

    @property
    def is_expanded(self) -> bool:
        """True once the brief has real content, not just an entry."""
        return bool(self.brief.title.strip())

    def problems(self) -> list[str]:
        """Everything that breaks the brief structure. Empty means the brief is sound."""
        found: list[str] = []
        b, w = self.brief, self.writeback

        if self.task_type not in TASK_TYPES:
            found.append(f"task_type '{self.task_type}' is not one of: {', '.join(TASK_TYPES)}.")
        if not b.title.strip():
            found.append("The brief has no title.")
        elif len(b.title) > TITLE_MAX:
            found.append(f"The title is {len(b.title)} characters; the limit is {TITLE_MAX}.")
        if not b.description.strip():
            found.append("The brief has no description.")
        if not b.status.strip():
            found.append("The brief has no status.")
        if not b.calendar_date.strip():
            found.append("Calendar date is empty; write a date or 'Not supplied'.")
        if not 1 <= len(b.context) <= 4:
            found.append(f"Context has {len(b.context)} paragraphs; it needs 1 to 4.")
        if not 2 <= len(b.actions) <= 6:
            found.append(f"There are {len(b.actions)} actions; the list needs 2 to 6.")
        if b.actions and not b.actions[0].lstrip().lower().startswith("next action:"):
            found.append("The first action must start with 'Next action:'.")
        if not b.plan.output.strip():
            found.append("The execution plan has no Output.")
        if not b.plan.steps:
            found.append("The execution plan has no Steps.")
        if not b.plan.done_when.strip():
            found.append("The execution plan has no 'Done when'.")
        if not w.title.strip():
            found.append("The To Do write-back has no title.")
        elif len(w.title) > WRITEBACK_TITLE_MAX:
            found.append(f"The write-back title is {len(w.title)} characters; the limit is {WRITEBACK_TITLE_MAX}.")
        if not w.description.strip():
            found.append("The To Do write-back has no description.")
        elif len(w.description) > WRITEBACK_DESCRIPTION_MAX:
            found.append(
                f"The write-back description is {len(w.description)} characters; "
                f"the limit is {WRITEBACK_DESCRIPTION_MAX}."
            )
        return found


def _known(cls: type, data: dict[str, Any], skip: tuple[str, ...] = ()) -> dict[str, Any]:
    """Keep only the keys the dataclass knows, so stray fields never crash a load."""
    names = {f for f in cls.__dataclass_fields__ if f not in skip}  # type: ignore[attr-defined]
    return {k: v for k, v in (data or {}).items() if k in names and v is not None}


def model_example() -> TaskBrief:
    """The neutral example used as the layout model in a blank template."""
    return TaskBrief.load(spec.model_example_path())


def slugify(text: str, max_words: int = 6, max_length: int = 48) -> str:
    """A short, file-safe name built from the first few words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    slug = "-".join(words[:max_words])[:max_length].strip("-")
    return slug or "task"
