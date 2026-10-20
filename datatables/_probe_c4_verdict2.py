# -*- coding: utf-8 -*-
"""C4 最终裁定：把「库有行但 sidecar 无面板」509 条按来路分类。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

S = {}
for r in F.rd(F.SIDE)[1:]:
    if len(r) > 1 and r[1].strip().isdigit():
        S[F.norm_key(r[1])] = r


def cell(k, i):
    r = S.get(k)
    return r[i].strip() if r and i < len(r) else ''


ATTR_COL = {'POWER': 10, 'STABILITY': 11, 'RAPIDDELAY': 12, 'RANGE': 13,
            'RELOAD': 14, 'LOCKON_CAM': 16, 'HIGH_LOCKON': 17, 'COOLTIME': 12}

with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value) '
                'from cfg."WEAPON_BATTLE_DETAIL"')
    rows = [(F.norm_key(k), a.strip(), v.strip()) for k, a, v in cur.fetchall()]

cls = collections.Counter()
keys_of = collections.defaultdict(set)
for k, a, v in rows:
    if k not in S:
        cls['非 sidecar 键（现役短号，另册）'] += 1
        continue
    col = ATTR_COL.get(a)
    if col is None:
        cls['属性名未在映射内'] += 1
        continue
    if RAW.first_tier(cell(k, col)):
        continue
    # 该属性在 sidecar 没有面板 ⇒ 库里的行无来源
    if not RAW.first_tier(cell(k, 10)):
        c = 'A 版面异常页（sidecar 连威力都没有）'
    elif a == 'RELOAD' and RAW.first_tier(cell(k, 15)):
        c = 'B 装填只写在 col15(装填时间)，库行是旧刻度'
    else:
        c = 'C 该列本页确为空白（真正无此属性）'
    cls[c] += 1
    keys_of[c].add(k)

print('=== 509 条的来路分类 ===')
tot = 0
for c, n in cls.most_common():
    kk = keys_of[c]
    print('  %-42s 行=%-4d 键=%d' % (c, n, len(kk)))
    if kk and len(kk) <= 80:
        print('      键：%s' % sorted(kk))
    elif kk:
        print('      例：%s' % sorted(kk)[:20])
    tot += n
print('  ---- 合计 %d' % tot)

print()
side_keys = set(S)
print('sidecar 键总数 %d；其中「连威力都没有」的键 %d 个'
      % (len(side_keys), sum(1 for k in side_keys if not RAW.first_tier(cell(k, 10)))))
print('各列空白的键数：%s' % {
    nm: sum(1 for k in side_keys if not RAW.first_tier(cell(k, c)))
    for nm, c in ATTR_COL.items() if nm != 'COOLTIME'})
