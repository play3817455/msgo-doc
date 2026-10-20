# -*- coding: utf-8 -*-
"""_audit_official_ids.py —— 钉死「官方 item/weapon_set 到底用哪一族武器号」。

线索：
  A) msma_weapon_set.csv.bak（wiki 重写之前的原版）里武器号是 7 位（1040101）
  B) 装备ID-资源ID映射表.csv 的「来源」列：9 位里 1617 条写着 `ITEM表|weapon_set`
     —— 但若该表是 wiki 重写**之后**建的，`weapon_set` 指的就是我们自己生成的文件（循环论证）
  ⇒ 必须先看**文件时间**，再看原版 .bak 的号在 ITEM 表里有没有真名字。
"""
import csv
import io
import os
import sys
import time
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(p):
    p = os.path.join(ROOT, p)
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


FILES = [
    "datatables/names/装备ID-资源ID映射表.csv",
    "server/datafiles/lounge/msma/msma_weapon_set.csv",
    "server/datafiles/lounge/msma/msma_weapon_set.csv.bak",
    "server/datafiles/lounge/msma/msma_weapon_set.csv.bak_wiki20260928-174043",
    "server/datafiles/lounge/item/item.csv",
    "server/datafiles/lounge/item/item.csv.bak_bom",
    "datatables/gen_weapon_set_wiki.py",
    "datatables/names/武器分配明细.csv",
]
print("=== 文件时间 ===")
for p in FILES:
    ap = os.path.join(ROOT, p)
    if os.path.exists(ap):
        print("  %-58s %s" % (os.path.basename(p), time.strftime("%Y-%m-%d %H:%M:%S",
                                                                  time.localtime(os.path.getmtime(ap)))))
    else:
        print("  %-58s (缺)" % os.path.basename(p))

# 原版 .bak 的武器号
bak = [r for r in rd("server/datafiles/lounge/msma/msma_weapon_set.csv.bak")
       if r[0].strip().isdigit()]
wcol = Counter()
for r in bak:
    for c in r:
        s = c.strip()
        if s.isdigit() and len(s) >= 5:
            wcol[len(s)] += 1
print()
print("=== 原版 msma_weapon_set.csv.bak：%d 行，武器号号长 %s ===" % (len(bak), dict(wcol)))
print("  前 6 行完整:", bak[:6])

# ITEM 表里的名字
items = {}
for r in rd("server/datafiles/lounge/item/item.csv"):
    items[r[0].strip().lstrip("\ufeff")] = r[2].strip() if len(r) > 2 else ""
src = {}
for r in rd("datatables/names/装备ID-资源ID映射表.csv"):
    src[r[0].strip().lstrip("\ufeff")] = (r[1].strip(), r[13].strip() if len(r) > 13 else "")

print()
print("=== 原版 .bak 用到的武器号，在 ITEM 表 / 映射表里是什么 ===")
seen = set()
for r in bak:
    for c in r:
        s = c.strip()
        if s.isdigit() and len(s) >= 5 and s not in seen:
            seen.add(s)
            nm, s2 = src.get(s, ("", ""))
            print("  %-10s item.csv名=%-22s 映射表名=%-22s 来源=%s"
                  % (s, items.get(s, "(不在 item.csv)") or "(空)", nm or "(空)", s2 or "(空)"))
    if len(seen) >= 8:
        break

# 6 把报警号在原版 .bak 里出现过吗
alarm = {"2600151", "2012401", "2240601", "12520101", "2210351", "2600101"}
allc = {c.strip().lstrip("\ufeff") for r in bak for c in r}
print()
print("=== 报警号是否出现在原版 weapon_set：%s ==="
      % {a: (a in allc) for a in sorted(alarm)})
