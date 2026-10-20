# -*- coding: utf-8 -*-
"""★只看 case 里的 **call + 其前的 push 常量**（最省输出的"结构侦察" ✓）。

为什么需要它：大结构（`cinfo` / 成员表 / 逐字段读取器）藏在**内层助手**里，
整段反汇编太长（一个 case 上千行）；而"调用了哪些助手 + 传了什么常量"
恰好把**结构骨架与各处上限**全暴露出来 ✓

输出形如（`→` = call，右边是紧邻其前的 push 常量）：
    00B65F75  → sub_B418D0          push 4      ← "预留 4×N 的数组"
    00B66003  → sub_B4C8F0          push ?      ← 条目读取器（点进去看线宽）

★走法用 `ida_ua.decode_insn + cur += ln`（**不要用 `idc.next_head`** ✗ ——
  它在跳表/函数边界会返回 BADADDR，导致"一条都不打印"，本工具第一版就踩了这个坑 ✓）

读 `reverse-login-chain/tools/_case_addrs.txt`（每行 `0xADDR # 说明`）。
"""
import os
import re

import ida_funcs
import ida_ua
import idc

ROOT = r"F:\9ymsgo\9you"
ADDRS = os.path.join(ROOT, "reverse-login-chain", "tools", "_case_addrs.txt")
GATE_FN = 0xB41120
MAXINS = 600
# ★★★ 2026-09-17【第三十九轮】"截断深度"旋钮：
#   默认 1 = 读到**第 1 处** `sub_B41110`（错误分支）就停 ✓（够用于"独占 case"）
#   ★但**共享段**里，公共段先有一处错误分支 ⇒ 自己那段在它**后面** ✗
#     ⇒ 要看自己的读取序就把这个数调大（2、3…）✓✓
STOP_AT_ERRS = 1
PUSHNUM = re.compile(r"push\s+([0-9A-F]+h|\d+)$")
# `mov esi, 0B5h` / `mov edx, 3Dh` —— cstr 上限就是这么传的 ✓
MOVNUM = re.compile(r",\s*([0-9A-F]+h|\d+)$")


def line(ea):
    return idc.generate_disasm_line(ea, 0) or ""


def case_end(f, t):
    """case 终点 = 分发函数里**下一个** case 起点（`push gate; mov ecx,esi; call B41120`）✓。"""
    s, en = f.start_ea, f.end_ea
    prev = []
    cur = s
    while cur < en:
        insn = ida_ua.insn_t()
        ln = ida_ua.decode_insn(insn, cur)
        if ln == 0:
            cur += 1
            continue
        mnem = idc.print_insn_mnem(cur)
        if mnem == "call" and idc.get_operand_value(cur, 0) == GATE_FN:
            if len(prev) >= 2 and prev[-1][1] == "mov" and prev[-2][1] == "push":
                if prev[-2][0] > t:
                    return prev[-2][0]
        prev.append((cur, mnem))
        if len(prev) > 3:
            prev.pop(0)
        cur += ln
    return t + 0x400


def case_start(f, t):
    """★★★ 2026-09-17【第三十七轮补】**往前找该 case 的起点**（解"共享 case 段" ✓）。

    为什么需要：有些 entry **落在公共段里**（只有结尾的 `cmp` + 错误分支 ✗），
      真正的读取序在**前面**的公共段 ⇒ 只看 entry 会"一条都读不到" ✗✗

    做法：从函数开头**正向**走一遍，记录所有"分发点"
      （`push <gate>; mov ecx,esi; call sub_B41120` ✓ 与 `case_end` 同一判据 ✓）
      ⇒ 取**最后一个 < entry 的分发点** = 该 entry 所属 case 的起点 ✓
    """
    s = f.start_ea
    end = f.end_ea
    prev = []
    last = s
    cur = s
    while cur < t and cur < end:
        insn = ida_ua.insn_t()
        ln = ida_ua.decode_insn(insn, cur)
        if ln == 0:
            cur += 1
            continue
        mnem = idc.print_insn_mnem(cur)
        if mnem == "call" and idc.get_operand_value(cur, 0) == GATE_FN:
            if len(prev) >= 2 and prev[-1][1] == "mov" and prev[-2][1] == "push":
                # 分发点本身（`push <gate>` 的地址）就是"上一个 case 的结束"= 本段起点附近 ✓
                last = prev[-2][0]
        prev.append((cur, mnem))
        if len(prev) > 3:
            prev.pop(0)
        cur += ln
    return last


