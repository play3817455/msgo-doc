# -*- coding: utf-8 -*-
"""_probe_w36_shape.py —— #36 的形状：属性值到底存在哪（只读）

#37 的 148 个数据列里，只有 14 个有值：所有战斗数值列
（weapon_power / range_meter / *_multiplier / bullet_id …）**全空**。
本脚本查 #36 的形状，判定"数值是不是全在 #36 里、#37 只是壳"。
"""
import collections
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""SELECT ordinal_position, column_name, data_type
                     FROM information_schema.columns
                    WHERE table_schema='cfg' AND table_name='WEAPON_BATTLE_DETAIL'
                    ORDER BY ordinal_position""")
    cols = cur.fetchall()
    print("#36 WEAPON_BATTLE_DETAIL 物理列 %d 个" % len(cols))
    for pos, name, dt in cols:
        print("  phys %-3d CSV %-4s %-8s %s" % (pos, pos - 2, dt, name))
    cur.execute("""SELECT ordinal_position, column_name FROM information_schema.columns
                    WHERE table_schema='cfg' AND table_name='WEAPON_BATTLE_DETAIL'
                    ORDER BY ordinal_position""")
    c2 = cur.fetchone()
    cur.execute('SELECT count(*) FROM cfg."WEAPON_BATTLE_DETAIL"')
    print("总行 %d" % cur.fetchone()[0])
    cur.execute('SELECT count(DISTINCT btrim(attr_name)) FROM cfg."WEAPON_BATTLE_DETAIL"')
    print("去重 attr_name %d" % cur.fetchone()[0])

    print()
    print("=== attr_name 长度分布 ===")
    cur.execute("""SELECT length(btrim(attr_name)) l, count(*) FROM cfg."WEAPON_BATTLE_DETAIL"
                    GROUP BY 1 ORDER BY 1""")
    for l, n in cur.fetchall():
        print("  长度 %-3d 行 %d" % (l, n))

    print()
    print("=== attr_name 样本（按长度分组）===")
    for L in (5, 6, 8, 9, 10, 11):
        cur.execute("""SELECT btrim(attr_name) FROM cfg."WEAPON_BATTLE_DETAIL"
                        WHERE length(btrim(attr_name)) = %s LIMIT 6""", (L,))
        print("  长度 %-3d : %s" % (L, [r[0] for r in cur.fetchall()]))

    print()
    print("=== 抽一行 9 位（武器号）attr_name 的真值 ===")
    cur.execute("""SELECT * FROM cfg."WEAPON_BATTLE_DETAIL"
                    WHERE btrim(attr_name) = '211101101'""")
    row = cur.fetchone()
    if row:
        names = [d.name for d in cur.description]
        for n, v in zip(names, row):
            if str(v).strip() not in ("", "0", "None"):
                print("    %-24s = %r" % (n, v))
    else:
        print("    (没有该行)")

    print()
    print("=== #36 里哪个 attr_name 长得像武器号（9 位）且有多少 ===")
    cur.execute("""SELECT count(DISTINCT btrim(attr_name)) FROM cfg."WEAPON_BATTLE_DETAIL"
                    WHERE btrim(attr_name) ~ '^[0-9]{9}$'""")
    print("  9 位纯数字 attr_name：%d" % cur.fetchone()[0])

    print()
    print("=== 全表每列非空非 0 计数 ===")
    with psycopg.connect(DSN) as conn:
        for pos, name, dt in cols:
            cur = conn.cursor()
            sql = 'SELECT count(*) FROM cfg."WEAPON_BATTLE_DETAIL" WHERE btrim("' + name + "\"::text) NOT IN ('', '0')"
            cur.execute(sql)
            print("  %-24s 非空非0 %d / 9579" % (name, cur.fetchone()[0]))
