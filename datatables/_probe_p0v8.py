# -*- coding: utf-8 -*-
"""P0 复核 v8：库 MSMA_WEAPONSET vs 种子 CSV —— 逐行对账，找列错位/丢行。

只报告，不写。
"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")


def lens(vals):
    d = {}
    for v in vals:
        d[len(v)] = d.get(len(v), 0) + 1
    return dict(sorted(d.items()))


def main():
    rows = list(csv.reader(open(SEED, encoding="utf-8-sig", errors="replace")))
    data = [r for r in rows[1:] if r and r[0].strip() and not r[0].startswith("#")]
    print("种子 CSV: %d 列 / %d 行" % (max(len(r) for r in data), len(data)))
    print("  col0 去重 %d 长度 %s 样例 %s"
          % (len({r[0].strip() for r in data}), lens({r[0].strip() for r in data}),
             sorted({r[0].strip() for r in data})[:5]))
    for i in range(0, 6):
        vals = {r[i].strip() for r in data if len(r) > i and r[i].strip()}
        print("  col%d: 去重 %-5d 长度 %s 样例 %s"
              % (i, len(vals), lens(vals), sorted(vals)[:4]))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""select column_name from information_schema.columns
                        where table_schema='cfg' and table_name='MSMA_WEAPONSET'
                        order by ordinal_position""")
        dcols = [r[0] for r in cur.fetchall()]
        print("\n库列 %d: %s" % (len(dcols), dcols[:6]))
        cur.execute('select %s from cfg."MSMA_WEAPONSET"'
                    % ",".join('btrim(coalesce("%s"::text,\'\'))' % c for c in dcols))
        dbrows = cur.fetchall()
        print("库行数 %d" % len(dbrows))

        # 找出库里可能有 8 位号的任意列
        for j, c in enumerate(dcols):
            vals = {r[j] for r in dbrows if r[j]}
            if not vals:
                continue
            L = lens(vals)
            if 8 in L or 7 in L or 5 in L:
                print("   列 %-28s 去重 %-5d 长度 %s 样例 %s"
                      % (c, len(vals), L, sorted(vals)[:4]))

        # 逐行对账：种子 (col0, col2) 是否在库
        dbpairs = {(r[dcols.index("weapon_group_id")], r[dcols.index("weapon_item_id")])
                   for r in dbrows}
        seedpairs = {(r[0].strip(), r[2].strip()) for r in data}
        print("\n=== (组ID, 武器物品ID) 对账 ===")
        print("  种子对 %d / 库对 %d / 交集 %d" % (len(seedpairs), len(dbpairs),
                                                len(seedpairs & dbpairs)))
        miss = sorted(seedpairs - dbpairs)
        print("  种子有库没有 %d；样例 %s" % (len(miss), miss[:5]))
        print("  库有种子没有 %d；样例 %s" % (len(dbpairs - seedpairs),
                                            sorted(dbpairs - seedpairs)[:5]))
        # 种子缺失行：它们的组ID在库里有吗？
        gdb = {r[dcols.index("weapon_group_id")] for r in dbrows}
        print("  种子缺失行的组ID 在库出现过的 = %d / %d"
              % (sum(1 for g, _ in miss if g in gdb), len(miss)))

        # 逐行比对同一组内的行数
        from collections import Counter
        cs = Counter(g for g, _ in seedpairs)
        cd = Counter(r[dcols.index("weapon_group_id")] for r in dbrows)
        big = [(g, cs[g], cd.get(g, 0)) for g in cs if abs(cs[g] - cd.get(g, 0)) > 0]
        print("  组内行数不一致的组 %d 个；样例 %s" % (len(big), big[:8]))


if __name__ == "__main__":
    main()
