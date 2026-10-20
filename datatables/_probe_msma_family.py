# -*- coding: utf-8 -*-
"""msma 家族跨表键域一致性体检（只读）。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# 逻辑表 -> (cfg 表名, 键列名猜测列表)
FAMILY = [
    ("CHARA_PARAM",  "msma/msma_settings.csv"),
    ("CHARA_MODEL",  "msma/msma_model.csv"),
    ("MSMA_RENTAL",  "msma/msma_rental.csv"),
    ("MSMA_MODULE",  "msma/msma_module.csv"),
    ("MSMA_BREAKUP", "msma/msma_breakup.csv"),
]

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge")


def keys(rel):
    with open(os.path.join(SEED, rel), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    out = []
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s.split(",", 1)[0].strip())
    return out


ks = {n: keys(rel) for n, rel in FAMILY}
cs = {n: set(v) for n, v in ks.items()}

for n in ks:
    print("%-14s n=%4d uniq=%4d" % (n, len(ks[n]), len(cs[n])))

print()
print("== 键域关系（种子 CSV 首发列） ==")
base = cs["CHARA_PARAM"]
print("CHARA_PARAM \\ CHARA_MODEL : %s" % sorted(base - cs["CHARA_MODEL"])[:8])
print("CHARA_PARAM == MSMA_RENTAL ? %s" % (base == cs["MSMA_RENTAL"]))
print("MSMA_MODULE \\ CHARA_PARAM : %s" % sorted(cs["MSMA_MODULE"] - base)[:8])
print("CHARA_PARAM \\ MSMA_MODULE : %d 个" % len(base - cs["MSMA_MODULE"]))
print("MSMA_BREAKUP \\ CHARA_PARAM: %s" % sorted(cs["MSMA_BREAKUP"] - base)[:8])

print()
print("== 全库各表行数（对照） ==")
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select file, row_count from meta.cfg_manifest "
        "where file like 'MSMA%' or file like 'CHARA%' order by file")
    for f, n in cur.fetchall():
        print("  %-24s %6d" % (f, n))
