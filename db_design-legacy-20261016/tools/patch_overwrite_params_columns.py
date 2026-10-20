#!/usr/bin/env python3
"""MSMA_OVERWRITE_PARAMS 扩列：把「变长键值对」行显式建模成固定物理宽度。

背景：本表行格式 `<TYPE>,<REGION>,<ID>[,<FIELD>,<VALUE>]...` 是**变长**的，文档 78 一直写
「不按列号建模」。但 cfg 管线（`importCSVFile` / `ExportTableRawCSV`）是**面向列**的：

  · 导入时 `len(colNames) < maxCol+1` ⇒ 一行 5 字段就会撞「schema 只有 1 列」而**整表导入失败**；
  · 导出时 `dataColumns()` 按 physical 顺序取列 ⇒ 列集与 schema 不一致会出现「导出的 CSV 列序错位」。

于是 1 列建模的二义性被夹在中间：占位行能过，**真数据永远回灌不了**。
本补丁按**有据可依的上界**扩列，而不是拍脑袋定宽度。

宽度依据（★2026-10-06 订正，旧值 10/23 作废）：
用 `idautils.XrefsTo(<UTF-16 字面量 VA>)` 按函数分桶，把五个处理器的**可识别字段名**全部数清：

    TYPE     处理器        字段名数
    MS       sub_57EEB0     9
    WEAPON   sub_57F320    26   ← 上界
    PLAN     sub_57FAC0     3
    BULLET   sub_57FCE0     1
    WRESTLE  sub_57FEA0     3

⇒ 一行**最多** 3 前缀 + 26×2 = **55** 字段。

⚠️ 旧值 23 = 3 + 10×2 是错的：那个「10」数是 MS 字面量块里**物理相邻**的字面量个数，
而其中的 `CHARGE_LV2_SPEED` 其实由 `WEAPON` 处理器（`sub_57F320`）读、写 `+0x8D4`
⇒ 23 列**装不下一行满配 `WEAPON`**，真数据一来就被上面那道闸门整表拒收。
（本次扩列是 append-only：`overwrite_field_11..26` / `overwrite_value_11..26` 追加在尾部，
 已存在的 0..22 号列名与物理序**不动**。）

为什么「尾部空对」无害：客户端 `sub_57EEB0` 等处理器读 FIELD 名做逐名比较，**不认识就只
`++idx` 跳过它的 VALUE**（不报错、不影响后续对）⇒ 导出时补齐的空对会被静默跳过；
且 55 = 3 + 52 是**偶数对**，不会让配对错位。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "schema" / "cfg" / "tables" / "MSMA_OVERWRITE_PARAMS.json"

PAIRS = 26
RULE = "★确证（规则）"

FIELD_HINT = (
    "可用名：`MS` RESPAWN/WARP/COST/ARMOR/BOOST/BOOST_CHARGE/BOOST_SPEED/PAYLOAD/MODULE_SLOT(9)｜"
    "`WEAPON` CHARGE_LV1|LV2_POWER/SCALE/SPEED、POWER/RANGE/HIGH_LOCKON/STABILITY/RAPID_DELAY/"
    "COOL_TIME/RELOAD_TIME/WEAPON_CHANGE_TIME/SHIELD/LOCKON/LOCKON_TIME/LOCK_RADIUS/DELAY_TIME/"
    "CONDITION_TIME/CONDITION_TYPE/BULLET_ID/MAGAZINE_NUM/MAGAZINE_NUM_TOTAL/WEIGHT/DOWN_POINT(26)｜"
    "`PLAN` SP_PARTS1/2/3(3)｜`BULLET` EXP_RANGE(1)｜`WRESTLE` BOOST/DELAY/MOVE(3)"
)


def main() -> None:
    data = json.loads(TABLE.read_text(encoding="utf-8"))
    cols = data.get("columns") or []
    keep = {c.get("csv_index"): c for c in cols}

    row_type = keep[0]
    row_type["read_order"] = 1

    region = {
        "read_order": 2,
        "csv_index": 1,
        "db_column": "region",
        "type": "str",
        "memory_offset": None,
        "asm_reader": "sub_5800D0",
        "asm_va": "0x580116",
        "meaning": "发行区域关键字：`CHINA`（字面量 @0xD7A87C，len 5）或 `CHINA_TPE`（@0xD7A868，len 9）；"
                   "**其余值整行丢弃**（不报错）；比较用 sub_408530（返回 0 = 相等）",
        "confidence": "○ASM确证",
        "status": "confirmed",
        "name": "region",
        "display_name": "发行区域（CHINA / CHINA_TPE）",
    }

    target_id = {
        "read_order": 3,
        "csv_index": 2,
        "db_column": "target_id",
        "type": "u32",
        "memory_offset": None,
        "asm_reader": "sub_5800D0",
        "asm_va": "0x580116",
        "meaning": "目标行/目标的 ID：TYPE=MS ⇒ `CHARA_PARAM` 的 `msma_id`（行基址 = 树节点+0x18）；"
                   "TYPE=WEAPON ⇒ 武器运行时对象的 ID（`sub_57F320` 写该对象 +0x774…+0x9F0）；"
                   "TYPE=PLAN ⇒ `MSMA_PLAN.plan_id`（写行 +8/+12/+16）；TYPE=BULLET/WRESTLE 同理",
        "confidence": "★确证",
        "status": "confirmed",
        "name": "target_id",
        "display_name": "目标行 ID",
    }

    out = [row_type, region, target_id]
    for i in range(1, PAIRS + 1):
        idx = 3 + (i - 1) * 2
        out.append({
            "read_order": idx + 1,
            "csv_index": idx,
            "db_column": f"overwrite_field_{i}",
            "type": "str",
            "memory_offset": None,
            "asm_reader": "sub_5800D0",
            "asm_va": "0x580116",
            "meaning": f"第 {i} 组覆写对的 **FIELD**：目标表字段的**语义名**（处理器用 exe 内硬编码 UTF-16 "
                       f"字面量逐名匹配后写到该行的固定内存偏移）；**不认识的名字 ⇒ 只跳过它的 VALUE**，"
                       f"不报错、不影响后续对。{FIELD_HINT}",
            "confidence": RULE,
            "status": "confirmed",
            "name": f"overwrite_field_{i}",
            "display_name": f"第 {i} 组 · 字段名",
        })
        out.append({
            "read_order": idx + 2,
            "csv_index": idx + 1,
            "db_column": f"overwrite_value_{i}",
            "type": "str",
            "memory_offset": None,
            "asm_reader": "sub_5800D0",
            "asm_va": "0x580116",
            "meaning": f"第 {i} 组覆写对的 **VALUE**：写进上格 FIELD 对应偏移的新值。"
                       f"类型随 FIELD 而定 —— 字符串槽用 sub_402310（窄串赋值），数值槽用 sub_BBB370（取整）",
            "confidence": RULE,
            "status": "confirmed",
            "name": f"overwrite_value_{i}",
            "display_name": f"第 {i} 组 · 新值",
        })

    data["columns"] = out
    disp = (data.get("dispatch") or {}).get("field0_values")
    if isinstance(disp, dict):
        disp["MS"] = "sub_57EEB0 → 覆写 CHARA_PARAM 行（dword_11E3F14）；**9** 个字段名"
        disp["WEAPON"] = "sub_57F320 → 覆写**武器运行时对象**（同 sub_59A070 那个）；**26** 个字段名（★上界）"
        disp["PLAN"] = "sub_57FAC0 → 覆写 MSMA_PLAN 行 +8/+12/+16；**3** 个字段名（SP_PARTS1/2/3）"
        disp["BULLET"] = "sub_57FCE0 → **只有 1 个字段名 `EXP_RANGE`**（→ +0x1C float）；" \
                         "旧记「EXP_RANGE / MOVE / DELAY」是误记，MOVE/DELAY 属 WRESTLE"
        disp["WRESTLE"] = "sub_57FEA0 → 3 个字段名（BOOST +0x10 / DELAY +8 / MOVE +0x5C）"
    data["row_format_note"] = (
        "变长行：前 3 格是固定前缀，其后是任意多 `<字段名>,<值>` 对。字段名在本表内不存在「列号」概念"
        "——它是目标行字段的**语义名**，由各处理器用硬编码 UTF-16 字面量逐名匹配后写到固定内存偏移。"
        "★字段名上界 = **26**（WEAPON）⇒ 物理列宽 3 + 26×2 = 55。"
    )
    data["columns_note"] = (
        "本表行是**变长键值对**（`<TYPE>,<REGION>,<ID>[,<FIELD>,<VALUE>]...`），语义上「没有列号」。"
        "但 cfg 管线是面向列的（导入有 `schema列数 < csv最大列+1` 校验、导出按 physical 列序），"
        "1 列建模会让真数据**永远回灌不了** ⇒ 这里把**固定前缀 3 格 + 最多 26 组对**显式落成 55 个物理列。"
        "26 的来源（★2026-10-06 订正）：`idautils.XrefsTo(<字面量>)` 按处理器分桶数清可识别字段名 ——"
        "MS `sub_57EEB0` 9 / WEAPON `sub_57F320` **26（上界）** / PLAN `sub_57FAC0` 3 / "
        "BULLET `sub_57FCE0` 1 / WRESTLE `sub_57FEA0` 3。"
        "（旧值 23 按 MS 字面量块的「10 个物理相邻字面量」定，而其中 `CHARGE_LV2_SPEED` 实归 WEAPON，"
        "⇒ 23 装不下一行满配 WEAPON，真数据会被闸门整表拒收。）"
        "尾部未用的对**留空**，客户端对不认识的 FIELD 只跳过其 VALUE ⇒ 补齐空对是安全的。"
        "**超过 55 字段时只能追加列**（见 tools/patch_overwrite_params_columns.py）。CSV#1 = 区域关键字、CSV#2 = 目标行 ID。"
    )
    data["column_gap_note"] = ""
    data["column_defined"] = len(out)
    data["column_confirmed"] = len(out)
    data["column_partial"] = 0
    data["column_gap"] = 0
    data["column_pending"] = 0

    TABLE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{TABLE.name}: columns={len(out)} (3 prefix + {PAIRS} pairs)")


if __name__ == "__main__":
    main()
