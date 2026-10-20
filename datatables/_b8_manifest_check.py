# -*- coding: utf-8 -*-
"""核对 meta.cfg_manifest 里 CHARA_MODEL / MSMA_WEAPONSET 的 header 与 raw_csv 列数。"""
import io
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in ("CHARA_MODEL", "MSMA_WEAPONSET", "CHARA_PARAM", "ITEM_PART"):
        cur.execute("select header_text, row_count, filepath, length(raw_csv) from meta.cfg_manifest where file=%s", (t,))
        row = cur.fetchone()
        if not row:
            print(f"== {t}: manifest 无行")
            continue
        header, rc, fp, n = row
        cols = len(header.split(","))
        print(f"== {t}: header 列 {cols} / rows {rc} / raw {n}B / filepath {fp}")
        hdrs = header.split(",")
        print("   head:", hdrs[:6], "... tail:", hdrs[-4:])
        cur.execute("select split_part(raw_csv, chr(10), 2) from meta.cfg_manifest where file=%s", (t,))
        r2 = cur.fetchone()
        if r2 and r2[0]:
            print("   首数据行列数:", len(r2[0].split(",")))
    # 全表逐行与 schema 列数比对（raw_csv 每行列数）
    print("--- 全表 raw_csv 列数 vs schema ---")
    cur.execute("select file, header_text, raw_csv from meta.cfg_manifest")
    import csv as _csv
    bad = 0
    for f, header, raw in cur.fetchall():
        if raw is None:
            continue
        want = len((header or "").split(","))
        nl = raw.decode("utf-8", "replace").split("\n")
        for i, line in enumerate(nl):
            line = line.rstrip("\r")
            if not line or line.startswith("#"):
                continue
            got = len(next(_csv.reader([line], skipinitialspace=True, lazy_quotes=True)))
            if want and got != want:
                bad += 1
                print(f"!! {f} line{i+1}: {got} 列 (header {want})")
                break
    print(f"== 列数不一致表 {bad}")
