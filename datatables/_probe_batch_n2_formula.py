# -*- coding: utf-8 -*-
"""n2 收口：成长/等级类的"列是不是同一份公式"判定。

对每张表，逐列取 22/50/64/100 行的值向量，然后：
  ① 把值向量两两比较，找出**完全相同**的列簇（同簇 = 一次批量填充的痕迹）；
  ② 对每个非空列，试三个候选公式（id×100 / id×10000 / 10·id·(id+10)），报告命中。
只读。
"""
import io
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")

TABLES = [
    ("LVUP_PILOT", "growth/lvup_pilot.csv", 45),
    ("LVUP_PILOT_EXAM", "growth/lvup_exam.csv", 5),
    ("LVUP_PILOT_CLASS", "growth/lvup_class.csv", 14),
    ("LVUP_CLAN", "growth/lvup_clan.csv", 13),
    ("LVUP_FAVMS", "growth/lvup_ms_favorite.csv", 12),
]


def rows(rel):
    t = open(os.path.join(LOUNGE, rel), "rb").read().decode("utf-8", "replace")
    if t.startswith("\ufeff"):
        t = t[1:]
    return [ln.rstrip() for ln in t.replace("\r\n", "\n").split("\n")
            if ln.strip() and not ln.lstrip().startswith("#")]


for name, rel, ncol in TABLES:
    R = rows(rel)
    key = [r.split(",")[0].strip() for r in R]

    def vec(i):
        return [ (r.split(",")[i].strip() if i < len(r.split(",")) else "") for r in R ]

    # ① 完全相同列簇
    same = {}
    for i in range(ncol):
        vi = vec(i)
        if not any(vi):
            continue
        for j in range(i + 1, ncol):
            if vi == vec(j):
                same.setdefault(i, []).append(j)

    # ② 公式命中
    formulas = {
        "*100": lambda k: str(int(k) * 100),
        "*10000": lambda k: str(int(k) * 10000),
        "10k(k+10)": lambda k: str(10 * int(k) * (int(k) + 10)),
    }
    print("=" * 78)
    print("## %s  (%s)  行 %d / 列 %d" % (name, rel, len(R), ncol))
    print("  列簇（值向量完全相同）:")
    if not same:
        print("    （无）")
    for i, js in sorted(same.items()):
        print("    col%-3d == %s" % (i, ["col%d" % j for j in js]))
    print("  逐列公式命中:")
    for i in range(ncol):
        vi = vec(i)
        if not any(vi):
            continue
        ks = [k for k in key if k.isdigit()]
        hits = []
        for fn, f in formulas.items():
            try:
                if all(vi[key.index(k)] == f(k) for k in ks):
                    hits.append(fn)
            except Exception:
                pass
        # 常量列
        uniq = set(v for v in vi if v)
        kind = "常量 %s" % sorted(uniq)[:3] if len(uniq) == 1 else ("公式 " + ",".join(hits) if hits else "无公式")
        print("    col%-3d %-30s 唯一值 %3d  %s" % (i, str(sorted(uniq)[:3])[:30], len(uniq), kind))
