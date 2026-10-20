# -*- coding: utf-8 -*-
"""把「CSV 页面名 vs cache 文件名」的比对结果写成 JSON（避免控制台编码搅乱）。"""
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
rows = list(csv.DictReader(open(os.path.join(HERE, 'wiki_ms_weapons.csv'),
                                encoding='utf-8-sig', newline='')))
names = os.listdir(CACHE)
out = []
for p in sorted(set(r['#页面'] for r in rows)):
    if p.startswith('#'):
        continue
    fn = re.sub(r'[\\/:*?"<>|]', '_', p) + '.txt'
    if fn not in names:
        near = [n for n in names if n[:3] == p[:3]]
        out.append({'page': p, 'page_len': len(p), 'want': fn,
                    'exists_plain': os.path.exists(os.path.join(CACHE, p + '.txt')),
                    'near': near[:6]})
json.dump(out, open(os.path.join(HERE, '_probe_pagematch.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('missing count', len(out))
