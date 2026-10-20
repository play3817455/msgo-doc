#!/usr/bin/env python3
"""Import field index from protocol_analysis/commands/*/fields.csv into schema/fields/index.json."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTO_DIR = ROOT / "protocol_analysis" / "commands"
SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schema"
OUT_PATH = SCHEMA_DIR / "fields" / "index.json"
META_PATH = SCHEMA_DIR / "_meta.json"

SKIP_NAMES = {"opcode", "（长度闭合）"}
SKIP_PATTERN = re.compile(r"长度闭合|^\（")

# 字段索引的自检口径：**字段名里不该出现尖括号或裸的 `N`**。
# `fields.csv` 的线类型格写 `array<X,N>`，那个 ASCII 逗号一旦没加引号，裸 `csv.DictReader`
# 就会把整行切歪，把碎片 `N>` 顶到「字段名」列上——于是索引里凭空多一个字段名 `N>`、
# 同时真名（`news`）丢失。这一层此前**没有任何门禁**，脏数据就一直躺着没人喊。
FRAGMENT_NAME_RE = re.compile(r"[<>]|^N\d*$|^array$|^\d+$")


def parse_command_dir(dirname: str) -> dict:
    """Extract metadata from folder name like CS-0xFD3E-lounge-pilot_create."""
    parts = dirname.split("-", 3)
    direction = parts[0] if parts else ""
    opcode = parts[1] if len(parts) > 1 else ""
    rest = parts[2] if len(parts) > 2 else ""
    if len(parts) > 3:
        proto_class, cmd_name = parts[2], parts[3]
    else:
        sub = rest.split("-", 1)
        proto_class = sub[0] if sub else ""
        cmd_name = sub[1] if len(sub) > 1 else rest
    return {
        "id": dirname,
        "direction": direction,
        "opcode": opcode,
        "protocol_class": proto_class,
        "command_name": cmd_name,
    }


def load_fields_csv(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("字段名") or "").strip()
            if not name or name in SKIP_NAMES or SKIP_PATTERN.search(name):
                continue
            if SKIP_PATTERN.search(row.get("含义") or ""):
                continue
            rows.append(
                {
                    "offset": row.get("偏移", ""),
                    "length": row.get("长度", ""),
                    "wire_type": row.get("线类型", ""),
                    "name": name,
                    "meaning": row.get("含义", ""),
                    "usage": row.get("用途", ""),
                    "confidence": row.get("置信度", ""),
                }
            )
    return rows


def main() -> None:
    if not PROTO_DIR.is_dir():
        raise SystemExit(f"protocol_analysis not found: {PROTO_DIR}")

    by_name: dict[str, dict] = {}
    command_count = 0
    total_rows = 0

    for cmd_dir in sorted(PROTO_DIR.iterdir()):
        if not cmd_dir.is_dir():
            continue
        csv_path = cmd_dir / "fields.csv"
        if not csv_path.is_file():
            continue
        command_count += 1
        meta = parse_command_dir(cmd_dir.name)
        fields = load_fields_csv(csv_path)
        total_rows += len(fields)

        for field in fields:
            name = field["name"]
            entry = by_name.setdefault(
                name,
                {
                    "name": name,
                    "wire_types": set(),
                    "appear_count": 0,
                    "commands": [],
                    "meanings": set(),
                    "disposition": "TBD",
                    "entity": None,
                },
            )
            entry["appear_count"] += 1
            wt = field["wire_type"]
            if wt:
                entry["wire_types"].add(wt)
            meaning = field["meaning"]
            if meaning:
                entry["meanings"].add(meaning)
            entry["commands"].append(
                {
                    "command": meta["id"],
                    "opcode": meta["opcode"],
                    "direction": meta["direction"],
                    "command_name": meta["command_name"],
                    "offset": field["offset"],
                    "length": field["length"],
                    "wire_type": wt,
                }
            )

    # Heuristic pre-classification for common transient fields
    transient_hints = {"result", "opcode"}
    for name, entry in by_name.items():
        if name in transient_hints:
            entry["disposition"] = "TRANSIENT"
        elif name.startswith("target_") or name in {"ent_id", "frame_no"}:
            entry["disposition"] = "EVENT"

    fields_list = []
    for name in sorted(by_name.keys(), key=lambda n: (-by_name[n]["appear_count"], n)):
        e = by_name[name]
        fields_list.append(
            {
                "name": name,
                "wire_types": sorted(e["wire_types"]),
                "appear_count": e["appear_count"],
                "disposition": e["disposition"],
                "entity": e["entity"],
                "meaning_sample": sorted(e["meanings"])[0] if e["meanings"] else "",
                "commands": e["commands"],
            }
        )

    # 门禁（写盘之前）：碎片名 = csv 行被切歪的信号。别让它写进索引再静默存活，
    # 修法是 `db_design/tools/fix_fields_csv.py --write`（给 `array<X,N>` 加规范引号），
    # 不是手改 csv、更不是在这里过滤掉——过滤只会把「真名丢了」藏起来。
    fragments = [f["name"] for f in fields_list if FRAGMENT_NAME_RE.search(f["name"])]
    if fragments:
        print(f"FAIL 字段索引里出现 {len(fragments)} 个疑似 csv 碎片名：{sorted(fragments)[:10]}")
        print("     ⇒ 跑 db_design/tools/fix_fields_csv.py --check 定位畸形行，--write 修好后重跑本工具")
        raise SystemExit(1)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": date.today().isoformat(),
        "source": "protocol_analysis/commands/*/fields.csv",
        "stats": {
            "commands_scanned": command_count,
            "field_rows": total_rows,
            "unique_names": len(fields_list),
        },
        "fields": fields_list,
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(fields_list)} unique fields from {command_count} commands)")

    if META_PATH.is_file():
        meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        meta["updated"] = date.today().isoformat()
        meta["stats"]["fields_indexed"] = total_rows
        meta["stats"]["unique_field_names"] = len(fields_list)
        meta["stats"]["commands_scanned"] = command_count
        META_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Updated {META_PATH}")


if __name__ == "__main__":
    main()
