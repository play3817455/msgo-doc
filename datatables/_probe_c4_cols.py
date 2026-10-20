# -*- coding: utf-8 -*-
"""逐字段定位 CHARA_PARAM 种子 vs manifest 的差异列（用于确认 csv_index=89 留空是否为唯一差异）。"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
CSV = os.path.join(LOUNGE, "msma", "msma_settings.csv")


def rows(text):
    if text.startswith("\ufeff"):
        text = text[1:]
    out = {}
    for ln in text.replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        f = ln.split(",")
        out[f[0]] = f
    return out


with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute("select raw_csv from meta.cfg_manifest where file=%s", ("CHARA_PARAM",))
    r = cur.fetchone()
man = r[0] if isinstance(r[0], str) else r[0].decode("utf-8", "replace")

seed = rows(open(CSV, "rb").read().decode("utf-8", "replace"))
mf = rows(man)
print("种子行 %d / mf 行 %d / 键差 %d" % (len(seed), len(mf), len(set(seed) ^ set(mf))))

from collections import Counter

col_diff = Counter()
widths = Counter()
samples = []
for k, sv in seed.items():
    mv = mf.get(k)
    if mv is None:
        continue
    widths[(len(sv), len(mv))] += 1
    if len(sv) != len(mv):
        for i in range(min(len(sv), len(mv))):
            if sv[i] != mv[i]:
                col_diff[i] += 1
        continue
    d = [i for i in range(len(sv)) if sv[i] != mv[i]]
    for i in d:
        col_diff[i] += 1
    if d and len(samples) < 3:
        samples.append((k, d, [(i, sv[i], mv[i]) for i in d]))

print("字段数分布 (种子, mf):", dict(widths))
print("差异列 -> 命中行数:", dict(sorted(col_diff.items())))
for k, d, cells in samples:
    print("样例", k, "差异列", d, cells)

# 只看 col89（csv_index=89）的对照
n89 = 0
for k, sv in seed.items():
    mv = mf.get(k)
    if mv and len(sv) > 89 and len(mv) > 89 and sv[89] != mv[89]:
        n89 += 1
        if n89 <= 3:
            print("col89 例:", k, "种子=%r mf=%r" % (sv[89], mv[89]))
print("col89 不同行数:", n89)
print("schema 尾三列:", [x for x in json.load(io.open(os.path.join(ROOT, "db_design", "schema", "cfg", "tables", "_chara_param.json"), encoding="utf-8"))["columns"][-3:]] if os.path.exists(os.path.join(ROOT, "db_design", "schema", "cfg", "tables", "_chara_param.json")) else "(no schema file)")
