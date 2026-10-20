# -*- coding: utf-8 -*-
"""C4 ???HIGH_LOCKON ????????? 207 ? `HIGH_LOCKON` ????????

?? H1????????????????????**????**????????? `HIGH_LOCKON`
   ?? ??????? == sidecar col18?????????
?? H2?????????????**??????**???????
   ?? ??????????????????????

????????? `????`???????????????`<sup>?????` / ?? `????=`??
"""
import collections
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'wiki'))
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


side = {F.norm_key(r[1]): r for r in rd(F.SIDE) if len(r) > 1 and r[1].strip().isdigit()}
csvm = {(r[0].strip(), F.norm_key(r[1])) for r in rd(os.path.join(
    ROOT, 'server', 'datafiles', 'lounge', 'item', 'weapon_battle_detail.csv')) if len(r) > 1}


def cell(r, i):
    return (r[i].strip() if r and len(r) > i else '')


db = {}
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_value) from cfg.' + Q
                + 'WEAPON_BATTLE_DETAIL' + Q + " where btrim(attr_name)='HIGH_LOCKON'")
    for k, v in cur.fetchall():
        db[F.norm_key(k)] = v.strip()

stale = sorted(k for k in side if k in db and ('HIGH_LOCKON', k) not in csvm)
print('?? HIGH_LOCKON ? %d??????? %d?? CSV ???????%d'
      % (len(db), sum(1 for k in db if k in side), len(stale)))

num = lambda x: ('%.6f' % float(x)) if x else ''
hit18 = hit17 = hit_other = n18 = 0
for k in stale:
    v = num(db[k])
    g = num(RAW.first_tier(cell(side[k], 18)))     # col18 ????
    r = num(RAW.first_tier(cell(side[k], 17)))     # col17 ????
    if g and g == v:
        hit18 += 1
    elif r and r == v:
        hit17 += 1
    else:
        hit_other += 1
    n18 += 1 if g else 0
print('  ?? == sidecar col18???????%d / %d' % (hit18, len(stale)))
print('  ?? == sidecar col17???????%d' % hit17)
print('  ???????%d' % hit_other)
print('  ???? col18 ????%d???:' % n18)
for k in stale[:10]:
    print('     %-11s %-22s ?=%-10s ??=%-8s ??=%-8s ??=%s'
          % (k, cell(side[k], 5)[:22], db[k], cell(side[k], 18), cell(side[k], 17),
             cell(side[k], 4)[:24]))

CACHE = os.path.join(HERE, 'wiki', 'cache')
pages = sorted({cell(side[k], 4) for k in stale})
form = collections.Counter()
for p in pages:
    t = None
    for c in (p, p.replace('?', '(').replace('?', ')')):
        fp = os.path.join(CACHE, c + '.txt')
        if os.path.exists(fp):
            t = open(fp, encoding='utf-8').read()
            break
    if t is None:
        form['???'] += 1
        continue
    if re.search(r'????\s*=\s*\d', t):
        form['?? ????= ?'] += 1
    elif re.search(r'????\s*[:?]\s*\d', t):
        form['??? <sup>????? ?'] += 1
    else:
        form['???????'] += 1
print()
print('  ??????? %d ??????????: %s' % (len(pages), dict(form)))
