# -*- coding: utf-8 -*-
"""对照：新修复器 vs 现行 `import_commands.repair_row`（模型就是按后者建的）。

两者不同的行 = 这次**真正要改**的语义。逐条列出，便于确认每条都是订正而非引入错误。
"""
from __future__ import annotations

import csv
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import fix_fields_csv as F  # noqa: E402
import import_commands as IC  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')
OUT = pathlib.Path('db_design/tools/_fixcsv_vs_repair.txt')


def main() -> None:
    buf: list[str] = []
    W = buf.append
    same = diff = 0
    for cmd_dir in sorted(ROOT.iterdir()):
        csvp = cmd_dir / 'fields.csv'
        if not csvp.is_file():
            continue
        rows = list(csv.reader(io.StringIO(csvp.read_text(encoding='utf-8-sig', newline=''))))
        readme = F.readme_rows(cmd_dir)
        for line_no, raw in enumerate(rows[1:], start=2):
            if not any(c.strip() for c in raw):
                continue
            if len(raw) == 10:
                continue
            old, _ = IC.repair_row(list(raw))
            new, fix = F.fix_row(list(raw), readme.get(F.norm(raw[0]) or '-'))
            if old == new:
                same += 1
                continue
            diff += 1
            W('%s:%d  %s' % (cmd_dir.name, line_no, fix))
            W('   old(repair_row) = %r' % (old,))
            W('   new(fix_fields) = %r' % (new,))
            if old and new:
                for i, name in enumerate(F.HEADER):
                    if old[i] != new[i]:
                        W('     %-8s old=%r' % (name, old[i]))
                        W('     %-8s new=%r' % ('', new[i]))
            r = readme.get(F.norm(raw[0]) or '-')
            if r:
                W('   readme = %r' % ([r[3], r[4], r[5], r[6], r[7], r[8]],))
            W('')
    W('与 repair_row 相同 %d 行，不同 %d 行' % (same, diff))
    OUT.write_text('\n'.join(buf) + '\n', encoding='utf-8')
    print('相同 %d / 不同 %d -> %s' % (same, diff, OUT))


if __name__ == '__main__':
    main()
