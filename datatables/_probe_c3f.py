# -*- coding: utf-8 -*-
"""C3 取证 ⑤（决定性）：把 #36 的 RAPIDDELAY/COOLTIME 逐行对 sidecar 判真伪。

判据（全部来自 IDA 实测，见 weapon_client_raw.py / sub_80F1A0 case 4）：
  机库「連射速度」白字 = trunc((2 - raw) * 0.5263158 * 1500 + 0.4)
  ⇒ 表里 RAPIDDELAY 必须落在 raw 域 [~0.06, ~2.01]；落在域外的值不可能是 rapid_raw 的产物。
"""
import os, sys, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import psycopg
from restore_purged_weapon_keys import DSN
import weapon_client_raw as RAW

LO, HI = 0.05, 2.01

SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
rows = [r for r in csv.reader(
    open(SIDE, encoding='utf-8', errors='replace', newline='').read().replace('\r\n', '\n').split('\n'))
    if r and any(x.strip() for x in r)]
sc = {}
for r in rows[1:]:
    if len(r) > 13 and r[1].strip():
        sc[r[1].strip()] = r

print("sidecar 键 %d；col12 非空 %d" % (len(sc), sum(1 for r in sc.values() if r[12].strip())))

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select btrim(attr_name), btrim(weapon_id_key), btrim(attr_value)
                   from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name) in ('RAPIDDELAY','COOLTIME')""")
    db = cur.fetchall()

for attr in ('RAPIDDELAY', 'COOLTIME'):
    rws = [(k, v) for a, k, v in db if a == attr]
    ok = bad = nokey = emptycol = 0
    badsamp, nokeysamp, emptysamp = [], [], []
    for k, v in rws:
        try:
            f = float(v)
        except ValueError:
            bad += 1
            badsamp.append((k, v))
            continue
        r = sc.get(k)
        if r is None:
            nokey += 1
            if len(nokeysamp) < 8:
                nokeysamp.append((k, v))
            continue
        c12 = RAW.first_tier(r[12])
        if not c12:
            emptycol += 1
            if len(emptysamp) < 8:
                emptysamp.append((k, v))
            continue
        exp = float(RAW.rapid_raw(c12))
        if abs(f - exp) < 5e-5:
            ok += 1
        else:
            bad += 1
            if len(badsamp) < 12:
                badsamp.append((k, v, '期望 %s (col12=%s)' % (RAW.rapid_raw(c12), r[12].strip())))
    print()
    print("=== %s 共 %d 行 ===" % (attr, len(rws)))
    print("  ① sidecar col12 能对上（真值）      : %4d" % ok)
    print("  ② sidecar 有键但 col12 空（无来源）  : %4d  %s" % (emptycol, emptysamp[:5]))
    print("  ③ sidecar 无此键                    : %4d  %s" % (nokey, nokeysamp[:5]))
    print("  ④ 与 col12 推出的值不符（错列/旧写） : %4d  %s" % (bad, badsamp[:8]))
    inband = sum(1 for k, v in rws if v.replace('.', '').lstrip('-').isdigit() and LO <= float(v) <= HI)
    print("  域内 [%.2f,%.2f] 的行数            : %4d / %d" % (LO, HI, inband, len(rws)))
    outband = [(k, v) for k, v in rws if v.replace('.', '').lstrip('-').isdigit() and not (LO <= float(v) <= HI)]
    print("  域外样例:", outband[:8])
    # 域外里有多少同时 col12 非空（= 明确可修）
    fix = [k for k, v in outband if k in sc and RAW.first_tier(sc[k][12])]
    print("  域外且 col12 非空（可修回真值）      : %d" % len(fix))
