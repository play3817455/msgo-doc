# -*- coding: utf-8 -*-
"""畸形行守卫：`fields.csv` 的**形状**必须一直是 10 列，模型侧 `needs_review` 必须为 0。

坑㊳ 的背景：`fields.csv` 是手写的、以逗号分隔，凡是在「线类型」「含义」「用途」
「证据VA」里写了逗号的，都会被读成多列。全库曾有 230 行这样（占 6%）：

  - 线类型 `array<item,A1>`、`struct{11,12}` → 逗号把类型劈成两格（103 行）
  - 含义/用途里的 `cmp ebx,68h` → 逗号把短语劈成两格（99 行）
  - 闭合行漏了「取值或枚举」列 → 整行只有 9 格（33 行）
  - `bytes` + `NUL串` 两格 → 本该是一格 `bytes(NUL 串)`（5 行）

导入器在 `repair_row` 里各自启发式拼回，所以**形状坏了不一定立刻报错**，而是悄悄
把字段名变成 `f_0`、把含义和用途调换。这正是要守卫的点：形状一坏，先炸出来。

判据两条，都不需要 README，跑得飞快：
  1. 每行恰好 10 格、表头字面一致；
  2. 模型里 `needs_review` 的字段数为 0（导入器给畸形行打的标）。
"""
from __future__ import annotations

import csv
import glob
import io
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = 'protocol_analysis/commands'
CMDS = 'db_design/schema/commands'
HEADER = ['序号', '偏移', '长度', '线类型', '字段名', '含义', '用途', '取值或枚举', '证据VA', '置信度']


def main() -> int:
    bad_cols: list[str] = []
    bad_header: list[str] = []
    rows_total = 0
    files = 0
    shape = Counter()
    for p in sorted(glob.glob(os.path.join(ROOT, '*', 'fields.csv'))):
        files += 1
        rows = list(csv.reader(io.open(p, encoding='utf-8-sig', newline='')))
        if not rows:
            bad_header.append('%s(空)' % p)
            continue
        if [c.strip() for c in rows[0]] != HEADER:
            bad_header.append(p)
        for ln, row in enumerate(rows[1:], start=2):
            if not any(c.strip() for c in row):
                continue
            rows_total += 1
            shape[len(row)] += 1
            if len(row) != 10:
                bad_cols.append('%s:%d  %d 列' % (os.path.basename(os.path.dirname(p)), ln, len(row)))

    review: list[str] = []
    n_cmds = 0
    for p in sorted(glob.glob(os.path.join(CMDS, '*.json'))):
        if os.path.basename(p).startswith('_'):
            continue
        d = json.load(io.open(p, encoding='utf-8'))
        if 'fields' not in d:
            continue
        n_cmds += 1
        n = sum(1 for f in d['fields'] if f.get('needs_review'))
        if n:
            review.append('%s  %d 行' % (d['id'], n))

    print('畸形行守卫：')
    print('  fields.csv 文件        %d' % files)
    print('  字段行                 %d   列数分布 %s' % (rows_total, dict(shape)))
    print('  表头异常               %d' % len(bad_header))
    print('  列数 != 10 的行        %d' % len(bad_cols))
    print('  模型 needs_review 字段 %d（涉及 %d 条命令）' % (len(review), len(review)))
    for x in bad_header[:5]:
        print('    - 表头', x)
    for x in bad_cols[:8]:
        print('    -', x)
    for x in review[:8]:
        print('    -', x)
    ok = not bad_cols and not bad_header and not review
    print()
    print('结论：' + ('形状完好（OK）' if ok else '**有畸形行或未还原字段**'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
