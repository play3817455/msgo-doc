# -*- coding: utf-8 -*-
"""查看 meta.cfg_manifest / cfg_table_def 中 MODULE 的登记形态，确定改列的落点。"""
import sys
import psycopg

sys.stdout.reconfigure(encoding="utf-8")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute("select table_name from information_schema.tables where table_schema='meta' order by 1")
    print("meta 表:", [r[0] for r in cur.fetchall()])

    for t in ("cfg_manifest", "cfg_table_def"):
        try:
            cur.execute(f'select * from meta.{t} limit 0')
            cols = [d.name for d in cur.description]
            print(f"\nmeta.{t} 列:", cols)
            key = "table_id" if "table_id" in cols else cols[0]
            cur.execute(f"select * from meta.{t} where btrim({key}::text) in ('50','MODULE') limit 3")
            for r in cur.fetchall():
                print("  行:", r)
            cur.execute(f"select count(*) from meta.{t}")
            print("  总行数:", cur.fetchone()[0])
        except Exception as e:
            print(f"\nmeta.{t}: {str(e).splitlines()[0]}")

    # 找 manifest 里的 MODULE 列定义
    cur.execute("select table_name from information_schema.tables where table_schema='meta' order by 1")
    for (t,) in cur.fetchall():
        try:
            cur.execute(f'select * from meta."{t}" limit 0')
            cols = [d.name for d in cur.description]
            if any("col" in x or "name" in x for x in cols):
                cur.execute(f'''select * from meta."{t}" where to_jsonb(meta."{t}")::text like '%4011301%' limit 2''')
                rr = cur.fetchall()
                if rr:
                    print(f"\n★ meta.{t} 命中 MODULE 数据: 列={cols}")
                    for r in rr:
                        print("   ", r)
        except Exception as e:
            pass
