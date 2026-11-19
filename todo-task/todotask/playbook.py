"""Builds the Word copy of the playbook from ``docs/PLAYBOOK.md``.

The Markdown file is the source. This turns the small part of Markdown the playbook uses
(headings, paragraphs, lists, tables, code blocks, bold and inline code) into a Word
document with the same look as the brief template, using the same checked building blocks.
"""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from . import render as r

DOCS = Path(__file__).resolve().parent.parent / "docs"
MONO = "Consolas"
CODE_INK = RGBColor(0x1F, 0x2A, 0x37)

_INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
_ITEM = re.compile(r"^(\s*)(-|\d+\.)\s+(.*)$")


def _inline(paragraph, text: str, *, size: float = 10.5, bold: bool = False) -> None:
    """Add text to a paragraph, honouring **bold**, `code` and [links](...)."""
    for part in _INLINE.split(text):
        if not part:
            continue
        if part.startswith("**"):
            r._run(paragraph, part[2:-2], size=size, bold=True)
        elif part.startswith("`"):
            run = r._run(paragraph, part[1:-1], size=size - 0.5, bold=bold, color=CODE_INK)
            run.font.name = MONO
            run._r.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), MONO)
        elif part.startswith("["):
            r._run(paragraph, part[1:part.index("](")], size=size, bold=bold)
        else:
            r._run(paragraph, part, size=size, bold=bold)


def _paragraph(doc, text: str, *, after: float = 6, indent: float = 0, hanging: float = 0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.first_line_indent = Cm(-hanging)
    _inline(p, text)
    return p


def _code(doc, lines: list[str], indent: float = 0) -> None:
    for i, line in enumerate(lines):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6 if i == len(lines) - 1 else 0)
        p.paragraph_format.left_indent = Cm(indent + 0.3)
        run = r._run(p, line or " ", size=9.5, color=CODE_INK)
        run.font.name = MONO
        r._panel_shade(p)


def _table(doc, rows: list[list[str]]) -> None:
    columns = max(len(row) for row in rows)
    rows = [row + [""] * (columns - len(row)) for row in rows]
    plain = lambda cell: re.sub(r"[*`]", "", cell)  # noqa: E731
    weights = [min(max(max(len(plain(row[c])) for row in rows), 8), 46) for c in range(columns)]
    widths = [r.CONTENT_WIDTH_CM * w / sum(weights) for w in weights]
    table = r._table(doc, len(rows), widths)
    for n, (row, cells) in enumerate(zip(table.rows, rows)):
        for cell, text, width in zip(row.cells, cells, widths):
            r._cell(cell, "", fill=r.PANEL if n == 0 else None, width_cm=width)
            _inline(cell.paragraphs[0], text, size=9.5, bold=n == 0)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _heading_style(doc, name: str, size: float, before: float) -> None:
    style = doc.styles[name]
    style.font.name, style.font.size, style.font.bold = r.FONT, Pt(size), True
    style.font.color.rgb = r.ACCENT
    fonts = style.element.rPr.rFonts
    fonts.set(qn("w:eastAsia"), r.FONT)
    for theme in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        fonts.attrib.pop(qn(f"w:{theme}"), None)
    style.paragraph_format.space_before = Pt(before)
    style.paragraph_format.space_after = Pt(4)
    style.paragraph_format.keep_with_next = True


def build_playbook(out: str | Path | None = None, source: str | Path | None = None) -> Path:
    source = Path(source) if source else DOCS / "PLAYBOOK.md"
    out = Path(out) if out else DOCS / "ToDo-Task-Playbook.docx"
    lines = source.read_text(encoding="utf-8").splitlines()

    meta: dict[str, str] = {}
    if lines and lines[0].strip() == "---":
        end = lines.index("---", 1)
        for line in lines[1:end]:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        lines = lines[end + 1:]

    doc = Document()
    r._page_setup(doc)
    r._styles(doc)
    _heading_style(doc, "Heading 1", 16, 18)
    _heading_style(doc, "Heading 2", 12.5, 12)
    doc.core_properties.author = "ToDo Task"
    doc.core_properties.title = meta.get("title", "Playbook")
    doc.core_properties.comments = meta.get("subtitle", "")
    r._text(doc, meta.get("title", "Playbook"), size=24, bold=True, color=r.ACCENT, after=2)
    if meta.get("subtitle"):
        r._text(doc, meta["subtitle"], size=12, color=r.MUTED, after=12)

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            _code(doc, block)
        elif line.startswith("# "):
            doc.add_paragraph(line[2:].strip(), style="Heading 1")
            i += 1
        elif line.startswith("## "):
            doc.add_paragraph(line[3:].strip(), style="Heading 2")
            i += 1
        elif line.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i])
                i += 1
            _table(doc, [_cells(row) for n, row in enumerate(block) if n != 1])
        elif line.startswith("    "):
            block = []
            while i < len(lines) and (lines[i].startswith("    ") or not lines[i].strip()):
                block.append(lines[i][4:])
                i += 1
            while block and not block[-1].strip():
                block.pop()
            _code(doc, block)
        elif _ITEM.match(line):
            i = _list(doc, lines, i)
        else:
            block = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "```", "    ")) and not _ITEM.match(lines[i]):
                block.append(lines[i].strip())
                i += 1
            _paragraph(doc, " ".join(block))

    r._footer(doc)
    return r.save_document(doc, out)


def _list(doc, lines: list[str], i: int) -> int:
    """One list, with wrapped lines and any code block that sits inside an item."""
    last = None
    while i < len(lines):
        match = _ITEM.match(lines[i])
        if not match or match.group(1):
            break
        marker, text = match.group(2), [match.group(3)]
        i += 1
        code: list[str] = []
        while i < len(lines):
            nxt = lines[i]
            if nxt.startswith("        "):
                code.append(nxt[8:])
            elif not nxt.strip() and i + 1 < len(lines) and lines[i + 1].startswith("        "):
                pass
            elif nxt.startswith("  ") and nxt.strip() and not code:
                text.append(nxt.strip())
            else:
                break
            i += 1
        label = "•" if marker == "-" else marker
        last = _paragraph(doc, f"{label} " + " ".join(text), after=3, indent=0.6, hanging=0.6)
        if code:
            _code(doc, code, indent=0.6)
            last = None
        while i < len(lines) and not lines[i].strip() and i + 1 < len(lines) and _ITEM.match(lines[i + 1] or ""):
            i += 1
    if last is not None:
        last.paragraph_format.space_after = Pt(8)  # room before whatever follows the list
    return i
