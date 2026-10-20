# -*- coding: utf-8 -*-
"""全量体检表头字面量：把 cache 里所有 wikitable 的表头格收集起来，按出现次数排序。

用途：
  1. 找出「看着像武器列但 `canon_hdr` 映射不到」的异体写法（该进 `HDR_SYN`）；
  2. 找出「含威力但表头明显不是武器表」的误收表（该在 `parse_weapons` 里挡掉）。
用法：python _probe_c4_headers.py [--cols]
      --cols  只打印**含「威力」**的表（会被 `parse_weapons` 收走的那批）
"""
import csv
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import parse_cache as P


def main():
    only_weapon = '--cols' in sys.argv
    fs = sorted(f for f in os.listdir(P.CACHE) if f.endswith('.txt'))
    lit = Counter()          # 原始字面量 → 次数（含威力的表）
    unmapped = defaultdict(set)   # 原始字面量 → 出现的页面
    per_col = Counter()      # 规范化后的列名 → 次数
    bad = Counter()          # 「含威力但列名可疑」的表
    n_all = n_weap = 0
    for f in fs:
        title = f[:-4]
        text = open(os.path.join(P.CACHE, f), encoding='utf-8').read()
        for headers, _rows in P.tables(text):
            n_all += 1
            if not headers:
                continue
            raws = [h for h in headers]
            if '威力' not in raws:
                continue
            n_weap += 1
            if only_weapon:
                print('%-40s %s' % (title[:40], raws))
            for h in raws:
                lit[h] += 1
                per_col[h] += 1
                if h not in P.WCOL and h not in ('武器名',):
                    unmapped[h].add(title)
            if '武器名' not in raws and '名称' not in raws:
                bad[tuple(raws)] += 1
    print('=' * 78)
    print('wikitable 总数 %d，其中含「威力」的（武器表）%d' % (n_all, n_weap))
    print('-' * 78)
    print('武器表表头字面量（次数）：')
    for h, c in lit.most_common():
        mark = 'OK ' if h in P.WCOL else '★  '
        print('  %s %-16s %5d   例：%s' % (mark, h, c, sorted(unmapped.get(h, []))[:2]))
    print('-' * 78)
    print('★ 含「威力」但**没有名称列**的表头组合（疑似误收）：')
    for k, c in bad.most_common(20):
        print('   %5d  %s' % (c, list(k)))


if __name__ == '__main__':
    main()
