#!/usr/bin/env python3
import json
import re
from pathlib import Path

TRANSCRIPT = Path(
    r"C:\Users\xxm38\.cursor\projects\f-9ymsgo-9you\agent-transcripts"
    r"\0e29259c-4851-4e3f-aa30-8f9d5492f173\0e29259c-4851-4e3f-aa30-8f9d5492f173.jsonl"
)
OUT = Path(__file__).resolve().parent

for line in TRANSCRIPT.open(encoding="utf-8"):
    try:
        o = json.loads(line)
    except json.JSONDecodeError:
        continue
    if o.get("role") != "assistant":
        continue
    for part in o.get("message", {}).get("content", []):
        if part.get("type") != "tool_use" or part.get("name") != "Write":
            continue
        inp = part.get("input", {})
        path = inp.get("path", "")
        if not path.endswith(".py") or "db_design/tools/_" not in path.replace("\\", "/"):
            continue
        contents = inp.get("contents", "")
        if not contents:
            continue
        name = Path(path).name
        dest = OUT / name
        dest.write_text(contents, encoding="utf-8")
        print("Extracted", dest)
