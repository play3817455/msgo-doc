# -*- coding: utf-8 -*-
"""按码点比对 CSV 页面名与 cache 文件名（排查字符级差异）。"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'wiki_ms_weapons.csv'),
                                encoding='utf-8-sig', newline='')))
pgs = sorted(set(r['#页面'] for r in rows if '钢加农' in r['#页面']))
files = [n[:-4] for n in os.listdir(os.path.join(HERE, 'cache')) if '钢加农' in n]
for p in pgs:
    print('CSV  :', [hex(ord(c)) for c in p], p)
for f in files:
    print('FILE :', [hex(ord(c)) for c in f], f)
