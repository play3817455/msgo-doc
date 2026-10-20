# -*- coding: utf-8 -*-
"""武器组覆盖：#4 col38 (武器组ID) vs #1 MSMA_WEAPONSET col0 / #2 MSMA_WEAPON_EQUIPCOMB col0。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge")


def rows(rel):
    with open(os.path.join(SEED, rel.replace("/", os.sep)), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return [l.rstrip() for l in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
            if l.strip() and not l.lstrip().startswith("#")]


cp = rows("msma/msma_settings.csv")
cp_keys = {r.split(",", 1)[0].strip() for r in cp}
grp = {r.split(",")[38].strip() for r in cp if len(r.split(",")) > 38 and r.split(",")[38].strip()}
print("#4 行 %d ／ col38 非空 %d ／ 唯一武器组 %d" % (len(cp), sum(
    1 for r in cp if len(r.split(",")) > 38 and r.split(",")[38].strip()), len(grp)))

ws = rows("msma/msma_weapon_set.csv")
ws_keys = {r.split(",", 1)[0].strip() for r in ws}
ec = rows("msma/msma_weapon_equipcomb.csv")
ec_keys = {r.split(",", 1)[0].strip() for r in ec}
print("#1 MSMA_WEAPONSET 行 %d ／唯一键 %d" % (len(ws), len(ws_keys)))
print("#2 MSMA_WEAPON_EQUIPCOMB 行 %d ／唯一键 %d" % (len(ec), len(ec_keys)))
print()
print("col38 未命中 #1 : %d %s" % (len(grp - ws_keys), sorted(grp - ws_keys)[:12]))
print("col38 未命中 #2 : %d %s" % (len(grp - ec_keys), sorted(grp - ec_keys)[:12]))
print("#1 键 - col38  : %d" % len(ws_keys - grp))
print("#2 键 - col38  : %d" % len(ec_keys - grp))
print()
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in ("MSMA_WEAPONSET", "MSMA_WEAPON_EQUIPCOMB"):
        cur.execute('select count(*) from cfg."%s"' % t)
        print("cfg.%-22s %d" % (t, cur.fetchone()[0]))
