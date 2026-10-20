# -*- coding: utf-8 -*-
"""#36 导出里 5 段行的真身 + 种子对照 + 文档列数。只读。"""
import io
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_battle_detail.csv")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_BATTLE_DETAIL'")
    raw = bytes(cur.fetchone()[0])
    t = raw.decode("utf-8", "replace").replace("\r\n", "\n")
    five = [l for l in t.split("\n") if l and not l.startswith("#") and len(l.split(",")) > 4]
    print("导出里 >4 段的行 %d 条：" % len(five))
    for l in five:
        print("   %r" % l)

    cur.execute("""select attr_name, weapon_id_key, attr_value, attr_value_2
                   from cfg."WEAPON_BATTLE_DETAIL"
                   where coalesce(attr_value_2,'') <> ''
                   order by _row_id limit 20""")
    rows = cur.fetchall()
    print()
    print("库内 attr_value_2 非空行 %d 条（前 20）：" % len(rows))
    for r in rows:
        print("   %r" % (r,))

print()
with open(SEED, "rb") as f:
    sraw = f.read()
st = sraw.decode("utf-8", "replace").replace("\r\n", "\n")
slines = [l for l in st.split("\n") if l and not l.startswith("#")]
print("种子行 %d ／ 段数分布 %s" % (len(slines), {k: sum(1 for l in slines if len(l.split(",")) == k)
                                             for k in {len(l.split(",")) for l in slines}}))
sfive = [l for l in slines if len(l.split(",")) > 4]
print("种子里 >4 段的行 %d 条：" % len(sfive))
for l in sfive[:20]:
    print("   %r" % l)
