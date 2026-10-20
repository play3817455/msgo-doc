#!/usr/bin/env python3
"""Recover deleted table/entity JSON from agent transcript tool writes."""
import json
from pathlib import Path

TRANSCRIPT = Path(
    r"C:\Users\xxm38\.cursor\projects\f-9ymsgo-9you\agent-transcripts"
    r"\0e29259c-4851-4e3f-aa30-8f9d5492f173\0e29259c-4851-4e3f-aa30-8f9d5492f173.jsonl"
)
SCHEMA = Path(__file__).resolve().parents[1] / "schema"
TABLES = SCHEMA / "_legacy_tables"
ENTITIES = SCHEMA / "entities"

tables: dict[str, str] = {}
entities: dict[str, str] = {}

for line in TRANSCRIPT.open(encoding="utf-8"):
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    if o.get("role") != "assistant":
        continue
    for part in o.get("message", {}).get("content", []):
        if part.get("type") != "tool_use":
            continue
        name = part.get("name")
        if name not in ("Write", "StrReplace"):
            continue
        inp = part.get("input", {})
        path = inp.get("path", "").replace("\\", "/")
        contents = inp.get("contents") or inp.get("new_string") or ""
        if "/schema/tables/tbl_" in path and path.endswith(".json") and contents.strip().startswith("{"):
            tables[Path(path).name] = contents
        elif "/schema/entities/" in path and path.endswith(".json") and "pilot.json" not in path and contents.strip().startswith("{"):
            entities[Path(path).name] = contents

print(f"Found {len(tables)} complete tables, {len(entities)} entities in transcript")

TABLES.mkdir(parents=True, exist_ok=True)
ENTITIES.mkdir(parents=True, exist_ok=True)
for fname, body in tables.items():
    (TABLES / fname).write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")
for fname, body in entities.items():
    (ENTITIES / fname).write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")

catalog = json.loads((SCHEMA / "_meta" / "struct_catalog.json").read_text(encoding="utf-8"))
all_ids = sorted(catalog.get("structs", catalog).keys()) if isinstance(catalog.get("structs"), dict) else []
missing = [f"tbl_{sid}" for sid in all_ids if f"tbl_{sid}.json" not in tables]
complete = sum(1 for v in tables.values() if '"status": "complete"' in v)
print(f"Complete among restored: {complete}/{len(tables)}")

print(f"Restored to {TABLES} and {ENTITIES}")
print(f"Still missing {len(missing)} tables: {missing[:20]}...")
