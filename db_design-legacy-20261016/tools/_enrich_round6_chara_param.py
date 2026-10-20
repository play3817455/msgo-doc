#!/usr/bin/env python3
"""Round 6 CHARA_PARAM cfg enrichment — cap_flag bitmap xrefs + gap cols."""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "db_design" / "schema" / "cfg" / "tables" / "CHARA_PARAM.json"
MD_PATH = ROOT / "datatables" / "01-列注释" / "04-4-CHARA_PARAM.md"
BATCH_PATH = ROOT / "db_design" / "tools" / "enrich_cfg_ida_batch.py"

# csv_index -> field updates
UPDATES_BY_CSV: dict[int, dict] = {
    18: {
        "name": "cap_flag_mission_transform",
        "db_column": "cap_flag_mission_transform",
        "display_name": "任务变形态",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +840 bit4：任务/关卡变形态资格（sub_477C10；sub_67FEB0 备选路径）",
    },
    31: {
        "name": "cap_flag_dual_slot_ui",
        "db_column": "cap_flag_dual_slot_ui",
        "display_name": "双槽切换UI",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +841 bit1：机体选择 UI 双槽切换/EX 武器槽显隐（sub_7E7600；sub_7E4A50；sub_7E2EF0）",
    },
    24: {
        "name": "cap_flag_skip_ex_anim",
        "db_column": "cap_flag_skip_ex_anim",
        "display_name": "跳过EX演出",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +841 bit2：清 0 时跳过 EX 武器演出路径（sub_7E7600 @0x7e7b90）",
    },
    25: {
        "name": "cap_flag_shield_equip",
        "db_column": "cap_flag_shield_equip",
        "display_name": "盾牌装备",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +841 bit3：盾牌装备能力门控（sub_474480 @+841&8；sub_48FF00）",
    },
    28: {
        "name": "cap_flag_tender_mode",
        "db_column": "cap_flag_tender_mode",
        "display_name": "工作舰模式",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +841 bit6：工作舰/母舰 deploy 模式（sub_478DA0 @+841&0x40；sub_507810）",
    },
    30: {
        "name": "cap_flag_disable_special",
        "db_column": "cap_flag_disable_special",
        "display_name": "禁止特殊行动",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +842 bit0：置 1 时禁止 deployable 特殊行动 type 0xA/0xB（sub_4E7FF0；sub_4EF710；sub_8D3CB0）",
    },
    34: {
        "name": "cap_flag_no_awakening",
        "db_column": "cap_flag_no_awakening",
        "display_name": "禁止觉醒爆发",
        "status": "confirmed",
        "confidence": "★确证",
        "meaning": "能力位 +842 bit3：置 1 时禁止觉醒/爆发模式（sub_4EC960 @+842&8）",
    },
}

GAP_INDICES = [
    12, 14, 23, 33, 39, 40, 41, 43, 45, 53, 57, 59, 61, 63, 65, 66, 68, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84,
]

GAP_NOTES: dict[int, str] = {
    23: "读表跳过（col22 cap_flag_b841_0 与 col24 cap_flag_b841_2 之间的 CSV 空隙；默认 0）",
    33: "读表跳过（+842 bit2 无 CSV 列；sub_582390 尾声 `*(_BYTE*)(a3+842)&=~4` 强制清零）",
}

