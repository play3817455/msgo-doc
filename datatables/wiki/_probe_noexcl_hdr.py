# -*- coding: utf-8 -*-
"""体检：**表头没用 `!` 的武器表**（`|名称 |重量 … |威力 …`）——这类表现在被当键值网格丢掉。

判定：表里第一个「单元格里含规范列名 威力」的行块，出现在任何含 `!` 的行块之前（或整表无 `!`）。
用法：python _probe_noexcl_hdr.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import parse_cache as P

WANT = ('名称', '重量', '弹数', '威力', '射程距离', '装填时间')


def main():
    fs = sorted(f for f in os.listdir(P.CACHE) if f.endswith('.txt'))
    pages, tables, samples = set(), 0, []
    for f in fs:
        title = f[:-4]
        text = open(os.path.join(P.CACHE, f), encoding='utf-8').read()
        for headers, rows in P.tables(text):
            if headers:
                continue
            # 无表头：看行块里有没有「一整行都是列名」（含威力）
            for r in rows[:3]:
                cells = [P.canon_hdr(c) for c in r]
                if '威力' in cells and sum(1 for c in cells if c in WANT) >= 3:
                    tables += 1
                    pages.add(title)
                    if len(samples) < 25:
                        samples.append((title, cells, len(rows)))
                    break
    print('疑似「表头没写 ! 」的武器表：%d 张，涉及 %d 页' % (tables, len(pages)))
    for t, cells, n in samples:
        print('  %-42s rows=%-3d %s' % (t[:42], n, cells))
    return 0


if __name__ == '__main__':
    sys.exit(main())
