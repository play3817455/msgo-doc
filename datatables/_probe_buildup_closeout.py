# -*- coding: utf-8 -*-
"""_probe_buildup_closeout.py —— t6 收口复核（只读）

① cfg.BUILDUP_WEAPON 全部 64 行里哪些非空，第 1 行逐列真值
② 种子 develop/buildup_weapon.csv 第 1 行逐列真值（对照）
③ cfg.MECHANIC_WEAPON 里 BUILDUP_GREATEST 一行的 success_rate_*（面板公式的另一半）
④ 有多少把武器把 col64 指向 buildup_id=1
"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "develop", "buildup_weapon.csv")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"


def _count(dsn, sql):
    with psycopg.connect(dsn) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def main():
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='BUILDUP_WEAPON'
                        ORDER BY ordinal_position""")
        cols = [r[0] for r in cur.fetchall()]
        cur.execute('SELECT * FROM cfg."BUILDUP_WEAPON" ORDER BY _row_id')
        rows = cur.fetchall()

    print("=== ① cfg.BUILDUP_WEAPON ===")
    print("列（%d）：%s" % (len(cols), cols))
    print("总行 %d" % len(rows))

    def nz(v):
        return str(v if v is not None else "").strip() not in ("", "0")

    nonempty = []
    for r in rows:
        if any(nz(v) for v in r[2:]):
            nonempty.append(r)
    print("  非空行（除键列以外有非 0 值）合计 %d / %d" % (len(nonempty), len(rows)))
    for r in nonempty:
        print("    _row_id=%s  buildup_id=%s  %s"
              % (r[0], r[1], " ".join("%s=%s" % (c, v) for c, v in zip(cols, r)
                                      if nz(v) and c != "_row_id")))
    if rows:
        print()
        print("第 1 行逐列：")
        for c, v in zip(cols, rows[0]):
            print("    %-22s = %r" % (c, v))

    print()
    print("=== ② 种子 CSV 第 1 行 ===")
    if not os.path.exists(SEED):
        print("  找不到 %s" % SEED)
    else:
        with open(SEED, encoding="utf-8-sig", newline="") as fh:
            rdr = list(csv.reader(fh))
        data = [r for r in rdr if r and r[0].strip() and not r[0].startswith("#")]
        print("  数据行 %d" % len(data))
        print("  第 1 行：%s" % (data[0] if data else "(空)"))
        filled = [r for r in data if any(c.strip() not in ("", "0") for c in r[1:])]
        print("  有非空单元格的行数：%d / %d" % (len(filled), len(data)))

    print()
    print("=== ③ cfg.MECHANIC_WEAPON 的 BUILDUP_GREATEST ===")
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='MECHANIC_WEAPON'
                        ORDER BY ordinal_position""")
        mcols = [r[0] for r in cur.fetchall()]
        inner = mcols[1]
        cur.execute('SELECT * FROM cfg."MECHANIC_WEAPON" ORDER BY _row_id')
        mrows = cur.fetchall()
    print("  列：%s" % mcols)
    for r in mrows:
        if (r[1] or "").strip() == "BUILDUP_GREATEST":
            print("  %s" % dict(zip(mcols, r)))
    print("  共 %d 行" % len(mrows))

    print()
    print("=== ④ 指向 buildup_id=1 的武器 ===")
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT column_name FROM information_schema.columns
                        WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                          AND ordinal_position = 65""")
        c64 = cur.fetchone()
        print("  #37 第 65 个物理列 = %s" % (c64[0] if c64 else "(无)"))
        if c64:
            print("  #37 总行数：%d" % _count(DSN, "SELECT count(*) FROM cfg.\"WEAPON_SETTING\""))
            print("  btrim(col63) = '1' 的行数：%d"
                  % _count(DSN, 'SELECT count(*) FROM cfg."WEAPON_SETTING" WHERE btrim("'
                           + c64[0] + "\") = '1'"))
            print("  非空非 0 的行数：%d"
                  % _count(DSN, 'SELECT count(*) FROM cfg."WEAPON_SETTING" WHERE btrim("'
                           + c64[0] + "\") NOT IN ('', '0')"))
            cur.execute('SELECT count(*) FROM cfg."WEAPON_SETTING"')
            print("  #37 总行数：%d" % cur.fetchone()[0])


if __name__ == "__main__":
    main()
