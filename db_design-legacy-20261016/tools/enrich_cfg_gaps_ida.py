#!/usr/bin/env python3
"""IDA-verified gap column audit: fix false gaps, enrich true gaps, enum '-' labels."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "schema" / "cfg" / "tables"
MANUAL = ROOT / "schema" / "cfg" / "enum_manual_zh.json"

# CHARA_PARAM / MSMA_RENTAL share sub_582390
CHARA_GAP_NOTES: dict[int, str] = {
    12: "能力位 col12 预留（读表跳至 col13 写 +840 bit0；默认 0）",
    14: "能力位 col14 预留（读表跳至 col15 写 +840 bit1；默认 0）",
    23: "能力位 col23 预留（col22 与 col24 之间无位图映射；默认 0）",
    33: "能力位 +842 bit2 无 CSV 列（sub_582390 尾声 `&=~4` 强制清零）",
    39: "数值列 col39 预留（读表跳至 col42；默认 0）",
    40: "数值列 col40 预留（读表跳至 col42；默认 0）",
    41: "数值列 col41 预留（读表跳至 col42；默认 0）",
    43: "字符串组 col43 预留（读表跳至 col44；默认 0）",
    45: "字符串组 col45 预留（读表跳至 col47；默认 0）",
    53: "数值列 col53 预留（读表跳至 col55；默认 0）",
    57: "数值列 col57 预留（读表跳至 col58；默认 0）",
    59: "数值列 col59 预留（读表跳至 col58/90；默认 0）",
    61: "数值列 col61 预留（读表跳至 col58；默认 0）",
    63: "数值列 col63 预留（读表跳至 col58；默认 0）",
    65: "数值列 col65 预留（读表跳至 col58；默认 0）",
    66: "数值列 col66 预留（读表跳至 col58；默认 0）",
    68: "数值列 col68 预留（读表跳至 col58；默认 0）",
    70: "数值列 col70 预留（读表跳至 col58；默认 0）",
    72: "数值列 col72 预留（读表跳至 col58；默认 0）",
    74: "数值列 col74 预留（读表跳至 col58；默认 0）",
    75: "数值列 col75 预留（读表跳至 col58；默认 0）",
    76: "数值列 col76 预留（读表跳至 col58；默认 0）",
    77: "数值列 col77 预留（读表跳至 col58；默认 0）",
    78: "数值列 col78 预留（读表跳至 col58；默认 0）",
    80: "数值列 col80 预留（读表跳至 col58；默认 0）",
    81: "数值列 col81 预留（读表跳至 col58；默认 0）",
    82: "数值列 col82 预留（读表跳至 col58；默认 0）",
    84: "数值列 col84 预留（读表跳至 col58；默认 0）",
}

CHALLENGE_GAP_NOTES: dict[int, str] = {
    2: "UI 分组后预留（读表跳至 col4 写 stat_type；默认 0）",
    3: "stat_type 前预留（读表跳至 col4；默认 0）",
    6: "目标值后预留（读表跳至下一奖励段；默认 0）",
    7: "目标值后预留（读表跳至下一奖励段；默认 0）",
    8: "排序/档位前预留（读表跳至下一有效列；默认 0）",
    9: "奖励段前预留（读表跳至 col11/col12；默认 0）",
    10: "CLAN 专用：奖励 GP 前预留（读表跳至 col11；默认 0）",
    13: "奖励数量前预留（读表跳至 col14；默认 0）",
    16: "bonus 前预留（读表跳至 col17；默认 0）",
}

MSMA_MODULE_GAP = (
    "奇数列预留（sub_57EA90 以步长 2 读 col2/4/6…；本列 CSV 存在但不读，默认 0）"
)

ENUM_DASH_ZH = "-（无效/未匹配；sub_585FD0 空串或未知名 ⇒ 27）"


def recount(data: dict) -> None:
    cols = data.get("columns", [])
    data["column_defined"] = len(cols)
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_pending"] = sum(1 for c in cols if c.get("status") == "pending")
    data["column_gap"] = sum(1 for c in cols if c.get("status") == "gap")
    data["column_count"] = sum(1 for c in cols if c.get("read_order") is not None)


def gap_meaning(table: str, reader: str, csv_index: int) -> str:
    if table in ("CHARA_PARAM", "MSMA_RENTAL", "CHARA_MODEL"):
        note = CHARA_GAP_NOTES.get(csv_index)
        if note:
            return note
        return f"CSV col{csv_index} 预留（{reader or '读表'} 跳过；默认 0）"
    if table in (
        "CLAN_CHALLENGE",
        "TROOP_CHALLENGE",
        "NETCAFE_CHALLENGE",
        "DAILY_RECORD",
    ):
        note = CHALLENGE_GAP_NOTES.get(csv_index)
        if note:
            return note
        return f"CSV col{csv_index} 预留（{reader} 跳过；默认 0）"
    if table == "MSMA_MODULE":
        return MSMA_MODULE_GAP
    if table == "MSMA_WEAPONSET":
        notes = {
            1: "col1 预留（读表跳至 col2 weapon_item_id；默认 0）",
            3: "col3 预留（读表跳至 col4 slot_category；默认 0）",
            17: "成本组与上限段间预留（读表跳至 col19 limit_trigger；默认 0）",
            18: "成本组与上限段间预留（读表跳至 col19 limit_trigger；默认 0）",
            20: "上限段内预留（读表跳至 col21 limit_param_a；默认 0）",
            26: "尾部预留（读表止于 col25 region_gate；默认 0）",
            27: "尾部预留（读表止于 col25 region_gate；默认 0）",
            28: "尾部预留（读表止于 col25 region_gate；默认 0）",
        }
        return notes.get(csv_index, f"CSV col{csv_index} 预留（sub_587160 跳过；默认 0）")
    if table == "PLAYER_NAVI":
        if csv_index == 12:
            return "col12 预留（sub_58C7C0 跳至 col13 dialog_style；默认 0）"
    if table == "MISSION_SAFETY_AREA" and csv_index == 0:
        return "col0 预留（sub_587780 从 col1 起读 area_id；默认 0）"
    if table == "COMMANDER_SUPPORT":
        return f"支援表 col{csv_index} 预留（读表跳过；默认 0）"
    return f"CSV col{csv_index} 预留（{reader or '读表'} 跳过；默认 0）"


def patch_gap_col(col: dict, table: str, reader: str) -> None:
    idx = col["csv_index"]
    col["status"] = "gap"
    col["read_order"] = None
    col["memory_offset"] = None
    col["asm_va"] = None
    col["name"] = f"reserved_u32_{idx}"
    col["db_column"] = f"reserved_u32_{idx}"
    meaning = gap_meaning(table, reader, idx)
    col["meaning"] = meaning
    col["display_name"] = f"预留列 col{idx}"


def rebuild_msma_weaponset(data: dict) -> None:
    """Fix csv_index drift vs sub_587160 (cost loop + limit tail)."""
    reader = "sub_587160"
    head = deepcopy([c for c in data["columns"] if c["csv_index"] <= 7])
    for col in head:
        for ev in col.get("enum_values") or []:
            if ev.get("name") == "-":
                ev["label_zh"] = ENUM_DASH_ZH

    def confirmed(
        ro: int,
        csv: int,
        name: str,
        typ: str,
        offset: int | None,
        va: str,
        meaning: str,
        **extra,
    ) -> dict:
        col = {
            "read_order": ro,
            "csv_index": csv,
            "db_column": name,
            "type": typ,
            "memory_offset": offset,
            "asm_reader": reader,
            "asm_va": va,
            "meaning": meaning,
            "confidence": extra.get("confidence", "★确证"),
            "status": "confirmed",
            "name": name,
            "display_name": extra.get("display_name", meaning.split("（")[0]),
        }
        col.update({k: v for k, v in extra.items() if k not in col})
        return col

    def gap(csv: int) -> dict:
        col = {"csv_index": csv, "type": "u32", "asm_reader": reader}
        patch_gap_col(col, "MSMA_WEAPONSET", reader)
        return col

    slot = "col8–16 三组循环 @0x587249"
    tail = [
        confirmed(
            7,
            8,
            "cost_a_slot0",
            "u32",
            28,
            "0x587252",
            f"成本组 A 槽0（csv8→+28；{slot}）",
        ),
        confirmed(
            8,
            9,
            "cost_a_slot1",
            "u32",
            32,
            "0x587260",
            f"成本组 A 槽1（csv9→+32；{slot}）",
        ),
        confirmed(
            9,
            10,
            "cost_a_slot2",
            "u32",
            36,
            "0x587276",
            f"成本组 A 槽2（csv10→+36；{slot}）",
        ),
        confirmed(
            10,
            11,
            "cost_b_slot0",
            "u32",
            40,
            "0x587252",
            f"成本组 B 槽0（csv11→+40；{slot}）",
        ),
        confirmed(
            11,
            12,
            "cost_b_slot1",
            "u32",
            44,
            "0x587260",
            f"成本组 B 槽1（csv12→+44；{slot}）",
        ),
        confirmed(
            12,
            13,
            "cost_b_slot2",
            "u32",
            48,
            "0x587260",
            f"成本组 B 槽2（csv13→+48；{slot}）",
        ),
        confirmed(
            13,
            14,
            "cost_c_slot0",
            "u32",
            52,
            "0x587252",
            f"成本组 C 槽0（csv14→+52；{slot}）",
        ),
        confirmed(
            14,
            15,
            "cost_c_slot1",
            "u32",
            56,
            "0x587260",
            f"成本组 C 槽1（csv15→+56；{slot}）",
        ),
        confirmed(
            15,
            16,
            "cost_c_slot2",
            "u32",
            60,
            "0x587276",
            f"成本组 C 槽2（csv16→+60；{slot}）",
        ),
        gap(17),
        gap(18),
        confirmed(
            16,
            19,
            "limit_trigger",
            "u32",
            68,
            "0x587297",
            "上限触发（csv19→+68）；>0 且 col21/22/23 全≤0 时 col23 强制 9999",
        ),
        gap(20),
        confirmed(
            17,
            21,
            "limit_param_a",
            "u32",
            72,
            "0x5872aa",
            "上限中间参数 A（csv21→+72；参与 9999 联动 @0x5872f4）",
        ),
        confirmed(
            18,
            22,
            "limit_param_b",
            "u32",
            76,
            "0x5872bd",
            "上限中间参数 B（csv22→+76；参与 9999 联动 @0x5872f4）",
        ),
        confirmed(
            19,
            23,
            "limit_cap",
            "u32",
            80,
            "0x5872ce",
            "数量上限（csv23→+80）；col19>0 且 col21/22/23 全≤0 ⇒ 9999",
        ),
        confirmed(
            20,
            24,
            "extra_param",
            "u32",
            84,
            "0x587315",
            "武器生成附加参（csv24→+84；sub_622A20 传入 sub_60D460）",
        ),
        confirmed(
            21,
            25,
            "region_gate",
            "str",
            None,
            "0x58731c",
            "地区开关（csv25）：JAPAN 整行丢弃；CHINA/其他保留",
        ),
        gap(26),
        gap(27),
        gap(28),
    ]
    data["columns"] = head + tail
    recount(data)


def enrich_gaps_in_table(path: Path) -> tuple[int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    table = data.get("id", path.stem)
    reader = data.get("asm_reader", "")

    if table == "MSMA_WEAPONSET":
        rebuild_msma_weaponset(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return data["column_gap"], 4

    fixed = 0
    enum_patched = 0
    for col in data.get("columns", []):
        for ev in col.get("enum_values") or []:
            if ev.get("name") == "-" and ev.get("label_zh") != ENUM_DASH_ZH:
                ev["label_zh"] = ENUM_DASH_ZH
                enum_patched += 1
        if col.get("status") != "gap":
            continue
        old = col.get("meaning", "")
        patch_gap_col(col, table, reader)
        if col["meaning"] != old:
            fixed += 1

    recount(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return data["column_gap"], fixed + enum_patched


def patch_enum_manual() -> None:
    manual = json.loads(MANUAL.read_text(encoding="utf-8"))
    if manual.get("-") != ENUM_DASH_ZH:
        manual["-"] = ENUM_DASH_ZH
        MANUAL.write_text(json.dumps(manual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    patch_enum_manual()
    total_gaps = 0
    for path in sorted(TABLES.glob("*.json")):
        gaps, changed = enrich_gaps_in_table(path)
        total_gaps += gaps
        if changed:
            print(f"{path.stem}: gap={gaps} patched={changed}")
    print(f"total gap columns remaining: {total_gaps}")


if __name__ == "__main__":
    main()
