# -*- coding: utf-8 -*-
"""看 manifest header_text 现状：多行注释头是否还在"""
import io
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select count(*) from meta.cfg_manifest")
    print("manifest 行数", cur.fetchone()[0])
    cur.execute("select count(*) from meta.cfg_manifest where header_text like '%' || chr(10) || '%'")
    print("多行 header 行数", cur.fetchone()[0])
    cur.execute(
        "select file, length(header_text)-length(replace(header_text, chr(10), '')) as nl, row_count "
        "from meta.cfg_manifest order by nl desc, file limit 12"
    )
    for f, nl, rc in cur.fetchall():
        print(f"   {f:<28} 换行 {nl} rows {rc}")
