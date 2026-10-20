# -*- coding: utf-8 -*-
"""第 8 批：把「伪 gap / 错位偏移」按 *静态反汇编 + Unicorn 仿真* 双证据回填。

背景（为什么这三张表要改）：
  * CHARA_MODEL 的 reader `sub_571380` 是**4 实参** ABI `(tbl, a2, a3, dst)`；
    旧仿真只压了 3 个实参 ⇒ 写点全落空 ⇒ 读集/偏移双盲。
  * `_emu_readers.py` 补了 `sub_BBB3F0`(64 位取列) 钩子 + 多 ABI 探测后，
    仿真读集 = 真值；再把 `sub_571380` 逐条 disasm 对照，得到列→偏移真值。
  * 结论：schema 把 5 列（csv44/46/53/58/60）误标成 gap，并且
    csv16..31（2×8 循环）与 csv45/47/48/49/54/56/57/59/61/62/63/73..76 的
    memory_offset 存在整体错位。
  * CHARA_PARAM / MSMA_RENTAL 的 csv83/85/86/89 被误标 gap，实为
    `sub_582390` 的基础数值列（偏移早已写对，只是状态错）。

证据格式：`asm_va` = 该列的**写点指令地址**（IDA VA）；含义文本里给出指令形态。
"""
from __future__ import annotations

import io
import json
import os
import shutil
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
BACKUP = os.path.join(HERE, "_rollback", "batch8_" + datetime.now().strftime("%Y%m%d-%H%M%S"))
TODAY = "2026-10-06"
READER = "sub_571380"


# ── CHARA_MODEL：csv -> 真值 ────────────────────────────────────────────────
# (name, memory_offset, type, asm_va, evidence)
CM = {
    # 2×8 循环：第 1 轮写 +3C+8i（本组 a），第 2 轮写 +40+8i（本组 b）
    16: ("mesh_pair0_a", 60, "u32", 0x571492, "`mov [ebx-8], eax`（第 1 轮；ebx=edi+44h）"),
    17: ("mesh_pair1_a", 68, "u32", 0x57149F, "`mov [ebx], eax`（第 1 轮）"),
    18: ("mesh_pair2_a", 76, "u32", 0x5714AB, "`mov [ebx+8], eax`（第 1 轮）"),
    19: ("mesh_pair3_a", 84, "u32", 0x5714B8, "`mov [ebx+10h], eax`（第 1 轮）"),
    20: ("mesh_pair4_a", 92, "u32", 0x5714C5, "`mov [ebx+18h], eax`（第 1 轮）"),
    21: ("mesh_pair5_a", 100, "u32", 0x5714D2, "`mov [ebx+20h], eax`（第 1 轮）"),
    22: ("mesh_pair6_a", 108, "u32", 0x5714DF, "`mov [ebx+28h], eax`（第 1 轮）"),
    23: ("mesh_pair7_a", 116, "u32", 0x5714E7, "`mov [ebx+30h], eax`（第 1 轮）"),
    24: ("mesh_pair0_b", 64, "u32", 0x571492, "`mov [ebx-8], eax`（第 2 轮；ebx=edi+48h）"),
    25: ("mesh_pair1_b", 72, "u32", 0x57149F, "`mov [ebx], eax`（第 2 轮）"),
    26: ("mesh_pair2_b", 80, "u32", 0x5714AB, "`mov [ebx+8], eax`（第 2 轮）"),
    27: ("mesh_pair3_b", 88, "u32", 0x5714B8, "`mov [ebx+10h], eax`（第 2 轮）"),
    28: ("mesh_pair4_b", 96, "u32", 0x5714C5, "`mov [ebx+18h], eax`（第 2 轮）"),
    29: ("mesh_pair5_b", 104, "u32", 0x5714D2, "`mov [ebx+20h], eax`（第 2 轮）"),
    30: ("mesh_pair6_b", 112, "u32", 0x5714DF, "`mov [ebx+28h], eax`（第 2 轮）"),
    31: ("mesh_pair7_b", 120, "u32", 0x5714E7, "`mov [ebx+30h], eax`（第 2 轮）"),
    # 44 起：旧 schema 把 44/46 当 gap ⇒ 后续整体错位
    44: ("render_flag_44", 268, "bool", 0x57169A, "`mov [edi+10Ch], al`（sub_BBB370 结果 !=0）"),
    45: ("render_u32_45", 272, "u32", 0x5716AA, "`mov [edi+110h], eax`"),
    46: ("render_param_46", 276, "float", 0x5716B5, "`fstp dword ptr [edi+114h]`（sub_BBB470）"),
    47: ("flag_effect_a", 280, "bool", 0x5716DA, "`mov [edi+118h], al`"),
    48: ("flag_effect_b", 281, "bool", 0x5716FA, "`mov [edi+119h], al`"),
    49: ("flag_effect_c", 282, "bool", 0x57171F, "`mov [edi+11Ah], al`"),
    53: ("lod_distance", 368, "float", 0x5717FD, "`fstp dword ptr [edi+170h]`（sub_BBB470，第 1 个 float）"),
    54: ("flag_lod_54", 372, "bool", 0x571820, "`mov [edi+174h], al`"),
    56: ("light_dir_x", 380, "float", 0x57187A, "`mov [edi+17Ch], eax`（sub_BBB470→float 三元组 x）"),
    57: ("light_dir_y", 384, "float", 0x571881, "`mov [edi+180h], ecx`（三元组 y；z 恒 0 写 +184h）"),
    58: ("light_color_x", 392, "float", 0x5718BC, "`mov [edi+188h], eax`（第 2 组三元组 x）"),
    59: ("light_color_y", 396, "float", 0x5718C3, "`mov [edi+18Ch], ecx`（三元组 y；z 恒 0 写 +190h）"),
    60: ("flag_shadow", 404, "bool", 0x5718E7, "`mov [edi+194h], al`"),
    61: ("shadow_scale", 408, "u32", 0x5718F7, "`mov [edi+198h], eax`（sub_BBB370 整型，非 float）"),
    62: ("flag_render_62", 412, "bool", 0x571914, "`mov [edi+19Ch], al`"),
    63: ("render_u32_63", 416, "u32", 0x571924, "`mov [edi+1A0h], eax`"),
    73: ("render_u32_73", 452, "u32", 0x571A21, "`mov [edi+1C4h], eax`"),
    74: ("render_u32_74", 444, "u32", 0x571A31, "`mov [edi+1BCh], eax`"),
    75: ("render_u32_75", 456, "u32", 0x571A41, "`mov [edi+1C8h], eax`"),
    76: ("render_u32_76", 448, "u32", 0x571A4F, "`mov [edi+1C0h], eax`"),
}

