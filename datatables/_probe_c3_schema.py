# -*- coding: utf-8 -*-
import os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select column_name, data_type, is_nullable, column_default
                   from information_schema.columns
                   where table_schema='cfg' and table_name='WEAPON_BATTLE_DETAIL'
                   order by ordinal_position""")
    for r in cur.fetchall():
        print("  %-18s %-28s null=%-4s default=%s" % r)
    cur.execute("""select indexdef from pg_indexes where schemaname='cfg' and tablename='WEAPON_BATTLE_DETAIL'""")
    print("索引：", cur.fetchall())
    cur.execute('select count(*) from cfg."WEAPON_BATTLE_DETAIL"')
    print("总行数", cur.fetchone()[0])
    cur.execute("""select btrim(attr_name), count(*) from cfg."WEAPON_BATTLE_DETAIL"
                   group by 1 order by 2 desc""")
    print("属性分布：", cur.fetchall())
