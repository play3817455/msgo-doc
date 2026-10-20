# -*- coding: utf-8 -*-
"""数值可追溯性体检：CSV 里一行的各格数值，必须能在**原文的同一个连续小窗口**里同时找到。

原理：列错位 = 读了隔壁行的格 ⇒ 本行的值分散在**不同行**上，凑不到同一个窗口里。
      而同一把武器在同一页出现多次（表格 + 纯“可携带性”表 + 日文表）是正常的，
      所以不能用「名字附近」定位，只能用「本行所有值共处一个窗口」判定。

用法：python _probe_verify_values.py [窗口半宽=10] [最多打印条数=40] [--page 页面名]
"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
CSV = os.path.join(HERE, 'wiki_ms_weapons.csv')
CHECK = ['威力', '集弹性能', '射程距离', '装填时间', '锁定', '重量', '弹数']


def norm_num(v):
    """取数值首段（`2,500` / `550 (605)` / `550(605)` → `550`），去千分位。"""
    s = re.sub(r'<[^>]*>', ' ', str(v))
    m = re.search(r'-?\d+(?:\.\d+)?', s.replace(',', ''))
    return m.group(0) if m else ''


def page_lines(title):
    """★跟随重定向（与 `parse_cache.main` 同规矩）。"""
    seen = set()
    while True:
        p = os.path.join(CACHE, re.sub(r'[\\/:*?"<>|]', '_', title) + '.txt')
        if not os.path.exists(p) or title in seen:
            return []
        seen.add(title)
        text = open(p, encoding='utf-8').read()
        if not text.lstrip().startswith(('#重定向', '#redirect', '#REDIRECT')):
            return text.replace('\r\n', '\n').split('\n')
        m = re.search(r'\[\[\s*([^\]|]+)', text)
        if not m:
            return []
        title = m.group(1).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    half = int(args[0]) if args else 10
    maxshow = int(args[1]) if len(args) > 1 else 40
    only = None
    if '--page' in sys.argv:
        only = sys.argv[sys.argv.index('--page') + 1]
    rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig', newline='')))
    cache, bad, checked = {}, [], 0
    for r in rows:
        pg = r['#页面']
        if pg.startswith('#') or (only and only not in pg):
            continue
        if pg not in cache:
            lines = page_lines(pg)
            flat = [l.replace(',', '').replace('，', '').replace(' ', '') for l in lines]
            cache[pg] = flat
        lines = cache[pg]
        if not lines:
            continue
        vals = [(c, norm_num(r.get(c, ''))) for c in CHECK]
        vals = [(c, v) for c, v in vals if v]
        if not vals:
            continue
        checked += 1
        anchors = [i for i, l in enumerate(lines) if vals[0][1] in l] or list(range(len(lines)))
        ok = False
        for a in anchors:
            lo, hi = max(0, a - half), min(len(lines), a + half + 1)
            if all(any(v in lines[i] for i in range(lo, hi)) for _c, v in vals):
                ok = True
                break
        if not ok:
            bad.append((pg, r['武器名'], r.get('数据格式'),
                        ','.join('%s=%s' % (c, v) for c, v in vals), r.get('机体序号')))
    print('体检 %d 行，同窗口凑不齐 %d 行（%.2f%%）' % (checked, len(bad), 100.0 * len(bad) / max(1, checked)))
    for pg, nm, fmt, vs, sn in bad[:maxshow]:
        print('  %-40s %-26s %-6s %s' % (pg[:40], nm[:26], fmt, vs))
    if len(bad) > maxshow:
        print('  ... 另有 %d 行' % (len(bad) - maxshow))
    return 0


if __name__ == '__main__':
    sys.exit(main())
