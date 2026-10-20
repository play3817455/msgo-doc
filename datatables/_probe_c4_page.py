# -*- coding: utf-8 -*-
"""C4：看某页解析出的全部武器行（原始 dict）。"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'wiki'))
import parse_cache as PC  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

for title in sys.argv[1:]:
    p = os.path.join(PC.CACHE, title + '.txt')
    text = open(p, encoding='utf-8').read()
    print('=' * 78)
    print(title)
    rs = PC.parse_weapons(title, text, {})
    print('  共 %d 行' % len(rs))
    for r in rs:
        print('   %-18s fmt=%-4s 威力=%-7s 集弹=%-6s 射程=%-6s 装填=%-6s 装填时=%-6s 锁定=%-6s 重量=%s'
              % (str(r.get('武器名'))[:18], r.get('数据格式', ''), r.get('威力', ''),
                 r.get('集弹性能', ''), r.get('射程距离', ''), r.get('装填性能', ''),
                 r.get('装填时间', ''), r.get('锁定', ''), r.get('重量', '')))
    print('  --- 表头一览 ---')
    for headers, rows in PC.tables(text):
        if headers:
            print('    hdr=%s  rows=%d' % ([PC.canon_hdr(h) for h in headers], len(rows)))
