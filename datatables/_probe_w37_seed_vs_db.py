# -*- coding: utf-8 -*-
"""_probe_w37_seed_vs_db.py —— #37：种子 34 列 vs 真库逐列对账（只读）

背景：抽看 `212301101` / `223005101` 时发现种子与库不一致
（种子 `223005101 = ONEHAND/MACHINEGUN/GUN_RAPID/SOLID`，
 库里同键 = `TWOHAND/WRESTLE/WRESTLE/BEAM`）。
本脚本给出**逐列差异规模**，判定"是不是该按种子重新收敛 #37 的 34 列"。

种子列号 → 库物理列名 的映射按 `#37` 列注释（CSV 列号 = 物理下标 - 1）。
"""
import collections
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


def main():
    with open(SEED, encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\r\n")
    seed = {}
    order = []
    for l in lines:
        if not l.strip() or l.startswith("#"):
            continue
        parts = l.split(",")
        if len(parts) < 34:
            parts = parts + [""] * (34 - len(parts))
        seed[parts[0].strip()] = parts[:34]
        order.append(parts[0].strip())
    print("种子数据行 %d ／ 去重键 %d" % (len(order), len(seed)))

    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT ordinal_position, column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                        ORDER BY ordinal_position""")
        phys = [(pos, name) for pos, name in cur.fetchall() if pos >= 2]
        # 实测 #1 的规则：CSV 列号 = 物理下标 - 2（phys1=_row_id 不算 CSV 列）
        want = [(csv, name) for pos, name in phys for csv in [pos - 2] if csv <= 33]
        cols = ", ".join('btrim("%s")' % n for _, n in want)
        cur.execute('SELECT ' + cols + ' FROM cfg."WEAPON_SETTING"')
        db = {}
        for row in cur.fetchall():
            db[row[0]] = row
        cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')

    both = sorted(set(seed) & set(db))
    print("库键 %d ／ 交集 %d ／ 只在种子 %d ／ 只在库 %d"
          % (len(db), len(both), len(set(seed) - set(db)), len(set(db) - set(seed))))
    print()
    print("=== 逐列差异（交集 %d 行内）===" % len(both))
    print("%-4s %-24s %-8s %s" % ("CSV", "库列名", "不同", "样本（库 → 种子）"))
    total_diff = 0
    for i, (csv, name) in enumerate(want):
        diff = 0
        samples = []
        for k in both:
            a = (db[k][i] or "").strip()
            b = (seed[k][csv] or "").strip()
            if a != b:
                diff += 1
                if len(samples) < 3:
                    samples.append("%s: %r→%r" % (k, a, b))
        total_diff += diff
        if diff:
            print("%-4d %-24s %-8d %s" % (csv, name, diff, " ; ".join(samples)))
    print()
    print("差异合计 %d 个单元格" % total_diff)

    print()
    print("=== 只在种子的键（库缺）===")
    print("  %s" % sorted(set(seed) - set(db)))
    print("=== 只在库的键（种子缺）===")
    print("  %s" % sorted(set(db) - set(seed)))


if __name__ == "__main__":
    main()
