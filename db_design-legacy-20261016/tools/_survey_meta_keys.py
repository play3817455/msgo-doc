# -*- coding: utf-8 -*-
"""_survey_meta_keys.py —— 普查 README §1 元信息表里**没被导入器认下**的键。

导入器的 `read_meta` 只收白名单（`META_KEYS` + `META_KEY_PREFIXES`）里的键；
README 后来出现过拼写变体（如 `名字串引用点` 少了「符」），这些行会被静默丢掉，
模型里对应的 `name_str_va` / `capacity_va` 等就成空。
"""

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(r'F:\9ymsgo\9you')
spec = importlib.util.spec_from_file_location('ic', str(ROOT / 'db_design' / 'tools' / 'import_commands.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

unknown = Counter()
examples = {}
for readme in sorted((ROOT / 'protocol_analysis' / 'commands').glob('*/README.md')):
    text = readme.read_text(encoding='utf-8', errors='replace')
    in_meta_section = False
    for line in text.splitlines():
        if line.startswith('## '):
            in_meta_section = line.startswith('## 1')
            continue
        if not in_meta_section:
            continue
        mm = re.match(r"^\|\s*([^|]+?)\s*\|\s*(.*?)\s*\|\s*$", line)
        if not mm:
            continue
        k = mm.group(1).strip()
        if k in {"项", "序号", "字段名"} or re.fullmatch(r":?-+:?", k):
            continue
        if k in m.META_KEYS or k.startswith(m.META_KEY_PREFIXES):
            continue
        unknown[k] += 1
        examples.setdefault(k, readme.parent.name)

print('未被导入器认下的元信息键：%d 种' % len(unknown))
for k, n in unknown.most_common():
    print('  %-40s x%-4d 例：%s' % (json.dumps(k, ensure_ascii=True), n, examples[k]))
