#!/usr/bin/env python3
"""Merge ASM-verified column updates into schema/cfg/tables/*.json and export GM schema."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CFG_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg"
TABLES_DIR = CFG_DIR / "tables"
GM_OUT = ROOT / "serverv" / "static" / "cfg_schema.json"
GM_REF = ROOT / "serverv" / "static" / "gm_data_boundaries.json"
GAME_MIGRATION = ROOT / "serverv" / "migrations" / "0003_game_persist.up.sql"

VALID_NAME = re.compile(r"^[a-z][a-z0-9_]{0,62}$")
GENERIC_MEANING = re.compile(
    r"^(整型参数|数值|u32\s*参数|float\s*参数|枚举/类别)(（待定）|\(待定\)|（启发）)?$",
    re.I,
)


def humanize_name(name: str) -> str:
    if name.startswith("reserved_u32_"):
        return f"CSV列{name.rsplit('_', 1)[-1]}（读表未读，默认0）"
    if name.startswith("unknown_"):
        return name.replace("_", " ")
    return name.replace("_", " ")


def is_generic_meaning(meaning: str) -> bool:
    m = re.sub(r"\*+", "", meaning or "").strip()
    m = re.sub(r"（待定）|\(待定\)|语义未定", "", m).strip(" 　（）()")
    return not m or bool(GENERIC_MEANING.match(m)) or m in ("整型参数", "数值 u32", "数值")


def asm_summary(c: dict) -> str:
    parts = [c.get("type") or "u32", f"csv{c.get('csv_index', '?')}"]
    if c.get("memory_offset") is not None:
        parts.append(f"mem+{c['memory_offset']}")
    if c.get("asm_va"):
        parts.append(str(c["asm_va"]))
    name = c.get("name") or ""
    if name:
        parts.append(f"→ {humanize_name(name)}")
    return " · ".join(parts)


def col_display(c: dict) -> str:
    meaning = re.sub(r"\*+", "", c.get("meaning") or "").strip()
    if not is_generic_meaning(meaning) and len(meaning) > 4:
        meaning = re.sub(r"（待定）|\(待定\)", "", meaning).strip()
        return meaning[:140]
    name = c.get("name") or ""
    if name:
        return humanize_name(name)
    return f"col{c.get('csv_index', 0)}"


def refresh_col_text(c: dict) -> None:
    if is_generic_meaning(c.get("meaning", "")):
        c["meaning"] = f"ASM已映射：{asm_summary(c)}"
    dn = (c.get("display_name") or "").strip()
    if dn and not is_generic_meaning(dn) and not dn.startswith("ASM已映射"):
        return
    c["display_name"] = col_display(c)


def ensure_csv_gap_columns(data: dict) -> None:
    """Insert gap column defs for CSV indices present in row width but skipped by ASM reader."""
    cols = data.get("columns", [])
    if not cols:
        return
    by_idx = {int(c["csv_index"]): c for c in cols if c.get("csv_index") is not None}
    if not by_idx:
        return
    max_idx = max(by_idx)
    reader = data.get("asm_reader") or "读表"
    table_id = data.get("id") or ""
    out: list[dict] = []
    read_order = 0
    for i in range(max_idx + 1):
        read_order += 1
        if i in by_idx:
            c = by_idx[i]
            c["read_order"] = read_order
            out.append(c)
            continue
        out.append(
            {
                "read_order": read_order,
                "csv_index": i,
                "name": f"col{i}",
                "db_column": f"col{i}",
                "type": "u32",
                "status": "gap",
                "meaning": (
                    f"CSV col{i} 预留（{reader} 不读本列；"
                    f"保持 CSV 列位对齐；内存不映射；默认 0）"
                ),
                "display_name": f"CSV col{i} 预留",
                "confidence": "○ASM确证",
                "asm_reader": reader if reader != "读表" else None,
            }
        )
    data["columns"] = out
    if table_id:
        data.setdefault("column_gap_note", f"CSV 行含 col0..col{max_idx}，读表跳过未映射列见 gap 标记")


def finalize_table(data: dict) -> dict:
    ensure_csv_gap_columns(data)
    cols = data.get("columns", [])
    confirmed = partial = pending = gap = 0
    for c in cols:
        st = c.get("status", "pending")
        name = c.get("name", "")
        if st == "confirmed" and VALID_NAME.match(name):
            c["db_column"] = name
        elif st == "partial" and VALID_NAME.match(name) and not name.startswith("unknown_"):
            c["db_column"] = name
        elif not c.get("db_column"):
            c["db_column"] = f"col{c.get('csv_index', 0)}"
        refresh_col_text(c)
        if st == "confirmed":
            confirmed += 1
        elif st == "partial":
            partial += 1
        elif st == "gap":
            gap += 1
        else:
            pending += 1
    data["column_confirmed"] = confirmed
    data["column_partial"] = partial
    data["column_gap"] = gap
    data["column_pending"] = pending
    data["column_defined"] = len(cols)
    # complete = every CSV column examined via ASM (confirmed/partial/gap OK; pending not OK)
    data["asm_status"] = (
        "complete"
        if pending == 0
        else "partial"
        if (confirmed + partial + gap) > 0
        else "pending"
    )
    return data


def _table_scope(data: dict) -> dict:
    disp = (data.get("disposition") or "DOWNLOAD").upper()
    if disp == "DOWNLOAD":
        return {
            "scope": "global",
            "scope_zh": "全服",
            "scope_note": "所有玩家共用同一份 CSV；客户端经 0xF86A 下载。改此处影响全服平衡/内容，不是单个玩家存档。",
        }
    if disp == "LOCAL":
        return {
            "scope": "global",
            "scope_zh": "全服（服务端）",
            "scope_note": "仅服务端读取，不下发客户端；仍全服共用，非玩家私有。",
        }
    if disp == "SCRIPT":
        return {
            "scope": "global",
            "scope_zh": "全服（脚本）",
            "scope_note": "AUTOEXEC 等脚本/工具用表；全服共用。",
        }
    return {
        "scope": "global",
        "scope_zh": "全服",
        "scope_note": "配置定义表，全服共用。",
    }


def _load_game_tables() -> list[dict]:
    if not GAME_MIGRATION.is_file():
        return []
    text = GAME_MIGRATION.read_text(encoding="utf-8")
    names = sorted(set(re.findall(r"CREATE TABLE game\.(\w+)", text)))
    return [
        {
            "table": n,
            "schema": "game",
            "scope": "player",
            "scope_zh": "玩家",
            "scope_note": "按 world_id + pilot_id 存储；每人不同。在 GM 中编辑 cfg 表不会改到此处。",
        }
        for n in names
    ]


_enums_ida_cache: dict | None = None


def _load_enums_ida() -> dict:
    global _enums_ida_cache
    if _enums_ida_cache is None:
        path = CFG_DIR / "enums_ida.json"
        raw = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        _enums_ida_cache = raw.get("converters", raw)
    return _enums_ida_cache


def _enum_values_for_column(c: dict) -> list[dict]:
    conv = c.get("enum_converter")
    ida_vals: list[dict] = []
    if conv:
        entry = _load_enums_ida().get(conv, {})
        if entry.get("kind", "enum") == "enum":
            ida_vals = entry.get("values") or []
    raw = c.get("enum_values") or ida_vals
    if not raw:
        return []
    if not ida_vals:
        return raw
    by_name = {v["name"]: v for v in ida_vals}
    merged: list[dict] = []
    for ev in raw:
        base = by_name.get(ev["name"], {})
        item = {"name": ev["name"], "value": ev.get("value", base.get("value"))}
        zh = ev.get("label_zh") or base.get("label_zh")
        if zh:
            item["label_zh"] = zh
        merged.append(item)
    return merged


def _gm_column_export(c: dict) -> dict:
    out = {
        "name": c["name"],
        "display_name": c.get("display_name", ""),
        "type": c.get("type", "u32"),
        "status": c.get("status", "pending"),
        "csv_index": c.get("csv_index", 0),
        "meaning": c.get("meaning", ""),
    }
    evs = _enum_values_for_column(c)
    if evs:
        out_enum = []
        for ev in evs:
            item = {"name": ev["name"], "value": ev["value"]}
            if ev.get("label_zh"):
                item["label_zh"] = ev["label_zh"]
            out_enum.append(item)
        out["enum_values"] = out_enum
    if c.get("enum_converter"):
        out["enum_converter"] = c["enum_converter"]
    if c.get("client_persist") is False:
        out["client_persist"] = False
    if c.get("asm_reader"):
        out["asm_reader"] = c["asm_reader"]
    if c.get("asm_va"):
        out["asm_va"] = c["asm_va"]
    return out


def main() -> None:
    index_tables = []
    gm_map = {}
    for path in sorted(TABLES_DIR.glob("*.json")):
        data = finalize_table(json.loads(path.read_text(encoding="utf-8")))
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index_tables.append(
            {
                "id": data["id"],
                "csv_path": data.get("csv_path", ""),
                "disposition": data.get("disposition", "DOWNLOAD"),
                "column_count": data.get("column_count", 0),
                "column_confirmed": data.get("column_confirmed", 0),
                "column_partial": data.get("column_partial", 0),
                "column_pending": data.get("column_pending", 0),
                "column_gap": data.get("column_gap", 0),
                "asm_status": data.get("asm_status", "pending"),
                "reader_func": data.get("asm_reader"),
                "source_md": data.get("source_md", ""),
            }
        )
        gm_map[data["id"]] = {
            "csv_path": data.get("csv_path", ""),
            "purpose": data.get("purpose", ""),
            "disposition": data.get("disposition", ""),
            "column_count": data.get("column_count", 0),
            **_table_scope(data),
            "columns": {
                c["db_column"]: _gm_column_export(c)
                for c in data.get("columns", [])
            },
        }

    index = json.loads((CFG_DIR / "index.json").read_text(encoding="utf-8"))
    index["tables"] = index_tables
    index["total"] = len(index_tables)
    index["download"] = sum(1 for e in index_tables if e.get("disposition") == "DOWNLOAD")
    index["local"] = sum(1 for e in index_tables if e.get("disposition") == "LOCAL")
    index["script"] = sum(1 for e in index_tables if e.get("disposition") == "SCRIPT")
    index["asm_complete"] = sum(1 for e in index_tables if e.get("asm_status") == "complete")
    index["column_confirmed_total"] = sum(e.get("column_confirmed", 0) for e in index_tables)
    index["column_partial_total"] = sum(e.get("column_partial", 0) for e in index_tables)
    index["column_gap_total"] = sum(e.get("column_gap", 0) for e in index_tables)
    index["asm_note"] = "db_column=订案名(confirmed/partial语义名); unknown_* 仍 colN"
    (CFG_DIR / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    GM_OUT.write_text(json.dumps(gm_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    game_tables = _load_game_tables()
    boundaries = {
        "summary": {
            "cfg": {
                "count": len(gm_map),
                "scope": "global",
                "scope_zh": "全服配置",
                "schema": "cfg",
                "note": "当前 GM 编辑器操作的对象。79 张均为全服定义，不含玩家私有存档。",
            },
            "game": {
                "count": len(game_tables),
                "scope": "player",
                "scope_zh": "玩家存档",
                "schema": "game",
                "note": "协议 PERSIST 表，键为 world_id + pilot_id（部分含 slot）。每人不同；勿与 cfg 混淆。",
            },
        },
        "cfg_tables": [
            {
                "table": tid,
                "schema": "cfg",
                **{k: meta[k] for k in ("scope", "scope_zh", "scope_note", "disposition", "csv_path") if k in meta},
            }
            for tid, meta in sorted(gm_map.items())
        ],
        "game_tables": game_tables,
    }
    GM_REF.write_text(json.dumps(boundaries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    complete = sum(1 for t in index_tables if t.get("asm_status") == "complete")
    print(f"merged {len(index_tables)} tables ({complete} asm complete) -> {GM_OUT}")
    print(f"data boundaries -> {GM_REF} ({len(game_tables)} game tables)")


if __name__ == "__main__":
    main()
