#!/usr/bin/env python3
"""Create the PARA folder tree on any target: local disk, a mounted NAS or
OneDrive folder, or Dropbox (via API).

The tree mirrors second-brain/ in this repository so every store uses the
same names. It only creates folders; it never moves or deletes.

Usage:
  python para_scaffold.py --target "D:/Brad"                 # local or NAS path
  python para_scaffold.py --target "/Volumes/NASMorley/Brad"
  python para_scaffold.py --dropbox "/Brad Smith"            # needs DROPBOX_ACCESS_TOKEN
  python para_scaffold.py --print                            # just show the tree
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

TREE = {
    "00_Inbox": ["_dictation", "_screenshots", "_downloads-to-sort"],
    "10_Projects": [
        "2026-11_second-brain-system",
        "2026-03_nexus-google-play",
        "2026-04_google-account-consolidation",
        "2026-06_hydralada-50-year-video",
        "2026-02_toop-street-alterations",
        "2026-05_morley-studio-fitout",
        "2026-07_substack-launch",
        "_template-project",
    ],
    "20_Areas": [
        "Health",
        "Hydralada-Marketing",
        "Toop-Street-Property",
        "Morley-Studio",
        "Finance-and-Subscriptions",
        "Spirituality",
        "Relationships-and-Associations",
        "IT-Devices-and-Storage",
        "Vision-Mission-Values",
        "Journal",
        "Habits",
    ],
    "30_Resources": [
        "Prompts",
        "Frameworks",
        "Inspiration/Architecture",
        "Inspiration/Manufacturing",
        "Inspiration/Innovation",
        "Inspiration/Branding",
        "Inspiration/Pinterest",
        "Inspiration/Quotes",
        "Inspiration/Quote-Cards",
        "Marketing-Swipe-File",
        "Learning",
        "Templates",
        "Reviews",
    ],
    "40_Archives": ["2024", "2025", "2026"],
}

PROJECT_README = """# {name}

Outcome (one sentence, what exists when this is done):
Target date:
PARA: Project

## Next actions
-

## Packets
(reusable outputs land in ./packets)
"""


def paths() -> list[str]:
    out: list[str] = []
    for root, subs in TREE.items():
        out.append(root)
        for s in subs:
            out.append(f"{root}/{s}")
    return out


def scaffold_local(target: Path) -> None:
    for rel in paths():
        p = target / rel
        p.mkdir(parents=True, exist_ok=True)
        if rel.startswith("10_Projects/") and not (p / "README.md").exists():
            (p / "README.md").write_text(PROJECT_README.format(name=rel.split("/", 1)[1]))
        if rel.startswith("10_Projects/"):
            (p / "packets").mkdir(exist_ok=True)
    print(f"created {len(paths())} folders under {target}")


def scaffold_dropbox(root: str) -> None:
    import requests  # local import so --print works without requests

    token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not token:
        print("DROPBOX_ACCESS_TOKEN is not set", file=sys.stderr)
        sys.exit(2)
    headers = {"Authorization": f"Bearer {token}"}
    ns = os.environ.get("DROPBOX_PATH_ROOT_NS")
    if ns:
        headers["Dropbox-API-Path-Root"] = json.dumps({".tag": "root", "root": ns})
    entries = [{"path": f"{root.rstrip('/')}/{rel}"} for rel in paths()]
    r = requests.post(
        "https://api.dropboxapi.com/2/files/create_folder_batch",
        headers=headers,
        json={"paths": [e["path"] for e in entries], "autorename": False, "force_async": False},
        timeout=120,
    )
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2)[:2000])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", help="local, NAS or OneDrive folder")
    ap.add_argument("--dropbox", help="Dropbox folder to scaffold under, e.g. '/Brad Smith'")
    ap.add_argument("--print", action="store_true", help="print the tree and exit")
    args = ap.parse_args()
    if args.print or not (args.target or args.dropbox):
        for rel in paths():
            print(rel)
        return 0
    if args.target:
        scaffold_local(Path(args.target))
    if args.dropbox:
        scaffold_dropbox(args.dropbox)
    return 0


if __name__ == "__main__":
    sys.exit(main())
