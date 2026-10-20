# -*- coding: utf-8 -*-
"""CHARA_PARAM/MSMA_RENTAL 的"格值级"种子 vs 库漂移（只读）。

行数三方都对（698/698/698），但 §4 说的那 10 台机体在库里补了 `battle_detail_key_*`
却**没有回写种子**吗？按 schema 的 csv_index 精确取列比对。
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

PAIRS = [
    ("CHARA_PARAM", "msma/msma_settings.csv"),
    ("MSMA_RENTAL", "msma/msma_rental.csv"),
]


def seed_rows(rel):
    with open(os.path.join(LOUNGE, rel.replace("/", os.sep)), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    out = {}
    order = []
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        f_ = ln.split(",")
        k = f_[0].strip()
        out[k] = f_
        order.append(k)
    return out, order


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t, rel in PAIRS:
        d = json.load(io.open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        by_idx = {}
        for col in d["columns"]:
            by_idx[col["csv_index"]] = col["name"]
        rows, order = seed_rows(rel)
        cur.execute(
            "select column_name from information_schema.columns "
            "where table_schema='cfg' and table_name=%s order by ordinal_position", (t,))
        dbcols = [r[0] for r in cur.fetchall() if r[0] != "_row_id"]
        # 按 schema csv_index 取关注的键列
        keys = {i: n for i, n in by_idx.items() if n.startswith("battle_detail_key_")}
        print("=" * 78)
        print("## %s（种子 %s，%d 行）" % (t, rel, len(order)))
        print("   battle_detail_key_* 的 csv_index ↔ 列名:", keys)

        # 库侧：逐键取 battle_detail_key_warp
        warp_idx = [i for i, n in keys.items() if n == "battle_detail_key_warp"][0]
        cur.execute(
            'select msma_id, name, battle_detail_key_warp from cfg."%s" order by msma_id' % t)
        db = cur.fetchall()
        only_db = []
        only_seed = []
        diff_val = []
        for k, name, v in db:
            sv = ""
            if k in rows and warp_idx < len(rows[k]):
                sv = rows[k][warp_idx].strip()
            dv = (v or "").strip()
            if dv and not sv:
                only_db.append((k, name, dv))
            elif sv and not dv:
                only_seed.append((k, name, sv))
            elif sv != dv:
                diff_val.append((k, name, sv, dv))
        print("   只在库有值（种子空）: %d" % len(only_db))
        for k, name, dv in only_db:
            print("      %-9s %-22s 库=%s" % (k, name, dv))
        print("   只在种子有值（库空）: %d" % len(only_seed))
        for k, name, sv in only_seed[:20]:
            print("      %-9s %-22s 种子=%s" % (k, name, sv))
        print("   两边都有但值不同    : %d" % len(diff_val))
        for k, name, sv, dv in diff_val[:20]:
            print("      %-9s %-22s 种子=%s 库=%s" % (k, name, sv, dv))
        print()
