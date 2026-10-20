# -*- coding: utf-8 -*-
"""A/B 试验 v2：同时补上「整型定长数组宽度」与「块级循环展开」两个盲区。

`primitive_widths` 只线性扫命令块、不展开**块内回跳循环**（`expand_loops` 只用在
被调函数体上）。于是 `call sub_B02DD0` + `cmp edi,5; jb` 这样的「5×u32 循环」
只会被记成一条 4B 读 —— 模型写 `u32[5]`（20B）反而对不上。

本脚本只为评估：把这两处一起补上后，915 条的整体结论会怎样。
"""
import collections
import re
import sys

sys.path.insert(0, "tools")
import verify_commands_ida as V  # noqa: E402

ARR_INT = re.compile(r"^(u|i)(8|16|32|64)\s*\[\s*(\d+)\s*\]$")

ORIG_SW = V.scalar_width
ORIG_WS = V.wire_shape
ORIG_COLLECT = V.collect_primitives


def scalar_width2(wire_type):
    if not wire_type:
        return None
    t = str(wire_type).strip().strip("`").lower()
    m = ARR_INT.match(t)
    if m:
        return int(m.group(3)) * (int(m.group(2)) // 8)
    return ORIG_SW(wire_type)


def wire_shape2(wire_type):
    t = str(wire_type or "").strip().strip("`").lower()
    if ARR_INT.match(t):
        return "fixed_arr"
    return ORIG_WS(wire_type)


def block_loops(sl, lo, hi):
    """块内回跳循环 → [(start_ea, end_ea, trip)]（trip=1 表示次数未定）。"""
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


def collect_primitives2(sl, lo, hi, direction):
    """原逻辑 + 把落在块内循环体里的原语按行程复制（带 loop_trip）。"""
    prims = ORIG_COLLECT(sl, lo, hi, direction)
    loops = block_loops(sl, lo, hi)
    if not loops:
        return [dict(p, loop_trip=1) for p in prims]
    out = []
    for p in prims:
        ea = V.as_int(p.get("va")) or 0
        trip = 1
        for s, e, t in loops:
            if s <= ea <= e:
                trip = max(trip, t)
        if trip > 256:
            continue                      # 行程过大 ⇒ 不可判定，丢弃而不是硬展开
        for _ in range(trip):
            out.append(dict(p, loop_trip=trip))
    return out


def run():
    cnt = collections.Counter()
    mism = []
    for p in sorted(V.RAW_DIR.glob("*.json")):
        cid = p.stem
        cp = V.CMD_DIR / (cid + ".json")
        if not cp.is_file():
            continue
        res = V.analyze(V.Slice(V.load_json(p)), V.load_json(cp))
        cnt[res["status"]] += 1
        if res["mismatches"]:
            mism.append((cid, res["mismatches"],
                         res["checks"]["primitive_widths"]["capacity_relation"]))
    return cnt, mism


def main():
    print("BEFORE :", dict(run()[0]))

    V.scalar_width = scalar_width2
    V.wire_shape = wire_shape2
    V.collect_primitives = collect_primitives2

    cnt, mism = run()
    print("AFTER  :", dict(cnt), "mismatch cmds:", len(mism))
    for cid, ms, cr in mism[:20]:
        print("  ", cid)
        for m in ms[:3]:
            print("       %-18s model=%r asm=%r"
                  % (m["check"], str(m.get("model"))[:34], str(m.get("asm"))[:46]))
        print("       cap_relation=%s obs=%s cap=%s"
              % (cr["relation"], cr["observed_min"], cr["capacity"]))


if __name__ == "__main__":
    main()
