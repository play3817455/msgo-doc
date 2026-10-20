# -*- coding: utf-8 -*-
"""C4 取证（落库前）：新 CSV 与真库的**三方对账**（真武器号 × #36 八族）。

回答两个问题：
 ① 新 CSV 里没有、库里却有的行（= 将被"整族重写"净化掉的）到底是什么值、什么来路；
 ② 库里 `HIGH_LOCKON` 比新 CSV 多出的那 ~200 行是**真值**还是老管线的陈旧映射。
"""
import collections
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'wiki'))

# ⚠️ 不要自己 wrap stdout：下面 import 的 `fix_rapid_delay_units` 会在 import 期
#    `sys.stdout = TextIOWrapper(...)`；自己那份 wrapper 一旦失去引用会被 GC 连带关掉底层 buffer。
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import parse_cache as PC  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

Q = chr(34)


def rd(p):
    return [r for r in csv.reader(open(p, encoding='utf-8-sig', errors='replace')
                                  .read().replace('\r\n', '\n').split('\n'))
            if r and any(x.strip() for x in r) and not r[0].strip().startswith('#')]


SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
T36 = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'item', 'weapon_battle_detail.csv')
side = {F.norm_key(r[1]): r for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()}
csvm = {(r[0].strip(), F.norm_key(r[1])): r[2].strip() for r in rd(T36) if len(r) > 1}

dbm = collections.defaultdict(dict)
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value), '
                'btrim(coalesce(attr_value_2, %s)) from cfg.%s%s%s'
                % ("''", Q, 'WEAPON_BATTLE_DETAIL', Q))
    for k, a, v, v2 in cur.fetchall():
        dbm[F.norm_key(k)][a.strip()] = (v.strip(), v2.strip())

REAL = set(side)
ATTRS = ['POWER', 'STABILITY', 'RANGE', 'RAPIDDELAY', 'COOLTIME', 'RELOAD',
         'LOCKON_CAM', 'HIGH_LOCKON']
print('真武器号 %d；库里属于真武器号的 #36 行 %d'
      % (len(REAL), sum(len(dbm[k]) for k in dbm if k in REAL)))
# 库里不属于真武器号的 attr 词表（别的管线写的，本脚本不碰）
other = collections.Counter(a for k, d in dbm.items() if k not in REAL for a in d)
print('非真武器号的 attr 词表:', dict(other.most_common()))

print()
print('=== ① 库有 · CSV 无（将被整族重写净化）===')
for a in ATTRS:
    stale = sorted((k, d[a][0]) for k, d in dbm.items() if k in REAL and a in d
                   and (a, k) not in csvm)
    if not stale:
        print('  %-12s 0 ✓' % a)
        continue
    cc = collections.Counter(round(float(v), 6) if _num(v) else v for k, v in stale) \
        if False else collections.Counter(v for _, v in stale)
    print('  %-12s %d 行  值分布 top: %s' % (a, len(stale), cc.most_common(8)))
    print('        例: %s' % stale[:6])

print()
print('=== ② 库有 · CSV 有 · 值不同（键内换值）===')
n_diff = 0
for a in ATTRS:
    diff = sorted((k, d[a][0], csvm[(a, k)]) for k, d in dbm.items()
                  if k in REAL and a in d and (a, k) in csvm and d[a][0] != csvm[(a, k)])
    n_diff += len(diff)
    if diff:
        print('  %-12s %d 行  例: %s' % (a, len(diff), diff[:4]))
print('  合计换值 %d 行' % n_diff)

# ── ②b 换值分类：单位换算修正 / 21 个改名的键 / 其余待看 ──────────────────────
GUARDED = ('STABILITY', 'RELOAD', 'LOCKON_CAM', 'RAPIDDELAY', 'COOLTIME')
RENAMED = set()
old_side = {F.norm_key(r[1]): r for r in rd(os.path.join(HERE, '_probe_sidecar_old.csv'))
            if len(r) > 1 and r[1].strip().isdigit()}
for k in set(old_side) & set(side):
    if (old_side[k][5].strip() if len(old_side[k]) > 5 else '') != \
       (side[k][5].strip() if len(side[k]) > 5 else ''):
        RENAMED.add(k)
cls = collections.Counter()
rest = []
for a in ATTRS:
    for k, d in dbm.items():
        if k not in REAL or a not in d or (a, k) not in csvm or d[a][0] == csvm[(a, k)]:
            continue
        if a in GUARDED and not RAW.is_raw_domain(a, d[a][0]) and RAW.is_raw_domain(a, csvm[(a, k)]):
            cls['① 单位换算修正（旧值越域=面板刻度直写）'] += 1
        elif k in RENAMED:
            cls['② 键绑定的武器改名（21 个，配对纠正）'] += 1
        else:
            cls['③ 待看'] += 1
            rest.append((a, k, d[a][0], csvm[(a, k)]))
print('  换值分类:', dict(cls))
print('  ③ 待看例（attr/键/旧/新）: %s' % rest[:14])
print('  改名键 %d 个: %s' % (len(RENAMED), sorted(RENAMED)[:24]))

print()
print('=== ③ HIGH_LOCKON：库里多出的那些行，wiki 页面到底有没有红锁距离 ===')
stale_hl = sorted(k for k, d in dbm.items() if k in REAL and 'HIGH_LOCKON' in d
                  and ('HIGH_LOCKON', k) not in csvm)
print('  将净化 %d 行；它们在**新解析**里 col17 红锁距离 = %s'
      % (len(stale_hl),
         collections.Counter((side[k][17] if len(side[k]) > 17 else '') for k in stale_hl).most_common(6)))
print('  这些键在**旧 sidecar** 里的 col17 = %s'
      % collections.Counter(
          (lambda r: r[17] if r and len(r) > 17 else 'NOT-IN-OLD')(
              next((x for x in rd(os.path.join(HERE, '_probe_sidecar_old.csv'))
                    if len(x) > 1 and F.norm_key(x[1]) == k), None))
          for k in stale_hl).most_common(6))
# 逐页取证：这些键所在页面的 wikitext 里有没有 红锁距离/<sup>
pages = collections.defaultdict(list)
for k in stale_hl:
    pages[side[k][4]].append((k, side[k][5], side[k][17] if len(side[k]) > 17 else ''))
print('  涉及页面 %d 个' % len(pages))
withsup = 0
for p, rows in pages.items():
    t = None
    for c in (p, p.replace('（', '(').replace('）', ')')):
        f = os.path.join(HERE, 'wiki', 'cache', c + '.txt')
        if os.path.exists(f):
            t = open(f, encoding='utf-8').read()
            break
    if t is None:
        print('    %s (缓存缺)' % p[:30])
        continue
    has = t.count('红锁距离') + t.count('红锁')
    if has:
        withsup += 1
    if len(pages) <= 12 or has:
        got = []
        try:
            ms = PC.parse_ms(p, t)
            got = [(x.get('武器名', ''), x.get('红锁距离', ''))
                   for x in PC.parse_weapons(p, t, ms) if x.get('红锁距离')]
        except Exception as e:
            got = [('解析异常', str(e))]
        print('    %-26s 文中「红锁」%d 次；新解析出的红锁 %s；库里的键 %s'
              % (p[:26], has, got[:4], [(k, v) for k, _, v in rows[:4]]))
print('  有「红锁」字样的页面 %d / %d' % (withsup, len(pages)))
