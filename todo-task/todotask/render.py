"""Builds the Word document, and the plain-text prompt, for one To Do entry.

The same document serves three moments:

* a blank **template** (entry placeholder, example brief in yellow),
* a **new** document for one entry (entry filled in, example brief still in yellow,
  ready for the green prompt to be sent to Claude in Word), and
* a **finished** document (the yellow section holds the real brief).

Everything inside the yellow section comes from :func:`brief_lines`, which is also what
:func:`brief_prompt` turns into the text pasted into a Claude Code session, so the Word
document and the prompt can never drift apart.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Iterable
from urllib.parse import quote

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from . import spec
from .models import TaskBrief, model_example

YELLOW = WD_COLOR_INDEX.YELLOW
GREEN = WD_COLOR_INDEX.BRIGHT_GREEN

FONT = "Calibri"
INK = RGBColor(0x1F, 0x2A, 0x37)
MUTED = RGBColor(0x5B, 0x65, 0x70)
ACCENT = RGBColor(0x1F, 0x4E, 0x79)
PANEL = "F3F5F7"
RULE = "C5CCD3"

PAGE_WIDTH_CM = 21.0
MARGIN_CM = 2.0
CONTENT_WIDTH_CM = PAGE_WIDTH_CM - 2 * MARGIN_CM

HOW_IT_WORKS = (
    "Make a copy of the template for the new task. Never type into the template itself.",
    "Paste the To Do entry at the top, exactly as you captured it.",
    "Copy all of the green text into the Claude panel in Word and send it.",
    "Read the yellow brief. Correct anything marked (to confirm) and add what you know.",
    "Paste the write-back title and description into the task in Microsoft To Do or Todoist.",
    f"Copy all of the yellow text into a new Claude Code session in the project “{spec.PROJECT_NAME}”.",
    "Add a row to the progress log for every update. An update without evidence is not finished.",
)


# --------------------------------------------------------------------------- #
# The brief as a list of lines: one source for Word and for the prompt
# --------------------------------------------------------------------------- #

def brief_lines(task: TaskBrief) -> list[tuple[str, str]]:
    """The yellow section as ``(kind, text)`` pairs, in reading order.

    Kinds: ``rules``, ``title``, ``meta``, ``heading``, ``para``, ``item``, ``field``.
    A ``field`` line is ``Label: value``. ``meta`` is the Description / Status /
    Calendar date line. The last lines repeat the original entry word for word.
    """
    b = task.brief
    lines: list[tuple[str, str]] = [("rules", spec.working_rules()), ("title", b.title)]
    lines.append(("meta", f"Description: {b.description} Status: {b.status} Calendar date: {_stop(b.calendar_date)}"))
    lines.append(("heading", b.context_heading))
    lines.extend(("para", text) for text in b.context)
    lines.append(("heading", spec.ACTIONS_HEADING))
    lines.extend(("item", f"{n}. {text}") for n, text in enumerate(b.actions, 1))
    lines.append(("heading", spec.PLAN_HEADING))
    lines.append(("field", f"Output: {b.plan.output}"))
    lines.append(("field", "Steps:"))
    lines.extend(("item", f"{n}. {text}") for n, text in enumerate(b.plan.steps, 1))
    lines.append(("field", f"Tools, skills and apps: {b.plan.tools}"))
    lines.append(("field", f"Rhythm: {b.plan.rhythm}"))
    lines.append(("field", f"Done when: {b.plan.done_when}"))
    # The brief is pasted into a session with nothing else attached, so it carries the entry.
    lines.append(("field", f"{spec.ORIGIN_LABEL} {task.entry.text.strip()}"))
    if task.entry.notes.strip():
        lines.append(("field", f"{spec.NOTES_LABEL} {task.entry.notes.strip()}"))
    return lines


def brief_prompt(task: TaskBrief) -> str:
    """The yellow section as plain text: what gets pasted into a Claude Code session."""
    out: list[str] = []
    for kind, text in brief_lines(task):
        if kind in ("title", "heading"):
            out.extend(["", text, ""])
        elif kind == "item":
            out.append(text)
        else:
            out.extend([text, ""])
    prompt = "\n".join(out)
    while "\n\n\n" in prompt:
        prompt = prompt.replace("\n\n\n", "\n\n")
    return prompt.strip() + "\n"


def session_link(task: TaskBrief, repo: str = "") -> str:
    """A link that opens a new Claude Code session with the brief already typed in."""
    link = "https://claude.ai/code/new?q=" + quote(brief_prompt(task), safe="-_.!~*'()")
    return link + (f"&repo={quote(repo, safe='')}" if repo else "")


def writeback_note(task: TaskBrief) -> str:
    """The text for the task's note or description: the new description, then the original."""
    parts = [task.writeback.description.strip(), "Original entry: " + task.entry.text.strip()]
    if task.entry.notes.strip():
        parts.append("Original notes: " + task.entry.notes.strip())
    return "\n\n".join(p for p in parts if p)


