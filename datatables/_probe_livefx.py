# -*- coding: utf-8 -*-
"""A 组取证 ②：从**在发的** raw_csv 里找「FX 列表为空但客户端照常跑」的现成样本。

思路：`meta.cfg_manifest.raw_csv`(#37) 是净化前的旧快照（2478 行 > 库 1645 行），
其中若有行第 74 列（effect_name_list）为空、且该键是真武器（在 #78 ITEM 里），
而客户端在此 payload 下已正常运行（抓包 111.pcapng 就是对着它跑的）⇒ **空值已被线上实测**。

另外统计：在发 payload 里第 74 列**非空≠键本身**的行（= 非占位真值样本）有没有。

只报告，不写。
"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
IDX = {"equip_slot_type": 13, "magazine_size": 14, "weapon_category": 21,
       "scatter_pattern": 29, "damage_attribute": 30, "lockon_mode": 31,
       "weapon_attribute": 32, "ammo_type_id": 64, "effect_name_list": 74,
       "sound_set_list": 87, "spawn_effect_list": 100}

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(item_id) from cfg."ITEM"')
    items = {k for (k,) in cur.fetchall() if k.strip().isdigit()}
    cur.execute("select raw_csv from meta.cfg_manifest where file='WEAPON_SETTING'")
    raw = cur.fetchone()[0]
raw = raw if isinstance(raw, str) else raw.decode("utf-8", "replace")
rows = [r for r in csv.reader(raw.replace("\r\n", "\n").split("\n"))
        if r and r[0].strip().isdigit()]

print("在发 #37 行数 %d；字段数分布 %s" % (len(rows), sorted({len(r) for r in rows})))
keyed = {r[0].strip(): r for r in rows}

real = {k: r for k, r in keyed.items() if k in items}
print("其中键在 #78 ITEM 里（= 真武器，客户端真的会去读它）: %d 行" % len(real))

for col, i in IDX.items():
    empty = [k for k, r in real.items() if (r[i].strip() if len(r) > i else "") == ""]
    key_like = [k for k, r in real.items()
                if (r[i].strip() if len(r) > i else "") in (k, k.zfill(8), k.lstrip("0"))]
    other = [k for k, r in real.items()
             if (r[i].strip() if len(r) > i else "") not in ("", k, k.zfill(8), k.lstrip("0"))]
    print("  第%3d列 %-20s 空=%-5d 占位(=键)=%-5d 其它值=%-4d  其它样例=%s"
          % (i, col, len(empty), len(key_like), len(other),
             [(k, r[i]) for k, r in list(real.items()) if k in other][:3]))

# ★ 结论探针：空 FX 列表的真武器样本
emp = [(k, keyed[k][13] if len(keyed[k]) > 13 else "", keyed[k][21] if len(keyed[k]) > 21 else "")
       for k, r in real.items() if (r[74].strip() if len(r) > 74 else "") == ""]
print()
print("★「第74列(effect_name_list)为空 且 是真武器」的样本 %d 个" % len(emp))
for k, grip, cat in emp[:12]:
    print("     %-12s 槽=%-8s 类=%-12s" % (k, grip, cat))
