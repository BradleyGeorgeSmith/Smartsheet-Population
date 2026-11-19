"""Checks for the brief model, the Word renderer and the core commands. No network."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

from todotask import cli, render, spec
from todotask.models import Entry, TaskBrief, model_example, slugify

ENTRY = "garden timelapse vid?? 30 days tomatoes.. phone on tripod.. music"


def highlighted(doc, colour) -> str:
    return "\n".join(
        "".join(r.text for r in p.runs if r.font.highlight_color == colour)
        for p in doc.paragraphs
        if any(r.font.highlight_color == colour for r in p.runs)
    )


def body_text(doc) -> str:
    return "\n".join(p.text for p in doc.paragraphs)


# ---- the model -------------------------------------------------------------

def test_model_example_follows_the_structure():
    assert model_example().problems() == []


def test_first_action_must_start_with_next_action():
    task = model_example()
    task.brief.actions[0] = "Choose the plant."
    assert any("Next action:" in p for p in task.problems())


def test_writeback_limits_are_enforced():
    task = model_example()
    task.writeback.title = "x" * 91
    task.writeback.description = "y" * 601
    problems = " ".join(task.problems())
    assert "write-back title is 91" in problems
    assert "write-back description is 601" in problems


def test_a_brief_needs_the_original_entry():
    with pytest.raises(ValueError):
        TaskBrief.from_dict({"entry": {"text": "  "}})


def test_unknown_fields_do_not_break_loading():
    data = model_example().to_dict()
    data["entry"]["surprise"] = 1
    data["brief"]["extra"] = "ignored"
    assert TaskBrief.from_dict(data).brief.title == model_example().brief.title


def test_round_trip(tmp_path):
    path = model_example().save(tmp_path / "brief.json")
    assert TaskBrief.load(path).to_dict() == model_example().to_dict()


@pytest.mark.parametrize("text,expected", [
    ("Buy shoes for Honor", "buy-shoes-for-honor"),
    ("vid frdg lgt thng 2moro maybe?? ask D", "vid-frdg-lgt-thng-2moro-maybe"),
    ("???", "task"),
])
def test_slugify(text, expected):
    assert slugify(text) == expected


# ---- the fixed wording -----------------------------------------------------

def test_working_rules_keep_the_owners_sentences_word_for_word():
    rules = spec.working_rules()
    for sentence in (
        "Report what was actually done instead of claiming that an action was completed.",
        "End each update with: Completed; Waiting on; Next action; and Completion evidence.",
        "Retain relevant decisions and lessons in the brief so future work builds on existing context.",
        "For health-related tasks, organise information and questions for the clinician without "
        "diagnosing or recommending treatment.",
    ):
        assert sentence in rules


def test_green_prompt_names_the_markers_the_document_uses():
    prompt = " ".join(spec.expansion_prompt())
    assert spec.BRIEF_START in prompt and spec.BRIEF_END in prompt
    assert "Working rules for Claude:" in prompt


# ---- the Word document -----------------------------------------------------

def test_blank_template_has_placeholder_green_prompt_and_example_brief():
    doc = render.build_document(None)
    text = body_text(doc)
    assert spec.ENTRY_PLACEHOLDER in text
    assert highlighted(doc, WD_COLOR_INDEX.BRIGHT_GREEN).startswith("Expand my To Do entry")
    yellow = highlighted(doc, WD_COLOR_INDEX.YELLOW)
    assert yellow.startswith("Working rules for Claude:")
    assert model_example().brief.title in yellow
    # the yellow section closes with the original entry, so it works as a prompt on its own
    assert yellow.rstrip().endswith(f"{spec.ORIGIN_LABEL} {model_example().entry.text}")


def test_entry_is_the_first_body_paragraph_after_its_heading():
    task = TaskBrief(entry=Entry(text=ENTRY))
    paragraphs = [p.text for p in render.build_document(task).paragraphs]
    heading = paragraphs.index("1 · Original To Do entry")
    assert paragraphs[heading + 2] == ENTRY  # heading, one-line hint, then the entry


def test_new_document_keeps_the_example_brief_until_claude_rewrites_it():
    task = TaskBrief(entry=Entry(text="Buy shoes for Honor"))
    doc = render.build_document(task)
    assert "Buy shoes for Honor" in body_text(doc)
    assert model_example().brief.title in highlighted(doc, WD_COLOR_INDEX.YELLOW)
    assert spec.WRITEBACK_PLACEHOLDER in "\n".join(c.text for t in doc.tables for r in t.rows for c in r.cells)


def test_finished_document_shows_the_real_brief_and_never_the_example():
    data = model_example().to_dict()
    data["entry"]["text"] = "learn to bake sourdough"
    data["brief"]["title"] = "Learn to Bake Sourdough: Plan the First Four Weekends"
    task = TaskBrief.from_dict(data)
    doc = render.build_document(task)
    yellow = highlighted(doc, WD_COLOR_INDEX.YELLOW)
    assert "Learn to Bake Sourdough" in yellow
    cells = [c.text for t in doc.tables for r in t.rows for c in r.cells]
    assert "learn to bake sourdough" in cells  # original entry kept in the write-back table


def test_markers_sit_outside_the_yellow_text():
    doc = render.build_document(None)
    yellow = highlighted(doc, WD_COLOR_INDEX.YELLOW)
    assert spec.BRIEF_START not in yellow and spec.BRIEF_END not in yellow
    text = body_text(doc)
    # the green prompt also names the markers, so look for the marker lines themselves
    start, end = text.index("▼ " + spec.BRIEF_START), text.index("▲ " + spec.BRIEF_END)
    assert start < text.index("Working rules for Claude:", start) < end


def test_prompt_matches_the_yellow_section_and_carries_the_original_entry():
    task = model_example()
    prompt = render.brief_prompt(task)
    for _, line in render.brief_lines(task):
        assert line in prompt
    assert prompt.rstrip().endswith(task.entry.text)


def test_session_link_round_trips_the_prompt():
    from urllib.parse import parse_qs, urlparse
    task = model_example()
    link = render.session_link(task, "owner/name")
    query = parse_qs(urlparse(link).query)
    assert link.startswith("https://claude.ai/code/new?q=")
    assert query["q"] == [render.brief_prompt(task)] and query["repo"] == ["owner/name"]


def test_writeback_note_keeps_the_original_entry():
    task = model_example()
    note = render.writeback_note(task)
    assert note.startswith(task.writeback.description)
    assert f"Original entry: {task.entry.text}" in note


def test_dotx_is_declared_as_a_template(tmp_path):
    path = render.render(None, tmp_path / "t.dotx")
    types = zipfile.ZipFile(path).read("[Content_Types].xml").decode()
    assert "template.main+xml" in types and "document.main+xml" not in types
    assert not list(tmp_path.glob("*.staging.docx"))


# ---- the commands ----------------------------------------------------------

def test_new_then_render_end_to_end(tmp_path, capsys):
    assert cli.main(["new", ENTRY, "--source", "Todoist", "--date", "2026-11-19", "--out", str(tmp_path)]) == 0
    folder = tmp_path / "2026-11-19-garden-timelapse-vid-30-days-tomatoes"
    assert (folder / f"{folder.name}.docx").exists()

    saved = json.loads((folder / "brief.json").read_text())
    assert saved["entry"]["text"] == ENTRY and saved["brief"]["title"] == ""

    # an unexpanded brief is refused, and nothing is overwritten
    assert cli.main(["render", str(folder / "brief.json")]) == 1

    filled = model_example().to_dict()
    filled["entry"] = saved["entry"]
    (folder / "brief.json").write_text(json.dumps(filled))
    assert cli.main(["render", str(folder / "brief.json")]) == 0
    assert (folder / "prompt.md").read_text().startswith("Working rules for Claude:")
    assert "TITLE\nPlan a 30-day tomato time-lapse video" in (folder / "writeback.txt").read_text()
    row = json.loads((folder / "app-row.json").read_text())
    assert row["stage"] == "Briefed" and row["title"] == row["brief"]["title"] and row["entry"]["text"] == ENTRY
    assert cli.app_row_id(TaskBrief.from_dict(row | {"entry": row["entry"] | {"task_id": "ab 12/x", "source": "Todoist"}}), folder) == "todoist-ab-12-x"
    assert (folder / "session-link.txt").read_text().startswith("https://claude.ai/code/new?q=")
    doc = Document(str(folder / f"{folder.name}.docx"))
    assert model_example().brief.title in highlighted(doc, WD_COLOR_INDEX.YELLOW)


def test_check_reports_problems(tmp_path, capsys):
    task = model_example()
    task.brief.actions = ["Do it."]
    path = task.save(tmp_path / "brief.json")
    assert cli.main(["check", str(path)]) == 1
    assert "Next action:" in capsys.readouterr().err


def test_missing_file_is_a_clean_error(tmp_path, capsys):
    assert cli.main(["check", str(tmp_path / "nope.json")]) == 2
    assert "todotask:" in capsys.readouterr().err


def test_template_command_writes_both_files(tmp_path):
    assert cli.main(["template", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "ToDo-Task-Brief-TEMPLATE.docx").exists()
    assert (tmp_path / "ToDo-Task-Brief-TEMPLATE.dotx").exists()


def test_word_skill_is_built_from_the_green_prompt(tmp_path):
    from todotask import wordskill
    archive = wordskill.build_word_skill(tmp_path)
    names = zipfile.ZipFile(archive).namelist()
    assert names == ["todo-task-brief/SKILL.md"]
    text = (tmp_path / "todo-task-brief" / "SKILL.md").read_text()
    assert text.startswith("---\nname: todo-task-brief\ndescription: ")
    assert len(wordskill.DESCRIPTION) <= 1024
    for step in spec.expansion_prompt()[1:]:
        assert step in text
    assert spec.working_rules() in text


def test_new_reads_an_entry_from_a_json_file_with_a_byte_order_mark(tmp_path):
    entry = {"text": 'call "D" re: fridge\nlight', "notes": "it's urgent", "source": "Microsoft To Do",
             "list": "Tasks", "task_id": "L1|T1", "captured_on": "2026-11-18T09:00:00Z"}
    source = tmp_path / "entry.json"
    source.write_bytes(b"\xef\xbb\xbf" + json.dumps(entry).encode("utf-8"))
    assert cli.main(["new", "--from-json", str(source), "--out", str(tmp_path / "out")]) == 0
    saved = json.loads(next((tmp_path / "out").glob("*/brief.json")).read_text())
    assert saved["entry"] == entry | {"captured_on": "2026-11-18", "labels": []}
    assert cli.main(["new", "x", "--labels", "read, needs-slot", "--out", str(tmp_path / "labelled")]) == 0
    assert json.loads(next((tmp_path / "labelled").glob("*/brief.json")).read_text())["entry"]["labels"] == ["read", "needs-slot"]


def test_new_without_an_entry_is_a_clean_error(tmp_path, capsys):
    assert cli.main(["new", "--out", str(tmp_path)]) == 2
    assert "empty" in capsys.readouterr().err


def test_playbook_word_copy_is_built_from_the_markdown(tmp_path):
    from todotask import playbook
    source = tmp_path / "p.md"
    source.write_text("---\ntitle: My Playbook\nsubtitle: Sub\n---\n\n# One\n\nA **bold** and `code` line\nthat wraps.\n\n"
                      "| A | B |\n|---|---|\n| x | `y` |\n\n1. First step\n   wrapped\n2. Second\n\n        Completed: x\n\n- bullet\n\n    code line\n")
    doc = Document(str(playbook.build_playbook(tmp_path / "p.docx", source)))
    text = [p.text for p in doc.paragraphs]
    assert text[0] == "My Playbook" and "One" in text and "A bold and code line that wraps." in text
    assert "1. First step wrapped" in text and "2. Second" in text and "Completed: x" in text
    assert "• bullet" in text and "code line" in text
    assert [c.text for c in doc.tables[0].rows[1].cells] == ["x", "y"]


def test_doc_command_turns_markdown_into_word_using_the_first_heading_as_title(tmp_path):
    source = tmp_path / "notes.md"
    source.write_text("# My Notes\n\nSome text.\n\n## Part\n\n| Family | How related |\n|---|---|\n|  |  |\n")
    assert cli.main(["doc", str(source)]) == 0
    doc = Document(str(tmp_path / "notes.docx"))
    assert doc.paragraphs[0].text == "My Notes" and doc.core_properties.title == "My Notes"
    assert [p.text for p in doc.paragraphs].count("My Notes") == 1
    assert len(doc.tables[0].rows) == 2
    assert cli.main(["doc", str(tmp_path / "missing.md")]) == 2
