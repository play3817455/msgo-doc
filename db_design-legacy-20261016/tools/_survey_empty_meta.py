# -*- coding: utf-8 -*-
"""列出「README 明明写了这一项、模型却是空」的命令（定位导入器缺口）。"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(r'F:\9ymsgo\9you')
CMD = ROOT / 'db_design' / 'schema' / 'commands'
PROTO = ROOT / 'protocol_analysis' / 'commands'

FIELD = sys.argv[1]
SRC = {
    'capacity_va': ('声明容量', '声明容量（解码缓冲）', '容量申请证据', '容量旁证证据'),
    'capacity': ('声明容量', '声明容量（解码缓冲）'),
    'closer_va': ('长度闭合点', '提交'),
    'name_str': ('名字符串', '名字字符串'),
    'handler': ('处理函数', '代码位置'),
}[FIELD]


def readme_meta(path):
    out = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", line)
        if m:
            out.setdefault(m.group(1).strip(), m.group(2).strip())
    return out


n = 0
for p in sorted(CMD.glob('*.json')):
    if p.name.startswith('_') or p.name == 'index.json':
        continue
    d = json.loads(p.read_text(encoding='utf-8'))
    if d.get(FIELD):
        continue
    meta = readme_meta(PROTO / d['id'] / 'README.md')
    hits = {k: meta[k] for k in SRC if k in meta}
    if not hits:
        continue
    n += 1
    if n <= 30:
        print(d['id'], '|', json.dumps(hits, ensure_ascii=False))
print('合计', n)
