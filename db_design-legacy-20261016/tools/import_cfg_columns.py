#!/usr/bin/env python3
"""Import datatables/01-列注释/*.md → db_design/schema/cfg/*.json"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD_DIR = ROOT / "datatables" / "01-列注释"
OUT_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg"
SERVERV_STATIC = ROOT / "serverv" / "static" / "cfg_schema.json"

TITLE_RE = re.compile(r"^#\s+(\S+)\s+[｜|]\s+`?([^`\n]+)`?", re.M)
PURPOSE_RE = re.compile(r"^\-\s+\*\*用途[^*]*\*\*：(.+)$", re.M)
COLUMN_COUNT_RE = re.compile(r"\*\*列数\s+(\d+)\*\*")
TABLE_ID_RE = re.compile(r"表ID\s+`(\d+)`")
DOWNLOAD_RE = re.compile(r"下载序\s+`(\d+)`")
CLASS_RE = re.compile(r"类名\s+`([^`]+)`")

TYPE_RE = re.compile(r"\b(u32|u16|u8|i32|int|float|f32|str|string|enum|bool|字符串)\b", re.I)

NAME_OVERRIDES: dict[str, dict[int, str]] = {
    "ITEM": {0: "item_id"},
    "MSMA_WEAPONSET": {
        0: "weapon_group_id",
        2: "weapon_item_id",
        4: "slot_category",
        5: "weapon_category",
        6: "enabled",
        7: "param_u32_7",
        8: "value_group_a_0",
        10: "value_group_b_0",
        11: "value_group_c_0",
        22: "limit_trigger",
        24: "limit_param_24",
        25: "limit_param_25",
        26: "limit_cap",
        27: "param_u32_27",
        28: "region_gate",
    },
    "MSMA_WEAPON_EQUIPCOMB": {
        0: "comb_rule_id",
        2: "judge_mode",
        3: "weapon_category_a",
        4: "weapon_category_b",
        5: "weapon_category_c",
        6: "param_u32_6",
        8: "param_u32_8",
        10: "region_gate",
    },
    "MSMA_COLORSET": {
        0: "color_group_id",
        2: "param_u32_2",
        3: "name",
        4: "param_u32_4",
        5: "price_a",
        7: "stock_cap_a",
        8: "price_b",
        10: "stock_cap_b",
        11: "param_u32_11",
        14: "price_c",
        16: "param_u32_16",
        17: "param_u32_17",
        18: "stock_cap_c",
        19: "vip_gate",
        20: "param_u32_20",
    },
    "MSMA_BATTLE_DETAIL": {0: "attr_name", 1: "attr_key", 2: "attr_value"},
    "WEAPON_BATTLE_DETAIL": {0: "attr_name", 1: "weapon_id_key", 2: "attr_value"},
}


def normalize_type(raw: str) -> str:
    t = raw.lower()
    if "string" in t or t == "str" or "字符串" in raw:
        return "str"
    if "enum" in t:
        return "enum"
    if "bool" in t:
        return "bool"
    if "float" in t or t == "f32":
        return "float"
    if t in ("int", "i32"):
        return "i32"
    if t == "u16":
        return "u16"
    return "u32"


def slug_name(meaning: str, table: str, idx: int, status: str = "") -> str:
    if status == "gap":
        return f"reserved_u32_{idx}"
    ov = NAME_OVERRIDES.get(table, {})
    if idx in ov:
        return ov[idx]
    t = meaning.strip()
    rules = [
        (r"武器组ID|组合规则ID|配色组ID", "group_id"),
        (r"物品ID|道具ID|武器ID", "item_id" if idx == 2 else "id"),
        (r"主键|索引ID", "id" if idx == 0 else f"key_u32_{idx}"),
        (r"\*\*名称\*\*|名称", "name"),
        (r"\*\*说明\*\*|说明", "description"),
        (r"物品类型", "item_type"),
        (r"属性名", "attr_name"),
        (r"\*\*键\*\*", "attr_key"),
        (r"\*\*值\*\*", "attr_value"),
        (r"槽位类别|槽位", "slot_category"),
        (r"武器类别", "weapon_category"),
        (r"启用开关|启用", "enabled"),
        (r"地区开关", "region_gate"),
        (r"裁定方式", "judge_mode"),
        (r"装备槽位", "equip_slot_type"),
    ]
    for pat, name in rules:
        if re.search(pat, t, re.I):
            if name == "id" and idx != 0:
                return f"{name}_{idx}"
            return name
    if "待定" in t or "未定" in t or "语义未定" in t:
        typ = normalize_type(t)
        return f"pending_{typ}_{idx}"
    m = re.search(r"★+\*\*([^*（(]+)", t)
    if m:
        s = re.sub(r"[^a-zA-Z0-9]+", "_", m.group(1).strip()).strip("_").lower()
        if s:
            return s[:48]
    return f"field_{idx}"


MAX_COL_INDEX = 256


def extract_col_indices(cell: str) -> list[int]:
    cell = cell.strip()
    cols = [int(x) for x in re.findall(r"col(\d+)", cell, re.I) if int(x) <= MAX_COL_INDEX]
    if cols:
        return cols
    nums = [int(x) for x in re.findall(r"`(\d+)`", cell) if int(x) <= MAX_COL_INDEX]
    if nums:
        return nums
    plain = re.match(r"^(\d+)$", cell.strip("` "))
    if plain and int(plain.group(1)) <= MAX_COL_INDEX:
        return [int(plain.group(1))]
    return []


def pick_type(cells: list[str]) -> str:
    for c in cells:
        m = TYPE_RE.search(c)
        if m:
            return normalize_type(m.group(1))
    return "u32"


def pick_meaning(cells: list[str]) -> tuple[str, str]:
    confidence = ""
    if cells and ("确证" in cells[-1] or cells[-1] in ("△", "推断")):
        confidence = cells[-1]
    best = ""
    best_score = -1
    for c in cells[1:]:
        if c.startswith("sub_") or "sub_BBB" in c or c.startswith("`+") or c.startswith("+"):
            continue
        if re.match(r"^[-:\s|]+$", c):
            continue
        score = len(re.findall(r"[\u4e00-\u9fff]", c))
        if "**" in c or "★" in c:
            score += 5
        if score > best_score:
            best_score = score
            best = c
    return best, confidence


def status_from_confidence(meaning: str, confidence: str) -> str:
    if "★确证" in confidence or "确证" in confidence:
        return "confirmed"
    if "推断" in confidence:
        return "partial"
    if "待定" in meaning or "未定" in meaning or "?" in meaning:
        return "pending"
    if "△" in confidence:
        return "partial"
    if meaning:
        return "partial"
    return "pending"


def parse_table_rows(text: str) -> list[dict]:
    parsed: dict[int, dict] = {}
    read_order = 0
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        inner = line.strip()[1:-1] if line.strip().endswith("|") else line.strip()[1:]
        cells = [c.strip() for c in inner.split("|")]
        if len(cells) < 2:
            continue
        if all(re.match(r"^[-:\s]+$", c) for c in cells if c):
            continue
        head = cells[0].lower()
        if (
            "csv 列" in head
            or "读序" in head
            or "列号" in head
            or head == "列"
            or "col0（" in head
            or head.startswith("col0")
            or head == "属性名"
        ):
            continue

        indices = extract_col_indices(cells[0])
        if not indices:
            continue

        col_type = pick_type(cells)
        meaning, confidence = pick_meaning(cells)
        if not meaning:
            continue

        for idx in indices:
            read_order += 1
            if idx in parsed:
                continue
            st = status_from_confidence(meaning, confidence)
            parsed[idx] = {
                "read_order": read_order,
                "csv_index": idx,
                "db_column": f"col{idx}",
                "type": col_type,
                "meaning": meaning,
                "confidence": confidence,
                "status": st,
            }
    return list(parsed.values())


def fill_gaps(rows: list[dict], column_count: int) -> list[dict]:
    if not rows:
        return rows
    max_idx = max(r["csv_index"] for r in rows)
    if column_count and column_count - 1 > max_idx:
        max_idx = column_count - 1
    by_idx = {r["csv_index"]: r for r in rows}
    table = ""  # filled by caller
    filled = []
    for i in range(max_idx + 1):
        if i in by_idx:
            r = by_idx[i]
        else:
            r = {
                "read_order": None,
                "csv_index": i,
                "db_column": f"col{i}",
                "type": "u32",
                "meaning": "CSV 列存在但 IDA 读表未单独取证（默认 0）",
                "confidence": "",
                "status": "gap",
            }
        filled.append(r)
    return filled


def finalize_rows(rows: list[dict], table: str) -> list[dict]:
    out = []
    for r in rows:
        meaning = r["meaning"]
        idx = r["csv_index"]
        out.append(
            {
                **r,
                "name": slug_name(meaning, table, idx, r.get("status", "")),
                "display_name": re.sub(r"\*+", "", meaning).strip()[:120],
            }
        )
    return out


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    title = TITLE_RE.search(text)
    if not title:
        raise ValueError(f"no title: {path}")
    table_name = title.group(1).strip()
    csv_path = title.group(2).strip().strip("()`")

    purpose_m = PURPOSE_RE.search(text)
    col_count_m = COLUMN_COUNT_RE.search(text)
    column_count = int(col_count_m.group(1)) if col_count_m else 0

    disposition = "DOWNLOAD"
    if "本地表" in csv_path or "本地表" in text[:800]:
        disposition = "LOCAL"
    if table_name == "AUTOEXEC" or "autoexec" in csv_path.lower():
        disposition = "SCRIPT"

    raw_rows = parse_table_rows(text)
    if table_name in ("MSMA_BATTLE_DETAIL", "WEAPON_BATTLE_DETAIL") and len(raw_rows) < 3:
        raw_rows = [
            {
                "read_order": 1,
                "csv_index": 0,
                "db_column": "col0",
                "type": "str",
                "meaning": "★**属性名**★（决定进哪张子表；`#` 开头整行跳过）",
                "confidence": "★确证",
                "status": "confirmed",
            },
            {
                "read_order": 2,
                "csv_index": 1,
                "db_column": "col1",
                "type": "str",
                "meaning": "★**键**★（字符串；机体/武器侧查表键）",
                "confidence": "★确证",
                "status": "confirmed",
            },
            {
                "read_order": 3,
                "csv_index": 2,
                "db_column": "col2",
                "type": "u32",
                "meaning": "★**值**★（子表 vtable 决定 int/float/复合）",
                "confidence": "★确证",
                "status": "confirmed",
            },
        ]
        column_count = max(column_count, 3)

    if raw_rows and not column_count:
        column_count = max(r["csv_index"] for r in raw_rows) + 1

    rows = finalize_rows(fill_gaps(raw_rows, column_count), table_name)

    return {
        "id": table_name,
        "title": table_name,
        "csv_path": csv_path,
        "purpose": purpose_m.group(1).strip() if purpose_m else "",
        "table_id": TABLE_ID_RE.search(text).group(1) if TABLE_ID_RE.search(text) else None,
        "download_order": DOWNLOAD_RE.search(text).group(1) if DOWNLOAD_RE.search(text) else None,
        "class_name": CLASS_RE.search(text).group(1) if CLASS_RE.search(text) else None,
        "column_count": column_count,
        "disposition": disposition,
        "source_md": str(path.relative_to(ROOT)).replace("\\", "/"),
        "columns": rows,
        "column_defined": len([r for r in rows if r["status"] != "gap"]),
        "column_pending": len([r for r in rows if r["status"] in ("pending", "gap")]),
        "column_confirmed": len([r for r in rows if r["status"] == "confirmed"]),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tables_dir = OUT_DIR / "tables"
    tables_dir.mkdir(exist_ok=True)

    entries = []
    for md in sorted(MD_DIR.glob("*.md")):
        try:
            tbl = parse_md(md)
        except Exception as e:
            print(f"WARN {md.name}: {e}")
            continue
        (tables_dir / f"{tbl['id']}.json").write_text(
            json.dumps(tbl, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        entries.append(
            {
                "id": tbl["id"],
                "csv_path": tbl["csv_path"],
                "disposition": tbl["disposition"],
                "column_count": tbl["column_count"],
                "column_defined": tbl["column_defined"],
                "column_confirmed": tbl["column_confirmed"],
                "column_pending": tbl["column_pending"],
                "source_md": tbl["source_md"],
            }
        )

    index = {
        "note": "79 表列定案；证据 datatables/01-列注释/；name=订案字段名，db_column=msgo cfg 当前物理列",
        "total": len(entries),
        "download": sum(1 for e in entries if e["disposition"] == "DOWNLOAD"),
        "local": sum(1 for e in entries if e["disposition"] == "LOCAL"),
        "script": sum(1 for e in entries if e["disposition"] == "SCRIPT"),
        "tables": entries,
    }
    (OUT_DIR / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    gm_map = {}
    for tbl_path in sorted(tables_dir.glob("*.json")):
        data = json.loads(tbl_path.read_text(encoding="utf-8"))
        gm_map[data["id"]] = {
            "csv_path": data["csv_path"],
            "purpose": data["purpose"],
            "disposition": data["disposition"],
            "column_count": data["column_count"],
            "columns": {
                c["db_column"]: {
                    "name": c["name"],
                    "display_name": c["display_name"],
                    "type": c["type"],
                    "status": c["status"],
                    "csv_index": c["csv_index"],
                    "meaning": c["meaning"],
                }
                for c in data["columns"]
            },
        }
    SERVERV_STATIC.parent.mkdir(parents=True, exist_ok=True)
    SERVERV_STATIC.write_text(
        json.dumps(gm_map, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    zero = [e["id"] for e in entries if e["column_count"] == 0]
    print(f"imported {len(entries)} tables → {OUT_DIR}")
    print(f"GM schema → {SERVERV_STATIC}")
    if zero:
        print(f"WARN zero columns: {', '.join(zero)}")


if __name__ == "__main__":
    main()
