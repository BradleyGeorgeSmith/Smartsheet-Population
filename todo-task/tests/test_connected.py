"""Checks for the Todoist and Claude commands. No network: both services are stand-ins."""

from __future__ import annotations

import io
import json
import urllib.error
from types import SimpleNamespace

import pytest

from todotask import connected, spec
from todotask.models import Entry, TaskBrief, model_example

CONFIG = dict(connected.DEFAULTS)


class FakeTodoist:
    """Answers the handful of Todoist calls from a script, and records every request."""

    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def __call__(self, request, timeout=None):
        body = json.loads(request.data.decode()) if request.data else None
        self.calls.append((request.get_method(), request.full_url, body, dict(request.header_items())))
        answer = self.routes(request.get_method(), request.full_url, body)
        if isinstance(answer, Exception):
            raise answer
        return _Reply(answer)


class _Reply:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return b"" if self.payload is None else json.dumps(self.payload).encode()


def http_error(code, body=None, headers=None):
    return urllib.error.HTTPError("https://x", code, "err", headers or {}, io.BytesIO(json.dumps(body or {}).encode()))


def test_a_missing_token_is_explained(monkeypatch):
    monkeypatch.delenv("TODOIST_API_TOKEN", raising=False)
    with pytest.raises(connected.ConnectionProblem, match="TODOIST_API_TOKEN"):
        connected.Todoist()


def test_filter_is_url_encoded_paged_and_sent_with_the_bearer_token():
    pages = iter([{"results": [{"id": "a"}], "next_cursor": "c1"}, {"results": [{"id": "b"}], "next_cursor": None}])
    fake = FakeTodoist(lambda *_: next(pages))
    tasks = connected.Todoist("tok", send=fake).filter_tasks("#Inbox & created after: -3 days & !recurring")
    assert [t["id"] for t in tasks] == ["a", "b"]
    method, url, _, headers = fake.calls[0]
    assert method == "GET" and url.startswith("https://api.todoist.com/api/v1/tasks/filter?query=%23Inbox+%26+created")
    assert "#" not in url and headers["Authorization"] == "Bearer tok"
    assert "cursor=c1" in fake.calls[1][1]


def test_rate_limits_are_retried_and_other_errors_explained():
    answers = iter([http_error(429, {"error_extra": {"retry_after": 7}}), {"results": [], "next_cursor": None}])
    waits = []
    todoist = connected.Todoist("tok", send=FakeTodoist(lambda *_: next(answers)), sleep=waits.append)
    assert todoist.filter_tasks("today") == [] and waits == [7.0]

    refused = connected.Todoist("tok", send=FakeTodoist(lambda *_: http_error(401)))
    with pytest.raises(connected.ConnectionProblem, match="refused the token"):
        refused.get_task("x")


def test_new_entries_skips_briefed_recurring_and_done_and_keeps_the_newest():
    tasks = [
        {"id": "1", "content": "old idea", "labels": [], "added_at": "2026-11-17T01:00:00Z"},
        {"id": "2", "content": "already done", "labels": ["briefed"], "added_at": "2026-11-18T01:00:00Z"},
        {"id": "3", "content": "from another automation", "labels": ["from-email"], "added_at": "2026-11-18T02:00:00Z"},
        {"id": "4", "content": "daily habit", "labels": [], "due": {"is_recurring": True}, "added_at": "2026-11-18T03:00:00Z"},
        {"id": "5", "content": "keep out", "labels": ["skip-ai"], "added_at": "2026-11-18T04:00:00Z"},
        {"id": "6", "content": "newest idea", "labels": ["read"], "added_at": "2026-11-19T01:00:00Z"},
        {"id": "7", "content": "ticked", "labels": [], "checked": True, "added_at": "2026-11-19T02:00:00Z"},
        {"id": "8", "content": "middle idea", "labels": [], "added_at": "2026-11-18T05:00:00Z"},
    ]
    fake = FakeTodoist(lambda *_: {"results": tasks, "next_cursor": None})
    kept, left = connected.new_entries(connected.Todoist("tok", send=fake), CONFIG, limit=2)
    assert [t["id"] for t in kept] == ["6", "8"] and left == 1
    assert "-3+days" in fake.calls[0][1] and "briefed" not in fake.calls[0][1]  # labels are checked here, not in the filter


def test_long_notes_are_cut_with_a_note_saying_so():
    entry = connected.entry_from_task({"id": "9", "content": " Dan - Sales Advice ", "description": "x" * 5000,
                                       "project_id": "P", "added_at": "2026-11-18T04:59:03Z"})
    assert entry.text == "Dan - Sales Advice" and entry.captured_on == "2026-11-18" and entry.task_id == "9"
    assert entry.notes.startswith("x" * 2000) and "about 3000 more characters" in entry.notes


def todoist_brief(**entry):
    data = model_example().to_dict()
    data["entry"].update({"source": "Todoist", "task_id": "T1", **entry})
    return TaskBrief.from_dict(data)


