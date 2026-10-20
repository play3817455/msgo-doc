# -*- coding: utf-8 -*-
"""校验 fix_fields_csv 的修复结果：结构合理性 + README 锚定列对照。"""
from __future__ import annotations

import csv
import io
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import fix_fields_csv as F  # noqa: E402

ROOT = pathlib.Path('protocol_analysis/commands')
OUT = pathlib.Path('db_design/tools/_fixcsv_validate.txt')

ENUM_OK = re.compile(r'^(?:-|—|\d+|0x[0-9A-Fa-f]+|\d+\.\.\d+|0/\d+|[^,;、]{0,40}(固定|上限|≤|<=|strlen|条数|元素线长|见).*)$')


def main() -> None:
    buf: list[str] = []
    W = buf.append
    bad = 0
    total = 0
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
            total += 1
            fixed, fix = F.fix_row(list(raw), readme.get(F.norm(raw[0]) or '-'))
            if fixed is None:
                W('修不出 %s:%d' % (cmd_dir.name, line_no)); bad += 1; continue
            probs = []
            if len(fixed) != 10:
                probs.append('列数=%d' % len(fixed))
            fname, meaning, purpose, enum, evid, conf = fixed[4], fixed[5], fixed[6], fixed[7], fixed[8], fixed[9]
            if conf.strip() not in F.CONFIDENCE_OK:
                probs.append('置信度=%r' % conf)
            if not F.vas(evid) and evid.strip() not in ('-', '—', ''):
                probs.append('证据无VA=%r' % evid[:30])
            if not (F.IDENT_RE.match(fname) or fname.strip() in F.CLOSURE_NAME):
                probs.append('字段名=%r' % fname[:30])
            if enum.strip() and not ENUM_OK.match(enum):
                probs.append('取值=%r' % enum[:40])
            if F.pbalance(meaning) or F.pbalance(purpose):
                probs.append('括号不平 meaning=%d purpose=%d' % (F.pbalance(meaning), F.pbalance(purpose)))
            r = readme.get(F.norm(raw[0]) or '-')
            if r:
                if F.norm(fixed[3]) != F.norm(r[3]) and F.norm(fixed[3]) not in F.norm(r[3]):
                    probs.append('线类型 vs README: %r | %r' % (fixed[3], r[3]))
                if F.norm(fname) != F.norm(r[4]) and F.norm(fname) not in F.norm(r[4]):
                    probs.append('字段名 vs README: %r | %r' % (fname, r[4]))
                if F.norm(enum) and F.norm(r[7]) and F.norm(enum) not in F.norm(r[7]) and F.norm(r[7]) not in F.norm(enum):
                    probs.append('取值 vs README: %r | %r' % (enum, r[7]))
            if probs:
                bad += 1
                W('%s:%d  raw=%d  %s' % (cmd_dir.name, line_no, len(raw), fix))
                for p in probs:
                    W('    ! ' + p)
                W('    now = %r' % (fixed,))
                if r:
                    W('    readme = %r' % ([r[3], r[4], r[5], r[6], r[7], r[8]],))
                W('')
    W('畸形行 %d，有问题 %d' % (total, bad))
    OUT.write_text('\n'.join(buf) + '\n', encoding='utf-8')
    print('畸形行 %d，有问题 %d  -> %s' % (total, bad, OUT))


if __name__ == '__main__':
    main()