CP_FLAGS_BATCH: dict[int, tuple[str, str, str, str]] = {
    13: ("cap_flag_transform_alt", "变换备用武装", "能力位 +840 bit0：变身形态备用武装（sub_49D280）", "confirmed"),
    15: ("cap_flag_melee_chain", "近战连锁", "能力位 +840 bit1：近战连锁攻击门控（sub_4A7B10）", "confirmed"),
    16: ("cap_flag_b840_2", "能力位 b840.2", "能力位 +840 bit2（无 consumer xref）", "partial"),
    17: ("cap_flag_b840_3", "能力位 b840.3", "能力位 +840 bit3（无 consumer xref）", "partial"),
    18: ("cap_flag_mission_transform", "任务变形态", "能力位 +840 bit4：任务/关卡变形态资格（sub_477C10；sub_67FEB0）", "confirmed"),
    19: ("cap_flag_b840_5", "能力位 b840.5", "能力位 +840 bit5（无 consumer xref）", "partial"),
    20: ("cap_flag_b840_6", "能力位 b840.6", "能力位 +840 bit6（无 consumer xref）", "partial"),
    21: ("cap_flag_b840_7", "能力位 b840.7", "能力位 +840 bit7（无 consumer xref）", "partial"),
    22: ("cap_flag_b841_0", "能力位 b841.0", "能力位 +841 bit0（无 consumer xref）", "partial"),
    31: ("cap_flag_dual_slot_ui", "双槽切换UI", "能力位 +841 bit1：机体选择 UI 双槽切换（sub_7E7600；sub_7E4A50）", "confirmed"),
    24: ("cap_flag_skip_ex_anim", "跳过EX演出", "能力位 +841 bit2：清 0 时跳过 EX 武器演出（sub_7E7600）", "confirmed"),
    25: ("cap_flag_shield_equip", "盾牌装备", "能力位 +841 bit3：盾牌装备能力（sub_474480；sub_48FF00）", "confirmed"),
    26: ("cap_flag_b841_4", "能力位 b841.4", "能力位 +841 bit4（无 consumer xref）", "partial"),
    27: ("cap_flag_b841_5", "能力位 b841.5", "能力位 +841 bit5（无 consumer xref）", "partial"),
    28: ("cap_flag_tender_mode", "工作舰模式", "能力位 +841 bit6：工作舰/母舰 deploy（sub_478DA0；sub_507810）", "confirmed"),
    29: ("cap_flag_b841_7", "能力位 b841.7", "能力位 +841 bit7（无 consumer xref）", "partial"),
    30: ("cap_flag_disable_special", "禁止特殊行动", "能力位 +842 bit0：禁止 deployable 特殊行动（sub_4E7FF0；sub_4EF710）", "confirmed"),
    32: ("cap_flag_dual_mode", "双模式标志", "能力位 +842 bit1：双模式/双形态标志（sub_6218F0→runtime+107）", "confirmed"),
    34: ("cap_flag_no_awakening", "禁止觉醒爆发", "能力位 +842 bit3：禁止觉醒/爆发（sub_4EC960）", "confirmed"),
}

CAP_FLAG_BIT_MAP = """
| 内存偏移 | bit | CSV col | db_column | 能力名 | consumer | status |
|---|---:|---:|---|---|---|---|
| +840 | 0 | 13 | cap_flag_transform_alt | 变换备用武装 | sub_49D280 | confirmed |
| +840 | 1 | 15 | cap_flag_melee_chain | 近战连锁 | sub_4A7B10 | confirmed |
| +840 | 2 | 16 | cap_flag_b840_2 | （未知） | — | partial |
| +840 | 3 | 17 | cap_flag_b840_3 | （未知） | — | partial |
| +840 | 4 | 18 | cap_flag_mission_transform | 任务变形态 | sub_477C10, sub_67FEB0 | confirmed |
| +840 | 5 | 19 | cap_flag_b840_5 | （未知） | — | partial |
| +840 | 6 | 20 | cap_flag_b840_6 | （未知） | — | partial |
| +840 | 7 | 21 | cap_flag_b840_7 | （未知） | — | partial |
| +841 | 0 | 22 | cap_flag_b841_0 | （未知） | — | partial |
| +841 | 1 | 31 | cap_flag_dual_slot_ui | 双槽切换UI | sub_7E7600, sub_7E4A50 | confirmed |
| +841 | 2 | 24 | cap_flag_skip_ex_anim | 跳过EX演出 | sub_7E7600 | confirmed |
| +841 | 3 | 25 | cap_flag_shield_equip | 盾牌装备 | sub_474480, sub_48FF00 | confirmed |
| +841 | 4 | 26 | cap_flag_b841_4 | （未知） | — | partial |
| +841 | 5 | 27 | cap_flag_b841_5 | （未知） | — | partial |
| +841 | 6 | 28 | cap_flag_tender_mode | 工作舰模式 | sub_478DA0, sub_507810 | confirmed |
| +841 | 7 | 29 | cap_flag_b841_7 | （未知） | — | partial |
| +842 | 0 | 30 | cap_flag_disable_special | 禁止特殊行动 | sub_4E7FF0, sub_4EF710 | confirmed |
| +842 | 1 | 32 | cap_flag_dual_mode | 双模式标志 | sub_6218F0 | confirmed |
| +842 | 2 | 33(gap) | — | （强制清零） | sub_582390 epilogue | gap |
| +842 | 3 | 34 | cap_flag_no_awakening | 禁止觉醒爆发 | sub_4EC960 | confirmed |
| +842 | 4–7 | — | — | （未知） | — | — |
"""


