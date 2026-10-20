# -*- coding: utf-8 -*-
"""probe_res.py —— 探测资源文件里到底写了什么机体数据（用户判断：数据可能在资源里）。

查三样：
 A. attr/*.vra（明文）里的 mesh 名 / material_id / Geometry —— 是否含武器挂点
 B. motionlist.csv 的动作段分布（000xx=基础 09xxx=必杀 10xxx=武器动作?）
 C. 服务端 #5 表 (msma_model.csv) 每一列的实际内容 —— 找出我们没用过但"有信息"的列
"""
import collections
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROOT, 'unpackdat', 'chara')

print('================ A. attr/*.vra（明文）里的网格与材质 ================')
for d in ('01/01/2850', '01/01/0202', '01/01/2840', '01/21/0102'):
    fs = glob.glob(os.path.join(UD, d, 'attr', '*.vra'))
    if not fs:
        continue
    t = open(fs[0], encoding='utf-8', errors='replace').read()
    names = re.findall(r'\(name string[^"]*"([^"]+)"', t)
    mats = re.findall(r'\(material_id[^0-9]*([0-9]+)', t)
    geo = re.findall(r'\(Geometry string[^"]*"([^"]+)"', t)
    tex = re.findall(r'\(texture string[^"]*"([^"]+)"', t)
    print('--- %s  mesh %d 个  geometry=%s' % (d, len(names), geo[:1]))
    print('    mesh:', names)
    print('    vramat id:', mats[:12], ' texture:', tex[:3])

print()
print('================ B. motionlist.csv 动作段分布 ================')
def seg(p):
    c = collections.Counter()
    for l in open(p, encoding='utf-8', errors='replace'):
        f = l.strip().split(',')
        if f and f[0].isdigit():
            c[int(f[0]) // 1000] += 1
    return dict(sorted(c.items()))
for d in ('01/01/2850', '01/01/2840', '01/01/0202', '01/34/0202', '01/21/0102'):
    p = os.path.join(UD, d, 'motionlist.csv')
    if os.path.exists(p):
        s = seg(p)
        ids = [int(l.split(',')[0]) for l in open(p, encoding='utf-8', errors='replace')
               if l.strip().split(',')[0].isdigit()]
        w = sorted(x for x in ids if 10000 <= x < 11000)     # 10xxx = 武器动作段？
        print('  %-12s 段计数 %-56s 10xxx(%d 个)前20=%s'
              % (d, s, len(w), w[:20]))

print()
print('================ C. #5 msma_model.csv 每列内容 ================')
M = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_model.csv')
lines = [l for l in open(M, encoding='utf-8', errors='replace').read().splitlines() if l.strip()]
rows = [l.rstrip(',').split(',') for l in lines if not l.startswith('#')]
print('  行数 %d，列数分布 %s' % (len(rows), collections.Counter(len(r) for r in rows).most_common(5)))
ncol = max(len(r) for r in rows)
for c in range(ncol):
    vals = [(r[c] if c < len(r) else '') for r in rows]
    nz = [v for v in vals if v.strip()]
    u = sorted(set(nz))
    flag = '★' if (len(nz) > 100 and 1 < len(u) < 500) else ' '
    if c < 4 or flag == '★':
        print('  %s列%2d 非空%3d/%d 唯一%3d  样例 %s' % (flag, c, len(nz), len(rows), len(u), u[:6]))
