# -*- coding: utf-8 -*-
"""修复前后对照：拿 README 字段表当裁判，量这 230 行的逐列命中率变化。

`_csvmalformed_report.txt` 是**修复前**跑的普查（`_survey_csvmalformed.py`），里面有这 230 行的
原始单元格（前若干行展开成 `raw[j] = ...`，其余整行 `%r`）。修复是**原地逐行**替换、不改行号，
所以拿 `(命令, 行号)` 就能把「修前」和现在的文件对上。

判分只看 6 个锚定列（线类型/字段名/含义/用途/取值/证据VA）——「偏移」「长度」不在 README 表里，
没法当锚。用与 `_validate_csvreadme.py` 完全相同的归一化和包含式比较。
"""
from __future__ import annotations

import ast
import csv
import io
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import fix_fields_csv as F  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')
SURVEY = pathlib.Path('db_design/tools/_csvmalformed_report.txt')
OUT = pathlib.Path('db_design/tools/_csvfix_beforeafter.txt')

ROW_HDR = re.compile(r'^--- (\S+) : line (\d+)\s+raw_cols=(\d+)')
ROW_INLINE = re.compile(r'^      (\S+):(\d+)\s+(\[.*\])$')
RAWCELL = re.compile(r'^    raw\[(\d+)\] = (.*)$')

ANCHORS = ((3, '线类型'), (4, '字段名'), (5, '含义'), (6, '用途'), (7, '取值'), (8, '证据VA'))


def parse_survey() -> dict[tuple[str, int], list[str]]:
    """从普查报告里把 230 行原始单元格抠回来。"""
    out: dict[tuple[str, int], list[str]] = {}
    cur: tuple[str, int] | None = None
    cells: dict[int, str] = {}
    for line in SURVEY.read_text(encoding='utf-8').splitlines():
        m = ROW_HDR.match(line)
        if m:
            if cur and cells:
                out[cur] = [cells[i] for i in sorted(cells)]
            cur = (m.group(1), int(m.group(2)))
            cells = {}
            continue
        m = ROW_INLINE.match(line)
        if m:
            if cur and cells:
                out[cur] = [cells[i] for i in sorted(cells)]
            cur = None
            cells = {}
            out[(m.group(1), int(m.group(2)))] = list(ast.literal_eval(m.group(3)))
            continue
        m = RAWCELL.match(line)
        if m and cur is not None:
            cells[int(m.group(1))] = ast.literal_eval(m.group(2))
            continue
        if line.startswith('    README') or line.startswith('    修后') or line.startswith('  …') or line.startswith('      '):
            continue
        if line and not line.startswith(' '):
            if cur and cells:
                out[cur] = [cells[i] for i in sorted(cells)]
            cur = None
            cells = {}
    if cur and cells:
        out[cur] = [cells[i] for i in sorted(cells)]
    return out


def matches(col: str, a: str, b: str) -> bool:
    na, nb = F.norm(a), F.norm(b)
    if na == nb:
        return True
    if col in ('含义', '用途'):
        return na in nb or nb in na
    if col == '证据VA':
        va, vb = F.vas(a), F.vas(b)
        return bool(va) and va == vb
    return na in nb or nb in na


def hits(cells: list[str], readme: list[str]) -> int:
    n = 0
    for idx, col in ANCHORS:
        if idx < len(cells) and matches(col, cells[idx], readme[idx]):
            n += 1
    return n


def main() -> None:
    raw_by = parse_survey()
    print('从普查报告抠回原始行 %d' % len(raw_by))

    buf: list[str] = []
    W = buf.append
    before = {c: 0 for _, c in ANCHORS}
    after = {c: 0 for _, c in ANCHORS}
    full_before = full_after = 0
    n = 0
    worse: list[str] = []
    notper: list[str] = []
    per_cmd = 0

    for key, raw in sorted(raw_by.items()):
        cid, line_no = key
        csvp = ROOT / cid / 'fields.csv'
        if not csvp.is_file():
            continue
        rows = list(csv.reader(io.StringIO(csvp.read_text(encoding='utf-8-sig', newline=''))))
        if line_no - 1 >= len(rows):
            notper.append('%s:%d' % key)
            continue
        fixed = rows[line_no - 1]
        readme = F.readme_rows(ROOT / cid)
        r = readme.get(F.norm(fixed[0]) or '-')
        if r is None:
            notper.append('%s:%d' % key)
            continue
        n += 1
        if len(fixed) != 10:
            per_cmd += 1
        hb, ha = hits(raw, r), hits(fixed, r)
        full_before += hb == 6
        full_after += ha == 6
        for idx, col in ANCHORS:
            if idx < len(raw) and matches(col, raw[idx], r[idx]):
                before[col] += 1
            if idx < len(fixed) and matches(col, fixed[idx], r[idx]):
                after[col] += 1
        if ha < hb:
            worse.append('%s:%d  修前 %d 列 -> 修后 %d 列' % (cid, line_no, hb, ha))
            W('回退 %s:%d' % (cid, line_no))
            W('  raw  = %r' % (raw,))
            W('  fixed= %r' % (fixed,))
            W('  rm   = %r' % ([r[i] for i, _ in ANCHORS],))
            W('')

    W('可判定行 %d（其余 %d 行 README 无同序号锚）' % (n, len(notper)))
    W('六列全中：修前 %d -> 修后 %d' % (full_before, full_after))
    W('')
    W('%-8s %8s %8s' % ('列', '修前命中', '修后命中'))
    for _, col in ANCHORS:
        W('%-8s %8d %8d' % (col, before[col], after[col]))
    W('')
    W('回退行 %d' % len(worse))
    for x in worse[:40]:
        W('  ' + x)
    W('')
    W('README 无锚行 %d：' % len(notper))
    for x in notper[:40]:
        W('  ' + x)
    OUT.write_text('\n'.join(buf) + '\n', encoding='utf-8')
    print('\n'.join(buf[:24]))
    print('  -> %s' % OUT)


if __name__ == '__main__':
    main()
