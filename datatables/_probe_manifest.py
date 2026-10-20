# -*- coding: utf-8 -*-
"""临时取证：`meta.cfg_manifest` 里 #36/#37 的**在发** raw_csv 与「当前库导出」是否一致。

背景（决定性）：`serverv/internal/cfg/csv_export.go::ExportTableRawCSV` 是
**从 cfg.{table} 行按 information_schema 物理列序拼出 CSV**，再由 `sync_db.go::exportManifest`
写进 `meta.cfg_manifest.raw_csv`；`dbstore.go` 明确 "Runtime must not read CSV from disk"。
⇒ **客户端实际下载到的是「库的导出」，不是 `server/datafiles/` 下的种子 CSV**。

只报告，不写。
"""
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    for tbl in ("WEAPON_BATTLE_DETAIL", "WEAPON_SETTING"):
        cur.execute("""select column_name from information_schema.columns
                        where table_schema='cfg' and table_name=%s
                        order by ordinal_position""", (tbl,))
        cols = [r[0] for r in cur.fetchall()]
        print("== cfg.\"%s\" 列数 %d" % (tbl, len(cols)))
        print("   列序:", cols[:6], "...", cols[-3:])
        cur.execute('select count(*) from cfg."%s"' % tbl)
        print("   行数:", cur.fetchone()[0])

    print()
    cur.execute("""select file, filepath, row_count, octet_length(raw_csv), sha256
                     from meta.cfg_manifest
                    where file in ('WEAPON_BATTLE_DETAIL','WEAPON_SETTING')
                       or filepath like '%%weapon%%'
                    order by file""")
    for f, fp, rc, ob, sh in cur.fetchall():
        print("== manifest %s  filepath=%s rows=%s bytes=%s sha=%s"
              % (f, fp, rc, ob, (sh or "")[:16]))

    # 在发的 #36 raw_csv 头几行 + 是否含已净化值
    cur.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_BATTLE_DETAIL'")
    row = cur.fetchone()
    if row and row[0]:
        raw = row[0] if isinstance(row[0], str) else row[0].decode("utf-8", "replace")
        lines = raw.replace("\r\n", "\n").split("\n")
        data = [l for l in lines if l.strip() and not l.startswith("#")]
        print()
        print("== 在发 #36 raw_csv：%d 行数据，sha=%s" % (len(data), hashlib.sha256(raw.encode()).hexdigest()[:16]))
        print("   头 4 行:", data[:4])
        for probe in ("STABILITY,01010401,", "STABILITY,1010401,", "RELOAD,1010401,"):
            hit = [l for l in data if l.startswith(probe)]
            print("   含 %-24s -> %s" % (probe, hit[:1] or "无"))
        print("   字段数分布:", sorted({len(l.split(',')) for l in data}))
    cur2 = conn.cursor()
    cur2.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_SETTING'")
    row = cur2.fetchone()
    if row and row[0]:
        raw = row[0] if isinstance(row[0], str) else row[0].decode("utf-8", "replace")
        data = [l for l in raw.replace("\r\n", "\n").split("\n") if l.strip() and not l.startswith("#")]
        print()
        print("== 在发 #37 raw_csv：%d 行数据" % len(data))
        print("   字段数分布:", sorted({len(l.split(',')) for l in data}))
        print("   头 1 行:", data[:1])
