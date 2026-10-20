# -*- coding: utf-8 -*-
"""数逗号（只读）：manifest 行 vs 种子行 的字段数到底差在哪。"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"f:\9ymsgo\9you"

with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as c:
    cur = c.cursor()
    for t, rel, key in (("CHARA_PARAM", "msma/msma_settings.csv", "1100001"),
                        ("MSMA_RENTAL", "msma/msma_rental.csv", "1100001")):
        cur.execute("select raw_csv from meta.cfg_manifest where file=%s", (t,))
        s = cur.fetchone()[0]
        if isinstance(s, (bytes, bytearray, memoryview)):
            s = bytes(s).decode("utf-8", "replace")
        m = [l for l in s.replace("\r\n", "\n").split("\n")
             if l.strip() and not l.lstrip().startswith("#") and l.split(",")[0] == key][0]
        p = os.path.join(ROOT, "server/datafiles/lounge", rel.replace("/", os.sep))
        q = [l.rstrip("\r") for l in open(p, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")
             if l.strip() and not l.lstrip().startswith("#") and l.split(",")[0] == key][0]
        print("## %s key=%s" % (t, key))
        for tag, x in (("mf", m), ("seed", q)):
            f = x.split(",")
            print("   %-5s 字节 %4d ／ 逗号 %3d ／ split 后 %3d ／ 末 3 个 %r"
                  % (tag, len(x.encode("utf-8")), x.count(","), len(f), f[-3:]))
            print("         f[88]=%r f[89]=%r f[90]=%r f[91]=%r f[92]=%r"
                  % (f[88] if len(f) > 88 else None, f[89] if len(f) > 89 else None,
                     f[90] if len(f) > 90 else None, f[91] if len(f) > 91 else None,
                     f[92] if len(f) > 92 else None))
    cur.execute("select count(*) from information_schema.columns "
                "where table_schema='cfg' and table_name='CHARA_PARAM' and column_name<>'_row_id'")
    print("库 CHARA_PARAM 数据列 =", cur.fetchone()[0])