CM_NOTE = (
    "★2026-10-06 第 8 批（sub_571380 逐条 disasm + Unicorn 真跑双证）："
    "①未映射列的 5 个伪 gap（csv44/46/53/58/60）全部**恢复为 confirmed** —— 它们是 "
    "`sub_BBB370/470` 的正常读列，旧判定因仿真缺 4 实参 ABI（dst 在第 4 个参数）而漏判；"
    "②csv16..31 是 **2×8 循环**（第 1 轮写 +3C+8i、第 2 轮写 +40+8i），即 8 个 8 字节结构项"
    "（.a/.b 两半），旧 schema 按「连续 dword」排布 ⇒ 16..31 偏移整体错位，现按 `ebx` 步进重排并更名 "
    "`mesh_pair0..7_a/_b`；③csv44 起旧 schema 少了 2 个列位（44/46）⇒ csv45/47/48/49 偏移各偏 4/8 字节，"
    "现按真值归位；④csv53/58/60 为 float/float/float 且三元组 z 分量恒 0（+184h/+190h），"
    "csv61 `shadow_scale` 实为 sub_BBB370 **整型**读（非 float）；⑤csv73..76 的落点顺序为 "
    "+1C4h(73)/+1BCh(74)/+1C8h(75)/+1C0h(76)，旧 schema 把 444/448/452/456 顺序贴错，现按真值归位。"
)

# ── CHARA_PARAM / MSMA_RENTAL：伪 gap 定案（偏移原本就对，只是状态错） ────────
BASE = {
    83: ("emergency_return_base", 252, "`mov [esi+0FCh], eax`", 0x582B8C),
    85: ("boost_gauge_base", 356, "`mov [esi+164h], eax`", 0x582B9A),
    86: ("boost_charge_base", 256, "`mov [esi+100h], eax`", 0x582BB1),
    89: ("max_speed_base", 244, "`mov [esi+0F4h], eax`", 0x582C10),
}
BASE_NOTE = (
    "★2026-10-06 第 8 批：这 4 列（csv83/85/86/89）是 reader `sub_582390` 的基础数值列，"
    "旧判定「未单独取证」是错的 —— 仿真（`sub_BBB370` 标记写点）与静态 disasm 双证："
    "csv83→+0FCh、csv85→+164h、csv86→+100h、csv89→+0F4h。状态 gap→confirmed，偏移沿用原值。"
)

