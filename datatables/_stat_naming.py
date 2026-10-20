# -*- coding: utf-8 -*-
import json, glob, collections, os
c = collections.Counter()
n = collections.Counter()
conf = collections.Counter()
for f in glob.glob(os.path.join('db_design', 'schema', 'cfg', 'tables', '*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for col in d.get('columns', []):
        c[col.get('status')] += 1
        nm = str(col.get('db_column') or '')
        if nm.startswith('unknown_u32'):
            n['unknown_u32'] += 1
        elif nm.startswith('reserved'):
            n['reserved_*'] += 1
        elif nm.startswith('col'):
            n['colN'] += 1
        else:
            n['named'] += 1
        conf[(col.get('status'), col.get('confidence'))] += 1
print('status:', dict(c))
print('naming:', dict(n))
for k, v in sorted(conf.items(), key=lambda kv: -kv[1]):
    print('   ', k, v)
