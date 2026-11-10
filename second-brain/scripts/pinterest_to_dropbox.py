#!/usr/bin/env python3
"""Mirror every pin image on your Pinterest boards into Dropbox.

Uses the official Pinterest API v5 (boards:read, pins:read) and the Dropbox
HTTP API v2 (files.content.write, files.metadata.read). No scraping.

Environment variables (never put these in files):
  PINTEREST_ACCESS_TOKEN   OAuth token for your Pinterest account
  DROPBOX_ACCESS_TOKEN     Dropbox app token
  DROPBOX_ROOT             Target folder in Dropbox, default
                           "/Brad Smith/30_Resources/Inspiration/Pinterest"
  DROPBOX_PATH_ROOT_NS     Optional team root namespace id (Hydralada team
                           account). When set, paths are resolved against the
                           team space via the Dropbox-API-Path-Root header.

Usage:
  python pinterest_to_dropbox.py --dry-run
  python pinterest_to_dropbox.py --since-last-run
  python pinterest_to_dropbox.py --board "Architecture" --board "Branding"

Writes a manifest JSON per run to --manifest-dir (default
second-brain/30_Resources/Inspiration/Pinterest/_manifests). Never deletes
anything on either side.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

PINTEREST_API = "https://api.pinterest.com/v5"
DROPBOX_CONTENT = "https://content.dropboxapi.com/2"
DROPBOX_API = "https://api.dropboxapi.com/2"
HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST_DIR = HERE.parent / "30_Resources" / "Inspiration" / "Pinterest" / "_manifests"
STATE_FILE = HERE / "data" / "pinterest_last_run.json"


def slugify(text: str, limit: int = 60) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text or "").strip("-").lower()
    return (text or "pin")[:limit]


class Pinterest:
    def __init__(self, token: str):
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"

    def _get(self, path: str, **params):
        for attempt in range(6):
            r = self.s.get(f"{PINTEREST_API}{path}", params=params, timeout=60)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", "30"))
                print(f"  rate limited, sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f"Pinterest kept rate limiting {path}")

    def _paged(self, path: str, **params):
        bookmark = None
        while True:
            data = self._get(path, page_size=100, bookmark=bookmark, **params)
            for item in data.get("items", []):
                yield item
            bookmark = data.get("bookmark")
            if not bookmark:
                return

    def boards(self):
        return list(self._paged("/boards", privacy="ALL"))

    def pins(self, board_id: str):
        return list(self._paged(f"/boards/{board_id}/pins"))


def best_image_url(pin: dict) -> str | None:
    media = pin.get("media") or {}
    images = media.get("images") or {}
    # Prefer the largest rendition the API exposes.
    for key in ("originals", "1200x", "600x", "400x300", "150x150"):
        if key in images and images[key].get("url"):
            return images[key]["url"]
    # Fallback: any image.
    for v in images.values():
        if isinstance(v, dict) and v.get("url"):
            return v["url"]
    return None


class Dropbox:
    def __init__(self, token: str, path_root_ns: str | None):
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"
        if path_root_ns:
            self.s.headers["Dropbox-API-Path-Root"] = json.dumps(
                {".tag": "root", "root": path_root_ns}
            )

    def exists(self, path: str) -> bool:
        r = self.s.post(
            f"{DROPBOX_API}/files/get_metadata",
            json={"path": path},
            timeout=60,
        )
        if r.status_code == 409:
            return False
        r.raise_for_status()
        return True

    def ensure_folder(self, path: str) -> None:
        r = self.s.post(
            f"{DROPBOX_API}/files/create_folder_v2",
            json={"path": path, "autorename": False},
            timeout=60,
        )
        if r.status_code == 409:  # already exists
            return
        r.raise_for_status()

    def upload(self, path: str, content: bytes) -> dict:
        args = {"path": path, "mode": "add", "autorename": False, "mute": True}
        r = self.s.post(
            f"{DROPBOX_CONTENT}/files/upload",
            headers={
                "Dropbox-API-Arg": json.dumps(args),
                "Content-Type": "application/octet-stream",
            },
            data=content,
            timeout=300,
        )
        r.raise_for_status()
        return r.json()


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_run": None, "seen_pin_ids": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="list boards, pins and target paths; upload nothing")
    ap.add_argument("--since-last-run", action="store_true", help="skip pins already recorded in the state file")
    ap.add_argument("--board", action="append", default=[], help="only these board names (repeatable)")
    ap.add_argument("--manifest-dir", default=str(DEFAULT_MANIFEST_DIR))
    ap.add_argument("--limit", type=int, default=0, help="stop after N pins (testing)")
    args = ap.parse_args()

    p_token = os.environ.get("PINTEREST_ACCESS_TOKEN")
    d_token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    root = os.environ.get("DROPBOX_ROOT", "/Brad Smith/30_Resources/Inspiration/Pinterest").rstrip("/")
    if not p_token:
        print("PINTEREST_ACCESS_TOKEN is not set", file=sys.stderr)
        return 2
    if not d_token and not args.dry_run:
        print("DROPBOX_ACCESS_TOKEN is not set (use --dry-run to list only)", file=sys.stderr)
        return 2

    pin_api = Pinterest(p_token)
    dbx = Dropbox(d_token, os.environ.get("DROPBOX_PATH_ROOT_NS")) if d_token else None
    state = load_state()
    seen = set(state.get("seen_pin_ids", []))

    boards = pin_api.boards()
    if args.board:
        wanted = {b.lower() for b in args.board}
        boards = [b for b in boards if b.get("name", "").lower() in wanted]
    print(f"Boards: {len(boards)}")

    manifest = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "root": root,
        "boards": [],
        "downloaded": 0,
        "skipped_existing": 0,
        "skipped_seen": 0,
        "failed": [],
    }
    http = requests.Session()
    count = 0

    for board in boards:
        name = board.get("name", "untitled")
        folder = f"{root}/{slugify(name, 40)}"
        pins = pin_api.pins(board["id"])
        entry = {"board_id": board["id"], "name": name, "folder": folder, "pin_count": len(pins), "pins": []}
        print(f"- {name}: {len(pins)} pins -> {folder}")
        if not args.dry_run:
            dbx.ensure_folder(folder)
        for pin in pins:
            pid = pin.get("id")
            if args.since_last_run and pid in seen:
                manifest["skipped_seen"] += 1
                continue
            url = best_image_url(pin)
            if not url:
                manifest["failed"].append({"pin": pid, "reason": "no image url (video or missing)"})
                continue
            ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
            title = pin.get("title") or pin.get("description") or pin.get("alt_text") or ""
            target = f"{folder}/{pid}_{slugify(title, 50)}{ext}"
            record = {
                "pin_id": pid,
                "title": pin.get("title"),
                "description": pin.get("description"),
                "alt_text": pin.get("alt_text"),
                "link": pin.get("link"),
                "created_at": pin.get("created_at"),
                "image_url": url,
                "dropbox_path": target,
            }
            if args.dry_run:
                entry["pins"].append(record)
                count += 1
                if args.limit and count >= args.limit:
                    break
                continue
            try:
                if dbx.exists(target):
                    manifest["skipped_existing"] += 1
                    seen.add(pid)
                    entry["pins"].append(record | {"status": "exists"})
                    continue
                img = http.get(url, timeout=120)
                img.raise_for_status()
                record["sha256"] = hashlib.sha256(img.content).hexdigest()
                record["bytes"] = len(img.content)
                dbx.upload(target, img.content)
                manifest["downloaded"] += 1
                seen.add(pid)
                entry["pins"].append(record | {"status": "uploaded"})
                count += 1
                time.sleep(0.2)  # be polite to both APIs
            except Exception as exc:  # noqa: BLE001
                manifest["failed"].append({"pin": pid, "reason": str(exc)})
            if args.limit and count >= args.limit:
                break
        manifest["boards"].append(entry)
        if args.limit and count >= args.limit:
            break

    mdir = Path(args.manifest_dir)
    mdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    mpath = mdir / f"{stamp}{'_dryrun' if args.dry_run else ''}.json"
    mpath.write_text(json.dumps(manifest, indent=2))
    print(
        f"downloaded={manifest['downloaded']} existing={manifest['skipped_existing']} "
        f"seen={manifest['skipped_seen']} failed={len(manifest['failed'])} manifest={mpath}"
    )

    if not args.dry_run:
        state["last_run"] = manifest["run_at"]
        state["seen_pin_ids"] = sorted(seen)
        save_state(state)
    return 0 if not manifest["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