def test_write_back_keeps_existing_labels_and_the_original_entry():
    def routes(method, url, body):
        if method == "GET" and url.endswith("/tasks/T1"):
            return {"id": "T1", "content": "garden timelapse vid??", "description": "", "labels": ["read"]}
        if method == "GET" and "/labels" in url:
            return {"results": [{"name": "read"}], "next_cursor": None}
        return {}
    fake = FakeTodoist(routes)
    task = todoist_brief()
    result = connected.write_back(connected.Todoist("tok", send=fake), task, CONFIG)
    posts = [(url, body) for method, url, body, _ in fake.calls if method == "POST"]
    assert posts[0] == ("https://api.todoist.com/api/v1/labels", {"name": "briefed"})
    update = dict(posts)["https://api.todoist.com/api/v1/tasks/T1"]
    assert update["content"] == task.writeback.title and update["labels"] == ["read", "briefed"]
    assert update["description"].endswith("Original entry: " + task.entry.text)
    comment = dict(posts)["https://api.todoist.com/api/v1/comments"]
    assert comment["task_id"] == "T1" and comment["content"].startswith("Working rules for Claude:")
    assert result["sent"] is True


def test_write_back_leaves_a_long_description_alone_and_dry_run_sends_nothing():
    fake = FakeTodoist(lambda method, url, body: {"id": "T1", "content": "x", "description": "y" * 900, "labels": []})
    result = connected.write_back(connected.Todoist("tok", send=fake), todoist_brief(), CONFIG, dry_run=True)
    assert "description" not in result["change"] and result["sent"] is False
    assert all(method == "GET" for method, *_ in fake.calls)


def test_write_back_refuses_an_unfinished_or_foreign_brief():
    todoist = connected.Todoist("tok", send=FakeTodoist(lambda *_: {}))
    with pytest.raises(ValueError, match="did not come from Todoist"):
        connected.write_back(todoist, model_example(), CONFIG)
    with pytest.raises(ValueError, match="not ready"):
        connected.write_back(todoist, TaskBrief(entry=Entry(text="x", source="Todoist", task_id="T1")), CONFIG)


def test_existing_brief_finds_a_task_by_id(tmp_path):
    todoist_brief().save(tmp_path / "2026-11-19-a" / "brief.json")
    (tmp_path / "broken").mkdir()
    (tmp_path / "broken" / "brief.json").write_text("not json")
    assert connected.existing_brief(tmp_path, "T1") == tmp_path / "2026-11-19-a" / "brief.json"
    assert connected.existing_brief(tmp_path, "nope") is None


# ---- Claude ------------------------------------------------------------------

class FakeClaude:
    def __init__(self, message):
        self.message, self.request = message, None
        self.beta = SimpleNamespace(messages=SimpleNamespace(stream=self._stream))

    def _stream(self, **request):
        self.request = request
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def get_final_message(self):
        return self.message


def reply(data, stop="end_turn"):
    return SimpleNamespace(stop_reason=stop, stop_details=SimpleNamespace(category="cyber"),
                           content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=json.dumps(data))])


def test_the_request_carries_the_rules_the_example_and_the_entry():
    request = connected.expansion_request(Entry(text="buy \\1 shoes {{x}}", notes="", captured_on="2026-11-19"))
    assert "Entry: <<<buy \\1 shoes {{x}}>>>" in request and "Notes already on the task: <<<None>>>" in request
    assert "The entry was captured on: 2026-11-19" in request and model_example().brief.title in request
    assert "{{ENTRY}}" not in request and "{{TODAY}}" not in request
    tricky = connected.expansion_request(Entry(text="what is {{NOTES}}?", notes="real notes"))
    assert "Entry: <<<what is {{NOTES}}?>>>" in tricky and "task: <<<real notes>>>" in tricky


def test_expand_keeps_the_entry_and_asks_for_the_most_capable_model_with_a_fallback():
    written = {k: model_example().to_dict()[k] for k in ("task_type", "brief", "writeback")}
    claude = FakeClaude(reply(written))
    before = TaskBrief(entry=Entry(text="garden timelapse vid??", source="Todoist", task_id="T9", captured_on="2026-11-19"))
    after = connected.expand_entry(before, client=claude)
    assert after.entry == before.entry and after.brief.title == model_example().brief.title and after.problems() == []
    sent = claude.request
    assert sent["model"] == "claude-fable-5-2" and sent["fallbacks"] == "default"
    assert sent["betas"] == ["server-side-fallback-2026-07-01"] and "thinking" not in sent
    assert sent["output_config"]["format"]["type"] == "json_schema"
    assert sent["output_config"]["format"]["schema"]["properties"]["task_type"]["enum"] == list(connected.TASK_TYPES)


def test_a_refusal_or_a_cut_off_reply_is_reported_not_parsed():
    task = TaskBrief(entry=Entry(text="x"))
    with pytest.raises(connected.ConnectionProblem, match=r"declined.*cyber"):
        connected.expand_entry(task, client=FakeClaude(reply({}, stop="refusal")))
    with pytest.raises(connected.ConnectionProblem, match="cut off"):
        connected.expand_entry(task, client=FakeClaude(reply({}, stop="max_tokens")))


def test_config_local_overrides_config(tmp_path):
    (tmp_path / "config.json").write_text(json.dumps({"window_days": 5, "max_briefs_per_run": 4}))
    (tmp_path / "config.local.json").write_text(json.dumps({"window_days": 9}))
    config = connected.load_config(tmp_path)
    assert config["window_days"] == 9 and config["max_briefs_per_run"] == 4
    assert config["skip_labels"] == [spec.LABEL_BRIEFED, spec.LABEL_SKIP, "from-email"]
