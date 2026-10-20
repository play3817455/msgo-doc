# -*- coding: utf-8 -*-
"""统计 #36 里 POWER 明显偏小（疑似 wiki 列错位）的武器数量，并给出可恢复的真值候选。"""
import collections
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T36 = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_battle_detail.csv")

rows = collections.defaultdict(dict)
for line in io.open(T36, encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = line.split(",")
    if len(parts) < 3:
        continue
    rows[parts[1]][parts[0].strip()] = parts[2].strip()


def num(s):
    try:
        return float(s)
    except Exception:
        return None


pows = []
for wid, d in rows.items():
    p = num(d.get("POWER", ""))
    if p is not None:
        pows.append((p, wid, num(d.get("STABILITY", "")), num(d.get("RAPIDDELAY", "")), num(d.get("RANGE", ""))))
pows.sort()
print("总武器行 =", len(pows))
print("POWER 分布（每 200 一档）：")
h = collections.Counter(int(p) // 200 * 200 for p, *_ in pows if p > 0)
for k in sorted(h)[:8]:
    print("   %6d-%6d : %d" % (k, k + 199, h[k]))
print("POWER<=0 的 =", sum(1 for p, *_ in pows if p <= 0))

sus = [(p, w, st, rd, rg) for p, w, st, rd, rg in pows if 0 < p < 200]
print()
print("疑似错位（0<POWER<200）共 %d 把：" % len(sus))
for p, w, st, rd, rg in sus:
    print("  %-11s POWER=%-6g STABILITY=%-8s RAPIDDELAY=%-8s RANGE=%s" % (w, p, st, rd, rg))

big = [(p, w, st) for p, w, st, *_ in pows if st is not None and st > 1500]
print()
print("STABILITY>1500（集弹性能不可能这么大）共 %d 把" % len(big))
print("其中 POWER<200 的 =", sum(1 for p, w, st in big if p < 200))
