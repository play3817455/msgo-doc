# -*- coding: utf-8 -*-
"""_map_legacy_by_name.py —— 用「中文武器名」把遗留号接到 9 位真武器上，看接得唯一不唯一。

链路：遗留号 → `names/装备ID-资源ID映射表.csv` 的中文名 → `names/武器分配明细.csv`（wiki 真武器）
      的同名列 → 9 位武器ID + 面板威力。
判据：同名在 sidecar 里**唯一命中**才可自动抄值；0 命中或 ≥2 命中一律报出来给人工。
"""
import csv
import io
import os
import sys
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = sys.argv[1:] or ["2600151", "2012401", "2240601", "12520101", "2210351", "2600101"]


def rd(p):
    with open(os.path.join(HERE, p), encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


leg = {}
for r in rd("names/装备ID-资源ID映射表.csv"):
    k = r[0].strip().lstrip("\ufeff")
    if k.isdigit():
        leg["%08d" % int(k)] = r[1].strip()

side = defaultdict(list)
for r in rd("names/武器分配明细.csv"):
    if len(r) > 10 and r[1].strip().isdigit():
        side[r[5].strip()].append((r[1].strip(), r[10].strip(), r[2].strip()))

print("%-10s %-34s %-28s %s" % ("遗留号", "映射表中文名", "sidecar 命中(9位ID, 面板威力)", "槽位"))
for raw in IDS:
    key = "%08d" % int(raw)
    name = leg.get(key, "(映射表无名)")
    hits = side.get(name, [])
    print("%-10s %-34s %-28s %s" % (raw, name, len(hits), hits[:4] if hits else ""))

print()
print("=== 反向：sidecar 里 6 把报警武器若按名字反查，唯一性如何 ===")
multi = {n: v for n, v in side.items() if len(v) > 1}
print("sidecar 同名多条的武器名 %d 个（例：%s）" % (len(multi), list(multi)[:5]))
