# -*- coding: utf-8 -*-
"""C3 取证 ⑥：sidecar col12 空的武器，wiki 原始表里到底有没有「連射速度」。"""
import os, sys, csv, io, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import weapon_client_raw as RAW

WIKI = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
W = [r for r in csv.reader(open(WIKI, encoding='utf-8-sig', errors='replace')) if r and any(x.strip() for x in r)]
H = W[0]
print("wiki 表头 %d 列: %s" % (len(H), H))
print("行数 %d" % (len(W) - 1))
# col2 数据格式?
print("col0/1/2 取值分布样例:", collections.Counter(tuple(r[:3]) for r in W[1:]).most_common(4))

SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
S = [r for r in csv.reader(open(SIDE, encoding='utf-8', errors='replace')) if r and any(x.strip() for x in r)]
# sidecar 行 -> wiki 行 的桥：sidecar col1=武器ID, col0=#練度ID
print()
print("sidecar 表头:", [x.strip() for x in S[0]][:8])
empty_keys = [r for r in S[1:] if len(r) > 12 and r[1].strip().isdigit() and not RAW.first_tier(r[12])]
print("sidecar col12 空的行 %d" % len(empty_keys))
for r in empty_keys[:6]:
    print("   key=%-10s col0=%-8s col3类别=%-10s col5名=%-16s col10威力=%-10s col13射程=%-8s col14装填=%-8s"
          % (r[1].strip(), r[0].strip(), r[3].strip(), r[5].strip(), r[10].strip(), r[13].strip(), r[14].strip()))
print()
# 这些 key 在 wiki 里有没有 連射(col10)
byproc = collections.defaultdict(list)
for r in W[1:]:
    byproc[r[0].strip()].append(r)
hit = miss = 0
for r in empty_keys:
    page = r[4].strip()
    ws = byproc.get(page, [])
    got = [w[10].strip() for w in ws if len(w) > 10 and RAW.first_tier(w[10])]
    if got:
        hit += 1
        if hit <= 5:
            print("  命中：key=%s 页面=%s wiki 連射=%s（sidecar col12 空）" % (r[1].strip(), page, got))
    else:
        miss += 1
print()
print("col12 空的 %d 行里：wiki 页面能找到非空「連射速度」的 %d 行；找不到的 %d 行" % (len(empty_keys), hit, miss))
