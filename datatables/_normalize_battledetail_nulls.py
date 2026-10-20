# -*- coding: utf-8 -*-
"""把本批补出来的值槽列的 `NULL` 归一成 `''`（cfg 其余列都是 `''` 口径，`ExportTableRawCSV` 两者都导出成空字段）。

自证：先把两张表的 `raw_csv` 取哈希，`UPDATE` 之后再取一次 —— **必须逐字节相同**（下发件不受影响），
列/行数/原列取值由 `_verify_battledetail.py` 复查。
"""
import hashlib
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# 本批 ADD COLUMN 加出来、且带 NULL 的列
NEW_COLS = {
    "WEAPON_BATTLE_DETAIL": ["attr_value_3", "attr_value_4", "attr_value_5",
                             "attr_value_6", "attr_value_7"],
    "MSMA_BATTLE_DETAIL": [f"entry_value_{i}" for i in range(2, 15)],
}


def manifest_hashes(cur, tables):
    cur.execute("SELECT file, raw_csv FROM meta.cfg_manifest WHERE file = ANY(%s)", (tables,))
    out = {}
    for f, raw in cur.fetchall():
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
        out[f] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return out


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    tables = sorted(NEW_COLS)
    before = manifest_hashes(cur, tables)
    for t, cols in NEW_COLS.items():
        fixed = 0
        for c in cols:
            cur.execute(f'UPDATE cfg."{t}" SET "{c}" = %s WHERE "{c}" IS NULL', ("",))
            fixed += cur.rowcount
        print(f"[{t}] {len(cols)} 列 NULL → ''：改写 {fixed} 格")
    conn.commit()
    after = manifest_hashes(cur, tables)

for t in tables:
    same = before.get(t) == after.get(t)
    print(f"[{t}] manifest raw_csv sha256 {'未变 ✓' if same else '★变了 ✗'}  {before.get(t)}")
    if not same:
        sys.exit(1)
print("OK：NULL → '' 归一完成，下发件逐字节未变")
