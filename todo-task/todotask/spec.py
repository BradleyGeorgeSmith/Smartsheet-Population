"""Loads the fixed text that every brief shares.

The wording lives in ``todo-task/spec`` so that the Word template, the Claude Code
skill and this package all read the same source.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

SPEC_DIR = Path(__file__).resolve().parent.parent / "spec"

PROJECT_NAME = "Ideas to Contextual Development using ToDo, Word and Claude"
GROUP_NAME = "ToDo Task"

BRIEF_START = "TASK BRIEF STARTS"
BRIEF_END = "TASK BRIEF ENDS"

ACTIONS_HEADING = "Information Needed and Next Actions"
PLAN_HEADING = "Execution Plan for Claude"
ORIGIN_LABEL = "Original entry (word for word):"
NOTES_LABEL = "Notes on the task (word for word):"

ENTRY_PLACEHOLDER = "[Type or paste your To Do entry here, exactly as you captured it]"
WRITEBACK_PLACEHOLDER = "[Claude fills this in]"

STAGES = ["Captured", "Briefed", "In session", "Waiting on me", "Done"]

# Todoist labels that mirror the stages. ``skip-ai`` opts a task out.
LABEL_BRIEFED = "briefed"
LABEL_IN_SESSION = "in-session"
LABEL_WAITING = "waiting-on-me"
LABEL_DONE = "content-done"
LABEL_SKIP = "skip-ai"


@lru_cache(maxsize=None)
def working_rules() -> str:
    """The fixed first paragraph of every brief."""
    return (SPEC_DIR / "working-rules.txt").read_text(encoding="utf-8").strip()


@lru_cache(maxsize=None)
def expansion_prompt() -> tuple[str, ...]:
    """The green prompt, one string per paragraph."""
    text = (SPEC_DIR / "expansion-prompt.txt").read_text(encoding="utf-8")
    return tuple(block.strip() for block in text.split("\n\n") if block.strip())


@lru_cache(maxsize=None)
def brief_schema() -> dict:
    return json.loads((SPEC_DIR / "brief.schema.json").read_text(encoding="utf-8"))


def model_example_path() -> Path:
    """The neutral example shown in the yellow section of a blank template."""
    return SPEC_DIR / "examples" / "tomato-timelapse.json"
