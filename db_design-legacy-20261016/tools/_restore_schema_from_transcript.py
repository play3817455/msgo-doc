#!/usr/bin/env python3
"""Recover deleted db_design/schema/{composites,tables,entities}/*.json by replaying
Write/StrReplace tool calls from agent transcripts.

只写回**当前磁盘缺失**的文件；已存在的一律不动（避免覆盖后续人工/脚本修改）。
"""
import io
import json
import sys
from pathlib import Path

TRANSCRIPTS = Path(r"C:\Users\xxm38\.cursor\projects\f-9ymsgo-9you\agent-transcripts")
SCHEMA = Path(__file__).resolve().parents[1] / "schema"
APPLY = "--apply" in sys.argv

DIRS = {
    "composites": SCHEMA / "composites",
    "tables": SCHEMA / "_legacy_tables",
    "entities": SCHEMA / "entities",
}

files = sorted(
    (p for d in TRANSCRIPTS.iterdir() if d.is_dir() for p in d.glob("*.jsonl")),
    key=lambda p: p.stat().st_mtime,
)

state: dict[tuple[str, str], str] = {}
history: dict[tuple[str, str], list[str]] = {}

for path in files:
    tag = path.parent.name[:8]
    with io.open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("role") != "assistant":
                continue
            for part in (obj.get("message", {}) or {}).get("content", []) or []:
                if part.get("type") != "tool_use":
                    continue
                name = part.get("name")
                if name not in ("Write", "StrReplace"):
                    continue
                inp = part.get("input") or {}
                norm = str(inp.get("path", "")).replace("\\", "/").lower()
                key = None
                for sub in DIRS:
                    if f"/schema/{sub}/" in norm:
                        fname = norm.rsplit("/", 1)[-1]
                        if fname.endswith(".json"):
                            key = (sub, fname[:-5])
                        break
                if key is None:
                    continue
                if name == "Write":
                    body = inp.get("contents") or ""
                    if body.strip().startswith("{"):
                        state[key] = body
                        history.setdefault(key, []).append(f"{tag}:W{lineno}")
                else:
                    cur = state.get(key)
                    if cur is None:
                        continue
                    old = inp.get("old_string") or ""
                    new = inp.get("new_string") or ""
                    if inp.get("replace_all"):
                        state[key] = cur.replace(old, new)
                    elif old in cur:
                        state[key] = cur.replace(old, new, 1)
                    else:
                        print(f"  ! {tag}:{lineno} {key} StrReplace 未命中，跳过")
                        continue
                    history.setdefault(key, []).append(f"{tag}:S{lineno}")

missing = []
for (sub, stem), body in sorted(state.items()):
    target = DIRS[sub] / f"{stem}.json"
    if target.exists():
        continue
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        print(f"  ! {sub}/{stem} 回放结果非法: {exc}")
        continue
    n = len(data.get("members", data.get("columns", [])))
    missing.append((sub, stem, body, n))

print(f"\ntranscript 记录的 schema JSON 写入 {len(state)} 个；当前磁盘缺失 {len(missing)} 个：")
for sub, stem, _body, n in missing:
    print(f"  {sub:10s} {stem:34s} 条目={n:<4d} 末次={history[(sub, stem)][-1]}")

if not APPLY:
    print("\n(dry-run，加 --apply 落盘)")
    raise SystemExit(0)

for sub, stem, body, _n in missing:
    (DIRS[sub] / f"{stem}.json").write_text(body if body.endswith("\n") else body + "\n", encoding="utf-8")
print(f"\n已写回 {len(missing)} 个文件")