def recount(data: dict) -> None:
    cols = data.get("columns", [])
    data["column_defined"] = len(cols)
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_pending"] = sum(1 for c in cols if c.get("status") == "pending")
    data["column_gap"] = sum(1 for c in cols if c.get("status") == "gap")
    data["column_count"] = sum(1 for c in cols if c.get("read_order") is not None)


def patch_gap(col: dict) -> None:
    idx = col["csv_index"]
    note = GAP_NOTES.get(idx, f"sub_582390 读表跳过（CSV col{idx} 无 read_order；默认 0）")
    col["name"] = f"reserved_u32_{idx}"
    col["db_column"] = f"reserved_u32_{idx}"
    col["display_name"] = f"预留列{idx}"
    col["status"] = "gap"
    col["meaning"] = note


def sync_md(md_path: Path, data: dict) -> None:
    if not md_path.is_file():
        return
    col_by_csv = {c["csv_index"]: c for c in data.get("columns", [])}
    out: list[str] = []
    in_table = False
    inserted_r6 = False
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## 1. 逐列") and not inserted_r6:
            out.append("")
            out.append("## 1.1 Round 6 IDA 能力位定案（2026-09-21）")
            out.append("")
            out.append("> 读表 `sub_582390`；能力位散在 +840/+841/+842 三字节位图。")
            out.append(CAP_FLAG_BIT_MAP.strip())
            out.append("")
            out.append("**confirmed 40→47**（+7 能力位）；partial 24→17；gap 28 不变。")
            out.append("")
            inserted_r6 = True
        if line.startswith("| 读序 |"):
            in_table = True
        if in_table and line.startswith("|") and "`" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                m = re.search(r"`(\d+)`", parts[2])
                if m:
                    col = col_by_csv.get(int(m.group(1)))
                    if col:
                        disp = col.get("display_name") or col.get("name", "")
                        meaning = col.get("meaning", disp)
                        if col.get("status") == "confirmed":
                            cell = f"★**{disp}** — {meaning[:160]}"
                        elif col.get("status") == "gap":
                            cell = f"⛔**{disp}** — {meaning[:120]}"
                        else:
                            cell = f"{disp} — {meaning[:120]}"
                        parts[4] = cell
                        line = "| " + " | ".join(parts[1:4] + [parts[4]]) + " |"
        out.append(line)
    # Append gap col appendix if missing
    if "## 2. GAP 列清单" not in "\n".join(out):
        out.append("")
        out.append("## 2. GAP 列清单（sub_582390 未读取）")
        out.append("")
        out.append("| CSV col | db_column | 说明 |")
        out.append("|---|---|---|")
        for idx in GAP_INDICES:
            col = col_by_csv.get(idx, {})
            out.append(f"| `{idx}` | `{col.get('db_column', f'reserved_u32_{idx}')}` | {col.get('meaning', '')} |")
    md_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def patch_batch_cp_flags() -> None:
    if not BATCH_PATH.is_file():
        return
    text = BATCH_PATH.read_text(encoding="utf-8")
    start = text.find("CP_FLAGS = {")
    end = text.find("\nCP_STRINGS", start)
    if start < 0 or end < 0:
        return
    lines = ["CP_FLAGS = {"]
    for idx in sorted(CP_FLAGS_BATCH.keys()):
        name, disp, meaning, status = CP_FLAGS_BATCH[idx]
        lines.append(f'    {idx}: ("{name}", "{disp}", "{meaning}", "{status}"),')
    lines.append("}")
    text = text[:start] + "\n".join(lines) + text[end:]
    BATCH_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    before_conf = sum(1 for c in data["columns"] if c.get("status") == "confirmed")
    before_partial = sum(1 for c in data["columns"] if c.get("status") == "partial")
    before_gap = sum(1 for c in data["columns"] if c.get("status") == "gap")

    for col in data["columns"]:
        idx = col["csv_index"]
        if idx in UPDATES_BY_CSV:
            col.update(deepcopy(UPDATES_BY_CSV[idx]))
        if col.get("status") == "gap" or idx in GAP_INDICES:
            patch_gap(col)

    recount(data)
    JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sync_md(MD_PATH, data)
    patch_batch_cp_flags()

    print(f"confirmed: {before_conf} -> {data['column_confirmed']}")
    print(f"partial:   {before_partial} -> {data['column_partial']}")
    print(f"gap:       {before_gap} -> {data['column_gap']}")
    print("\n--- cap_flag bit map ---")
    print(CAP_FLAG_BIT_MAP.strip())


if __name__ == "__main__":
    main()
