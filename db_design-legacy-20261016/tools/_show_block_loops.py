# -*- coding: utf-8 -*-
"""把某命令字段窗口内的块内指令按「含回跳的循环区间」标注出来打印。

用途：判断 `primitive_widths` 报的缺口，究竟是模型错，还是「块内循环只扫到一趟」
这类工具伪影——`collect_primitives` 只线性扫块，不展开块级循环。
"""
import sys

sys.path.insert(0, "tools")
import verify_commands_ida as V  # noqa: E402
from verify_commands_ida import JCC  # noqa: E402


def loops_of(insns, lo, hi):
    out = []
    for i, ins in enumerate(insns):
        if ins.mnem not in JCC:
            continue
        tgt = ins.ov(0) if ins.ot(0) in (V.O_NEAR, V.O_FAR) else None
        if tgt and tgt < ins.ea:
            out.append((tgt, ins.ea))
    return out


def main():
    cid = sys.argv[1]
    sl = V.Slice(V.load_json(V.RAW_DIR / (cid + ".json")))
    md = V.load_json(V.CMD_DIR / (cid + ".json"))
    guard = V.find_guard(sl)
    disp = V.find_dispatch(sl, exclude_va=(V.find_capacity(sl) or {}).get("alloc_va"))
    lo = (V.as_int(guard["va"]) + 1) if guard else sl.block[0]
    hi = V.as_int(disp["va"]) if disp else sl.block[1]
    print("block %s..%s  window %s..%s" % (V.hx(sl.block[0]), V.hx(sl.block[1]), V.hx(lo), V.hx(hi)))
    lps = loops_of(sl.insns, lo, hi)
    print("块内回跳（循环）区间：%s" % [("%s->%s" % (V.hx(a), V.hx(b))) for a, b in lps])
    print()
    for ins in sl.insns:
        if ins.ea < lo or ins.ea > hi:
            continue
        mark = ""
        for a, b in lps:
            if a <= ins.ea <= b:
                mark = "  <== 循环体 %s..%s" % (V.hx(a), V.hx(b))
                break
        print("  %-10s %-34s%s" % (V.hx(ins.ea), ins.text[:34], mark))


if __name__ == "__main__":
    main()
