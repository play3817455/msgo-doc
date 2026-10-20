# -*- coding: utf-8 -*-
"""损伤普查：顶层点位字段 vs `asm_verification.checks` 里已判定的汇编结论。

`checks` 是判定层留下的、不会随导入被清掉的那一份；顶层字段是复核器回填进模型、
会被 `import_commands.py` 重跑冲掉的那一份。两者不一致 ⇒ 顶层被冲掉了。
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CMDS = 'db_design/schema/commands'
cnt = Counter()
examples = []
for f in sorted(os.listdir(CMDS)):
    if not f.endswith('.json') or f.startswith('_') or f == 'index.json':
        continue
    d = json.load(io.open(os.path.join(CMDS, f), encoding='utf-8'))
    ck = ((d.get('asm_verification') or {}).get('checks') or {})
    if not ck:
        continue
    cap = ck.get('capacity')
    if isinstance(cap, dict) and cap.get('value') is not None:
        want = '0x%X' % cap['value']
        if d.get('capacity') != want:
            cnt['capacity'] += 1
            if len(examples) < 6:
                examples.append((d['id'], 'capacity', d.get('capacity'), want))
    clo = ck.get('closer')
    if isinstance(clo, dict) and clo.get('va'):
        if not d.get('closer_va'):
            cnt['closer_va'] += 1
    disp = ck.get('dispatch_slot')
    if isinstance(disp, dict) and disp.get('slot'):
        if not d.get('dispatch_slot'):
            cnt['dispatch_slot'] += 1

print('顶层被冲掉的点位字段计数：')
for k, v in cnt.most_common():
    print('  %-14s %d' % (k, v))
print()
for e in examples:
    print('  ', e)
