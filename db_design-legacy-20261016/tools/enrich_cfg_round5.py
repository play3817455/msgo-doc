#!/usr/bin/env python3
"""Round 5 cfg enrichment: challenge csv_index realignment + partial table completion."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = ROOT / "db_design" / "schema" / "cfg" / "tables"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

STAT_46_MEANING = (
    "战绩统计项（enum sub_592DB0，46 项：VERSUS/WIN/KILL/SCORE_* 等；"
    "与客户端「战斗记录」页签及 badge_config リボンタイプ 同源）"
)
STAT_46_CLAN = (
    "部队挑战统计项（enum sub_571D00，46 项 + PERFECT；"
    "与 DAILY_RECORD 同一套战绩体系，换到部队维度）"
)
STAT_46_TROOP = STAT_46_MEANING.replace("战斗记录", "势力挑战")
STAT_46_NETCAFE = (
    "网吧挑战统计项（enum sub_5874A0，46 项 + NETCAFE；"
    "与 DAILY_RECORD 同一套战绩体系）"
)

BADGE_TIER = [
    {"name": "BRONZE", "value": 0},
    {"name": "SILVER", "value": 1},
    {"name": "GOLD", "value": 2},
]

GAP_MEANING = "CSV 列存在但 IDA 读表未单独取证（默认 0）"


def load_enums() -> dict:
    return json.loads(ENUMS_JSON.read_text(encoding="utf-8"))


def enum_values(enums: dict, fn: str) -> list[dict]:
    r = enums.get(fn)
    if not r:
        return []
    if r.get("shape") == "table" and r.get("table"):
        return [{"name": n, "value": v} for n, v in r["table"]]
    lits, consts = r.get("lits") or [], r.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    return []


def gap_col(csv_index: int) -> dict:
    return {
        "read_order": None,
        "csv_index": csv_index,
        "db_column": f"col{csv_index}",
        "type": "u32",
        "meaning": GAP_MEANING,
        "confidence": "",
        "status": "gap",
        "name": f"reserved_u32_{csv_index}",
        "display_name": f"保留列 col{csv_index}",
    }


def mapped_col(
    read_order: int,
    csv_index: int,
    name: str,
    typ: str,
    meaning: str,
    *,
    memory_offset: int | None = None,
    asm_va: str | None = None,
    asm_reader: str | None = None,
    enum_converter: str | None = None,
    enum_values_list: list[dict] | None = None,
    confidence: str = "★确证",
) -> dict:
    col = {
        "read_order": read_order,
        "csv_index": csv_index,
        "db_column": name,
        "type": typ,
        "meaning": meaning,
        "confidence": confidence,
        "status": "confirmed",
        "name": name,
        "display_name": meaning.split("（")[0].split("（")[0][:24],
    }
    if memory_offset is not None:
        col["memory_offset"] = memory_offset
    if asm_va:
        col["asm_va"] = asm_va
    if asm_reader:
        col["asm_reader"] = asm_reader
    if enum_converter:
        col["enum_converter"] = enum_converter
        col["enum_doc"] = ENUM_DOC
        if enum_values_list:
            col["enum_values"] = enum_values_list
    return col


def build_columns(max_csv: int, mapped: list[dict], gaps: set[int]) -> list[dict]:
    by_idx = {c["csv_index"]: c for c in mapped}
    out = []
    for i in range(max_csv + 1):
        if i in by_idx:
            out.append(by_idx[i])
        elif i in gaps:
            out.append(gap_col(i))
    return out


def recount(data: dict) -> None:
    cols = data.get("columns", [])
    data["column_defined"] = len(cols)
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_pending"] = sum(1 for c in cols if c.get("status") == "pending")
    data["column_gap"] = sum(1 for c in cols if c.get("status") == "gap")
    data["column_count"] = sum(1 for c in cols if c.get("read_order") is not None)


def rebuild_clan_challenge(enums: dict) -> dict:
    ev = enum_values(enums, "sub_571D00")
    mapped = [
        mapped_col(1, 0, "challenge_id", "u32", "部队挑战 ID（主键）", asm_va="0x571dcd", asm_reader="sub_571DA0", memory_offset=0),
        mapped_col(2, 1, "display_group", "u8", "UI 显示分组（u8 col1）", asm_va="0x571ddb", asm_reader="sub_571DA0", memory_offset=4, confidence="○ASM确证"),
        mapped_col(3, 4, "stat_type", "enum", STAT_46_CLAN, asm_va="0x571df8", asm_reader="sub_571DA0", memory_offset=8, enum_converter="sub_571D00", enum_values_list=ev),
        mapped_col(4, 5, "target_value", "u32", "部队累计目标值（u32 col5 → +12）", asm_va="0x571e2a", asm_reader="sub_571DA0", memory_offset=12, confidence="○ASM确证"),
        mapped_col(5, 11, "reward_gp", "u32", "达成奖励 GP（u32 col11 → +16）", asm_va="0x571e35", asm_reader="sub_571DA0", memory_offset=16, confidence="○ASM确证"),
        mapped_col(6, 12, "reward_item_id", "u32", "达成奖励物品 ID（u32 col12 → +20）", asm_va="0x571e40", asm_reader="sub_571DA0", memory_offset=20, confidence="○ASM确证"),
        mapped_col(7, 14, "reward_qty", "u32", "奖励物品数量（u32 col14 → +24）", asm_va="0x571e4b", asm_reader="sub_571DA0", memory_offset=24, confidence="○ASM确证"),
        mapped_col(8, 15, "bonus_point", "u32", "附加点数/积分（u32 col15 → +28）", asm_va="0x571e56", asm_reader="sub_571DA0", memory_offset=28, confidence="○ASM确证"),
        mapped_col(9, 17, "bonus_param", "u32", "附加奖励参数（u32 col17 → +32）", asm_va="0x571e6a", asm_reader="sub_571DA0", memory_offset=32, confidence="○ASM确证"),
        mapped_col(10, 18, "challenge_title", "str", "挑战标题（wstring col18 → +36）", asm_va="0x571e6d", asm_reader="sub_571DA0", memory_offset=36),
        mapped_col(11, 19, "challenge_desc", "str", "挑战说明（wstring col19 → +64）", asm_va="0x571ead", asm_reader="sub_571DA0", memory_offset=64),
    ]
    gaps = {2, 3, 6, 7, 8, 9, 10, 13, 16}
    data = json.loads((TABLES_DIR / "CLAN_CHALLENGE.json").read_text(encoding="utf-8"))
    data["columns"] = build_columns(19, mapped, gaps)
    recount(data)
    return data


def rebuild_troop_challenge(enums: dict) -> dict:
    ev = enum_values(enums, "sub_592DB0")
    mapped = [
        mapped_col(1, 0, "challenge_id", "u32", "势力挑战 ID（主键；联邦/吉翁阵营挑战）", asm_va="0x592e7d", asm_reader="sub_592E50", memory_offset=0),
        mapped_col(2, 1, "troop_faction", "u8", "目标势力/阵营（u8 col1）", asm_va="0x592e8b", asm_reader="sub_592E50", memory_offset=4, confidence="○ASM确证"),
        mapped_col(3, 4, "stat_type", "enum", STAT_46_TROOP, asm_va="0x592ea8", asm_reader="sub_592E50", memory_offset=8, enum_converter="sub_592DB0", enum_values_list=ev),
        mapped_col(4, 5, "target_value", "u32", "势力累计目标值（u32 col5 → +12）", asm_va="0x592eda", asm_reader="sub_592E50", memory_offset=12, confidence="○ASM确证"),
        mapped_col(5, 8, "display_order", "u32", "列表排序权重（u32 col8 → +16）", asm_va="0x592ee5", asm_reader="sub_592E50", memory_offset=16, confidence="○ASM确证"),
        mapped_col(6, 10, "tier_param", "u32", "挑战档位参数（u32 col10 → +20；非 enum）", asm_va="0x592ef0", asm_reader="sub_592E50", memory_offset=20, confidence="○ASM确证"),
        mapped_col(7, 11, "reward_gp", "u32", "达成奖励 GP（u32 col11 → +24）", asm_va="0x592efb", asm_reader="sub_592E50", memory_offset=24, confidence="○ASM确证"),
        mapped_col(8, 12, "reward_item_id", "u32", "达成奖励物品 ID（u32 col12 → +28）", asm_va="0x592f06", asm_reader="sub_592E50", memory_offset=28, confidence="○ASM确证"),
        mapped_col(9, 14, "reward_qty", "u32", "奖励物品数量（u32 col14 → +32）", asm_va="0x592f11", asm_reader="sub_592E50", memory_offset=32, confidence="○ASM确证"),
        mapped_col(10, 15, "bonus_point", "u32", "附加点数/积分（u32 col15 → +36）", asm_va="0x592f1c", asm_reader="sub_592E50", memory_offset=36, confidence="○ASM确证"),
        mapped_col(11, 17, "bonus_param", "u32", "附加奖励参数（u32 col17 → +40）", asm_va="0x592f30", asm_reader="sub_592E50", memory_offset=40, confidence="○ASM确证"),
        mapped_col(12, 18, "challenge_title", "str", "挑战标题（wstring col18 → +44）", asm_va="0x592f33", asm_reader="sub_592E50", memory_offset=44),
        mapped_col(13, 19, "challenge_desc", "str", "挑战说明（wstring col19 → +72）", asm_va="0x592f72", asm_reader="sub_592E50", memory_offset=72),
    ]
    gaps = {2, 3, 6, 7, 9, 13, 16}
    data = json.loads((TABLES_DIR / "TROOP_CHALLENGE.json").read_text(encoding="utf-8"))
    data["columns"] = build_columns(19, mapped, gaps)
    recount(data)
    return data


def rebuild_netcafe_challenge(enums: dict) -> dict:
    ev = enum_values(enums, "sub_5874A0")
    mapped = [
        mapped_col(1, 0, "challenge_id", "u32", "网吧挑战 ID（主键）", asm_va="0x58760d", asm_reader="sub_5875E0", memory_offset=0),
        mapped_col(2, 1, "display_group", "u8", "UI 显示分组（u8 col1）", asm_va="0x58761b", asm_reader="sub_5875E0", memory_offset=4, confidence="○ASM确证"),
        mapped_col(3, 4, "stat_type", "enum", STAT_46_NETCAFE, asm_va="0x587638", asm_reader="sub_5875E0", memory_offset=8, enum_converter="sub_5874A0", enum_values_list=ev),
        mapped_col(4, 5, "target_value", "u32", "网吧累计目标值（u32 col5 → +12）", asm_va="0x58766a", asm_reader="sub_5875E0", memory_offset=12, confidence="○ASM确证"),
        mapped_col(5, 8, "display_order", "u32", "列表排序权重（u32 col8 → +16）", asm_va="0x58767a", asm_reader="sub_5875E0", memory_offset=16, confidence="○ASM确证"),
        mapped_col(6, 10, "badge_tier_ref", "enum", "绶带等级参照（enum col10 sub_587540：BRONZE/SILVER/GOLD）", asm_va="0x58768b", asm_reader="sub_5875E0", memory_offset=20, enum_converter="sub_587540", enum_values_list=BADGE_TIER),
        mapped_col(7, 11, "reward_gp", "u32", "达成奖励 GP（u32 col11 → +24）", asm_va="0x5876bd", asm_reader="sub_5875E0", memory_offset=24, confidence="○ASM确证"),
        mapped_col(8, 12, "reward_item_id", "u32", "达成奖励物品 ID（u32 col12 → +28）", asm_va="0x5876c8", asm_reader="sub_5875E0", memory_offset=28, confidence="○ASM确证"),
        mapped_col(9, 14, "reward_qty", "u32", "奖励物品数量（u32 col14 → +32）", asm_va="0x5876d3", asm_reader="sub_5875E0", memory_offset=32, confidence="○ASM确证"),
        mapped_col(10, 15, "bonus_point", "u32", "附加点数/积分（u32 col15 → +36）", asm_va="0x5876de", asm_reader="sub_5875E0", memory_offset=36, confidence="○ASM确证"),
        mapped_col(11, 17, "bonus_param", "u32", "附加奖励参数（u32 col17 → +40）", asm_va="0x5876f2", asm_reader="sub_5875E0", memory_offset=40, confidence="○ASM确证"),
        mapped_col(12, 18, "challenge_title", "str", "挑战标题（wstring col18 → +44）", asm_va="0x5876f5", asm_reader="sub_5875E0", memory_offset=44),
        mapped_col(13, 19, "challenge_desc", "str", "挑战说明（wstring col19 → +72）", asm_va="0x587734", asm_reader="sub_5875E0", memory_offset=72),
    ]
    gaps = {2, 3, 6, 7, 9, 13, 16}
    data = json.loads((TABLES_DIR / "NETCAFE_CHALLENGE.json").read_text(encoding="utf-8"))
    data["columns"] = build_columns(19, mapped, gaps)
    recount(data)
    return data


def confirm_asm_mapped(data: dict) -> int:
    n = 0
    for col in data.get("columns", []):
        if col.get("status") == "gap" or col.get("read_order") is None:
            continue
        if col.get("asm_va") or col.get("asm_reader"):
            if col.get("status") != "confirmed":
                col["status"] = "confirmed"
                n += 1
            if not col.get("confidence"):
                col["confidence"] = "○ASM确证"
    recount(data)
    return n


def fix_lvup_favms(data: dict) -> dict:
    gaps = {2, 5, 8}
    for col in data["columns"]:
        idx = col["csv_index"]
        if idx in gaps:
            col.update(gap_col(idx))
        elif col.get("read_order") is not None and col.get("asm_va"):
            col["status"] = "confirmed"
            if not col.get("confidence") or col["confidence"] == "△":
                col["confidence"] = "○ASM确证"
    # ensure gap cols exist
    existing = {c["csv_index"] for c in data["columns"]}
    for g in gaps - existing:
        data["columns"].append(gap_col(g))
    data["columns"].sort(key=lambda c: c["csv_index"])
    recount(data)
    return data


def fix_action_module_info(data: dict) -> dict:
    patches = {
        17: {
            "name": "attach_resource_a",
            "db_column": "attach_resource_a",
            "type": "str",
            "meaning": "附加资源路径 A（wstring col17 → +240）",
            "display_name": "附加资源 A",
            "memory_offset": 240,
        },
        18: {
            "name": "attach_resource_b",
            "db_column": "attach_resource_b",
            "type": "str",
            "meaning": "附加资源路径 B（wstring col18 → +268）",
            "display_name": "附加资源 B",
            "memory_offset": 268,
        },
        19: {
            "name": "param_u32_19",
            "db_column": "param_u32_19",
            "type": "u32",
            "meaning": "扩展整型参数（u32 col19 → +296）",
            "display_name": "扩展参数",
            "memory_offset": 296,
        },
    }
    by_idx = {c["csv_index"]: c for c in data["columns"]}
    for idx, patch in patches.items():
        if idx in by_idx:
            by_idx[idx].update(patch)
            by_idx[idx]["status"] = "confirmed"
            by_idx[idx]["confidence"] = "○ASM确证"
            by_idx[idx].pop("enum_converter", None)
    # add missing cols 20, 21 from ASM
    if 20 not in by_idx:
        data["columns"].append(mapped_col(
            21, 20, "overlay_label", "str", "覆盖显示标签（wstring col20 → +40）",
            asm_va="0x56df67", asm_reader="sub_56DCD0", memory_offset=40,
        ))
    if 21 not in by_idx:
        data["columns"].append(mapped_col(
            22, 21, "overlay_desc", "str", "覆盖说明文本（wstring col21 → +68）",
            asm_va="0x56dfa9", asm_reader="sub_56DCD0", memory_offset=68,
        ))
    data["columns"].sort(key=lambda c: c["csv_index"])
    recount(data)
    return data


def fmt_type(col: dict) -> str:
    t = col.get("type", "u32")
    fn = col.get("enum_converter")
    if t == "enum" and fn:
        return f"enum `{fn}`"
    return t


def write_md(data: dict) -> None:
    md_path = ROOT / data.get("source_md", "")
    tid = data["id"]
    csv_path = data.get("csv_path", "")
    purpose = data.get("purpose", "")
    asm = data.get("asm_reader") or "None"
    cc = data.get("column_count", 0)

    lines = [
        f"# {tid} ｜ `{csv_path}`",
        "",
        f"- **用途**：{purpose}",
        f"- 表ID `{data.get('table_id', '')}` ｜ 下载序 `{data.get('download_order', '')}` "
        f"｜ 类名 `{data.get('class_name', '')}` ｜ disposition `{data.get('disposition', '')}`",
        f"- 逐列读取函数 `{asm}` ｜ **列数 {cc}**",
        "",
        "| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |",
        "|---|---|---|---|---|---|",
    ]
    for col in sorted(
        [c for c in data.get("columns", []) if c.get("read_order") is not None],
        key=lambda c: c.get("read_order") or 0,
    ):
        ro = col.get("read_order", "")
        ci = col.get("csv_index", "")
        name = col.get("name", "")
        typ = fmt_type(col)
        mem = col.get("memory_offset")
        mem_s = f"+{mem}" if mem is not None else "—"
        meaning = col.get("meaning", "")
        lines.append(f"| {ro} | `{ci}` | `{name}` | {typ} | {mem_s} | {meaning} |")

    gap_cols = [c for c in data.get("columns", []) if c.get("status") == "gap"]
    if gap_cols:
        lines.extend(["", "**Gap 列**（CSV 存在但读表函数跳过，默认 0）："])
        for c in sorted(gap_cols, key=lambda x: x["csv_index"]):
            lines.append(f"- CSV `{c.get('csv_index')}`：{c.get('meaning', GAP_MEANING)}")

    lines.extend([
        "",
        "**填写规则**：",
        "- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。",
        "- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。",
        "- **越界列 = 0**：只需写到最大列号，后面可省略。",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def col_map_summary(data: dict) -> list[str]:
    lines = []
    for col in sorted(
        [c for c in data.get("columns", []) if c.get("read_order") is not None],
        key=lambda c: c.get("read_order") or 0,
    ):
        lines.append(
            f"  ro{col['read_order']:2d} csv{col['csv_index']:2d} {col['name']}"
        )
    return lines


def main() -> None:
    enums = load_enums()
    touched = []

    for tid, builder in [
        ("CLAN_CHALLENGE", rebuild_clan_challenge),
        ("TROOP_CHALLENGE", rebuild_troop_challenge),
        ("NETCAFE_CHALLENGE", rebuild_netcafe_challenge),
    ]:
        data = builder(enums)
        path = TABLES_DIR / f"{tid}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_md(data)
        touched.append(tid)
        print(f"{tid}: read={data['column_count']} defined={data['column_defined']} gap={data['column_gap']} confirmed={data['column_confirmed']}")

    for tid in ("WRESTLE_PARAM", "BULLET", "AI_PARAM"):
        path = TABLES_DIR / f"{tid}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        n = confirm_asm_mapped(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_md(data)
        touched.append(tid)
        print(f"{tid}: confirmed+{n} -> partial={data['column_partial']} confirmed={data['column_confirmed']}")

    for tid, fixer in [
        ("LVUP_FAVMS", fix_lvup_favms),
        ("ACTION_MODULE_INFO", fix_action_module_info),
    ]:
        path = TABLES_DIR / f"{tid}.json"
        data = fixer(json.loads(path.read_text(encoding="utf-8")))
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_md(data)
        touched.append(tid)
        print(f"{tid}: read={data['column_count']} gap={data['column_gap']} partial={data['column_partial']} confirmed={data['column_confirmed']}")

    print("\n=== Column maps ===")
    for tid in ("CLAN_CHALLENGE", "TROOP_CHALLENGE", "NETCAFE_CHALLENGE"):
        data = json.loads((TABLES_DIR / f"{tid}.json").read_text(encoding="utf-8"))
        print(f"\n{tid}:")
        for line in col_map_summary(data):
            print(line)


if __name__ == "__main__":
    main()
