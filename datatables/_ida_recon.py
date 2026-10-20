# -*- coding: utf-8 -*-
"""IDA 侧侦察：78 个 cfg reader 的形状（循环/助手调用/立即数 push）-> datatables/_out_ida_recon.txt

只做线性扫描，不解析寄存器常量 —— 目的是先看清代码形态，再决定提取器怎么做。
"""
import io
import json
import os
import sys

import ida_bytes
import ida_funcs
import idc
import idautils

OUT = r"f:\9ymsgo\9you\datatables\_out_ida_recon.txt"
READERS = r"f:\9ymsgo\9you\datatables\_out_reader_list.json"

HELPERS = ("sub_BBB370", "sub_BBB4F0", "sub_456D90")

log = []


def emit(s=""):
    log.append(s)


def operands(ea):
    out = []
    for i in range(3):
        t = idc.get_operand_type(ea, i)
        if t == idc.o_void:
            break
        out.append((t, idc.get_operand_value(ea, i), idc.print_operand(ea, i)))
    return out


def main():
    readers = json.load(open(READERS, encoding="utf-8"))
    rows = []
    for name in sorted(readers):
        if not name.startswith("sub_"):
            continue
        ea = idc.get_name_ea_simple(name)
        if ea == idc.BADADDR:
            rows.append((name, None, "NOT_FOUND"))
            continue
        f = ida_funcs.get_func(ea)
        if not f:
            rows.append((name, None, "NO_FUNC"))
            continue
        nins = 0
        backjumps = []
        helper_calls = {h: 0 for h in HELPERS}
        imm_pushes = []
        call_targets = {}
        other_calls = {}
        for insn_ea in idautils.Heads(f.start_ea, f.end_ea):
            nins += 1
            mnem = idc.print_insn_mnem(insn_ea)
            ops = operands(insn_ea)
            if mnem == "call" and ops:
                tgt = ops[0][2]
                if tgt in HELPERS:
                    helper_calls[tgt] += 1
                    # 最近两次 push（不含本指令）
                    pushes = []
                    p = idc.prev_head(insn_ea)
                    while p != idc.BADADDR and len(pushes) < 3 and p >= f.start_ea:
                        if idc.print_insn_mnem(p) == "push":
                            pushes.append((p, idc.print_operand(p, 0)))
                        p = idc.prev_head(p)
                    call_targets.setdefault(tgt, []).append(
                        {"ea": hex(insn_ea), "pushes": [x[1] for x in pushes]}
                    )
                else:
                    other_calls[tgt] = other_calls.get(tgt, 0) + 1
            if mnem == "push" and ops and ops[0][0] == idc.o_imm:
                imm_pushes.append(ops[0][1])
            if mnem.startswith("j"):
                tgt = idc.get_operand_value(insn_ea, 0)
                if tgt != idc.BADADDR and tgt < insn_ea:
                    backjumps.append((hex(insn_ea), hex(tgt)))
        rows.append(
            (
                name,
                {
                    "start": hex(f.start_ea),
                    "end": hex(f.end_ea),
                    "nins": nins,
                    "backjumps": len(backjumps),
                    "helpers": helper_calls,
                    "other_calls": len(other_calls),
                    "imm_pushes": imm_pushes,
                    "tables": readers[name]["tables"],
                    "declared": readers[name]["declared"],
                    "non_gap": readers[name]["non_gap"],
                    "call_detail": call_targets,
                },
                "OK",
            )
        )

    emit("reader         nins  backjmp  BBB370 BBB4F0 456D90  imm_pushes")
    emit("-" * 120)
    for name, info, status in rows:
        if info is None:
            emit(f"{name:14s} {status}")
            continue
        h = info["helpers"]
        emit(
            f"{name:14s} {info['nins']:4d} {info['backjumps']:7d} {h['sub_BBB370']:6d} "
            f"{h['sub_BBB4F0']:6d} {h['sub_456D90']:6d}  {info['imm_pushes']}"
        )

    emit()
    emit("== 含循环（backjump>0）的 reader ==")
    loopy = [(n, i) for n, i, s in rows if i and i["backjumps"]]
    for n, i in loopy:
        emit(f"  {n}  backjumps={i['backjumps']}  tables={i['tables']}  declared={i['declared']}")
    if not loopy:
        emit("  无")

    emit()
    emit("== 无 BBB370/BBB4F0/456D90 调用的 reader（另类读法，需单独处理） ==")
    odd = [
        (n, i)
        for n, i, s in rows
        if i and sum(i["helpers"].values()) == 0
    ]
    for n, i in odd:
        emit(f"  {n}  tables={i['tables']}  other_calls={i['other_calls']}  nins={i['nins']}")
    if not odd:
        emit("  无")

    emit()
    emit("== 助手调用次数 != 声明非gap列数的 reader ==")
    mism = []
    for n, i, s in rows:
        if not i:
            continue
        want = len(i["non_gap"])
        got = sum(i["helpers"].values())
        if want != got:
            mism.append((n, want, got, i["tables"], i["declared"], i["non_gap"]))
    for n, want, got, t, d, ng in mism:
        emit(f"  {n}: 声明非gap={want} 助手调用={got}  tables={t}")
        emit(f"      declared={d}")
        emit(f"      non_gap ={ng}")
    if not mism:
        emit("  无")

    data = {n: i for n, i, s in rows if i}
    with open(r"f:\9ymsgo\9you\datatables\_out_ida_recon.json", "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print(f"readers={len(data)} wrote {OUT}")


main()
