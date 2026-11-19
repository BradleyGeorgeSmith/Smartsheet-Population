"""Packages the green prompt as a Claude skill, for use inside Claude for Word.

Skills enabled on a Claude account appear in the Word add-in: type ``/`` in the Claude
panel and choose the skill, instead of copying the green text each time. The skill text
is built from ``spec/expansion-prompt.txt`` so it never drifts from the Word template.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

from . import spec
from .render import settle_zip

SKILL_NAME = "todo-task-brief"
SKILL_DIR = Path(__file__).resolve().parent.parent / "word-skill"

DESCRIPTION = (
    "Expand the short To Do entry at the top of a ToDo Task Brief document into the full task brief. "
    "Use in Word when the open document has a section called 'Original To Do entry' and the lines "
    "'TASK BRIEF STARTS' and 'TASK BRIEF ENDS', or when asked to expand a To Do entry into a brief."
)


def skill_text() -> str:
    steps = "\n\n".join(spec.expansion_prompt()[1:])
    return f"""---
name: {SKILL_NAME}
description: {DESCRIPTION}
---

# ToDo Task brief

The open Word document is a ToDo Task Brief. The person's raw To Do entry is under
"1 · Original To Do entry". Expand it into a full task brief inside the document, by
following every step below. The steps are written by the person, so "I" and "my" in them
mean the person.

{steps}

## The fixed first paragraph

The brief always begins with this paragraph, word for word. If it is missing or has been
changed, put it back exactly:

{spec.working_rules()}

## If something goes wrong

- If the document has no "TASK BRIEF STARTS" line, say so and stop. Do not write the brief
  anywhere else.
- If the entry under section 1 is still the placeholder in square brackets, ask for the
  entry and stop.
- If an edit times out, finish the brief first, then fill "4 · To Do write-back" as a
  second edit.
"""


def build_word_skill(out_dir: str | Path | None = None) -> Path:
    """Write the skill folder and a ZIP of it, ready to upload at Customize, then Skills."""
    root = Path(out_dir) if out_dir else SKILL_DIR
    folder = root / SKILL_NAME
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(skill_text(), encoding="utf-8")
    archive = root / f"{SKILL_NAME}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        bundle.write(folder / "SKILL.md", f"{SKILL_NAME}/SKILL.md")
    settle_zip(archive)  # fixed dates, so an unchanged skill gives an unchanged file
    return archive