def document_text(task: TaskBrief | None = None) -> str:
    """The whole document as plain text, as an assistant reading the file would see it."""
    shown, entry_text, notes, filled = _resolve(task)
    out = ["ToDo Task Brief", "", "1 · Original To Do entry", entry_text, f"More from the task's notes: {notes}", ""]
    out += ["2 · Expansion prompt (green)", *spec.expansion_prompt(), ""]
    out += ["3 · Task brief (yellow)", spec.BRIEF_START]
    out += [text for _, text in brief_lines(shown)]
    out += [spec.BRIEF_END, "", "4 · To Do write-back"]
    out += [
        f"Title: {shown.writeback.title if filled else spec.WRITEBACK_PLACEHOLDER}",
        f"Description: {shown.writeback.description if filled else spec.WRITEBACK_PLACEHOLDER}",
        "",
        "5 · Progress log",
        "Date | Completed | Waiting on | Next action | Completion evidence",
    ]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
# The Word document
# --------------------------------------------------------------------------- #

def build_document(task: TaskBrief | None = None) -> Document:
    """Build the document.

    ``task=None`` gives the blank template. A task whose brief has no title gives a
    new document for that entry, with the example brief left in the yellow section.
    A task with a brief gives the finished document.
    """
    shown, entry_text, notes, filled = _resolve(task)
    is_template = task is None

    doc = Document()
    _page_setup(doc)
    _styles(doc)
    doc.core_properties.author = spec.GROUP_NAME
    doc.core_properties.title = shown.brief.title if filled else "ToDo Task Brief"
    doc.core_properties.comments = "One document for one To Do entry. To Do, then Word, then Claude."

    _text(doc, "ToDo Task Brief", size=22, bold=True, color=ACCENT, after=2)
    _text(doc, "One document for one To Do entry.  To Do → Word → Claude", size=10.5, color=MUTED, after=10)

    # 1 · the entry -----------------------------------------------------------
    _section(doc, "1 · Original To Do entry",
             "Type or paste the entry exactly as you captured it. It is never tidied up here.")
    entry = _text(doc, entry_text, size=12, after=4,
                  color=MUTED if is_template else INK, italic=is_template)
    _panel(entry)
    _labelled(doc, "More from the task’s notes (optional): ", notes, after=6)

    # 2 · the green prompt ----------------------------------------------------
    _section(doc, "2 · Expansion prompt (green)",
             "Copy all of the green text into the Claude panel in Word and send it.")
    for block in spec.expansion_prompt():
        _text(doc, block, size=10.5, highlight=GREEN, after=5)

    # 3 · the yellow brief ----------------------------------------------------
    hint = ("Claude rewrites this section. When it reads correctly, copy all of the yellow "
            "text into a new Claude Code session.")
    if not filled:
        hint += (f" The brief shown now is only an example of the layout, written from the "
                 f"entry “{shown.entry.text}”.")
    _section(doc, "3 · Task brief (yellow)", hint, new_page=True)
    _marker(doc, f"▼ {spec.BRIEF_START}")
    _brief(doc, shown)
    _marker(doc, f"▲ {spec.BRIEF_END}")

    # 4 · write-back ----------------------------------------------------------
    _section(doc, "4 · To Do write-back",
             "Paste these into the task in Microsoft To Do or Todoist. Keep the original entry underneath.")
    rows = [
        ("Title", shown.writeback.title if filled else spec.WRITEBACK_PLACEHOLDER),
        ("Description", shown.writeback.description if filled else spec.WRITEBACK_PLACEHOLDER),
    ]
    if filled:
        rows.append(("Original entry", task.entry.text.strip()))  # type: ignore[union-attr]
    _key_value_table(doc, rows)

    # 5 · progress log --------------------------------------------------------
    _section(doc, "5 · Progress log",
             "Add one row for every update. An update without evidence is not finished.")
    _grid(doc, ["Date", "Completed", "Waiting on", "Next action", "Completion evidence"],
          widths=[2.2, 4.0, 3.2, 3.6, 4.0], empty_rows=3)
    _labelled(doc, "Decisions and lessons: ", "", before=8, after=6)

    # task record -------------------------------------------------------------
    _section(doc, "Task record", "Where this task lives, so the three places stay linked.")
    e = task.entry if task else None
    _key_value_table(doc, [
        ("Captured on", e.captured_on if e else ""),
        ("Source", e.source if e else "Microsoft To Do  /  Todoist"),
        ("List or project", e.list if e else ""),
        ("Task link or ID", e.task_id if e else ""),
        ("Claude session link", ""),
        ("Stage", "Briefed" if filled else "  →  ".join(spec.STAGES)),
    ])

    # how it works ------------------------------------------------------------
    _section(doc, "How this document works", "")
    for n, step in enumerate(HOW_IT_WORKS, 1):
        _text(doc, f"{n}. {step}", size=10.5, after=3)

    _footer(doc)
    return doc


