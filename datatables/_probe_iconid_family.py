# -*- coding: utf-8 -*-
"""#37 全量：按规范化 8 位键分组，统计 #36 POWER 覆盖。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def norm(k):
    s = str(k).strip()
    if s.isdigit() and len(s) < 8:
        return s.zfill(8)
    return s


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select btrim(weapon_setting_id), btrim(weapon_category) from cfg."WEAPON_SETTING"')
    raw = cur.fetchall()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name) from cfg."WEAPON_BATTLE_DETAIL"')
    det = {}
    for k, a in cur.fetchall():
        det.setdefault(norm(k), set()).add(a)

ws = {}
dup = 0
for k, cat in raw:
    n = norm(k)
    if n in ws:
        dup += 1
    ws[n] = cat
print("#37 行 %d；规范键 %d；重复 %d" % (len(raw), len(ws), dup))
print()

fams = {}
for n, cat in ws.items():
    fams.setdefault(n[:2], []).append((n, cat))
for p in sorted(fams):
    fam = fams[p]
    nopow = [(k, cat) for k, cat in fam if "POWER" not in det.get(k, ())]
    nodet = [(k, cat) for k, cat in fam if not det.get(k)]
    print("== 前缀 %s：%4d 把 | 无 #36 任何行 %3d | 无 POWER %3d"
          % (p, len(fam), len(nodet), len(nopow)))
    for k, cat in nopow[:12]:
        print("      %s %-16s 有:%s" % (k, cat, sorted(det.get(k, ()))))
    if len(nopow) > 12:
        print("      ... 余 %d" % (len(nopow) - 12))
print()
# 全局：有 #36 行的键里无 POWER 的
allnopow = [(n, cat) for n, cat in ws.items() if det.get(n) and "POWER" not in det[n]]
print("全局『有 #36 行但无 POWER』共 %d 把：" % len(allnopow))
for k, cat in sorted(allnopow):
    print("   %s %-16s %s" % (k, cat, sorted(det[k])))
