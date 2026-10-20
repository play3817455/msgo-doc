# -*- coding: utf-8 -*-
"""盲区探针：分别开关「整型定长数组宽度」与「块内回跳循环展开」，看差异面。

用法：
    python tools/_probe_blindspots.py                 # 两个盲区都关（基线）
    python tools/_probe_blindspots.py --int-arr       # 只补整型定长数组宽度
    python tools/_probe_blindspots.py --loops naive   # 再加「无条件展开块内回跳」
    python tools/_probe_blindspots.py --loops classed # 再加「按分类展开」
    python tools/_probe_blindspots.py --int-arr --loops classed --detail

只打差异命令清单与每条的首个不匹配；不改任何落盘文件。
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_commands_ida as V  # noqa: E402

ARR_INT = re.compile(r"^(u|i)(8|16|32|64)\s*\[\s*(\d+)\s*\]$")

ORIG_SW = V.scalar_width
ORIG_WS = V.wire_shape
ORIG_COLLECT = V.collect_primitives


def scalar_width_arr(wire_type):
    m = ARR_INT.match(str(wire_type or "").strip().strip("`").lower())
    if m:
        return int(m.group(3)) * (int(m.group(2)) // 8)
    return ORIG_SW(wire_type)


def wire_shape_arr(wire_type):
    if ARR_INT.match(str(wire_type or "").strip().strip("`").lower()):
        return "fixed_arr"
    return ORIG_WS(wire_type)


def block_loops(sl, lo, hi):
    """块内回跳循环 → [(start_ea, end_ea, trip, back_edge_insn)]。"""
    out = []
    for i, ins in enumerate(sl.insns):
        if ins.mnem not in V.JCC:
            continue
        tgt = ins.ov(0) if ins.ot(0) in (V.O_NEAR, V.O_FAR) else None
        if not tgt or tgt >= ins.ea:
            continue
        if tgt < lo or ins.ea > hi:
            continue
        trip = 1
        for j in range(i - 1, max(-1, i - 8), -1):
            ij = sl.insns[j]
            if ij.ea < tgt:
                break
            if ij.mnem == "cmp" and ij.is_imm(1) and ij.imm(1):
                trip = ij.imm(1)
                break
        out.append((tgt, ins.ea, max(1, trip)))
    return out


def _loop_is_array_read(sl, start, end):
    """块内循环是否「每迭代读一个线字段」）。

    判据（三条同时成立）：
      1. 循环体里恰好有 **≥1 个线读**（`call <读原语>` 或 `mov rN,[CV]`）；
      2. 体内所有条件跳转**要么是回边本身、要么是「读失败 → 错误出口」**——
         即目标落在循环外**之后**（前向逃逸），不存在「体内分支跳过后续读」的
         跳过型分支（去重/重试/条件字段那类会回跳的循环正是靠这一条挡掉）；
      3. 体内有独立的**计数器**寄存器（`add r,1` / `inc r`），且 `cmp r,IMM; jcc`
         的回边计数与之一致 —— 排除「`cmp <游标>,<末尾>` 那种按数据定长的循环」。
    """
    body = [ins for ins in sl.insns if start <= ins.ea <= end]
    if not body:
        return False, "空循环体"

    # 1) 线读
    reads = 0
    cur_regs = set()
    for ins in body:
        if ins.mnem == "call" and ins.ot(0) == V.O_NEAR and ins.ov(0) in V.PRIM_READ:
            reads += 1
        elif ins.mnem in ("mov", "movzx", "movsx") and ins.is_reg(0) and ins.is_mem(1):
            if re.match(r"^\[[a-z0-9_]+\]$", ins.ox(1).strip().lower()):
                cur_regs.add(ins.ox(0).strip().lower())
    reads += len(cur_regs)
    if reads < 1:
        return False, "体内无线读"

    # 2) 条件跳转：只允许回边与「前向逃逸」
    for ins in body:
        if ins.mnem not in V.JCC:
            continue
        tgt = ins.ov(0) if ins.ot(0) in (V.O_NEAR, V.O_FAR) else None
        if tgt is None:
            continue
        if tgt == start and ins.ea == end:
            continue                       # 回边
        if tgt > end:
            continue                       # 前向逃逸（错误出口）
        return False, "体内跳过型分支 @%s" % hex(ins.ea)

    # 3) 计数器
    counter = None
    for ins in body:
        if ins.mnem in ("add", "sub") and ins.is_reg(0) and ins.is_imm(1) and ins.ov(1) == 1:
            counter = ins.ox(0).strip().lower()
        elif ins.mnem == "inc" and ins.nops() >= 1 and ins.is_reg(0):
            counter = ins.ox(0).strip().lower()
    if counter is None:
        return False, "无 1 步计数器"
    for ins in sl.insns:
        if ins.ea == end and ins.mnem == "cmp" and ins.is_reg(0) \
                and ins.ox(0).strip().lower() == counter and ins.is_imm(1):
            return True, "数组读（%s，%d 次）" % (counter, ins.imm(1))
    return False, "回边比较的不是 1 步计数器"


def make_collect(mode):
    def collect(sl, lo, hi, direction):
        prims = ORIG_COLLECT(sl, lo, hi, direction)
        loops = block_loops(sl, lo, hi)
        if not loops or mode == "off":
            return [dict(p, loop_trip=1) for p in prims]
        out = []
        for p in prims:
            ea = V.as_int(p.get("va")) or 0
            trip = 1
            for s, e, t in loops:
                if s <= ea <= e:
                    if mode == "classed":
                        ok, _why = _loop_is_array_read(sl, s, e)
                        if not ok:
                            continue
                    trip = max(trip, t)
            if trip > 256:
                continue
            for _ in range(trip):
                out.append(dict(p, loop_trip=trip))
        return out
    return collect


def run():
    cnt = collections.Counter()
    mism = []
    for p in sorted(V.RAW_DIR.glob("*.json")):
        cp = V.CMD_DIR / (p.stem + ".json")
        if not cp.is_file():
            continue
        res = V.analyze(V.Slice(V.load_json(p)), V.load_json(cp))
        cnt[res["status"]] += 1
        if res["mismatches"]:
            mism.append((p.stem, res["mismatches"],
                         res["checks"]["primitive_widths"]["capacity_relation"]))
    return cnt, mism


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--int-arr", action="store_true")
    ap.add_argument("--loops", choices=["off", "naive", "classed"], default="off")
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()

    if args.int_arr:
        V.scalar_width = scalar_width_arr
        V.wire_shape = wire_shape_arr
    V.collect_primitives = make_collect(args.loops)

    cnt, mism = run()
    print("int_arr=%s loops=%s -> %s mismatch_cmds=%d"
          % (args.int_arr, args.loops, dict(cnt), len(mism)))
    for cid, ms, cr in mism:
        print("  ", cid)
        if args.detail:
            for m in ms[:2]:
                print("       %-18s model=%r" % (m["check"], str(m.get("model"))[:70]))
                print("       %-18s asm  =%r" % ("", str(m.get("asm"))[:70]))
            print("       cap_relation=%s obs=%s cap=%s"
                  % (cr["relation"], cr["observed_min"], cr["capacity"]))


if __name__ == "__main__":
    main()