def save_document(doc: Document, path: str | Path) -> Path:
    """Save as .docx, or as a Word template when the path ends in .dotx."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".dotx":
        staging = path.with_suffix(".staging.docx")
        doc.save(str(staging))
        _retype_as_template(staging, path)
        staging.unlink()
    else:
        doc.save(str(path))
    return path


def render(task: TaskBrief | None, path: str | Path) -> Path:
    return save_document(build_document(task), path)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _resolve(task: TaskBrief | None) -> tuple[TaskBrief, str, str, bool]:
    """Which brief to show in yellow, the entry text, the notes text, and whether it is real."""
    filled = bool(task and task.is_expanded)
    shown = task if filled else model_example()
    entry_text = task.entry.text.strip() if task else spec.ENTRY_PLACEHOLDER
    notes = (task.entry.notes.strip() if task else "") or "None"
    return shown, entry_text, notes, filled  # type: ignore[return-value]


def _stop(text: str) -> str:
    text = text.strip()
    return text if text.endswith((".", "!", "?")) else text + "."


def _page_setup(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(PAGE_WIDTH_CM), Cm(29.7)  # A4
    section.left_margin = section.right_margin = Cm(MARGIN_CM)
    section.top_margin = section.bottom_margin = Cm(1.8)
    zoom = doc.settings.element.find(qn("w:zoom"))
    if zoom is not None and zoom.get(qn("w:percent")) is None:
        zoom.set(qn("w:percent"), "100")


def _styles(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(11)
    normal.font.color.rgb = INK
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.12

    heading = doc.styles["Heading 2"]
    heading.font.name = FONT
    heading.font.size = Pt(13)
    heading.font.bold = True
    heading.font.color.rgb = ACCENT
    fonts = heading.element.rPr.rFonts
    fonts.set(qn("w:eastAsia"), FONT)
    for theme in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        fonts.attrib.pop(qn(f"w:{theme}"), None)  # theme fonts would override the name
    heading.paragraph_format.space_before = Pt(16)
    heading.paragraph_format.space_after = Pt(2)
    heading.paragraph_format.keep_with_next = True


def _text(doc, text, *, size=11.0, bold=False, italic=False, color=None,
          highlight=None, before=0.0, after=6.0, keep_with_next=False):
    """One paragraph holding one run."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.keep_with_next = keep_with_next
    _run(p, text, size=size, bold=bold, italic=italic, color=color, highlight=highlight)
    return p


