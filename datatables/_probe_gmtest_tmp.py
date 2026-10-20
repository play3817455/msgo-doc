# -*- coding: utf-8 -*-
"""查 `cfg.gmtest_tmp`：它出现在 meta.cfg_manifest 里，但 db_design/schema/cfg/tables 下没有对应 JSON。
只读。
"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select table_name from information_schema.tables"
                " where table_schema='cfg' order by 1")
    tables = [r[0] for r in cur.fetchall()]
    print("cfg 物理表 %d 张" % len(tables))
    print("  含 gmtest 的：%s" % [t for t in tables if "gmtest" in t.lower()])

    cur.execute("select table_name, column_name, data_type from information_schema.columns"
                " where table_schema='cfg' and lower(table_name) like '%%gmtest%%'"
                " order by ordinal_position")
    cols = cur.fetchall()
    for t, cname, dt in cols:
        print("    %s.%s  %s" % (t, cname, dt))

    for (t,) in [(x,) for x in tables if "gmtest" in x.lower()]:
        cur.execute('select count(*) from cfg."%s"' % t)
        n = cur.fetchone()[0]
        print("    → %s 行数 %d" % (t, n))
        cur.execute('select * from cfg."%s" limit 5' % t)
        for r in cur.fetchall():
            print("       %r" % (r,))

    cur.execute("select count(*) from meta.cfg_manifest")
    print()
    print("meta.cfg_manifest 行数 %d" % cur.fetchone()[0])
    cur.execute("select file from meta.cfg_manifest where lower(file) like '%%gmtest%%'"
                " or lower(file) like '%%bgm%%' or lower(file) like '%%lvup_msma%%'"
                " or lower(file) like '%%msma_material%%' or lower(file) like '%%overwrite%%'")
    print("  本地/测试表在 manifest 里：%s" % [r[0] for r in cur.fetchall()])