# ── 仿真豁免（不是数据问题，是判据问题）：写明后 sweep 不再计入读集差 ────────
EXEMPT = {
    "ACTION_MODULE_INFO": {
        0: "表级键：`sub_56DCD0` 是值提取器（不读 col0），行键由容器 AddRow 读取 ⇒ 不计入仿真读集比对",
    },
    "SCORE_CONFIG_CATEGORY": {
        0: "表级键：`sub_58DDB0` 只读 col1（sub_BBB4F0 查 sub_5812E0），col0 由容器 AddRow 读取 ⇒ 不计入仿真读集比对",
    },
    "ITEM_PART": {
        i: "★条件列：8 组中每出现一次 `MS_BOOST_GAUGE_RECOV`(109) 组该组多占 1 列；"
           "本表当前数据（64 行全空）走常态布局读不到 ⇒ 不计入仿真读集比对（见 17-addendum-ITEM_PART光标槽位.md）"
        for i in range(42, 50)
    },
}


def load(tid):
    p = os.path.join(TABLES, tid + ".json")
    return p, json.load(open(p, encoding="utf-8"))


def save(tid, p, d):
    d["updated"] = TODAY
    p2 = os.path.join(TABLES, tid + ".json")
    with open(p2, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def backup(tid):
    os.makedirs(BACKUP, exist_ok=True)
    src = os.path.join(TABLES, tid + ".json")
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(BACKUP, tid + ".json"))


def patch_chara_model():
    tid = "CHARA_MODEL"
    backup(tid)
    p, d = load(tid)
    by_idx = {c.get("csv_index"): c for c in d["columns"]}
    changed = []
    for ci, (name, off, typ, va, ev) in sorted(CM.items()):
        c = by_idx.get(ci)
        if c is None:
            print(f"  !! CHARA_MODEL csv{ci} 缺列定义")
            continue
        old = (c.get("status"), c.get("name"), c.get("memory_offset"))
        c["status"] = "confirmed"
        c["name"] = name
        c["db_column"] = name
        c["type"] = typ
        c["memory_offset"] = off
        c["confidence"] = "○ASM确证"
        c["asm_reader"] = READER
        c["asm_va"] = hex(va)
        if old[0] == "gap":
            c["meaning"] = f"csv{ci} → +{off}（0x{off:X}），{typ}；旧 schema 误标 gap，实为读列。ASM: {ev}"
        else:
            c["meaning"] = (
                f"csv{ci} → +{off}（0x{off:X}），{typ}。ASM: {ev}"
                + (f"｜旧 schema 偏移 {old[2]}" if old[2] != off else "")
            )
        slot = c.get("csv_index")
        if 16 <= slot <= 31:
            k = (slot - 16) % 8
            half = "a" if slot < 24 else "b"
            c["display_name"] = f"网格定制槽{k}.{half}"
        else:
            c["display_name"] = f"csv{slot} @+{off}"
        changed.append((ci, old, (c["status"], c["name"], off)))
    d["columns_note"] = (d.get("columns_note", "").rstrip() + "\n\n" + CM_NOTE).strip()
    save(tid, p, d)
    print(f"{tid}: patched {len(changed)} 列")
    for ci, old, new in changed:
        print(f"   csv{ci:<3d} {str(old):42s} -> {new}")


def patch_base_stats(tid):
    backup(tid)
    p, d = load(tid)
    n = 0
    for c in d["columns"]:
        ci = c.get("csv_index")
        if ci in BASE:
            name, off, ins, va = BASE[ci]
            c["status"] = "confirmed"
            c["name"] = name
            c["db_column"] = name
            c["memory_offset"] = off
            c["confidence"] = "○ASM确证"
            c["asm_reader"] = "sub_582390"
            c["asm_va"] = hex(va)
            c["meaning"] = f"csv{ci} → +{off}（0x{off:X}）基础数值。ASM: {ins}（sub_BBB370）"
            n += 1
    d["columns_note"] = (d.get("columns_note", "").rstrip() + "\n\n" + BASE_NOTE).strip()
    save(tid, p, d)
    print(f"{tid}: promoted {n} 列 gap->confirmed")


def patch_exempt(tid):
    backup(tid)
    p, d = load(tid)
    n = 0
    for c in d["columns"]:
        ci = c.get("csv_index")
        if ci in EXEMPT.get(tid, {}):
            c["emu_exempt"] = EXEMPT[tid][ci]
            n += 1
    save(tid, p, d)
    print(f"{tid}: marked emu_exempt on {n} 列")


def main():
    print("backup ->", BACKUP)
    patch_chara_model()
    patch_base_stats("CHARA_PARAM")
    patch_base_stats("MSMA_RENTAL")
    for tid in EXEMPT:
        patch_exempt(tid)


main()
