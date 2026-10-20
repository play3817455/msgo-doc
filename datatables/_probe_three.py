# -*- coding: utf-8 -*-
"""探针：QUEST / WEAPON_SETTING / MISSION_COOP 的库物理列、行数、manifest 行宽。"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TARGETS = ["QUEST", "WEAPON_SETTING", "MISSION_COOP"]


def width(raw):
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8", "replace")
    best, n = 0, 0
    for line in raw.split("\n"):
        s = line.rstrip("\r").strip()
        if not s or s.startswith("#"):
            continue
        n += 1
        best = max(best, s.count(",") + 1)
    return best, n


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TARGETS:
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        cols = [r[0] for r in cur.fetchall()]
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        rc = cur.fetchone()[0]
        print("=" * 90)
        print(f"{t}: 物理列 {len(cols)} 行数 {rc}")
        print("  列序: " + ", ".join(cols))
        cur.execute("SELECT file, filepath, header_text, raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        row = cur.fetchone()
        if row:
            f, p, hdr, raw = row
            w, n = width(raw or "")
            print(f"  manifest: filepath={p} 行宽={w} 行数={n}")
            print(f"  header: {(hdr or '')[:200]!r}")
            if raw:
                lines = [l for l in raw.decode("utf-8", "replace").split("\n") if l.strip() and not l.strip().startswith("#")]
                if lines:
                    print(f"  首数据行: {lines[0][:200]!r}")
        else:
            print("  manifest: 无记录")
