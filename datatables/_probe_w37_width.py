# -*- coding: utf-8 -*-
"""#37 WEAPON_SETTING 的"宽度差"取证（只读）：种子 34 列 vs 库 N 列。

判据：种子 `item/weapon_settings.csv` 只写 col0..col33；库/schema 有近 150 列。
若 `-recreate` 按种子重建，库里那 11 个 `#36` 连接键（=`weapon_setting_id` 的拷贝）
会不会被清空？本脚本给出数量级。
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_settings.csv")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables", "WEAPON_SETTING.json")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

LINKS = ["effect_name_list", "hit_effect_list", "muzzle_effect_list", "trail_effect_list",
         "sound_set_list", "voice_set_list", "camera_shake_list", "screen_flash_list",
         "buff_effect_list", "debuff_effect_list", "spawn_effect_list"]

# 种子宽度
widths = {}
with open(SEED, encoding="utf-8") as fh:
    for l in fh:
        if not l.strip() or l.startswith("#"):
            continue
        n = len(l.rstrip("\r\n").split(","))
        widths[n] = widths.get(n, 0) + 1
print("种子 %s" % os.path.relpath(SEED, ROOT))
print("  字段数分布（含尾逗号产生的空尾格）:", dict(sorted(widths.items())))

d = json.load(io.open(SCHEMA, encoding="utf-8"))
print("  schema 列数 %d，csv_index %d..%d，status 统计:"
      % (len(d["columns"]), min(c["csv_index"] for c in d["columns"]),
         max(c["csv_index"] for c in d["columns"])))
from collections import Counter
print("   ", dict(Counter(c.get("status") for c in d["columns"])))

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select column_name from information_schema.columns "
        "where table_schema='cfg' and table_name='WEAPON_SETTING' order by ordinal_position")
    cols = [r[0] for r in cur.fetchall()]
    print("  库列数 %d  首 6=%s  尾 6=%s" % (len(cols), cols[:6], cols[-6:]))
    cur.execute('select count(*) from cfg."WEAPON_SETTING"')
    n = cur.fetchone()[0]
    print("  库行 %d ／ 种子 %d" % (n, sum(widths.values())))
    for c_ in LINKS:
        cur.execute('select count(*) from cfg."WEAPON_SETTING" where btrim("%s") <> btrim(weapon_setting_id)' % c_)
        bad = cur.fetchone()[0]
        cur.execute('select count(*) from cfg."WEAPON_SETTING" where coalesce(btrim("%s"),\'\') = \'\'' % c_)
        empty = cur.fetchone()[0]
        print("    %-22s 不等于 key 的行 %4d ／ 空 %4d" % (c_, bad, empty))
    cur.execute("""select count(*) from cfg."WEAPON_SETTING"
                   where coalesce(btrim(ammo_type_id),'') = ''""")
    print("    ammo_type_id 空行", cur.fetchone()[0])
