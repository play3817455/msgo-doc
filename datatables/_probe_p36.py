# -*- coding: utf-8 -*-
"""#36 WEAPON_BATTLE_DETAIL (EAV) 属性分布 + POWER 覆盖度哨兵。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select distinct attr_name from cfg."WEAPON_BATTLE_DETAIL" '
                "order by 1")
    names = [r[0] for r in cur.fetchall()]
    print("attr_name(%d): %s" % (len(names), names))
    cur.execute('select count(distinct weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
    print("distinct weapon_id_key:", cur.fetchone()[0])
    print()
    print("== 每属性覆盖的武器数 ==")
    for n in names:
        cur.execute('select count(distinct weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL" '
                    "where attr_name=%s", (n,))
        print("  %-16s %s" % (n, cur.fetchone()[0]))
    print()
    print("== 无 POWER 的武器 ==")
    cur.execute(
        'select distinct weapon_id_key from cfg."WEAPON_BATTLE_DETAIL" '
        "where weapon_id_key not in (select weapon_id_key from cfg.\"WEAPON_BATTLE_DETAIL\" "
        "where attr_name='POWER') order by weapon_id_key")
    for (w,) in cur.fetchall():
        print("  ", w)
