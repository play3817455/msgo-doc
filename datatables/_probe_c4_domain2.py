# -*- coding: utf-8 -*-
"""C4 取证（第二轮）：为 STABILITY / RELOAD / LOCKON_CAM 定「原值域」哨。

⚠️ 本探针**不 import `gen_weapon_tables_wiki`**：那边 import 期就 `sys.stdout = TextIOWrapper(...)`，
   父进程一旦回收 wrapper 会关掉底层 buffer（`fpmf_scan` 的 print 直接炸 I/O on closed file）。
   所以 `norm_key` 抄一份逐字相同的实现。

三路证据：
 ① wiki 面板域（`wiki/wiki_ms_weapons.csv`）→ 换算 ⇒ 原值域的**像**；
 ② 真库实测（真武器号 #36 行）→ 值聚类（域内/域外是否分得干净）；
 ③ sidecar col15「装填时间」的取值分布（RELOAD 回退源的可靠性）。
"""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WIKI = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
COLS = {'威力': 8, '集弹性能': 9, '连射速度': 10, '射程距离': 11,
        '装填性能': 12, '装填时间': 13, '锁定': 14, '红锁距离': 15}
FN = {'威力': RAW.power_raw, '集弹性能': RAW.stability_raw, '连射速度': RAW.rapid_raw,
      '装填性能': RAW.reload_raw, '装填时间': RAW.reload_raw, '锁定': RAW.lockon_raw}


def norm_key(k):
    k = str(k).strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


def rd(p):
    if not os.path.exists(p):
        return []
    return [r for r in csv.reader(open(p, encoding='utf-8-sig', errors='replace')
                                  .read().replace('\r\n', '\n').split('\n'))
            if r and any(x.strip() for x in r) and not r[0].strip().startswith('#')]


print('=== ① wiki 面板域 → 原值域的像（%s）===' % os.path.relpath(WIKI, ROOT))
panels = collections.defaultdict(list)
for r in rd(WIKI):
    for nm, c in COLS.items():
        if len(r) > c:
            t = RAW.first_tier(r[c])
            if t:
                panels[nm].append(int(float(t)))
print('%-10s %6s %9s %9s   %s' % ('列', 'n', '面板min', '面板max', '原值域(像)'))
for nm in COLS:
    ps = sorted(panels.get(nm, []))
    fn = FN.get(nm)
    if not ps or fn is None:
        print('%-10s %6d %9d %9d   %s' % (nm, len(ps), ps[0], ps[-1], '原样'))
        continue
    vs = sorted(float(fn(p)) for p in (ps[0], ps[-1]))
    # 面板分位（看长尾多长）
    print('%-10s %6d %9d %9d   [%.6f, %.6f]  p50面板=%d p99面板=%d'
          % (nm, len(ps), ps[0], ps[-1], vs[0], vs[-1], ps[len(ps) // 2], ps[int(len(ps) * 0.99)]))

print()
print('=== ② 真库实测：真武器号的 #36 值（%s）===' % F.DSN.split('@')[-1])
ids = {norm_key(r[1]) for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()}
dbm = collections.defaultdict(list)
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(attr_name), btrim(weapon_id_key), btrim(attr_value) '
                'from cfg."WEAPON_BATTLE_DETAIL"')
    for a, k, v in cur.fetchall():
        if norm_key(k) in ids:
            try:
                dbm[a.strip()].append((k.strip(), float(v)))
            except ValueError:
                pass

# ★原值域（像）：来自 ①，只取「面板域内」那段的像；手填自上面输出
DOM = {
    'POWER': (0.0, 10000.0),          # 面板 ≤ 100000；下游另有 >10000 哨
    'STABILITY': (-0.01, 5.0),        # 面板 0..980 → mem 0..500 → 原值/100
    'RANGE': (0.0, 2000.0),
    'RAPIDDELAY': (RAW.RAPID_RAW_LO, RAW.RAPID_RAW_HI),
    'RELOAD': (0.0, 10.0),            # 面板 0..1000 → trunc((10−v)×100+0.4)
    'LOCKON_CAM': (0.0, 400.0),       # 面板 0..4000 → v = 面板/10
    'HIGH_LOCKON': (0.0, 400.0),
}
print('%-12s %6s %10s %10s %8s %8s' % ('attr', 'n', 'min', 'max', '域内', '域外'))
BAD = {}
for a in ('POWER', 'STABILITY', 'RANGE', 'RAPIDDELAY', 'RELOAD', 'LOCKON_CAM', 'HIGH_LOCKON'):
    rows = dbm.get(a, [])
    if not rows:
        continue
    xs = sorted(v for _, v in rows)
    lo, hi = DOM[a]
    bad = [(k, v) for k, v in rows if not (lo <= v <= hi)]
    BAD[a] = bad
    # 真值簇上界（面板刻度残渣的地板取 500；看两簇之间有没有空档）
    tru = [v for v in xs if v < 500]
    print('%-12s %6d %10.4f %10.4f %8d %8d   真值簇 max=%s 空档=%s'
          % (a, len(xs), xs[0], xs[-1], len(rows) - len(bad), len(bad),
             ('%.4f' % tru[-1]) if tru else '-',
             ('(%.4f, %.4f)' % (tru[-1], min(v for v in xs if v >= 500))) if tru and len(tru) < len(xs) else '-'))

print()
print('=== ②c 三属性「真值簇 vs 残渣簇」的分界（去重值 × 键数，0..1200 窗口）===')
for a in ('STABILITY', 'RELOAD', 'LOCKON_CAM'):
    rows = dbm.get(a, [])
    cc = collections.Counter(round(v, 6) for _, v in rows)
    ks = sorted(cc)
    print('  %-11s 去重值 %d 种；最小值档:' % (a, len(ks)))
    print('      %s' % ' '.join('%g×%d' % (v, cc[v]) for v in ks if v <= 1200))
    big = [v for v in ks if v > 1200]
    print('      >1200 的 %d 种: %s' % (len(big), ['%g×%d' % (v, cc[v]) for v in big[:12]]))

print()
print('=== ③ RELOAD 回退源（sidecar col14 空 / col15 装填时间 的取值）===')
side = [r for r in rd(SIDE) if len(r) > 1 and r[1].strip().isdigit()]
c14 = c15 = both = neither = 0
v15, v14 = [], []
for r in side:
    a = RAW.first_tier(r[14]) if len(r) > 14 else ''
    b = RAW.first_tier(r[15]) if len(r) > 15 else ''
    if a and b:
        both += 1
    elif a:
        c14 += 1
    elif b:
        c15 += 1
        v15.append(int(float(b)))
    else:
        neither += 1
    if a:
        v14.append(int(float(a)))
print('  sidecar 行 %d：col14 有%-5d col15 有%-5d 两者都有 %-5d 都空 %-5d'
      % (len(side), c14, c15, both, neither))
for tag, vs in (('col14 装填性能', v14), ('col15 装填时间（回退源）', v15)):
    if not vs:
        continue
    s = sorted(vs)
    dom = sum(1 for v in s if 0 <= float(RAW.reload_raw(v)) <= 10)
    print('  %-24s n=%-5d 面板 min=%-6d p50=%-6d p99=%-6d max=%-7d 换算后在域内 %d/%d'
          % (tag, len(s), s[0], s[len(s) // 2], s[int(len(s) * 0.99)], s[-1], dom, len(s)))
    cc = collections.Counter(v for v in s if not (0 <= float(RAW.reload_raw(v)) <= 10))
    print('      换算越域的面板值 top: %s' % cc.most_common(8))
