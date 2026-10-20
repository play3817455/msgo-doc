# -*- coding: utf-8 -*-
"""_probe_bullet.py —— #BULLET 里有没有 7 位打包 FX ID？（上轮扫描只覆盖 text 列，漏了 int 列）"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

FXDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "机动战士敢达Online", "GundamOnline", "unpackdat", "fx")
PAT = re.compile(r"^PP_(\d{2})_(\d{3})_(\d{2})\.vra$", re.I)
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


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

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    for tbl in ("BULLET", "DAMAGE_FIELD_PARAM"):
        cur.execute("select column_name,data_type from information_schema.columns"
                    " where table_schema='cfg' and table_name=%s order by ordinal_position", (tbl,))
        cols = cur.fetchall()
        cur.execute('select count(*) from cfg."%s"' % tbl)
        n = cur.fetchone()[0]
        print("=== %s（%d 行 × %d 列）===" % (tbl, n, len(cols)))
        for c, t in cols:
            print("   %-24s %s" % (c, t))
        print()

        # 每个列扫：既看整值在 IDS 里，也看"整值二次打包"的可能
        for c, t in cols:
            try:
                cur.execute('select distinct btrim("%s"::text) from cfg."%s"'
                            ' where btrim("%s"::text) ~ \'^[0-9]{4,9}$\'' % (c, tbl, c))
            except Exception:
                conn.rollback()
                continue
            vals = [r[0] for r in cur.fetchall() if r[0]]
            if not vals:
                continue
            hit = [v for v in vals if int(v) in IDS]
            if hit:
                print("   ★ %s.%s：%d/%d 值 = 合法 FX a2  样例 %s"
                      % (tbl, c, len(hit), len(vals), hit[:5]))
        print()

    print("=== 全库复查：**所有**列（含 int）落进合法 a2 集合的 ===")
    cur.execute("select table_name, column_name, data_type from information_schema.columns"
                " where table_schema='cfg' and data_type not in ('boolean','bytea')"
                " order by table_name, ordinal_position")
    cols = cur.fetchall()
    total = 0
    for t, c, dt in cols:
        try:
            cur.execute('select distinct btrim("%s"::text) from cfg."%s"'
                        ' where btrim("%s"::text) ~ \'^[0-9]{5,7}$\'' % (c, t, c))
        except Exception:
            conn.rollback()
            continue
        vals = [r[0] for r in cur.fetchall() if r[0]]
        if not vals:
            continue
        hit = [v for v in vals if int(v) in IDS]
        if hit and len(hit) >= 3:
            total += 1
            print("   %-26s %-22s %-10s %4d/%-5d %s" % (t, c, dt, len(hit), len(vals), hit[:4]))
    print("   命中列数 %d" % total)
