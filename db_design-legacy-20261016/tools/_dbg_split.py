# -*- coding: utf-8 -*-
"""调试：把某行的所有候选切分连同分数打出来。"""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import fix_fields_csv as F  # noqa: E402

CID = sys.argv[1]
LINE = int(sys.argv[2])

csvp = pathlib.Path('protocol_analysis/commands') / CID / 'fields.csv'
rows = list(F.csv.reader(io.StringIO(csvp.read_text(encoding='utf-8-sig', newline=''))))
raw = rows[LINE - 1]
print('raw =', raw)
readme = F.readme_rows(csvp.parent).get(F.norm(raw[0]) or '-')
print('readme =', readme)
cells = [c.strip() for c in raw]
rest = cells[4:-1]
print('rest =', rest)
import itertools
scored = []
for cuts in itertools.combinations(range(1, len(rest)), 4):
    b = (0,) + cuts + (len(rest),)
    groups = [','.join(rest[b[i]:b[i + 1]]) for i in range(5)]
    scored.append((F.score_split(groups, readme), cuts, groups))
scored.sort(key=lambda kv: -kv[0])
for s, cuts, g in scored:
    print('%8.2f  cuts=%s  %r' % (s, cuts, g))

print()
print('--- 前 3 名分项 ---')
for s, cuts, g in scored[:3]:
    parts = F.score_parts(g, readme)
    print('cuts=%s score=%.2f  %r' % (cuts, s, g))
    print('   ', {k: v for k, v in sorted(parts.items(), key=lambda kv: -abs(kv[1]))})


