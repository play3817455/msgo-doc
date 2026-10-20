# -*- coding: utf-8 -*-
"""订正两张属性长表的**行宽**：把「值槽」列补全到客户端子表真读的最大 CSV 列号。

依据（IDA 静态反汇编，2026-10-05）：
  * 两张表共用容器行解析 `sub_A47BC0`（只读 col0 属性名）→ 词表分派出子表 →
    子表 AddRow 读 col1 键 → 子表 **vtable[0] 读值列**（列号依属性名而定）。
  * `WEAPON_BATTLE_DETAIL` 值列读取上限 = **col8**（SHIELD `sub_595D60`）⇒ 全宽 **9** 列。
  * `MSMA_BATTLE_DETAIL`   值列读取上限 = **col15**（BOOST_SPEED `sub_57B9F0`）⇒ 全宽 **16** 列。

`column_count` = reader 真映射列数（= 全宽，本两表无 gap 列）；`column_defined` = 全宽。
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(os.path.dirname(HERE), "db_design", "schema", "cfg", "tables")


def col(idx, name, meaning, display, reader, typ="mixed"):
    return {
        "read_order": idx + 1,
        "csv_index": idx,
        "name": name,
        "db_column": name,
        "type": typ,
        "memory_offset": None,
        "asm_reader": reader,
        "asm_va": None,
        "meaning": meaning,
        "display_name": display,
        "status": "confirmed",
        "confidence": "★确证",
    }


# ---------------------------------------------------------------- WEAPON_BATTLE_DETAIL
WHEAD = [
    {
        "read_order": 1, "csv_index": 0, "name": "attr_name", "db_column": "attr_name",
        "type": "str", "memory_offset": None, "asm_reader": "sub_A47BC0", "asm_va": "0xa47cb1",
        "meaning": "战斗属性名（sub_595CC0 词表 off_D7DF10 → 11 张子表分派；POWER/RANGE/STABILITY/…）",
        "display_name": "属性名", "status": "confirmed", "confidence": "★确证",
    },
    {
        "read_order": 2, "csv_index": 1, "name": "weapon_id_key", "db_column": "weapon_id_key",
        "type": "str", "memory_offset": None, "asm_reader": "sub_A5D270", "asm_va": None,
        "meaning": "武器 ID 字符串键（子表 AddRow sub_BBB4F0(idx=1)；与 #37 键域同口径）",
        "display_name": "武器键", "status": "confirmed", "confidence": "★确证",
    },
]

WR = "子表 vtable[0]（POWER sub_57B970 · RANGE/LOCKON_CAM/HIGH_LOCKON sub_595A10 · STABILITY sub_595A30 · RECOIL sub_595AB0 · SHIELD sub_595D60 · 其余 sub_595AF0）"
WVAL = [
    col(2, "attr_value",
        "值槽 0（每行必给）。随 attr_name 解释：POWER=int(+1936)｜RANGE/HIGH_LOCKON/LOCKON_CAM=float×100(+1940/+1948/+1996)｜"
        "STABILITY f[1]=float×100(+1956)｜RAPIDDELAY/COOLTIME/RELOAD/SWITCHTIME=float(+1972/+1980/+1988/+2008)｜"
        "RECOIL f[0]=float×π/180(+2000)｜SHIELD[0]=int(+2012)",
        "值槽 0", WR),
    col(3, "attr_value_2",
        "值槽 1：STABILITY f[0]=float×100(+1952)｜RECOIL f[1]=float×π/180(+2004)｜SHIELD[1]=float(+2016)",
        "值槽 1", WR),
    col(4, "attr_value_3",
        "值槽 2：STABILITY f[2]=float(+1960；本列 ≤0 ⇒ 消费侧取缺省 flt_D91AF8=0.5)｜SHIELD[2]=float(+2020)",
        "值槽 2", WR),
    col(5, "attr_value_4",
        "值槽 3：STABILITY f[3]=float(+1964；本列 ≤0 ⇒ 消费侧取缺省 1.0)｜SHIELD[3]=枚举名 BEAM|BLAST(+2024)",
        "值槽 3", WR),
    col(6, "attr_value_5",
        "值槽 4：STABILITY f[4]=float(+1968)｜SHIELD[4]=float(+2028)",
        "值槽 4", WR),
    col(7, "attr_value_6",
        "值槽 5：SHIELD[5]=float(+2032)；其余属性不用",
        "值槽 5", WR),
    col(8, "attr_value_7",
        "值槽 6：SHIELD[6]=int→bool(+2036)；其余属性不用",
        "值槽 6", WR),
]

# ---------------------------------------------------------------- MSMA_BATTLE_DETAIL
MHEAD = [
    {
        "read_order": 1, "csv_index": 0, "name": "attribute_name", "db_column": "attribute_name",
        "type": "str", "memory_offset": None, "asm_reader": "sub_A47BC0", "asm_va": "0xa47cb1",
        "meaning": "属性名（容器 vtable[0] sub_57BD40 词表 off_D7A298 → 13 张子表分派）",
        "display_name": "属性名", "status": "confirmed", "confidence": "★确证",
    },
    {
        "read_order": 2, "csv_index": 1, "name": "entry_key", "db_column": "entry_key",
        "type": "str", "memory_offset": None, "asm_reader": "sub_A5D270", "asm_va": None,
        "meaning": "条目键字符串（子表 AddRow sub_BBB4F0(idx=1)；必须与 CHARA_PARAM 对应槽串逐字节相等）",
        "display_name": "条目键", "status": "confirmed", "confidence": "★确证",
    },
]

MR = "子表 vtable[0]（RESPAWN sub_57B940 · ENERGY sub_57B990 · MOVE sub_57B9C0 · BOOST_SPEED sub_57B9F0 · JUMP sub_57BAA0 · 其余 sub_57B970/sub_595AF0）"
MVAL = [
    col(2, "entry_value",
        "值槽 0（每行必给）：RESPAWN[0]=int(+192)｜WARP_TIME int(+236)｜COST int(+240)｜MAX_HP int(+164)｜"
        "BOOST_GAUGEMAX int(+168)｜BOOST_GAUGEHEAL float(+176)｜ENERGY[0]=u32(+184)｜MOVE float(+180)｜"
        "BOOST_SPEED[0]=float(+260)｜JUMP[0]=float(+316)",
        "值槽 0", MR),
    col(3, "entry_value_2",
        "值槽 1：RESPAWN[1](+196)｜ENERGY[1]=u32(+188)｜BOOST_SPEED[1]=float(+264)｜JUMP[1]=float(+320)",
        "值槽 1", MR),
    col(4, "entry_value_3",
        "值槽 2：RESPAWN[2]｜BOOST_SPEED[2]=u32(+268)｜JUMP[2]=float(+324)",
        "值槽 2", MR),
    col(5, "entry_value_4",
        "值槽 3：RESPAWN[3]｜BOOST_SPEED[3]=float(+272)｜JUMP[3]=float(+328)",
        "值槽 3", MR),
    col(6, "entry_value_5",
        "值槽 4：RESPAWN[4]｜BOOST_SPEED[4]=float(+276)｜JUMP[4]=u32(+332)",
        "值槽 4", MR),
    col(7, "entry_value_6",
        "值槽 5：RESPAWN[5]｜BOOST_SPEED[5]=u32(+280)｜JUMP[5]=float(+336)",
        "值槽 5", MR),
    col(8, "entry_value_7",
        "值槽 6：RESPAWN[6]｜BOOST_SPEED[6]=u32(+284，注入时取负)｜JUMP[6]=u32(+340)",
        "值槽 6", MR),
    col(9, "entry_value_8",
        "值槽 7：RESPAWN[7]｜BOOST_SPEED[7]=float(+288)｜JUMP[7]=u32(+344)",
        "值槽 7", MR),
    col(10, "entry_value_9",
        "值槽 8：RESPAWN[8]｜BOOST_SPEED[8]=float(+292)｜JUMP[8]=u32(+348，注入时取负)",
        "值槽 8", MR),
    col(11, "entry_value_10",
        "值槽 9：RESPAWN[9]｜BOOST_SPEED[9]=float(+296)｜JUMP[9]=u32(+352)",
        "值槽 9", MR),
    col(12, "entry_value_11",
        "值槽 10：RESPAWN[10]｜BOOST_SPEED[10]=float(+300)｜JUMP[10]=float(+356)",
        "值槽 10", MR),
    col(13, "entry_value_12",
        "值槽 11：BOOST_SPEED[11]=float(+304)｜JUMP[11]=bool(+364)",
        "值槽 11", MR),
    col(14, "entry_value_13",
        "值槽 12：BOOST_SPEED[12]=u32(+308)",
        "值槽 12", MR),
    col(15, "entry_value_14",
        "值槽 13：BOOST_SPEED[13]=float(+312)；其余属性不用",
        "值槽 13", MR),
]


def apply(table: str, head: list, vals: list, reader_max: int):
    path = os.path.join(TABLES, table + ".json")
    d = json.load(open(path, encoding="utf-8"))
    d["columns"] = head + vals
    d["column_count"] = reader_max + 1
    d["column_defined"] = reader_max + 1
    d["column_confirmed"] = reader_max + 1
    d["column_partial"] = 0
    d["column_pending"] = 0
    d["column_gap"] = 0
    d["asm_status"] = "complete"
    d["column_gap_note"] = (
        f"CSV 行含 col0..col{reader_max}，全部由 reader 映射（无 gap 列）；"
        "col2 起是「值槽」，语义随 col0 属性名而定（子表 vtable[0] 各自读）"
    )
    d["reader_max_csv_index"] = reader_max
    d["columns_note"] = (
        "★值槽模型（2026-10-05）：col2..colN 不是「一个值」，而是**按属性名定宽的复合值槽**"
        "——每个属性名对应 11/13 张子表中的一张，其 vtable[0] 从固定的一组列号读值。"
        "旧 schema 记 3 列（只到 col2），col3+ 被越界兜底吃成 0。"
    )
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(path, "a", encoding="utf-8").write("\n")
    print(f"{table}: 列数 {len(d['columns'])}（column_count={d['column_count']}）")


apply("WEAPON_BATTLE_DETAIL", WHEAD, WVAL, 8)
apply("MSMA_BATTLE_DETAIL", MHEAD, MVAL, 15)
