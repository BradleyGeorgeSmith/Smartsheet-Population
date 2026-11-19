"""Assembles the ToDo Task Builder page from its parts and the shared spec.

The page's wording (working rules, green prompt, expansion rules, example brief) is read
from ``spec/`` at build time, so the page, the Word template and the command line can
never disagree about what a brief is.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import render, spec
from .models import model_example

APP_DIR = Path(__file__).resolve().parent.parent / "app"
DEFAULT_MODEL = "claude-fable-5-2"
PAGE_NAME = "todo-task-builder.html"


def page_spec() -> dict:
    """Everything the page needs to know, as one JSON-ready object."""
    return {
        "rules": spec.working_rules(),
        "green": list(spec.expansion_prompt()),
        "expand": (spec.SPEC_DIR / "expand-json-prompt.txt").read_text(encoding="utf-8").strip(),
        "example": model_example().to_dict(),
        "how": list(render.HOW_IT_WORKS),
        "model": DEFAULT_MODEL,
        "project": spec.PROJECT_NAME,
    }


def build_app(out_dir: str | Path | None = None) -> Path:
    source = APP_DIR / "src"
    data = json.dumps(page_spec(), ensure_ascii=False, indent=1).replace("</", "<\\/")
    script = "\n".join([
        f"const SPEC = {data};",
        (source / "core.js").read_text(encoding="utf-8"),
        (source / "ui.js").read_text(encoding="utf-8"),
    ])
    page = (source / "page.html").read_text(encoding="utf-8")
    marker = "/*__SCRIPT__*/"
    if marker not in page:
        raise ValueError(f"{source / 'page.html'} has no {marker} marker.")
    out = Path(out_dir) if out_dir else APP_DIR
    out.mkdir(parents=True, exist_ok=True)
    path = out / PAGE_NAME
    path.write_text(page.replace(marker, script), encoding="utf-8")
    return path
