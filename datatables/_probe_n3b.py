# -*- coding: utf-8 -*-
"""#20 MECHANIC_MSMA 键 1124102 溯源 + #50 MODULE 枚举求证。"""
import sys
import psycopg

sys.stdout.reconfigure(encoding="utf-8")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()

    def dom(t, col):
        cur.execute(f'select btrim({col}::text), count(*) over () from cfg."{t}" limit 1')
        r = cur.fetchall()
        if not r:
            return set()
        cur.execute(f'select btrim({col}::text) from cfg."{t}"')
        return set(x[0] for x in cur.fetchall())

    print("=== 键域 ===")
    for t, col in [("MSMA_MODULE", "msma_id"), ("CHARA_PARAM", "msma_id"),
                   ("MECHANIC_WEAPON", "col0"), ("MODULE", "module_id"),
                   ("MECHANIC_MSMA", "col0"), ("ITEM", "item_id")]:
        try:
            d = dom(t, col)
            print(f"  {t}.{col}: n={len(d)} 含1124102={'1124102' in d} 含4011301={'4011301' in d}")
        except Exception as e:
            print(f"  {t}.{col}: 错误 {str(e).splitlines()[0]}")

    print("\n=== MECHANIC_MSMA.col0 逐键溯源 ===")
    cur.execute('select btrim(col0::text) from cfg."MECHANIC_MSMA"')
    for (k,) in cur.fetchall():
        hits = []
        for t, col in [("MSMA_MODULE", "msma_id"), ("CHARA_PARAM", "msma_id"),
                       ("MECHANIC_WEAPON", "col0"), ("MECHANIC_SUCCESS", "odds_key"),
                       ("MODULE", "module_id"), ("ITEM", "item_id")]:
            try:
                d = dom(t, col)
                if k in d:
                    hits.append(f"{t}.{col}")
            except Exception:
                pass
        print(f"  {k!r} -> {hits if hits else '无上游命中'}")

    print("\n=== MODULE 值域细节 ===")
    cur.execute('select btrim(linked_item_id::text) from cfg."MODULE"')
    print("  linked_item_id 取值:", set(x[0] for x in cur.fetchall()))
    cur.execute('select btrim(slot_index::text), count(*) from cfg."MODULE" group by 1 order by 1')
    print("  slot_index:", cur.fetchall())
    cur.execute('select btrim(param_a::text), count(*) from cfg."MODULE" group by 1 order by 1')
    print("  param_a:", cur.fetchall())
    cur.execute('select btrim(unlock_level::text), count(*) from cfg."MODULE" group by 1 order by 1')
    print("  unlock_level:", cur.fetchall())
    cur.execute('select btrim(reserved_u32_1::text), btrim(param_b::text), btrim(reserved_u32_6::text) '
                'from cfg."MODULE" order by _row_id')
    print("  (res1,param_b,res6) 前3行:", cur.fetchall()[:3])

    print("\n=== 上游 MSMA_MODULE 里 4011301 系列的出现情况 ===")
    cur.execute('select msma_id, module_slot_0, module_slot_1, module_slot_2 from cfg."MSMA_MODULE" order by _row_id limit 5')
    for r in cur.fetchall():
        print("   ", r)
