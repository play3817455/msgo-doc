# -*- coding: utf-8 -*-
"""全量校验：每份 fields.csv 的**每一行**都拿同目录 README 的字段表逐列对位。

`_validate_fixcsv.py` 只跑「列数 != 10」的行——畸形行修完它就没东西可查了（自证空转）。
这里换成**无条件**逐行对照，用来回答两个问题：

  1. 修复后是否还有错列/错位（结构性）；
  2. 全部 3828 行的线类型/字段名/含义/用途/取值/证据VA 与 README 是否一致（语义性）。

README 是当初写 CSV 时的**上游**，所以列不一致只有两种解释：CSV 被逗号切坏了，
或者 README 后来改过而 CSV 没跟。两种都值得看一眼，但只有前者算这次修复的锅。
"""
from __future__ import annotations

import csv
import io
import pathlib
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import fix_fields_csv as F  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')
OUT = pathlib.Path('db_design/tools/_csvreadme_validate.txt')
HEADER = ['序号', '偏移', '长度', '线类型', '字段名', '含义', '用途', '取值或枚举', '证据VA', '置信度']


def main() -> None:
    bad_cols = Counter()
    bad_rows = 0
    total_rows = 0
    no_readme = 0
    unmatched_seq = 0
    structural = 0
    details: list[str] = []
    cmds_checked = 0

    for cmd_dir in sorted(ROOT.iterdir()):
        csvp = cmd_dir / 'fields.csv'
        if not csvp.is_file():
            continue
        cmds_checked += 1
        rows = list(csv.reader(io.StringIO(csvp.read_text(encoding='utf-8-sig', newline=''))))
        if not rows:
            continue
        if [c.strip() for c in rows[0]] != HEADER:
            structural += 1
            details.append('表头异常 %s: %r' % (cmd_dir.name, rows[0]))
        readme = F.readme_rows(cmd_dir)
        if not readme:
            no_readme += 1

        for line_no, raw in enumerate(rows[1:], start=2):
            if not any(c.strip() for c in raw):
                continue
            total_rows += 1
            probs: list[str] = []
            if len(raw) != 10:
                structural += 1
                probs.append('列数=%d' % len(raw))
            else:
                m, p = F.pbalance(raw[5]), F.pbalance(raw[6])
                if m or p:
                    probs.append('括号不平 meaning=%d purpose=%d' % (m, p))
            r = readme.get(F.norm(raw[0]) or '-') if readme else None
            if readme and r is None:
                unmatched_seq += 1
            if r:
                for idx, col in ((3, '线类型'), (4, '字段名'), (5, '含义'), (6, '用途'), (7, '取值'), (8, '证据VA')):
                    a, b = raw[idx] if len(raw) > idx else '', r[idx]
                    na, nb = F.norm(a), F.norm(b)
                    if na == nb:
                        continue
                    if col in ('含义', '用途'):
                        same = na in nb or nb in na
                    elif col == '证据VA':
                        # CSV 是**人手筛过的证据清单**，README 是散文式记录：
                        # 只要求 README 提到的 VA 都被 CSV 收进去（`vb ⊆ va`），
                        # 反过来 CSV 多列是常态（补了去向/日志/打印器点），不算差异。
                        va, vb = F.vas(a), F.vas(b)
                        same = bool(va) and vb <= va
                    else:
                        same = na in nb or nb in na
                    if not same:
                        bad_cols[col] += 1
                        probs.append('%s: csv=%r readme=%r' % (col, a[:60], b[:60]))
            if probs:
                bad_rows += 1
                if len(details) < 400:
                    details.append('%s:%d' % (cmd_dir.name, line_no))
                    for p in probs:
                        details.append('    ! ' + p)

    lines = [
        '命令目录 %d   字段行 %d' % (cmds_checked, total_rows),
        '列数/表头结构性异常 %d' % structural,
        'README 无字段表 %d   序号对不上 README 的行 %d' % (no_readme, unmatched_seq),
        '有差异的行 %d' % bad_rows,
        '',
        '按列差异计数：',
    ]
    for col in ('线类型', '字段名', '含义', '用途', '取值', '证据VA'):
        lines.append('  %-6s %d' % (col, bad_cols[col]))
    lines.append('')
    lines += details
    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines[:12]))
    print('  -> %s' % OUT)


if __name__ == '__main__':
    main()
