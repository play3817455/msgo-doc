# -*- coding: utf-8 -*-
"""全库 `cfg` 列 `NULL → ''` 归一（cfg 口径：空值一律是空串）。

由来：前两批用 `ADD COLUMN` 补出来的列在**旧行**里是 `NULL`（`ADD COLUMN` 不写默认值），
而 cfg 其余列都是 `''`（`ExportTableRawCSV` 两者都导出成空字段，故此前无可见影响）。
附录 C.7 记为遗留 —— 本脚本一次扫全库、一次改干净。

自证：改前/改后把 **全部** `meta.cfg_manifest.raw_csv` 取 sha256 —— 必须逐字节相同。
"""
import hashlib
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def hashes(cur):
    cur.execute("SELECT file, raw_csv FROM meta.cfg_manifest ORDER BY file")
    out = {}
    for f, raw in cur.fetchall():
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
        out[f] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return out


DRY = "-dry" in sys.argv
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute("""SELECT table_name, column_name FROM information_schema.columns
                   WHERE table_schema='cfg' AND column_name<>'_row_id'
                   ORDER BY table_name, ordinal_position""")
    cols = cur.fetchall()
    before = hashes(cur)
    total = 0
    hit = 0
    for t, c in cols:
        cur.execute(f'SELECT count(*) FROM cfg."{t}" WHERE "{c}" IS NULL')
        n = cur.fetchone()[0]
        if not n:
            continue
        hit += 1
        total += n
        print(f"  {t}.{c}: {n} 格 NULL" + ("（dry）" if DRY else ""))
        if not DRY:
            cur.execute(f'UPDATE cfg."{t}" SET "{c}" = %s WHERE "{c}" IS NULL', ("",))
    if not DRY:
        conn.commit()
    after = hashes(cur)

print(f"共 {hit} 列、{total} 格 NULL" + ("（dry run，未改）" if DRY else " → ''"))
if DRY:
    sys.exit(0)
bad = [f for f in before if before[f] != after.get(f)]
print(f"manifest raw_csv sha256：{len(before)} 张表，{'全部未变 ✓' if not bad else '★变了 ' + str(bad)}")
sys.exit(1 if bad else 0)
