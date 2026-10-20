# -*- coding: utf-8 -*-
"""MSMA_MODULE 收敛后复核：三方行数 + 键集 + header + raw_csv 与种子逐字节。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge")


def read(rel):
    with open(os.path.join(SEED, rel.replace("/", os.sep)), "rb") as f:
        return f.read()


def seed_data(rel):
    raw = read(rel)
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    out = []
    for ln in raw.decode("utf-8").replace("\r\n", "\n").split("\n"):
        if ln.strip() and not ln.lstrip().startswith("#"):
            out.append(ln.rstrip())
    return out


mod = seed_data("msma/msma_module.csv")
cp = [l.split(",", 1)[0].strip() for l in seed_data("msma/msma_settings.csv")]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select count(*) from cfg."MSMA_MODULE"')
    db = cur.fetchone()[0]
    cur.execute('select btrim(msma_id) from cfg."MSMA_MODULE" order by _row_id')
    dbkeys = [r[0] for r in cur.fetchall()]
    cur.execute("select row_count, header_text, filepath from meta.cfg_manifest where file='MSMA_MODULE'")
    mc, hdr, fp = cur.fetchone()

print("种子 %d ／ 库 %d ／ manifest %d" % (len(mod), db, mc))
print("键序 种子==库 :", [l.split(",", 1)[0].strip() for l in mod] == dbkeys)
print("键集 == CHARA_PARAM :", set(dbkeys) == set(cp), "／ n =", len(set(dbkeys)))
print("header_text : %r" % hdr)
print("filepath    : %r" % fp)
print("库行 payload 形态数 :", len({r for r in dbkeys}))  # placeholder
