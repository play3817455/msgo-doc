# -*- coding: utf-8 -*-
"""标定：对每条 >10 列的畸形行，比较 `repair_row` 的结果与 README 锚定列。

锚定列 = 线类型(3)/字段名(4)/取值或枚举(7)/证据VA(8)。这几列 README 与 CSV
应当一致（只是反引号/空白差异），所以能当判据。
"""
from __future__ import annotations

import csv
import io
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import import_commands as IC  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')
OUT = pathlib.Path('db_design/tools/_calib_report.txt')


def norm(s: str) -> str:
    s = s.replace('\\', '')
    s = re.sub(r'[`*\s]', '', s or '')
    s = s.replace('（', '(').replace('）', ')').replace('，', ',')
    for d in '—–−':
        s = s.replace(d, '-')
    return s


VA_RE = re.compile(r'0x[0-9A-Fa-f]{3,}|(?<![A-Za-z_])[0-9A-F]{6,8}(?![A-Za-z0-9_])')


def vas(s: str) -> set[str]:
    return {v.lower().removeprefix('0x') for v in VA_RE.findall(s or '')}


def readme_rows(cmd_dir: pathlib.Path) -> dict[str, list[str]]:
    p = cmd_dir / 'README.md'
    if not p.is_file():
        return {}
    out: dict[str, list[str]] = {}
    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) < 10 or cells[0] in ('序号',) or set(cells[0]) <= set('-: '):
            continue
        key = norm(cells[0]) or '?'
        out.setdefault(key, cells)
    return out


def main() -> None:
    buf: list[str] = []
    W = buf.append
    stats: Counter = Counter()
    mism: list[str] = []
    no_readme = 0
    total = 0

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
            total += 1
            cells, fix = IC.repair_row(list(raw))
            seq = norm(raw[0]) or '-'
            r = rm.get(seq)
            if not r:
                no_readme += 1
                continue
            if not cells:
                stats['repair_failed'] += 1
                continue
            ok = []
            for idx, name in ((3, '线类型'), (4, '字段名'), (7, '取值'), (8, '证据VA')):
                if idx == 8:
                    a, b = vas(cells[idx]), vas(r[idx])
                    if a and b and a <= b:
                        ok.append(name)
                    elif a and b and len(a & b) / len(a) >= 0.6:
                        ok.append(name + '~')
                    else:
                        stats['mismatch_' + name] += 1
                elif norm(cells[idx]) == norm(r[idx]):
                    ok.append(name)
                elif norm(cells[idx]) and norm(cells[idx]) in norm(r[idx]):
                    ok.append(name + '~')
                else:
                    stats['mismatch_' + name] += 1
            if len(ok) == 4:
                stats['all4_ok'] += 1
            else:
                mism.append('%s:%d raw=%d ok=%s\n      rep  =%r\n      readme=%r'
                            % (cmd_dir.name, line_no, len(raw), ok, [cells[3], cells[4], cells[7], cells[8]],
                               [r[3], r[4], r[7], r[8]]))

    W('总畸形行 %d  无 README 对照 %d' % (total, no_readme))
    W('统计：')
    for k, v in stats.most_common():
        W('   %-22s %d' % (k, v))
    W('')
    W('不一致明细（最多 60 条）：')
    for m in mism[:60]:
        W(m)
        W('')
    OUT.write_text('\n'.join(buf) + '\n', encoding='utf-8')
    print('写出', OUT, '总行', total, '不一致', len(mism))
    for k, v in stats.most_common():
        print('  %-22s %d' % (k, v))


if __name__ == '__main__':
    main()
