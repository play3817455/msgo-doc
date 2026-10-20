# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FXDIR = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline", "unpackdat", "fx")
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
with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as conn:
    cur = conn.cursor()
    cur.execute('select * from cfg."BULLET" order by _row_id limit 12')
    cols = [d.name for d in cur.description]
    rows = cur.fetchall()
    print("BULLET 前 12 行：")
    for r in rows:
        nz = {c: v for c, v in zip(cols, r) if v not in (None, "", "0", "0.0", "0.000000")}
        print("   %s" % nz)
    print()
    cur.execute('select count(*) from cfg."BULLET"')
    print("BULLET 行数 %d" % cur.fetchone()[0])
    for c in cols:
        if c == "_row_id":
            continue
        cur.execute('select distinct btrim("%s"::text) from cfg."BULLET"' % c)
        vals = sorted({r[0] for r in cur.fetchall() if r[0] and r[0] != ""})
        if vals:
            hit = [v for v in vals if v.isdigit() and int(v) in IDS]
            print("   %-22s 去重 %3d  样例 %-42s FX命中 %s"
                  % (c, len(vals), str(vals[:4])[:42], hit[:4]))
