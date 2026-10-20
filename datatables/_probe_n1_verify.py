# -*- coding: utf-8 -*-
"""复核：MSMA_MODULE 收尾后（库 666 / 种子 666 / manifest 666）与 n1 五表的 manifest 行数。只读。"""
import io
import json
import os

import psycopg

ROOT = r"f:\9ymsgo\9you"
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

T = ["CHARA_PARAM", "CHARA_MODEL", "MSMA_RENTAL", "MSMA_MODULE", "MSMA_BREAKUP"]
SEEDS = {
    "CHARA_PARAM": "server/datafiles/lounge/msma/msma_settings.csv",
    "CHARA_MODEL": "server/datafiles/lounge/msma/msma_model.csv",
    "MSMA_RENTAL": "server/datafiles/lounge/msma/msma_rental.csv",
    "MSMA_MODULE": "server/datafiles/lounge/msma/msma_module.csv",
    "MSMA_BREAKUP": "server/datafiles/lounge/msma/msma_breakup.csv",
}


def count_seed(rel):
    p = os.path.join(ROOT, rel)
    b = open(p, "rb").read()
    crlf = b.count(b"\r\n")
    lf = b.count(b"\n") - crlf
    n = 0
    for line in b.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        s = line.strip()
        if s and not s.startswith("#"):
            n += 1
    return n, crlf, lf


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    print("%-14s %8s %8s %8s   %s" % ("表", "库行", "种子行", "manifest", "种子行尾"))
    for name in T:
        cur.execute('select count(*) from cfg."%s"' % name)
        dbn = cur.fetchone()[0]
        cur.execute(
            "select row_count from meta.cfg_manifest where file=%s", (name,)
        )
        r = cur.fetchone()
        mf = r[0] if r else None
        sn, crlf, lf = count_seed(SEEDS[name])
        flag = "OK" if (dbn == sn == (mf if mf is not None else sn)) else "★查"
        print("%-14s %8d %8d %8s   CRLF=%-6d 裸LF=%-4d %s"
              % (name, dbn, sn, mf, crlf, lf, flag))

    cur.execute(
        "select row_count, raw_csv is not null from meta.cfg_manifest where file='MSMA_MODULE'"
    )
    print()
    print("MSMA_MODULE manifest:", cur.fetchone())
    cur.execute(
        "select count(*) from cfg.\"MSMA_MODULE\" where btrim(msma_id) in ('0','101286001')"
    )
    print("脏键残留:", cur.fetchone()[0])
