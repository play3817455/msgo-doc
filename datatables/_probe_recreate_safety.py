# -*- coding: utf-8 -*-
"""比对 manifest.raw_csv（库内快照）与种子 CSV 是否逐字节一致 + 盘点待改列的库内取值。

用途：决定「重命名列」能否安全走 cfgsync -recreate（DROP + 从 bootstrap CSV 重建）。
"""
import hashlib
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


def norm(b):
    if isinstance(b, str):
        b = b.encode("utf-8")
    return b.replace(b"\r\n", b"\n").strip()


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in ["WEAPON_SETTING", "MISSION_COOP", "QUEST"]:
        spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        seed = os.path.join(SEED_ROOT, *spec["csv_path"].split("/"))
        sb = open(seed, "rb").read()
        cur.execute("SELECT raw_csv, row_count, sha256 FROM meta.cfg_manifest WHERE file=%s", (t,))
        raw, rc, sha = cur.fetchone()
        same = norm(raw) == norm(sb)
        print(f"### {t}")
        print(f"  seed  bytes={len(sb)} sha={hashlib.sha256(sb).hexdigest()[:16]}")
        print(f"  raw_csv bytes={len(raw)} sha={hashlib.sha256(raw).hexdigest()[:16]} manifest.row_count={rc} manifest.sha256={sha[:16] if sha else sha}")
        print(f"  ==> 归一化(去CR/尾空)一致: {same}")
        diff = 0
        if not same:
            a = norm(sb).decode("utf-8", "replace").split("\n")
            b = norm(raw).decode("utf-8", "replace").split("\n")
            print(f"  行数 seed={len(a)} manifest={len(b)}")
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    diff += 1
                    if diff <= 3:
                        print(f"   第{i}行 seed: {x[:160]}")
                        print(f"   第{i}行 mani: {y[:160]}")
            print(f"  首个不一致起，共 {diff} 行不同（截断显示前 3）")
        print()

    # 待改列库内取值盘点
    for t, cols in [("WEAPON_SETTING", [35, 37, 39, 42, 44, 46, 48, 50, 52, 54, 58, 60, 61, 62, 63]),
                    ("MISSION_COOP", [8])]:
        spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        names = {c["csv_index"]: c["db_column"] for c in spec["columns"]}
        cur.execute("SELECT count(*) FROM cfg.\"%s\"" % t)
        total = cur.fetchone()[0]
        print(f"### {t} 待改列库内非空计数（总 {total} 行）")
        for i in cols:
            nm = names.get(i, f"col{i}")
            cur.execute('SELECT count(*) FROM cfg."%s" WHERE COALESCE("%s",\'\')<>\'\'' % (t, nm))
            n = cur.fetchone()[0]
            print(f"    csv{i:3d} db={nm:22s} 非空 {n}")
        print()