def _run(p, text, *, size=11.0, bold=False, italic=False, color=None, highlight=None):
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    if highlight is not None:
        run.font.highlight_color = highlight
    return run


def _labelled(doc, label, value, *, highlight=None, size=11.0, before=0.0, after=6.0):
    """A paragraph that starts with a bold label."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    _run(p, label, size=size, bold=True, highlight=highlight)
    if value:
        _run(p, value, size=size, highlight=highlight)
    return p


def _section(doc, title: str, hint: str, *, new_page: bool = False) -> None:
    heading = doc.add_paragraph(title, style="Heading 2")
    heading.paragraph_format.page_break_before = new_page
    if hint:
        _text(doc, hint, size=9.5, italic=True, color=MUTED, after=6, keep_with_next=True)


def _marker(doc, text: str) -> None:
    p = _text(doc, text, size=8.5, bold=True, color=MUTED, before=2, after=4, keep_with_next=text.startswith("▼"))
    _edge(p, "bottom" if text.startswith("▼") else "top")


def _brief(doc, task: TaskBrief) -> None:
    """The yellow section. Every run is highlighted so it can be selected as one block."""
    for kind, text in brief_lines(task):
        if kind == "rules":
            label, _, rest = text.partition(":")
            p = _labelled(doc, label + ":", rest, highlight=YELLOW, size=10, after=8)
        elif kind == "title":
            _text(doc, text, size=14, bold=True, highlight=YELLOW, before=4, after=6, keep_with_next=True)
        elif kind == "meta":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(8)
            for label, value in _split_meta(text):
                _run(p, label, bold=True, highlight=YELLOW)
                _run(p, value, highlight=YELLOW)
        elif kind == "heading":
            _text(doc, text, size=12, bold=True, highlight=YELLOW, before=6, after=4, keep_with_next=True)
        elif kind == "item":
            p = _text(doc, text, highlight=YELLOW, after=3)
            p.paragraph_format.left_indent = Cm(0.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
        elif kind == "field":
            label, _, value = text.partition(":")
            _labelled(doc, label + ":", value, highlight=YELLOW, after=4)
        else:
            _text(doc, text, highlight=YELLOW, after=6)


def _split_meta(text: str) -> Iterable[tuple[str, str]]:
    """Split 'Description: … Status: … Calendar date: …' into label and value pairs."""
    labels = ["Description:", " Status:", " Calendar date:"]
    positions = [text.find(label) for label in labels]
    for i, (label, start) in enumerate(zip(labels, positions)):
        end = positions[i + 1] if i + 1 < len(labels) else len(text)
        yield label, text[start + len(label):end]


P_PR_ORDER = (
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl", "numPr",
    "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens", "kinsoku", "wordWrap",
    "overflowPunct", "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd",
    "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc",
    "textDirection", "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
    "sectPr", "pPrChange",
)
TBL_PR_ORDER = (
    "tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize", "tblStyleColBandSize",
    "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout", "tblCellMar",
    "tblLook", "tblCaption", "tblDescription",
)
TC_PR_ORDER = (
    "cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap", "tcMar",
    "textDirection", "tcFitText", "vAlign", "hideMark",
)


def _place(parent, child, order: tuple[str, ...]) -> None:
    """Insert ``child`` where the Word schema expects it. Word rejects misordered properties."""
    rank = {qn(f"w:{name}"): i for i, name in enumerate(order)}
    mine = rank[child.tag]
    for existing in parent:
        if rank.get(existing.tag, -1) > mine:
            existing.addprevious(child)
            return
    parent.append(child)


def _panel(p) -> None:
    """Light grey box with a rule down the left, used for the original entry."""
    p_pr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    for key, value in (("val", "single"), ("sz", "18"), ("space", "8"), ("color", "1F4E79")):
        left.set(qn(f"w:{key}"), value)
    borders.append(left)
    _place(p_pr, borders, P_PR_ORDER)
    shade = OxmlElement("w:shd")
    for key, value in (("val", "clear"), ("color", "auto"), ("fill", PANEL)):
        shade.set(qn(f"w:{key}"), value)
    _place(p_pr, shade, P_PR_ORDER)
    p.paragraph_format.left_indent = Cm(0.35)
    p.paragraph_format.space_before = Pt(2)


def _panel_shade(p) -> None:
    """Light grey behind a paragraph, with no rule. Used for code in the playbook."""
    shade = OxmlElement("w:shd")
    for key, value in (("val", "clear"), ("color", "auto"), ("fill", PANEL)):
        shade.set(qn(f"w:{key}"), value)
    _place(p._p.get_or_add_pPr(), shade, P_PR_ORDER)


def _edge(p, side: str) -> None:
    p_pr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    edge = OxmlElement(f"w:{side}")
    for key, value in (("val", "single"), ("sz", "6"), ("space", "2"), ("color", RULE)):
        edge.set(qn(f"w:{key}"), value)
    borders.append(edge)
    _place(p_pr, borders, P_PR_ORDER)


def _cell(cell, text, *, bold=False, size=10.0, fill=None, width_cm=None, color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    _run(p, text, size=size, bold=bold, color=color)
    if width_cm is not None:
        cell.width = Cm(width_cm)
    if fill:
        shade = OxmlElement("w:shd")
        for key, value in (("val", "clear"), ("color", "auto"), ("fill", fill)):
            shade.set(qn(f"w:{key}"), value)
        _place(cell._tc.get_or_add_tcPr(), shade, TC_PR_ORDER)


def _table(doc, rows: int, widths: list[float]):
    table = doc.add_table(rows=rows, cols=len(widths))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.autofit = False
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        edge = OxmlElement(f"w:{side}")
        for key, value in (("val", "single"), ("sz", "4"), ("space", "0"), ("color", RULE)):
            edge.set(qn(f"w:{key}"), value)
        borders.append(edge)
    _place(table._tbl.tblPr, borders, TBL_PR_ORDER)
    for column, width in zip(table.columns, widths):
        column.width = Cm(width)
    return table


def _key_value_table(doc, rows: list[tuple[str, str]]) -> None:
    widths = [3.6, CONTENT_WIDTH_CM - 3.6]
    table = _table(doc, len(rows), widths)
    for row, (key, value) in zip(table.rows, rows):
        _cell(row.cells[0], key, bold=True, fill=PANEL, width_cm=widths[0])
        _cell(row.cells[1], value, width_cm=widths[1])


def _grid(doc, headers: list[str], widths: list[float], empty_rows: int) -> None:
    table = _table(doc, 1 + empty_rows, widths)
    for cell, header, width in zip(table.rows[0].cells, headers, widths):
        _cell(cell, header, bold=True, fill=PANEL, width_cm=width)
    for row in table.rows[1:]:
        for cell, width in zip(row.cells, widths):
            _cell(cell, "", width_cm=width)


def _footer(doc: Document) -> None:
    p = doc.sections[0].footer.paragraphs[0]
    _run(p, f"{spec.GROUP_NAME}  ·  To Do → Word → Claude  ·  page ", size=8.5, color=MUTED)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        run = p.add_run()
        run.font.size = Pt(8.5)
        run.font.color.rgb = MUTED
        if kind:
            mark = OxmlElement("w:fldChar")
            mark.set(qn("w:fldCharType"), kind)
            run._r.append(mark)
        else:
            code = OxmlElement("w:instrText")
            code.set(qn("xml:space"), "preserve")
            code.text = text
            run._r.append(code)


def _retype_as_template(docx_path: Path, dotx_path: Path) -> None:
    """A .dotx is a .docx whose main part is declared as a template."""
    document = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
    template = "application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
    temporary = dotx_path.with_suffix(".tmp")
    with zipfile.ZipFile(docx_path) as source, zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.decode("utf-8").replace(document, template).encode("utf-8")
            target.writestr(item, data)
    shutil.move(str(temporary), str(dotx_path))
