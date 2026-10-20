# -*- coding: utf-8 -*-
"""_survey_meta_coverage.py —— 统计命令模型里 README 元信息的落库覆盖率。

用来量「导入器的键白名单」缺口（拼写变体会让整行静默丢掉）：
`name_str_va` / `capacity_va` / `error_vas` 的空值率，按方向与 README 变体分组看。

也覆盖**表格之外**的缺口：`dispatch_slot`/`dispatch_va` 常写在 §3 散文里
（`交 `vt[0x5A4]`（`0xB530F6`）` 这种），只扫表格的解析器会整条丢掉（坑㉛）。
这类没有「README 有哪一行」可查，改用「README 正文里出现过合法的 `vt[...]` 吗」当判据。
"""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r'F:\9ymsgo\9you')
CMD = ROOT / 'db_design' / 'schema' / 'commands'
PROTO = ROOT / 'protocol_analysis' / 'commands'

KEYS = ('handler', 'name_str', 'name_str_va', 'capacity', 'capacity_va', 'closer_va',
        'dispatch_slot', 'dispatch_va')

VT_RE = re.compile(r'vt\[(0x[0-9A-Fa-f]+)\]')
PROSE_MAX_SLOT = 0x1000
PROSE_ERROR_SLOT = 0x64


def readme_meta(path: Path) -> dict:
    out = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", line)
        if m:
            out.setdefault(m.group(1).strip(), m.group(2).strip())
    return out


tot = Counter()
empty = Counter()
by_has = Counter()
prose_missing = []
for p in sorted(CMD.glob('*.json')):
    if p.name.startswith('_') or p.name == 'index.json':
        continue
    d = json.loads(p.read_text(encoding='utf-8'))
    direction = d.get('direction')
    readme = PROTO / d['id'] / 'README.md'
    meta = readme_meta(readme)
    prose = readme.read_text(encoding='utf-8', errors='replace') if readme.is_file() else ''
    for k in KEYS:
        val = d.get(k)
        tot[(direction, k)] += 1
        if not val:
            empty[(direction, k)] += 1
            if k in ('dispatch_slot', 'dispatch_va'):
                # 散文缺口：README 正文里出现过**合法**的 vt 槽就算「README 有」
                if any(0 < int(s, 16) <= PROSE_MAX_SLOT and int(s, 16) != PROSE_ERROR_SLOT
                       for s in VT_RE.findall(prose)):
                    by_has[(direction, k)] += 1
                    if k == 'dispatch_slot':
                        prose_missing.append(d['id'])
                continue
            # 只有 README 里确实写了这一项，才算导入器的缺口
            src = {'name_str': ('名字符串', '名字字符串'),
                   'name_str_va': ('名字符串引用点', '名字串引用点', '名字符串'),
                   'capacity': ('声明容量', '声明容量（解码缓冲）'),
                   'capacity_va': ('声明容量', '声明容量（解码缓冲）', '容量申请证据', '容量旁证证据'),
                   'closer_va': ('长度闭合点', '提交'),
                   'handler': ('处理函数', '代码位置')}.get(k, ())
            if any(s in meta for s in src):
                by_has[(direction, k)] += 1

print('%-10s %-14s %6s %6s %10s' % ('方向', '字段', '总数', '空值', 'README有却空'))
for (direction, k), n in sorted(tot.items()):
    print('%-10s %-14s %6d %6d %10d' % (direction, k, n, empty[(direction, k)], by_has[(direction, k)]))

if prose_missing:
    print('\n【去向缺口】README 正文有合法 vt 槽、但模型 dispatch_slot 为空：%d 条' % len(prose_missing))
    for cid in prose_missing[:30]:
        print('  ', cid)
else:
    print('\n【去向缺口】无：README 写了去向的命令，模型都落库了。')
