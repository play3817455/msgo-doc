# -*- coding: utf-8 -*-
"""C3 取证 ⑥：sidecar col12 空 的那些武器，wiki 原始表里到底有没有「連射速度」。"""
import os, sys, csv, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
WIKI = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
b = open(WIKI, 'rb').read()
print("wiki 文件 %d 字节；前 3 字节 %s" % (len(b), b[:3]))
for enc in ('utf-8-sig', 'cp932', 'gbk', 'shift_jis'):
    try:
        t = b.decode(enc)
        print("  %-10s OK  首行: %s" % (enc, t.split('\n')[0][:160]))
    except Exception as e:
        print("  %-10s FAIL %s" % (enc, e)[:80])
