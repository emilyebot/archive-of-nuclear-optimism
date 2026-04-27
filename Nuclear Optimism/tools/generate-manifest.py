#!/usr/bin/env python3
"""Write images.json sorted by leading year in each filename."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "Image Archive"
OUT_JSON = ROOT / "images.json"
OUT_JS = ROOT / "gallery-data.js"

YEAR_PREFIX = re.compile(r"^(\d{3,4})(?:,|-)")


def sort_key(name: str) -> tuple:
    m = YEAR_PREFIX.match(name)
    if not m:
        return (99999, name)
    digits = m.group(1)
    year = int(digits, 10)
    # e.g. "195-, ..." → treat as start of decade
    if len(digits) == 3 and name.startswith(digits + "-"):
        year *= 10
    return (year, name)


def main() -> None:
    if not ARCHIVE.is_dir():
        raise SystemExit(f"Missing folder: {ARCHIVE}")
    files = sorted(
        (p.name for p in ARCHIVE.iterdir() if p.is_file() and not p.name.startswith(".")),
        key=sort_key,
    )
    items = [{"file": f, "path": f"Image Archive/{f}"} for f in files]
    OUT_JSON.write_text(json.dumps(items, indent=2) + "\n", encoding="utf-8")
    js_payload = json.dumps(items, ensure_ascii=False)
    OUT_JS.write_text(
        f"window.GALLERY_MANIFEST = {js_payload};\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(items)} entries to {OUT_JSON} and {OUT_JS}")


if __name__ == "__main__":
    main()
