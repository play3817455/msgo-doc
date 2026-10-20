# -*- coding: utf-8 -*-
"""把 meta.cfg_manifest 全量快照到 datatables/_out_manifest_snapshot.pkl（cfgsync 前后比对用）。
用法: python _manifest_snapshot.py save|diff
"""
import hashlib
import io
import os
import pickle
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "_out_manifest_snapshot.pkl")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
mode = sys.argv[1] if len(sys.argv) > 1 else "save"


def grab():
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute("SELECT file, filepath, sha256, row_count, raw_csv, header_text FROM meta.cfg_manifest ORDER BY file")
        return {r[0]: r[1:] for r in cur.fetchall()}


now = grab()


def sig(row):
    filepath, sha, rc, raw, header = row
    return (filepath or "", sha or "", rc, hashlib.sha256(raw or b"").hexdigest()[:16], len(raw or b""), header or "")


if mode == "save":
    with open(SNAP, "wb") as fh:
        pickle.dump(now, fh)
    print(f"saved {len(now)} manifest rows -> {os.path.relpath(SNAP, os.path.dirname(HERE))}")
else:
    old = pickle.load(open(SNAP, "rb"))
    added = sorted(set(now) - set(old))
    removed = sorted(set(old) - set(now))
    changed = sorted(f for f in set(old) & set(now) if sig(old[f]) != sig(now[f]))
    print(f"rows: {len(old)} -> {len(now)}")
    print(f"added  : {added}")
    print(f"removed: {removed}")
    print(f"changed: {len(changed)}")
    for f in changed:
        of, nf = old[f], now[f]
        print(f"  {f:24s} row_count {of[2]} -> {nf[2]}  bytes {len(of[3] or b'')} -> {len(nf[3] or b'')}  sha {of[1][:8]} -> {nf[1][:8]}")
