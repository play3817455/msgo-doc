# -*- coding: utf-8 -*-
"""_probe_eightdigit_survivors.py —— 收敛后仍然留在库里的 8 位号（只读）

收敛前 cfg.MSMA_WEAPONSET 有 1181 行 8 位武器，其中 36 行**在 #37 里有行**
（其余 1145 行是断引用）。这 36 行随收敛一起被移除 ⇒ 它们引用的 #37 行现在
可能变成**没人引用的 8 位残留**。本脚本查清：

  ① 真库 #37 / #36 / #78 ITEM 各自的号形分布（8 位 / 9 位）
  ② 那 36 个 8 位号在 #37 里到底有没有行、行长什么样
  ③ 现在还有谁引用它们
  ④ 收敛后 #37 里所有 8 位键的引用方统计
"""
import collections
import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROLLBACK = os.path.join(HERE, "_rollback", "20261005_120824_MSMA_WEAPONSET_full.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def shapes(vals):
    c = collections.Counter(len(v) for v in vals if v)
    return dict(sorted(c.items()))


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                          AND ordinal_position = 2""")
        k37 = cur.fetchone()[0]
        cur.execute('SELECT btrim("' + k37 + '") FROM cfg."WEAPON_SETTING"')
        d37 = [r[0] for r in cur.fetchall()]
        print("  #37 键列 = %s" % k37)
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_BATTLE_DETAIL'
                          AND ordinal_position = 2""")
        k36 = cur.fetchone()[0]
        cur.execute('SELECT btrim("' + k36 + '") FROM cfg."WEAPON_BATTLE_DETAIL"')
        d36 = [r[0] for r in cur.fetchall()]
        print("  #36 键列 = %s" % k36)
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='ITEM'
                          AND ordinal_position = 2""")
        k78 = cur.fetchone()[0]
        cur.execute('SELECT btrim("' + k78 + '") FROM cfg."ITEM"')
        d78 = [r[0] for r in cur.fetchall()]
        print("  #78 键列 = %s" % k78)
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='MSMA_WEAPONSET'
                          AND ordinal_position = 4""")
        kms = cur.fetchone()[0]
        cur.execute('SELECT btrim("' + kms + '") FROM cfg."MSMA_WEAPONSET"')
        ms = [r[0] for r in cur.fetchall()]
        print("  #1 武器号列 = %s" % kms)

    print("=== ① 号形分布（长度 → 个数）===")
    print("  #37 WEAPON_SETTING   %d 键  %s" % (len(set(d37)), shapes(d37)))
    print("  #36 WEAPON_BATTLE_DT %d 键  %s" % (len(set(d36)), shapes(d36)))
    print("  #78 ITEM             %d 键  %s" % (len(set(d78)), shapes(d78)))
    print("  #1  MSMA_WEAPONSET   %d 键  %s" % (len(set(ms)), shapes(ms)))

    eight37 = sorted({v for v in d37 if len(v) == 8})
    print()
    print("=== ④ 真库 #37 里仍存在的 8 位键：%d 个 ===" % len(eight37))
    print("  例：%s" % eight37[:12])
    ref = [v for v in eight37 if v in set(ms)]
    print("  被 #1 MSMA_WEAPONSET 引用的：%d" % len(ref))

    print()
    print("=== ② 收敛前那 36 个「有 #37 行的 8 位号」 ===")
    with open(ROLLBACK, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")
                and r[0].strip() not in ("_row_id", "id", "")]
    dset = set(d37)
    hit = sorted({(r[1].strip(), r[3].strip()) for r in rows
                  if len(r[3].strip()) == 8 and r[3].strip() in dset})
    print("  去重 (组, 武器) 对：%d" % len(hit))
    for g, i in hit[:20]:
        print("    %s → %s" % (g, i))
    ids = sorted({i for _, i in hit})
    print("  涉及武器号 %d 个" % len(ids))
    print("  这些号在 #37 有行 %d ／ 在 #36 有行 %d ／ 在 #78 ITEM 有行 %d"
          % (sum(1 for i in ids if i in dset),
             sum(1 for i in ids if i in set(d36)),
             sum(1 for i in ids if i in set(d78))))

    print()
    print("=== ③ 现在还有谁引用 #37 的 8 位键 ===")
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name, column_name FROM information_schema.columns
             WHERE table_schema = 'cfg' AND data_type IN ('text','character varying')
               AND table_name <> 'WEAPON_SETTING'
             ORDER BY table_name, ordinal_position
        """)
        cols = cur.fetchall()
    eight = set(eight37)
    for t, c in cols:
        try:
            with psycopg.connect(DSN) as conn:
                cur = conn.cursor()
                cur.execute('SELECT btrim("' + c + '") FROM cfg."' + t + '"')
                vals = {r[0] for r in cur.fetchall()}
        except Exception:  # noqa: BLE001
            continue
        inter = vals & eight
        if inter:
            print("  %-22s %-24s %d 个 → %s" % (t, c, len(inter), sorted(inter)[:6]))


if __name__ == "__main__":
    main()
