# -*- coding: utf-8 -*-
"""n1 五表：种子 CSV 真实数据行数（排除 # 注释行）vs manifest vs cfg。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

TABLES = [
    ("CHARA_PARAM",  "CHARA_PARAM",  "msma/msma_settings.csv"),
    ("CHARA_MODEL",  "CHARA_MODEL",  "msma/msma_model.csv"),
    ("MSMA_RENTAL",  "MSMA_RENTAL",  "msma/msma_rental.csv"),
    ("MSMA_MODULE",  "MSMA_MODULE",  "msma/msma_module.csv"),
    ("MSMA_BREAKUP", "MSMA_BREAKUP", "msma/msma_breakup.csv"),
]

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge")


def seed_stats(rel):
    with open(os.path.join(SEED, rel), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8", "replace")
    data, comments = [], 0
    for ln in text.replace("\r\n", "\n").split("\n"):
        if not ln.strip():
            continue
        if ln.lstrip().startswith("#"):
            comments += 1
            continue
        data.append(ln)
    return data, comments


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    print("%-14s %9s %9s %9s %9s  %s" % ("table", "manifest", "cfg", "seed", "cmt", "verdict"))
    bad = []
    for logi, cfgt, rel in TABLES:
        cur.execute("select row_count from meta.cfg_manifest where file=%s", (logi,))
        m = cur.fetchone()[0]
        cur.execute('select count(*) from cfg."%s"' % cfgt)
        db = cur.fetchone()[0]
        data, cmt = seed_stats(rel)
        sd = len(data)
        ok = (m == db == sd)
        if not ok:
            bad.append(logi)
        print("%-14s %9s %9s %9s %9s  %s" % (logi, m, db, sd, cmt, "OK" if ok else "MISMATCH"))
    print()
    # 关键列（第一列/主键）非空与唯一性抽查
    print("== 种子主键 col0 抽查 ==")
    for logi, cfgt, rel in TABLES:
        data, _ = seed_stats(rel)
        keys = [r.split(",")[0].strip() for r in data]
        nonnum = [k for k in keys if not k.isdigit()]
        dup = len(keys) - len(set(keys))
        print("  %-14s n=%4d  非数字=%d  重复=%d  头/尾=%s/%s"
              % (logi, len(keys), len(nonnum), dup, keys[0], keys[-1]))
