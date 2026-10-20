# -*- coding: utf-8 -*-
"""列出 cache 里所有含「喷射导弹发射器」的文件名（JSON），并打印 CSV 原行。"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
info = [{'name': n, 'len': len(n), 'cps': [hex(ord(c)) for c in n]}
        for n in os.listdir(CACHE) if '喷射导弹发射器' in n]
json.dump(info, open(os.path.join(HERE, '_probe_ls.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('files:', len(info))
raw = open(os.path.join(HERE, 'wiki_ms_weapons.csv'), encoding='utf-8-sig').read().split('\n')
hit = [l for l in raw if '喷射导弹发射器' in l]
print('csv lines:', len(hit))
for l in hit[:4]:
    print(repr(l[:120]))