def main():
    with open(ADDRS, encoding="utf-8") as fh:
        raw = [l.split("#")[0].strip() for l in fh]
    for spec in [x for x in raw if x]:
        t = int(spec, 16)
        f = ida_funcs.get_func(t)
        if not f:
            print("!! 0x%X 无函数" % t)
            continue
        # ★共享 case 段：entry 落在公共段里 ⇒ 从**段起点**开始 dump ✓
        start = case_start(f, t)
        if start != f.start_ea and start < t:
            print("  ★entry 落在共享段里 ⇒ 从段起点 %06X 开始 dump（entry=%06X ✓）" % (start, t))
        end = case_end(f, t)
        print("\n===== case %06X .. %06X =====" % (t, end))
        # ★从**段起点**开始（共享段时 start < t ✓）—— 这样公共读取序才看得到 ✓
        cur, n, pend = min(start, t), 0, None
        errs = [0]  # ★已见到的错误分支数（见 STOP_AT_ERRS ✓）
        while cur < end and n < MAXINS:
            n += 1
            insn = ida_ua.insn_t()
            ln = ida_ua.decode_insn(insn, cur)
            if ln == 0:
                cur += 1
                continue
            mnem = idc.print_insn_mnem(cur)
            t2 = line(cur).strip()
            if mnem in ("retn", "ret"):
                break
            if mnem == "push":
                m = PUSHNUM.match(t2)
                pend = m.group(1) if m else ("off" if "offset" in t2 else None)
            elif mnem == "call":
                if "sub_B41120" not in t2 and "sub_ABB2F0" not in t2:
                    print("  %06X  %-30s  push %s" % (cur, t2.replace("call", "→"), pend or ""))
                # ★★★ 2026-09-17【第三十六轮】读到**错误分支**（`sub_B41110`）就停 ✗
                #   根因：每个 case 的**读取序全在错误分支之前** ✓ 之后全是打印/日志 ✗
                #   ⇒ 一个 case 从 ~22 行缩到 ~6 行 ⇒ **一次能扫的族多 3 倍** ✓✓
                if "sub_B41110" in t2:
                    errs[0] += 1
                    if errs[0] >= STOP_AT_ERRS:
                        print("  ---- 第 %d 处错误分支 ⇒ 以下为打印/日志（略）----" % errs[0])
                        break
                    print("  ---- 第 %d 处错误分支（共享段的公共部分结束 ⇒ 继续找他自己的 ✓）----"
                          % errs[0])
                pend = None
            elif mnem == "cmp" and "," in t2:
                # ★**上限判据全在 `cmp reg, imm` 里**（`cmp ebx,64h; ja → 整包失败` ✓）
                #   不显示它就只能靠 alloc 反推猜上限 ✗ ⇒ 顺手打出来 ✓
                print("  %06X  %s" % (cur, t2))
                pend = None
            elif mnem == "mov" and MOVNUM.search(t2):
                # ★★★ 2026-09-17 本轮补：**cstr 的上限是 `mov esi, imm` 装进去的** ✗
                #     （不是 `push`）—— 只有打出 `mov reg,imm` 才能**直接读到**上限 ✓✓
                #     否则只能靠 alloc 等式反推，而"两个 cstr 之和"有**多解** ✗
                print("  %06X  %-30s  ← 上限候选" % (cur, t2))
                pend = None
            else:
                pend = None
            cur += ln


if __name__ == "__main__":
    main()
