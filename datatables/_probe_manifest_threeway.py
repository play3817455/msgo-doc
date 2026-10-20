# -*- coding: utf-8 -*-
"""三方对账：cfg 物理表 ／ meta.cfg_manifest 行 ／ db_design schema JSON。
目的：找出 manifest 里的**陈旧行**和库里**不在 schema 的野表**。只读。
"""
import json
import os

import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def slug(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


sch = sorted(slug(f[:-5]) for f in os.listdir(SCHEMA) if f.endswith(".json"))

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select table_name from information_schema.tables"
                " where table_schema='cfg' order by 1")
    phys = [(slug(r[0]), r[0]) for r in cur.fetchall()]
    cur.execute("select file, row_count, coalesce(length(raw_csv),0) from meta.cfg_manifest"
                " order by 1")
    man = [(slug(r[0]), r[0], r[1], r[2]) for r in cur.fetchall()]

ps = {s for s, _ in phys}
ms = {s for s, *_ in man}
ss = set(sch)
pset = {s: n for s, n in phys}

print("schema JSON %d ／ cfg 物理表 %d ／ manifest 行 %d" % (len(ss), len(ps), len(ms)))
print()

print("① manifest 行但 **schema 里没有**（陈旧行）：%s"
      % sorted(ms - ss))
print("② schema 有但 **manifest 没有**：%s" % sorted(ss - ms))
print("③ schema 有但 **库里没有物理表**（= skip_db 或未建）：%s" % sorted(ss - ps))
print("④ 库里有物理表但 **schema 里没有**（野表）：%s"
      % sorted(pset[s] for s in ps - ss))
print()
print("⑤ manifest 里 schema 没有的行的明细（row_count / raw_csv 长度）：")
for s, n, rc, ln in man:
    if s not in ss:
        print("   %-24s row_count=%s  raw_csv=%s 字节" % (n, rc, ln))
print()
print("⑥ schema 有、库里没有物理表的表（manifest 里有没有？）：")
for s in sorted(ss - ps):
    has = "有" if s in ms else "**没有**"
    print("   %-24s manifest %s" % (s, has))
