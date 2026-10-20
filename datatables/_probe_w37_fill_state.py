# -*- coding: utf-8 -*-
"""武器链体检：各表填充态 + #37 全列非空分布 + #36 属性族分布。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

CHAIN = ["WEAPON_SETTING", "WEAPON_BATTLE_DETAIL", "BULLET", "WRESTLE_PARAM",
         "DAMAGE_FIELD_PARAM", "BUILDUP_WEAPON", "BUFF", "AI_WEAPON_PARAM",
         "MECHANIC_WEAPON", "MSMA_WEAPONSET", "MSMA_WEAPON_EQUIPCOMB", "ITEM"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    print("=== 武器链各表填充态 ===")
    print("%-24s %6s %6s %-s" % ("表", "行数", "列数", "非空列（列名:非空行数）"))
    for t in CHAIN:
        cur.execute("select column_name from information_schema.columns"
                    " where table_schema='cfg' and table_name=%s order by ordinal_position", (t,))
        cols = [r[0] for r in cur.fetchall()]
        cur.execute('select count(*) from cfg."%s"' % t)
        n = cur.fetchone()[0]
        nz = []
        for cc in cols:
            if cc in ("_row_id",):
                continue
            cur.execute('select count(*) from cfg."%s" where btrim(coalesce("%s"::text,\'\'))'
                        " not in ('', '0')" % (t, cc))
            k = cur.fetchone()[0]
            if k:
                nz.append("%s:%d" % (cc, k))
        print("%-24s %6d %6d %s" % (t, n, len(cols),
                                    ("、".join(nz) if len(nz) <= 14
                                     else "、".join(nz[:14]) + " …共 %d 列" % len(nz))))
    print()

    print("=== #36 WEAPON_BATTLE_DETAIL 属性族分布 ===")
    cur.execute('select btrim(attr_name), count(*), count(distinct btrim(weapon_id_key))'
                ' from cfg."WEAPON_BATTLE_DETAIL" group by 1 order by 2 desc')
    for a, n, k in cur.fetchall():
        print("   %-14s 行 %6d ／ 武器键 %5d" % (a, n, k))
    cur.execute('select count(distinct btrim(weapon_id_key)) from cfg."WEAPON_BATTLE_DETAIL"')
    print("   武器键去重合计 %d ／ #37 行 1648" % cur.fetchone()[0])
