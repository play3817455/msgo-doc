# -*- coding: utf-8 -*-
"""C4：验收新解析器的两个决定性页面。"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'wiki'))
import parse_cache as PC  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CASES = [
    ('高达OL帕拉斯·雅典娜(重击装备)(国)', '蓄力式腕部2连光束枪',
     {'威力': '2,600', '集弹性能': '880', '射程距离': '630', '装填时间': '640', '锁定': '760'}),
    ('高达OL帕拉斯·雅典娜(重击装备)(国)', '腕部2连光束枪',
     {'威力': '3,200', '集弹性能': '900', '射程距离': '750', '装填时间': '640', '锁定': '740'}),
]
for title, wname, want in CASES:
    p = os.path.join(PC.CACHE, title + '.txt')
    text = open(p, encoding='utf-8').read()
    got = None
    for r in PC.parse_weapons(title, text, {}):
        if r.get('武器名') == wname:
            got = r
            break
    print('=' * 70)
    print('%s / %s' % (title, wname))
    if not got:
        print('   ✗ 没解析到')
        continue
    for k, v in want.items():
        g = str(got.get(k, '')).strip()
        print('   %-8s 期望 %-8s 实得 %-8s %s' % (k, v, g, 'OK' if g == v else '✗'))

# 第二组：修理喷枪页（表头 colspan、异体列名、装填<br/>时间）
for title in ['高达OL陆战型吉姆']:
    p = os.path.join(PC.CACHE, title + '.txt')
    text = open(p, encoding='utf-8').read()
    print('=' * 70)
    print(title)
    n = 0
    for r in PC.parse_weapons(title, text, {}):
        if r.get('武器名') in ('修理喷枪', '100mm机枪', '光束喷枪'):
            print('   %-14s 重量=%-6s 弹数=%-8s 威力=%-6s 射程=%-6s 装填时间=%-5s 锁定=%-5s 装填性能=%s'
                  % (r.get('武器名'), r.get('重量', ''), r.get('弹数', ''), r.get('威力', ''),
                     r.get('射程距离', ''), r.get('装填时间', ''), r.get('锁定', ''), r.get('装填性能', '')))
            n += 1
    if not n:
        print('   ✗ 没解析到')
