# -*- coding: utf-8 -*-
"""item.csv / weapon_battle_detail.csv / weapon_settings.csv 结构体检。"""
import collections
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")


def rd(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


rows = rd(os.path.join(DF, "item.csv"))
body = [r for r in rows if not r[0].lstrip("\ufeff").startswith("#")]
print("item.csv 总行 %d（注释 %d / 数据 %d）" % (len(rows), len(rows) - len(body), len(body)))

# 列数分布
ncols = collections.Counter(len(r) for r in body)
print("列数分布:", dict(sorted(ncols.items())))

# 各列位置出现 WEAPON/WRESTLE 的统计
for i in range(0, 8):
    c = sum(1 for r in body if len(r) > i and r[i].strip().upper() in ("WEAPON", "WRESTLE"))
    if c:
        print("  col%d 是 WEAPON/WRESTLE 的行数 = %d" % (i, c))

# 类型值集合（col3/col4 合并看）
types = collections.Counter()
for r in body:
    for i in (3, 4):
        if len(r) > i and r[i].strip() and not r[i].strip().isdigit():
            types[r[i].strip()] += 1
print("非数字类型值 top:", types.most_common(18))

# id 长度分布
lens = collections.Counter(len(r[0].strip()) for r in body if r[0].strip().isdigit())
print("id 位数分布:", dict(sorted(lens.items())))

# 按「类型字段是否 WEAPON」分组，看 id 位数
for label, pred in (("col3=WEAPON", lambda r: len(r) > 3 and r[3].strip().upper() == "WEAPON"),
                    ("col4=WEAPON", lambda r: len(r) > 4 and r[4].strip().upper() == "WEAPON"),
                    ("两者都不是", lambda r: not ((len(r) > 3 and r[3].strip().upper() == "WEAPON")
                                             or (len(r) > 4 and r[4].strip().upper() == "WEAPON")))):
    sel = [r for r in body if pred(r)]
    L = collections.Counter(len(r[0].strip()) for r in sel if r[0].strip().isdigit())
    print("%-12s %5d 行  id位数=%s  样例=%s" % (label, len(sel), dict(sorted(L.items())),
                                            [",".join(r[:5]) for r in sel[:2]]))

# 6 把报警号 + 100000 段 在 item.csv 里
alarm = ["2600151", "2012401", "2240601", "12520101", "2210351", "2600101",
         "02240601", "02012401", "02210351", "02600101", "02600151"]
ids = {r[0].strip() for r in body}
print()
print("报警号在 item.csv:", [a for a in alarm if a in ids])
print("100000-100005 在 item.csv:", [x for x in ("100000", "100001", "100005") if x in ids])

for fn, kc, note in (("weapon_battle_detail.csv", 1, "属性名,武器号,值"),
                     ("weapon_settings.csv", 0, "武器号,...")):
    rs = rd(os.path.join(DF, fn))
    bb = [r for r in rs if not r[0].lstrip("\ufeff").startswith("#")]
    L = collections.Counter(len(r[kc].strip()) for r in bb if len(r) > kc and r[kc].strip().isdigit())
    print("%s 数据 %d 行 (key=col%d %s) id位数=%s" % (fn, len(bb), kc, note, dict(sorted(L.items()))))
