# -*- coding: utf-8 -*-
"""空载荷表体检：库行数 / 非空格数 / manifest 行数 / 种子 CSV 行数与路径"""
import csv
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
TABLES = [
    "MSMA_OVERWRITE_PARAMS", "NETCAFE_CHALLENGE", "SEASON_CLASS_IMFORMATION",
    "SEASON_CLASS_UP_REWARD", "SEASON_RANKERBATTLE_REWARD", "TROOP_CHALLENGE",
    "BGMPACKAGE", "LVUP_MSMA", "MSMA_MATERIAL",
]


def seed_path(p):
    cand = os.path.join("server", "datafiles", "lounge", p.replace("/", os.sep))
    return cand if os.path.isfile(cand) else None


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in TABLES:
        cur.execute(
            "select column_name from information_schema.columns "
            "where table_schema='cfg' and table_name=%s and column_name<>'_row_id' "
            "order by ordinal_position", (t,))
        cols = [r[0] for r in cur.fetchall()]
        if not cols:
            print(f"== {t}: 库中无表")
            continue
        cur.execute(f'select count(*) from cfg."{t}"')
        n = cur.fetchone()[0]
        exprs = ", ".join([f'count(*) filter (where coalesce("{x}",\'\')<>\'\')' for x in cols])
        cur.execute(f'select {exprs} from cfg."{t}"')
        nonempty = dict(zip(cols, cur.fetchone()))
        tot = sum(nonempty.values())
        cur.execute("select row_count, length(coalesce(raw_csv,''::bytea)) from meta.cfg_manifest where file=%s", (t,))
        mrow = cur.fetchone()
        cur.execute("select csv_path, disposition from meta.cfg_table_def where table_name=%s", (t,))
        td = cur.fetchone()
        csvp = td[0] if td else None
        sp = seed_path(csvp) if csvp else None
        seedrows = None
        if sp:
            with open(sp, encoding="utf-8", errors="replace") as f:
                seedrows = sum(1 for l in f if l.strip() and not l.lstrip().startswith("#"))
        print(f"== {t} ({td[1] if td else '?'})")
        print(f"   库列 {len(cols)} / 库行 {n} / 非空格合计 {tot} / manifest rows={mrow[0] if mrow else None} bytes={mrow[1] if mrow else None}")
        nz = {k: v for k, v in nonempty.items() if v}
        print(f"   非空列 {nz if nz else '（全空）'}")
        print(f"   种子 {csvp} -> {sp} rows={seedrows}")
