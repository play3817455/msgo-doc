# -*- coding: utf-8 -*-
"""扫 `unpackdat/script/**/*.nut`（**UTF-16LE + BOM** ✓）找关键字所在文件与行。

★ 2026-09-17：一直以为脚本"加密读不了" ✗ —— 其实是**读法错**（当 utf-8 读 ✗）。
  真身 = UTF-16LE（头 `ff fe` ✓）⇒ 直接 decode 就是可读源码 ✓✓
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'f:\9ymsgo\9you\unpackdat'
KWS = sys.argv[1:] or ['演習', '練習', 'practice', 'Practice', 'getTutorialFlags',
                       'getTutorialFlag', '大規模戦演習', '開始大規模戦']

hits = {}
nfile = 0
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if not f.lower().endswith(('.nut', '.nut.bin')):
            continue
        p = os.path.join(dp, f)
        try:
            b = open(p, 'rb').read()
        except OSError:
            continue
        if b[:2] != b'\xff\xfe':
            continue
        nfile += 1
        try:
            t = b.decode('utf-16-le')
        except UnicodeDecodeError:
            continue
        L = t.splitlines()
        if 'bin' in f.lower():  # .nut.bin 是同一份脚本的二进制包装 ⇒ 跳过重复
            continue
        for i, l in enumerate(L, 1):
            for kw in KWS:
                if kw in l:
                    hits.setdefault(p, []).append((i, kw, l.strip()[:150]))
                    break

print('扫了 %d 个 UTF-16LE 脚本文件；命中 %d 个文件\n' % (nfile, len(hits)))
for p, rows in sorted(hits.items(), key=lambda kv: -len(kv[1])):
    print('== %s（%d 处）' % (p.replace(ROOT, ''), len(rows)))
    for i, kw, l in rows[:12]:
        print('   %5d [%s] %s' % (i, kw, l))
    print()
