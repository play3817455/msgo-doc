#!/usr/bin/env python3
"""Scan schema for members/fields missing Chinese meaning."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"

BAD_PATTERNS = (
    re.compile(r"^TBD$", re.I),
    re.compile(r"待.*取证"),
    re.compile(r"待定"),
    re.compile(r"^[\s?]+$"),
    re.compile(r"^member_\d+$", re.I),
    re.compile(r"^field_\d+$", re.I),
)
# At least one CJK character
HAS_CJK = re.compile(r"[\u4e00-\u9fff]")


def is_bad_meaning(text: str | None) -> str | None:
    if text is None:
        return "missing"
    t = text.strip()
    if not t:
        return "empty"
    for p in BAD_PATTERNS:
        if p.search(t):
            return f"bad:{t[:40]}"
    if not HAS_CJK.search(t):
        return f"no_cjk:{t[:60]}"
    return None


def walk(obj, path: str, issues: list):
    if isinstance(obj, dict):
        if "name" in obj and "meaning" in obj and ("offset" in obj or "wire_type" in obj or "disposition" in obj):
            reason = is_bad_meaning(obj.get("meaning"))
            if reason:
                issues.append({
                    "file": path,
                    "field": obj.get("name"),
                    "reason": reason,
                    "meaning": obj.get("meaning"),
                    "disposition": obj.get("disposition"),
                })
        if "name" in obj and "meaning" in obj and obj.get("disposition") == "COMPOSITE":
            reason = is_bad_meaning(obj.get("meaning"))
            if reason:
                issues.append({
                    "file": path,
                    "field": obj.get("name"),
                    "reason": reason,
                    "meaning": obj.get("meaning"),
                    "kind": "table_column",
                })
        for k, v in obj.items():
            walk(v, path, issues)
    elif isinstance(obj, list):
        for item in obj:
            walk(item, path, issues)


def main():
    issues: list[dict] = []
    for sub in ("composites", "entities", "tables"):
        d = ROOT / sub
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.json")):
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            walk(data, f"{sub}/{fp.name}", issues)

    by_file: dict[str, list] = {}
    for it in issues:
        by_file.setdefault(it["file"], []).append(it)

    print(f"Total issues: {len(issues)} across {len(by_file)} files\n")
    for f in sorted(by_file):
        print(f"## {f} ({len(by_file[f])})")
        for it in by_file[f]:
            print(f"  - {it['field']}: {it['reason']} => {it.get('meaning')!r}")
        print()


if __name__ == "__main__":
    main()
