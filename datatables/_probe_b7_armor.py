# -*- coding: utf-8 -*-
"""临时探针：wiki units.json 的装甲分布（给 sim 的默认靶子取一个有出处的值）。"""
import io, json, os, re, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
U = json.load(io.open(os.path.join(ROOT, 'gow_wiki/data/units.json'), encoding='utf-8'))


def iv(s):
    v = re.findall(r'-?\d+', (s or '').replace(',', ''))
    return int(v[0]) if v else None


a = []
for u in U:
    v = iv(((u.get('panel') or {}).get('アーマー') or [None])[0])
    if v:
        a.append(v)
a.sort()
o = io.open(os.path.join(HERE, '_probe_b7_armor.txt'), 'w', encoding='utf-8')
o.write('n=%d min=%d p10=%d p25=%d 中位=%d p75=%d p90=%d max=%d 均值=%.0f\n'
        % (len(a), a[0], a[len(a)//10], a[len(a)//4], a[len(a)//2], a[3*len(a)//4],
           a[9*len(a)//10], a[-1], statistics.mean(a)))
o.write('4000 以下 %d 台；5000 以下 %d 台\n' % (sum(1 for x in a if x < 4000), sum(1 for x in a if x < 5000)))
o.close()
print('ok')
