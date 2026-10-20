# -*- coding: utf-8 -*-
"""find_modelid_refs.py —— 用已确认的模型号反查：它到底写在哪个文件的哪张表里。

已知（用户实测 / 客户端表确认）：
   101020201 = ジム・トレーナー(chara/01/01/0202)    121010201 = ザク・ワーカー(chara/01/21/0102)
   101285001 = フリーダム(chara/01/01/2850)          101284001 = カラミティ(chara/01/01/2840)
   101280101 = エールストライク(chara/01/01/2801)    190300101 = スローネアイン(chara/01/03/3001)
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = ['101020201', '121010201', '101285001', '101284001', '101280101', '190300101']
ROOTS = [os.path.join(ROOT, 'server', 'datafiles'),          # ★服务端在发的表（最该查）
         os.path.join(ROOT, 'unpackdat', 'settings'),
         os.path.join(ROOT, 'unpackdat', 'loungue')]
MAXSZ = 4 * 1024 * 1024


def read_text(p):
    try:
        b = open(p, 'rb').read(MAXSZ)
    except Exception:
        return ''
    for enc in ('utf-8', 'cp932', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return ''


for base in ROOTS:
    if not os.path.isdir(base):
        print('(缺目录) %s' % base)
        continue
    print('================ %s ================' % os.path.relpath(base, ROOT))
    n = 0
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if not f.lower().endswith(('.csv', '.txt')):
                continue
            p = os.path.join(dp, f)
            t = read_text(p)
            if not t:
                continue
            for ln, line in enumerate(t.splitlines(), 1):
                for tg in TARGETS:
                    if tg in line:
                        cols = [i for i, x in enumerate(line.split(',')) if x.strip() == tg]
                        print('  %-58s L%-5d 列%s  %s'
                              % (os.path.relpath(p, base), ln, cols, line[:130]))
                        n += 1
    print('  → 命中 %d 处' % n)
