# -*- coding: utf-8 -*-
"""A/B：只看批次 23 的 15 条，在「补整型定长数组宽度」/「再补块内循环展开」两种修法下的结论变化。

回答两个问题：
  ① 这 15 条里有没有「因为盲区而被放过」的真差异？
  ② 修了盲区后新冒出来的差异，是这 15 条的还是别处的？
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_commands_ida as V  # noqa: E402
import _ab_intarray as AB  # noqa: E402

ROOT = os.path.dirname(HERE)
BATCH = json.load(io.open(os.path.join(ROOT, "schema", "commands", "_meta", "batch_23.json"),
                          encoding="utf-8"))
IDS = [t["id"] for t in BATCH["targets"]]


def run(ids=None):
    out = {}
    for p in sorted(V.RAW_DIR.glob("*.json")):
        cid = p.stem
        if ids and cid not in ids:
            continue
        cp = V.CMD_DIR / (cid + ".json")
        if not cp.is_file():
            continue
        res = V.analyze(V.Slice(V.load_json(p)), V.load_json(cp))
        out[cid] = res
    return out


def show(title, res):
    print("#" * 96)
    print(title)
    bad = []
    for cid in IDS:
        r = res.get(cid)
        if r is None:
            print("  %-46s (no raw)" % cid)
            continue
        none_keys = [k for k in V.SIX_CHECKS if r["checks"].get(k) is None]
        flag = "OK " if (not r["mismatches"] and not none_keys) else "!! "
        if flag == "!! ":
            bad.append(cid)
        print("  %s%-46s none=%-22s mism=%d" % (flag, cid, ",".join(none_keys) or "-",
                                                len(r["mismatches"])))
        for m in r["mismatches"]:
            print("        %-18s model=%r asm=%r %s"
                  % (m.get("check"), str(m.get("model"))[:36], str(m.get("asm"))[:40],
                     (m.get("note") or "")[:70]))
    print("  → 15 条里不正常：%s" % (bad or "无"))
    return bad


base = run()
show("BEFORE（原复核器）", base)

V.scalar_width = AB.scalar_width2
V.wire_shape = AB.wire_shape2
a = run()
show("A：补「整型定长数组」宽度（u16/32/64[N]）", a)

V.collect_primitives = AB.collect_primitives2
b = run()
show("B：再补「块内回跳循环」展开", b)

print("#" * 96)
print("全库影响：")
for name, res in (("A", a), ("B", b)):
    pass
for name, kwargs in (("before", {}), ("A", {"sw": 1}), ("B", {"sw": 1, "cp": 1})):
    pass
# 全库计数（A / B）
def run_all():
    out = {}
    for p in sorted(V.RAW_DIR.glob("*.json")):
        cid = p.stem
        cp = V.CMD_DIR / (cid + ".json")
        if not cp.is_file():
            continue
        out[cid] = V.analyze(V.Slice(V.load_json(p)), V.load_json(cp))
    return out


V.scalar_width = AB.scalar_width2
V.wire_shape = AB.wire_shape2
V.collect_primitives = AB.ORIG_COLLECT
fullA = run_all()
V.collect_primitives = AB.collect_primitives2
fullB = run_all()
for name, full in (("A", fullA), ("B", fullB)):
    mism = [c for c, r in full.items() if r["mismatches"]]
    inp15 = [c for c in mism if c in IDS]
    print("  %s 全库有差异 %d 条；其中属于这 15 条的：%s" % (name, len(mism), inp15 or "无"))
