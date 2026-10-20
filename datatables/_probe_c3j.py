# -*- coding: utf-8 -*-
"""C3 取证 ⑧（终局）：#36 里 col12 为空的那些 RAPIDDELAY 行，拿到 wiki 原始表按
(页面, 武器名) 精确定位同一把武器的那一行，看值对不对得上。"""
import os, sys, csv, io, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import psycopg
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
import weapon_client_raw as RAW

def rd(p, enc='utf-8'):
    return [r for r in csv.reader(open(p, encoding=enc, errors='replace')) if r and any(x.strip() for x in r)]

S = rd(os.path.join(HERE, 'names', '武器分配明细.csv'))
info = {}
for r in S[1:]:
    if len(r) > 12 and r[1].strip().isdigit():
        info[r[1].strip()] = (r[4].strip(), r[5].strip())

W = rd(os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv'), 'utf-8-sig')
byrow = collections.defaultdict(list)
for r in W[1:]:
    if len(r) > 10:
        byrow[(r[0].strip(), r[3].strip())].append(r[10].strip())

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name)='RAPIDDELAY'""")
    rap = [(k, float(v)) for k, v in cur.fetchall()]

tally = collections.Counter()
samples = collections.defaultdict(list)
for k, v in rap:
    page, name = info.get(k, ('?', '?'))
    if not RAW.first_tier(page) if False else False:
        pass
    ws = byrow.get((page, name), [])
    nums = set()
    for s in ws:
        t = RAW.first_tier(s)
        if t:
            nums.add(int(float(t)))
    if not nums:
        tally['wiki 同名行也无「連射」'] += 1
        if len(samples['none']) < 6:
            samples['none'].append((k, v, page, name, ws[:3]))
        continue
    if v in nums:
        tally['DB 值 == wiki 同一行的 連射速度（4 位数刻度）'] += 1
    elif v * 10 in nums:
        tally['DB 值 ×10 == wiki 值'] += 1
    else:
        # 反过来：wiki 值能不能解释 DB 值
        exp = set()
        for n in nums:
            exp.add(round(float(RAW.rapid_raw(n)), 6))
        if any(abs(v - e) < 5e-5 for e in exp):
            tally['DB 值 == rapid_raw(wiki 值)（原值刻度）'] += 1
        else:
            tally['对不上'] += 1
            if len(samples['bad']) < 10:
                samples['bad'].append((k, v, page, name, sorted(nums)[:6]))
print("=== #36 RAPIDDELAY 共 %d 行，按 (页面,武器名) 对 wiki ===" % len(rap))
for k, n in tally.most_common():
    print("  %-46s %4d" % (k, n))
print()
for tag, ss in samples.items():
    print("--- %s ---" % tag)
    for s in ss:
        print("   ", s)
