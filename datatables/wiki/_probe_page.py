# -*- coding: utf-8 -*-
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
t = open(sys.argv[1], encoding='utf-8').read()
print('长度', len(t))
print('含基础性能模板:', '高达OL基础性能' in t)
print('含武器-性能:', '武器-性能' in t)
print('含wikitable:', 'wikitable' in t)
print('含{{ :', '{{' in t)
for kw in ('基础性能', '装甲', '最高速度', '威力', '射程', 'COST', '武器', '机体'):
    print('  关键字[%s] 位置 %s' % (kw, t.find(kw)))
print('===== 前 3000 字 =====')
print(t[:3000])
