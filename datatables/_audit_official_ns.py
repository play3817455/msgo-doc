# -*- coding: utf-8 -*-
"""_audit_official_ns.py —— 官方 weapon_set 的武器号命名空间画像。

已知：
  · 原版 msma_weapon_set.csv.bak（2026-09-14）武器号是 7 位(3915) + 8 位(261)，没有 9 位
  · 官方 item.csv.bak_bom（2026-09-17）只有 16 个 9 位号
⇒ 要看清：8 位是什么武器（射击系？）、9 位那 16 个到底是什么（部件？），
        以及 6 把报警号在官方两表里的存在性。
"""
import csv
import io
import os
import sys
from collections import Counter, defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(p):
    with open(os.path.join(ROOT, p), encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


src = {}
for r in rd("datatables/names/装备ID-资源ID映射表.csv"):
    src[r[0].strip().lstrip("\ufeff")] = (r[1].strip(), r[2].strip(),
                                          r[13].strip() if len(r) > 13 else "")

# ---- 官方原版 weapon_set ----
bak = [r for r in rd("server/datafiles/lounge/msma/msma_weapon_set.csv.bak")
       if r[0].strip().isdigit()]
wid = defaultdict(set)
for r in bak:
    for c in r[2:6]:
        s = c.strip()
        if s.isdigit() and len(s) >= 5:
            wid[len(s)].add(s)
print("官方原版 weapon_set %d 行；武器号按号长：" % len(bak))
for L in sorted(wid):
    print("  %d 位：%d 个" % (L, len(wid[L])))
print()
for L in sorted(wid):
    print("--- %d 位样例（映射表名 / 类型 / 来源）---" % L)
    for s in sorted(wid[L])[:14]:
        nm, ty, so = src.get(s, ("(不在映射表)", "", ""))
        print("   %-10s %-26s %-10s %s" % (s, nm[:26], ty, so))

# ---- 官方原版 item 表的 9 位号 ----
print()
bom = [r for r in rd("server/datafiles/lounge/item/item.csv.bak_bom") if r[0].strip().isdigit()]
nine = [r for r in bom if len(r[0].strip()) >= 9]
print("官方原版 item 表（.bak_bom, %d 行）里的 9 位号 %d 个：" % (len(bom), len(nine)))
for r in nine:
    print("   %-12s %s | %s" % (r[0].strip(), (r[2].strip() if len(r) > 2 else "")[:24],
                                (r[4].strip() if len(r) > 4 else "")))

# ---- 报警号存在性 ----
print()
items_bom = {r[0].strip().lstrip("\ufeff") for r in bom}
print("报警号在官方原版 item 表 / 官方原版 weapon_set 里：")
for a in ("2600151", "2012401", "2240601", "12520101", "2210351", "2600101"):
    print("   %-10s item.bak_bom=%-5s weapon_set.bak=%s  映射表名=%s"
          % (a, a in items_bom, any(a in v for v in wid.values()), src.get(a, ("", "", ""))[0]))
