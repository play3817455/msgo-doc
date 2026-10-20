# -*- coding: utf-8 -*-
import csv, os, io
HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
rows = [r for r in csv.reader(open(WIKI, encoding='utf-8-sig', errors='replace')) if r and any(x.strip() for x in r)]
pages = {}
for r in rows:
    if r[0].startswith('#'):
        continue
    if '凤凰' in r[0] or '菲尼克斯' in r[0]:
        pages.setdefault(r[0], []).append(r)
out = []
for p, lst in pages.items():
    out.append('PAGE=%r  行数=%d  code=%s' % (p, len(lst), lst[0][1]))
    for r in lst:
        out.append('    col3(武器名)=%r col8(武器数?)=%r' % (r[3] if len(r) > 3 else '', r[8] if len(r) > 8 else ''))
open(os.path.join(HERE, 'names', '_phx_pages.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
