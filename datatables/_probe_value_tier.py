# -*- coding: utf-8 -*-
"""按列级口径重算「有真值 / 纯占位 / 空表」三档（口径：非主键列里是否存在"非空且非常量"的列）。"""
import sys
import psycopg

sys.stdout.reconfigure(encoding="utf-8")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute("""select table_name from information_schema.tables
                   where table_schema='cfg' order by table_name""")
    tables = [r[0] for r in cur.fetchall()]
    cur.execute("select table_name from meta.cfg_table_def")
    defined = set(r[0] for r in cur.fetchall())

    real, keyonly, empty = [], [], []
    for t in tables:
        cur.execute(f'select * from cfg."{t}" limit 0')
        cols = [d.name for d in cur.description if d.name != "_row_id"]
        cur.execute(f'select count(*) from cfg."{t}"')
        n = cur.fetchone()[0]
        if n == 0:
            empty.append((t, len(cols)))
            continue
        nonkey = cols[1:]
        if not nonkey:
            keyonly.append((t, len(cols), n))
            continue
        sel = ", ".join(f'count(distinct btrim({cols[i]}::text))' for i in range(1, len(cols)))
        cur.execute(f'select {sel} from cfg."{t}"')
        dists = cur.fetchone()
        # 有值列（distinct > 1 或 distinct == 1 但非空）
        alive = [cols[i + 1] for i, d in enumerate(dists) if d > 1]
        anyval = [cols[i + 1] for i, d in enumerate(dists) if d == 1]
        if alive:
            real.append((t, len(cols), n, len(alive)))
        else:
            keyonly.append((t, len(cols), n))

    print(f"总表 {len(tables)}；有真值(存在非常量非空列) {len(real)}；纯占位 {len(keyonly)}；空表 {len(empty)}")
    print("\n有真值表：")
    for t, w, n, a in sorted(real):
        print(f"   {t:34s} 列={w:3d} 行={n:6d} 非常量列={a}")
    print("\n纯占位（含'全部列同常量'与'仅主键'）：")
    for t, w, n in sorted(keyonly):
        tag = "" if t in defined else "  <不在 schema>"
        print(f"   {t:34s} 列={w:3d} 行={n:6d}{tag}")
    print("\n空表：", [(t, w) for t, w in sorted(empty)])
    print("\ncfg 有表但 meta.cfg_table_def 无:", sorted(set(tables) - defined))
    print("meta.cfg_table_def 有但 cfg 无表:", sorted(defined - set(tables)))
