#!/usr/bin/env python3
"""Round 7: MSMA_WEAPONSET / MSMA_COLORSET / MSMA_WEAPON_EQUIPCOMB cfg enrichment."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "db_design" / "schema" / "cfg" / "tables"
MD_DIR = ROOT / "datatables" / "01-列注释"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrich_cfg_round5 import recount, write_md  # noqa: E402

WEAPON_CATEGORY_ENUM = [
    {"name": n, "value": v}
    for n, v in [
        ("MACHINEGUN", 0), ("MACHINEGUN2", 1), ("MACHINEGUN3", 2), ("SUBMACHINEGUN", 3),
        ("SHOTGUN", 4), ("BEAM_RIFLE", 5), ("BEAM_SPRAYGUN", 6), ("WRESTLE", 7),
        ("CHARGE_RIFLE", 8), ("CHARGE_BAZOOKA", 9), ("SNIPER_RIFLE", 10), ("BEAM_SNIPE", 11),
        ("TRENCH_MORTAR", 12), ("REPAIR", 13), ("SHIELD", 14), ("BAZOOKA", 15),
        ("MISSILE", 16), ("HOWITZER", 17), ("LANDMINE", 18), ("HAND_THROW", 19),
        ("HAND_THROW2", 20), ("RADARPOD", 21), ("REPAIRPOD", 22), ("CAMERAGUN", 23),
        ("BULLET_PACK", 24), ("AAGPOD", 25), ("REPAIR_PACK", 26), ("-", 27),
    ]
]

SLOT_CATEGORY_ENUM = [
    {"name": "MAIN", "value": 0},
    {"name": "EX", "value": 1},
    {"name": "SUB", "value": 2},
    {"name": "0", "value": 3},
]

VERDICT_ENUM = [
    {"name": "FIXED", "value": 0},
    {"name": "CATEGORY_COMBINATION", "value": 1},
    {"name": "ID_COMBINATION", "value": 2},
    {"name": "PERMIT_ID_COMBINATION", "value": 3},
    {"name": "REQUIRED_ID_COMBINATION", "value": 4},
]


def patch(data: dict, csv_index: int, **kw) -> None:
    for c in data["columns"]:
        if c.get("csv_index") == csv_index:
            if kw.get("meaning"):
                kw.setdefault("display_name", kw["meaning"].split("（")[0][:40])
            for k, v in kw.items():
                if v is None:
                    c.pop(k, None)
                else:
                    c[k] = v
            return
    raise KeyError(f"{data['id']} missing csv_index={csv_index}")


def enrich_weaponset(data: dict) -> None:
    patch(
        data,
        4,
        enum_values=SLOT_CATEGORY_ENUM,
        meaning="槽位类别：MAIN 主武装 / EX 副武装 / SUB 副槽 / 0 占位（sub_586450 @0x5871cc）",
    )
    patch(
        data,
        7,
        name="sort_priority",
        status="confirmed",
        confidence="★确证",
        meaning="组内排序权重 u32（+12；sub_58723c 读入 88B 行；sub_586050 持久化）",
        asm_va="0x58723c",
    )
    slots = [
        (0, 8, 28, "a"), (0, 10, 40, "b"), (0, 11, 52, "c"),
        (1, 12, 32, "a"), (1, 14, 44, "b"), (1, 15, 56, "c"),
        (2, 16, 36, "a"), (2, 18, 48, "b"), (2, 19, 60, "c"),
    ]
    for slot, csv_i, off, grp in slots:
        name = f"cost_{grp}_slot{slot}"
        patch(
            data,
            csv_i,
            name=name,
            db_column=name,
            status="confirmed",
            confidence="★确证（布局）",
            meaning=(
                f"成本组 {grp.upper()} 槽{slot} u32（col{csv_i}→+{off}；"
                f"读表三组循环 @0x587249；同构 MSMA_COLORSET price {grp.upper()}）"
            ),
            asm_va="0x587252" if grp == "a" else ("0x587260" if grp == "b" else "0x587276"),
        )
    patch(
        data,
        24,
        name="limit_param_a",
        status="confirmed",
        confidence="★确证（规则）",
        meaning="上限中间参数 A（+72；col22>0 且本列/col25/col26 全≤0 时 col26 强制 9999 @0x5872f4）",
        asm_va="0x5872aa",
    )
    patch(
        data,
        25,
        name="limit_param_b",
        status="confirmed",
        confidence="★确证（规则）",
        meaning="上限中间参数 B（+76；参与 col22 联动 9999 判定 @0x5872f4）",
        asm_va="0x5872bd",
    )
    patch(
        data,
        27,
        name="extra_param",
        status="confirmed",
        confidence="★确证",
        meaning="武器生成附加参（+84；sub_622A20 @0x622de1 传入 sub_60D460 末参）",
        asm_va="0x587315",
    )


def enrich_colorset(data: dict) -> None:
    patch(
        data,
        2,
        name="color_entry_id",
        status="confirmed",
        confidence="★确证",
        meaning="配色条目序号（+4；与 color_group_id 配对；sub_57D920 索引键）",
        asm_va="0x57d0f2",
    )
    patch(
        data,
        4,
        name="display_flag",
        status="confirmed",
        confidence="★确证",
        meaning="显示/价格档索引 u32（+8；sub_97CBE0 @0x97cc92 按本列选 price 组）",
        asm_va="0x57d145",
    )
    patch(
        data,
        11,
        name="color_param_11",
        status="confirmed",
        confidence="★确证",
        meaning="配色 UI 附加参（+44；sub_97CBE0 @0x97cc1f 传入 UI vtable+736）",
        asm_va="0x57d19a",
    )
    patch(
        data,
        14,
        enum_converter=None,
        meaning="C组买价/触发值（+56）；>0 且 col16/17/18 全≤0 ⇒ col18 强制 9999 @0x57d269",
    )
    patch(
        data,
        16,
        name="price_c_param_a",
        status="confirmed",
        confidence="★确证（规则）",
        meaning="C组上限中间参数 A（+64；col14>0 且 col16/17/18 全≤0 ⇒ col18=9999 @0x57d269）",
        asm_va="0x57d1c3",
    )
    patch(
        data,
        17,
        name="price_c_param_b",
        status="confirmed",
        confidence="★确证（规则）",
        meaning="C组上限中间参数 B（+68；参与 C 组 9999 联动 @0x57d269）",
        asm_va="0x57d1d4",
    )
    patch(
        data,
        20,
        name="extra_param_20",
        status="confirmed",
        confidence="★确证",
        meaning="配色附加 u32（+76；sub_57D070 @0x57d247 读入行尾）",
        asm_va="0x57d247",
    )


def enrich_equipcomb(data: dict) -> None:
    for lbl, idx, off in [("a", 3, 4), ("b", 4, 8), ("c", 5, 12)]:
        patch(
            data,
            idx,
            enum_values=WEAPON_CATEGORY_ENUM,
        )
    patch(
        data,
        6,
        name="rule_param_a",
        status="confirmed",
        confidence="★确证",
        meaning="规则参数 A（+16；ID_COMBINATION 时 sub_6FC550 @0x6fc607→sub_56FA70 查表键）",
        asm_va="0x585af7",
    )
    patch(
        data,
        8,
        name="rule_param_b",
        status="confirmed",
        confidence="★确证",
        meaning="规则参数 B（+20；sub_6FC550 @0x6fc624 作数组下标；sub_6563B0 槽位阈值参照 +12 邻域）",
        asm_va="0x585b08",
    )


def gen_md_table(data: dict) -> str:
    lines = [
        f"# {data['id']} ｜ `{data.get('csv_path', '')}`",
        "",
        f"- **用途**：{data.get('purpose', '').lstrip('★**').rstrip('**')}",
        f"- 表ID `{data.get('table_id')}` ｜ 下载序 `{data.get('download_order')}` ｜ "
        f"类名 `{data.get('class_name', '')}` ｜ 逐列读取 `{data.get('asm_reader', '')}`",
        f"- 列数 {data.get('column_defined', data.get('column_count', '?'))} ｜ "
        f"确证 {data.get('column_confirmed', 0)} ｜ 部分 {data.get('column_partial', 0)} ｜ gap {data.get('column_gap', 0)}",
        "",
    ]
    if data["id"] == "MSMA_WEAPONSET":
        lines.extend([
            "## 1.1 Round 7 成本组 A/B/C（2026-09-21）",
            "",
            "- col8–19 三组循环 @`0x587249`：每武器槽 slot0/1/2 各含 **cost_a / cost_b / cost_c** 三通道（同构 MSMA_COLORSET price A/B/C）。",
            "- col22–26 上限联动：col22>0 且 col24/25/26 全≤0 ⇒ col26=9999（@`0x5872f4`）。",
            "",
        ])
    elif data["id"] == "MSMA_COLORSET":
        lines.extend([
            "## 1.1 Round 7 价格联动规则（2026-09-21）",
            "",
            "- A/B 组：col5>0 且 col7≤0 ⇒ col7=9999；col8>0 且 col10≤0 ⇒ col10=9999（@`0x57d183`）。",
            "- C 组：col14>0 且 col16/17/18 全≤0 ⇒ col18=9999（@`0x57d269`）。",
            "",
        ])
    elif data["id"] == "MSMA_WEAPON_EQUIPCOMB":
        lines.extend([
            "## 1.1 Round 7 规则参数 xrefs（2026-09-21）",
            "",
            "- 消费方 `sub_836D10`（装备界面）以机体 +396 查本表；`sub_6563B0` / `sub_6FC550` 读取 +16/+20 规则参。",
            "",
        ])
    lines.extend([
        "| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |",
        "|---|---|---|---|---|---|",
    ])
    ro = 0
    for c in data.get("columns", []):
        if c.get("status") == "gap":
            continue
        if c.get("read_order") is not None:
            ro = c["read_order"]
        elif c.get("status") != "gap":
            ro += 1
        mem = c.get("memory_offset")
        mem_s = f"+{mem}" if mem is not None else "—"
        typ = c.get("type", "u32")
        if c.get("enum_converter"):
            typ = f"enum `{c['enum_converter']}`"
        meaning = re.sub(r"\s+", " ", c.get("meaning", ""))[:140]
        lines.append(
            f"| {ro} | `{c.get('csv_index')}` | `{c.get('name', c.get('db_column'))}` | "
            f"{typ} | {mem_s} | {meaning} |"
        )
    lines.extend([
        "",
        "**填写规则**：",
        "- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。",
        "- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。",
        "- **越界列 = 0**：只需写到最大有效列号。",
        "",
    ])
    return "\n".join(lines)


def process(tid: str, enricher) -> tuple[int, int]:
    path = TABLES / f"{tid}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    before = data.get("column_confirmed", 0)
    enricher(data)
    recount(data)
    data["column_count"] = data.get("column_defined", len(data["columns"]))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_rel = data.get("source_md", "")
    if md_rel:
        md_path = ROOT / md_rel
        if not md_path.is_file():
            md_path = MD_DIR / Path(md_rel).name
        md_path.write_text(gen_md_table(data), encoding="utf-8")
    return before, data["column_confirmed"]


def main() -> None:
    tables = [
        ("MSMA_WEAPONSET", enrich_weaponset),
        ("MSMA_COLORSET", enrich_colorset),
        ("MSMA_WEAPON_EQUIPCOMB", enrich_equipcomb),
    ]
    print("=== Round 7 MSMA cfg enrichment ===\n")
    for tid, fn in tables:
        before, after = process(tid, fn)
        print(f"  {tid}: confirmed {before} → {after}")


if __name__ == "__main__":
    main()
