# -*- coding: utf-8 -*-
"""精确看 manifest 数据行与种子数据行的**同一行**（只读）。"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"f:\9ymsgo\9you"

CASES = [
    ("CHARA_PARAM", "msma/msma_settings.csv", "1100001"),
    ("MECHANIC_WEAPON", "develop/mechanic_weapon.csv", None),
    ("MSMA_BATTLE_DETAIL", "msma/msma_battle_detail.csv", None),
]

with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as c:
    cur = c.cursor()
    for t, rel, key in CASES:
        cur.execute("select raw_csv from meta.cfg_manifest where file=%s", (t,))
        raw = cur.fetchone()[0]
        s = raw if isinstance(raw, str) else raw.decode("utf-8", "replace")
        mlines = [l for l in s.replace("\r\n", "\n").split("\n")
                  if l.strip() and not l.lstrip().startswith("#")]
        m = [l for l in mlines if key is None or l.split(",")[0].strip() == key][0]
        p = os.path.join(ROOT, "server/datafiles/lounge", rel.replace("/", os.sep))
        sl = [l for l in open(p, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")
              if l.strip() and not l.lstrip().startswith("#")]
        q = [l for l in sl if key is None or l.split(",")[0].strip() == key][0]
        print("## %s  key=%s" % (t, key))
        print("   mf  字段 %3d 尾 30 = %r" % (len(m.split(",")), m[-30:]))
        print("   种子字段 %3d 尾 30 = %r" % (len(q.split(",")), q[-30:]))
