# -*- coding: utf-8 -*-
"""_audit_id_families.py —— 把 #36/#37/#78 + CSV 的武器 id 按「号长家族」分类。

为什么：读侧 `ItemKeyExpr` 把键规范成**8 位**（`FormatItemKey`）⇒ 库里的 7 位遗留号
其实存成 `02600151`。要判断"哪些行是遗留垃圾、哪些是 1625 个真武器"，必须按规范形看。
"""
import csv
import io
import os
import re
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
SIDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "names", "武器分配明细.csv")


def rd(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return [r for r in csv.reader(f.read().replace("\r\n", "\n").split("\n"))
                if r and any(x.strip() for x in r)]


def norm(s):
    s = s.strip().lstrip("\ufeff")
    if not s.isdigit():
        return None
    return "%08d" % int(s) if len(s) <= 8 else s


side = {int(r[1]) for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()}
print("sidecar 真武器 id %d 个（号长分布 %s）"
      % (len(side), dict(Counter(len(str(i)) for i in side))))

cur = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo").cursor()

for tag, tbl, col in (("#36", '"WEAPON_BATTLE_DETAIL"', "weapon_id_key"),
                      ("#37", '"WEAPON_SETTING"', "weapon_setting_id"),
                      ("#78", '"ITEM"', "item_id")):
    cur.execute('select btrim(%s) from cfg.%s where btrim(%s) ~ \'^[0-9]+$\'' % (col, tbl, col))
    keys = [k for (k,) in cur.fetchall()]
    fam = Counter()
    in_side = 0
    for k in keys:
        n = norm(k)
        fam["%d位原样(%d)" % (len(k), len(k))] += 1
        if n and int(n) in side:
            in_side += 1
    print("%s 键 %d：%s" % (tag, len(keys), dict(fam)))
    print("    其中属于 sidecar 真武器的键 %d" % in_side)

# CSV 侧
for fn in ("weapon_battle_detail.csv", "weapon_settings.csv", "item.csv"):
    rows = rd(os.path.join(DF, fn))
    ks = [r[0].strip().lstrip("\ufeff") for r in rows if r and r[0].strip().lstrip("\ufeff").isdigit()]
    fam = Counter(len(k) for k in ks)
    ins = sum(1 for k in ks if len(k) >= 9 or int(k) in side)
    print("CSV %-28s 行 %d 号长 %s（含 sidecar %d）" % (fn, len(rows), dict(fam), ins))

print()
print("=== 6 把报警武器在库里的真身（含 8 位规范形）===")
for raw in ("2600151", "2012401", "2240601", "12520101", "2210351", "2600101"):
    key = norm(raw)
    cur.execute('select btrim(attr_name),btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL" '
                'where btrim(weapon_id_key)=%s order by 1', (key,))
    attrs = cur.fetchall()
    cur.execute('select btrim(name) from cfg."ITEM" where btrim(item_id)=%s', (key,))
    n = cur.fetchone()
    cur.execute('select magazine_size,weapon_category from cfg."WEAPON_SETTING" '
                'where btrim(weapon_setting_id)=%s', (key,))
    s = cur.fetchone()
    print("%-10s→%-10s #78=%-24s #37=%s" % (raw, key, (n[0] if n else "(无)"), s))
    print("        #36 %s" % (" ".join("%s=%s" % a for a in attrs) or "(无)"))
