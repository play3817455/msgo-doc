# -*- coding: utf-8 -*-
"""畸形行普查（带 README 交叉对照）。

对 `fields.csv` 里列数 != 10 的每一行，打印：
  - 原始单元格（repr，可见逗号位置）
  - `import_commands.repair_row` 的修复结果
  - README 字段表里同 `序号` 的那一行（人手写的**意图**来源）
按「修复签名」分组，便于逐类定规则。
"""
from __future__ import annotations

import csv
import io
import os
import pathlib
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import import_commands as IC  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')
OUT = pathlib.Path('db_design/tools/_csvmalformed_report.txt')

SEQ_RE = re.compile(r'^\s*(\d+|-|—)\s*$')


def readme_rows(cmd_dir: pathlib.Path) -> dict[str, list[str]]:
    """README 字段表：按「序号」索引，返回原始单元格（去掉两端空白、去反引号留着）。"""
    p = cmd_dir / 'README.md'
    if not p.is_file():
        return {}
    out: dict[str, list[str]] = {}
    in_tbl = False
    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        s = line.strip()
        if not s.startswith('|'):
            in_tbl = False
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) < 10:
            continue
        if cells[0] in ('序号',) or set(cells[0]) <= set('-: '):
            in_tbl = True
            continue
        if not in_tbl:
            continue
        key = cells[0].strip('`').strip()
        if key not in out:
            out[key] = cells
    return out


def main() -> None:
    buf: list[str] = []
    W = buf.append
    sigc: Counter = Counter()
    groups: dict[tuple, list] = defaultdict(list)

    for cmd_dir in sorted(ROOT.iterdir()):
        csvp = cmd_dir / 'fields.csv'
        if not csvp.is_file():
            continue
        rows = list(csv.reader(io.StringIO(csvp.read_text(encoding='utf-8-sig', newline=''))))
        if not rows:
            continue
        rm = readme_rows(cmd_dir)
        for line_no, raw in enumerate(rows[1:], start=2):
            if not any(c.strip() for c in raw):
                continue
            if len(raw) == 10:
                continue
            cells, fix = IC.repair_row(list(raw))
            sig = tuple(sorted({f.split('_x')[0] for f in fix}))
            sigc[sig] += 1
            groups[sig].append((cmd_dir.name, line_no, raw, cells, fix, rm))

    W('畸形行签名分布：')
    for k, v in sigc.most_common():
        W('  %4d  %s' % (v, ' + '.join(k)))

    for sig, items in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        W('')
        W('=' * 100)
        W('### 签名 %s —— %d 行' % (' + '.join(sig), len(items)))
        W('=' * 100)
        for cid, line_no, raw, cells, fix, rm in items[:6]:
            W('')
            W('--- %s : line %d  raw_cols=%d  fix=%s' % (cid, line_no, len(raw), fix))
            for j, c in enumerate(raw):
                W('    raw[%d] = %r' % (j, c))
            if cells:
                W('    修后 = %r' % (cells,))
            seq = raw[0].strip().strip('`') if raw else ''
            r = rm.get(seq)
            if r:
                W('    README 同序号行:')
                for j, c in enumerate(r):
                    W('      r[%d] = %r' % (j, c))
            else:
                W('    README: 无同序号行 (seq=%r)' % seq)
        if len(items) > 6:
            W('')
            W('  … 另有 %d 行同签名：' % (len(items) - 6))
            for cid, line_no, raw, cells, fix, rm in items[6:]:
                W('      %s:%d  %r' % (cid, line_no, raw))

    OUT.write_text('\n'.join(buf) + '\n', encoding='utf-8')
    print('写出', OUT, len(buf), '行')


if __name__ == '__main__':
    main()
