# -*- coding: utf-8 -*-
import io, os, sys, csv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
P = os.path.join(ROOT, 'gow_wiki/data/weapons_combat_calc.csv')
b = open(P, 'rb').read()
o = io.open(os.path.join(HERE, '_probe_b7_fixture3.txt'), 'w', encoding='utf-8')
o.write('bytes=%d  BOM=%r\n' % (len(b), b[:3]))
o.write('first line raw repr: %r\n' % b.split(b'\n')[0])
for enc in ('utf-8-sig', 'gbk', 'cp932', 'utf-8'):
    try:
        line = b.split(b'\n')[0].decode(enc)
        o.write('%-10s OK  header=%s\n' % (enc, line.split(',')))
    except Exception as e:
        o.write('%-10s FAIL %s\n' % (enc, e))
o.close()
print('ok')
