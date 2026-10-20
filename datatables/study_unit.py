# -*- coding: utf-8 -*-
"""study_unit.py —— 把**一个机体编号(C)**挖穿：列出它在所有系列里的目录、代号、文件构成。

用法：python datatables/study_unit.py 0202
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def rows(p):
    return [[f.strip() for f in l.rstrip(',').split(',')]
            for l in read(p).replace('\r\n', '\n').split('\n')
            if l.strip() and not l.lstrip().startswith('#')]


C = sys.argv[1] if len(sys.argv) > 1 else '0202'
print('===== 机体编号 C=%s 的全部目录 =====' % C)
hits = []
for f in rows(os.path.join(HERE, 'names', 'chara模型代号.csv')):
    if len(f) < 6:
        continue
    if f[2].zfill(4) == C:
        hits.append((int(f[0]), int(f[1]), f[3], f[4], f[5]))
print('chara模型代号.csv 里 %d 条：' % len(hits))
for a, b, code, val, src in sorted(hits):
    print('   chara/%02d/%02d/%s   代号=%-20s 打包值=%s' % (a, b, C, code, val))

print()
print('===== 磁盘上真实存在的目录 & 文件构成 =====')
for d in sorted(glob.glob(os.path.join(ROOT, 'unpackdat', 'chara', '*', '*', C))):
    rel = os.path.relpath(d, os.path.join(ROOT, 'unpackdat')).replace('\\', '/')
    sub = sorted(os.listdir(d))
    files, samp = [], {}
    for s in sub:
        p2 = os.path.join(d, s)
        if os.path.isdir(p2):                      # ★目录才展开（有 motionlist.csv 这类文件）
            fs = sorted(os.listdir(p2))
            files.append('%s(%d)' % (s, len(fs)))
            if fs:
                samp[s] = fs[0]
        else:
            files.append('%s[文件]' % s)
    print('   %-24s %s' % (rel, ' '.join(files)))
    for s, x in samp.items():
        print('        %-10s 例: %s' % (s, x))

print()
print('===== 该 C 号在 icon / 其它地方 =====')
IC = os.path.join(ROOT, 'unpackdat', 'interface', 'icon')
for sub in sorted(os.listdir(IC)):
    p = os.path.join(IC, sub)
    if not os.path.isdir(p):
        continue
    n = [f for f in os.listdir(p) if C in f]
    if n:
        print('   icon/%s: %d 个 %s' % (sub, len(n), n[:4]))
    for s2 in os.listdir(p):
        if os.path.isdir(os.path.join(p, s2)):
            n2 = [f for f in os.listdir(os.path.join(p, s2)) if C in f]
            if n2:
                print('   icon/%s/%s: %d 个 %s' % (sub, s2, len(n2), n2[:4]))
