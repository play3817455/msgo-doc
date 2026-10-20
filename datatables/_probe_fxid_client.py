# -*- coding: utf-8 -*-
"""_probe_fxid_client.py —— 7 位 FX ID 会不会住在**客户端本地表**（`unpackdat/settings/*.csv`）？

判据：某列的值有多少落进「资源树反解出的合法 a2 集合」。高命中 = 真产出方。
只报告，不写。
"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FXDIR = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "fx")
SETT = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "settings")
PAT = re.compile(r"^PP_(\d{2})_(\d{3})_(\d{2})\.vra$", re.I)


def valid_ids():
    ids = set()
    for d in os.listdir(FXDIR):
        p = os.path.join(FXDIR, d)
        if not os.path.isdir(p) or not d.isdigit():
            continue
        for f in os.listdir(p):
            m = PAT.match(f)
            if m:
                cc, nnn, ii = (int(x) for x in m.groups())
                if cc == int(d):
                    ids.add(cc * 100000 + nnn * 100 + ii)
    return ids


IDS = valid_ids()
print("合法 a2 集合：%d 个" % len(IDS))
print("settings 目录：%s（存在 %s）" % (SETT, os.path.isdir(SETT)))
print()

files = sorted(f for f in os.listdir(SETT) if f.lower().endswith(".csv"))
print("本地表 %d 个，扫列 …" % len(files))
hits = []
for fn in files:
    p = os.path.join(SETT, fn)
    try:
        with open(p, encoding="utf-8-sig", errors="replace") as fh:
            rd = list(csv.reader(fh))
    except Exception:
        continue
    if len(rd) < 2:
        continue
    head = rd[0]
    for ci in range(len(head)):
        vals = []
        for r in rd[1:]:
            if len(r) > ci:
                v = r[ci].strip()
                if v.isdigit() and 5 <= len(v) <= 7:
                    n = int(v)
                    if n > 0:
                        vals.append(n)
        if len(vals) < 5:
            continue
        hit = [v for v in vals if v in IDS]
        # 要求：命中率高 **且** 命中值有足够多样性（排除单一常量巧合）
        if len(hit) >= 5 and len(set(hit)) >= 5 and 100.0 * len(hit) / len(vals) >= 50.0:
            hits.append((100.0 * len(hit) / len(vals), len(hit), len(set(hit)), len(vals),
                         fn, ci, head[ci].strip()[:22], sorted(set(hit))[:4]))

hits.sort(reverse=True)
print()
print("%-7s %7s %6s %8s  %-30s %-4s %s" % ("命中率", "命中", "去重", "该列", "文件", "列", "表头"))
for rate, n, nd, tot, fn, ci, h, ex in hits[:30]:
    print("%6.1f%% %7d %6d %8d  %-30s %-4d %s  %s" % (rate, n, nd, tot, fn, ci, h, ex))
if not hits:
    print("（没有任何本地表的列命中：排除 0/短值、要求去重≥5 且命中率≥50%）")
