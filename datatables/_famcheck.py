# -*- coding: utf-8 -*-
import os, sys, io, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(os.path.dirname(ROOT), '机动战士敢达Online', 'GundamOnline', 'unpackdat', 'settings')


def hx(p):
    return [l.split(',')[0].strip() for l in open(p, encoding='utf-8', errors='replace').read().splitlines()
            if l.strip() and not l.startswith('#')]


W = [x for x in hx(os.path.join(SET, 'weapon_visual_customize.csv')) if x.isdigit()]
M = [l.split(',')[1].strip() for l in open(os.path.join(SET, 'msma_mesh_customize.csv'), encoding='utf-8', errors='replace').read().splitlines()
     if l.strip() and not l.startswith('#') and len(l.split(',')) > 1]
M = [x for x in M if x.isdigit()]
IDS = sorted(set(W + M))
print('真实武器ID %d 个' % len(IDS))

# 每个真实武器ID 反推 lid[1:6]（= 武器ID[1:6]），再看 msma_settings 里哪些 lid 匹配
S = [r for r in __import__('csv').reader(open(os.path.join(os.path.dirname(ROOT), 'server/datafiles/lounge/msma/msma_settings.csv'),
                                             encoding='utf-8-sig')) if r and r[0].strip().isdigit()]
byfam = collections.defaultdict(list)
for r in S:
    byfam[r[0].strip()[1:6]].append((r[0].strip(), r[5]))

print()
print('--- 真实武器ID 归属的「家族」里是否有**跨阵营**成员（lid[6] 不同）---')
cross = 0
for w in IDS:
    fam = w[1:6]
    mem = byfam.get(fam, [])
    f6 = set(l[6] for l, _ in mem)
    if len(f6) > 1:
        cross += 1
        if cross <= 8:
            print('  %s (家族 %s) 归属候选: %s' % (w, fam, mem))
print('  ⇒ 落在跨阵营家族的真实武器ID: %d / %d' % (cross, len(IDS)))

print()
print('--- 家族内 lid[5] 与 sub4[0] 一致性复核 ---')
ok = bad = 0
for w in IDS:
    fam = w[1:6]
    sub4 = w[5:9]
    mem = byfam.get(fam, [])
    if not mem:
        continue
    if any(m[5] == sub4[0] for m, _ in mem):
        ok += 1
    else:
        bad += 1
        print('   ✗ %s sub4=%s 家族 lid[5]值=%s' % (w, sub4, sorted(set(m[5] for m, _ in mem))))
print('  ✓ %d / ✗ %d' % (ok, bad))

print()
print('--- 阵营对（lid[6]=1 vs 2）示例：武器ID 池是否相同？---')
# 取一个真实武器ID，看其家族的两个阵营成员
for w in IDS[:6]:
    fam = w[1:6]
    mem = byfam.get(fam, [])
    print('  %s → %s' % (w, mem))
