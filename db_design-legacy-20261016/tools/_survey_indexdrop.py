# -*- coding: utf-8 -*-
"""索引丢列普查：`index.json` 的逐条派生键 / 派生计数 是否还和模型对得上。

`index.json` 是**多写者共用**文件：导入器写命令门面与计数，`derive_behavior.py` 写
`db_effects`/`behavior_steps`/`capability_evidence` 与 `counts.commands_with_db_effects`，
复核器写 `asm_mismatches`。任何一个写者整份重写，都会**静默**抹掉别人的键 ——
坑㊲ 就是这样把 `DB 影响` 从 81 抹成 0（模型里 `db_effects` 一条没少）。
模型是「真身」，索引只是门面，所以拿模型对索引即可照出这种丢失。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CMDS = 'db_design/schema/commands'
DERIVED = ('db_effects', 'behavior_steps', 'capability_evidence')

models = {}
for f in sorted(os.listdir(CMDS)):
    if not f.endswith('.json') or f.startswith('_') or f == 'index.json':
        continue
    d = json.load(io.open(os.path.join(CMDS, f), encoding='utf-8'))
    models[d['id']] = d

idx = json.load(io.open(os.path.join(CMDS, 'index.json'), encoding='utf-8'))
entries = {e['id']: e for e in idx.get('commands', [])}

missing_id = [cid for cid in models if cid not in entries]
dropped = {k: [] for k in DERIVED}
for cid, d in models.items():
    e = entries.get(cid) or {}
    for k in DERIVED:
        if d.get(k) and not e.get(k):
            dropped[k].append(cid)

counts = idx.get('counts') or {}
expect_effects = sum(1 for d in models.values() if d.get('db_effects'))
got_effects = counts.get('commands_with_db_effects')

bad = missing_id or any(dropped.values()) or got_effects != expect_effects
print('索引丢列普查：')
print('  索引缺条目          %d' % len(missing_id))
for k in DERIVED:
    print('  模型有/%s索引无  %d' % (k.ljust(18), len(dropped[k])))
print('  counts.commands_with_db_effects: 索引=%s 模型=%d' % (got_effects, expect_effects))
for k in DERIVED:
    for cid in dropped[k][:4]:
        print('    -', cid, k)
for cid in missing_id[:4]:
    print('    -', cid, '(索引缺条目)')
print()
print('结论：' + ('**索引被别的写者抹过**' if bad else '索引与模型一致（OK）'))
