# -*- coding: utf-8 -*-
"""打印 5 张待补列表的：库物理列序 / schema DataColumnNames() / manifest 宽度 / 行数"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
SEED_ROOT = os.path.join(ROOT, "server", "datafiles", "lounge")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TABLES = sys.argv[1:] or ["PLAY_BONUS_REWARD", "PLAYER_NAVI", "BUFF", "MODULE_DEVELOP", "MISSION_EXTRULE"]


def data_column_names(spec):
    """复刻 Go TableSpec.DataColumnNames()"""
    cols = spec.get("columns") or []
    if not cols:
        return []
    max_idx = 0
    by_idx = {}
    for c in cols:
        i = c["csv_index"]
        max_idx = max(max_idx, i)
        nm = c.get("db_column") or c.get("name") or f"col{i}"
        by_idx[i] = nm
    return [by_idx.get(i, f"col{i}") for i in range(max_idx + 1)]


def width_of_raw(raw):
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8", "replace")
    best = n = 0
    for line in raw.split("\n"):
        s = line.rstrip("\r").strip()
        if not s or s.startswith("#"):
            continue
        n += 1
        best = max(best, s.count(",") + 1)
    return best, n


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        want = data_column_names(spec)
        cur.execute(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id' "
            "ORDER BY ordinal_position", (t,))
        actual = [r[0] for r in cur.fetchall()]
        cur.execute('SELECT count(*) FROM cfg."%s"' % t)
        rows = cur.fetchone()[0]
        cur.execute("SELECT raw_csv, row_count FROM meta.cfg_manifest WHERE file=%s", (t,))
        got = cur.fetchone()
        mw, mrows = width_of_raw(got[0]) if got and got[0] else (None, None)
        print(f"### {t}")
        print(f"  库物理列({len(actual)}): {actual}")
        print(f"  schema 目标({len(want)}): {want}")
        tail = want[len(actual):] if len(want) > len(actual) else []
        print(f"  ==> 库==目标前段: {actual == want[:len(actual)]} | 待追加: {tail}")
        print(f"  库行={rows}  manifest行={mrows}  manifest字段/行={mw}  manifest.row_count={got[1] if got else None}")
        seed = os.path.join(SEED_ROOT, *spec["csv_path"].split("/"))
        if os.path.isfile(seed):
            sraw = open(seed, encoding="utf-8", errors="replace").read()
            sw, sn = width_of_raw(sraw)
            print(f"  种子 {os.path.relpath(seed, ROOT)}: 字段={sw} 行={sn}")
        else:
            print(f"  种子缺失: {os.path.relpath(seed, ROOT)}")
        print()
