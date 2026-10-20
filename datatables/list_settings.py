# -*- coding: utf-8 -*-
"""list_settings.py —— 列出 unpackdat/settings 全部文件 + 行数 + 前 2 行，找名字源。"""
import glob
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, 'unpackdat', 'settings')


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


files = sorted(os.listdir(S))
print('settings 下共 %d 个文件' % len(files))
for n in files:
    p = os.path.join(S, n)
    if os.path.isdir(p):
        print('  [dir] %s' % n)
        continue
    sz = os.path.getsize(p)
    if n.lower().endswith(('.csv', '.txt')):
        t = read(p)
        L = [x for x in t.replace('\r\n', '\n').split('\n') if x.strip()]
        print('  %-40s %8d B  %5d 行  | %s' % (n, sz, len(L), (L[0][:80] if L else '')))
    else:
        print('  %-40s %8d B' % (n, sz))
