# -*- coding: utf-8 -*-
"""find_bridge_files.py —— 反查：哪个文件里**同时**出现已知的 (練度ID, モデルID) 真值对。

若存在这样的文件，它就是"練度ID ↔ モデルID"的天然桥表（不用再手工配代号）。
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = os.path.join(ROOT, 'unpackdat')

# (練度ID, モデルID, 机体名) —— 均为已确认真值
PAIRS = [
    ('1301011', '101020201', 'ジム・トレーナー'),
    ('1301012', '121010201', 'ザク・ワーカー'),
    ('1124081', '101285001', 'フリーダム'),
    ('1107011', '101020101', 'ジム・ライトアーマー'),
    ('1101011', '101010101', 'ジム'),
    ('1202001', '101284001', 'カラミティ'),
]
SKIP_EXT = {'.dxg', '.dds', '.mrb', '.asd', '.d3d', '.ogg', '.wav', '.hed', '.dat', '.bin'}

hits = {}
for dp, dns, fns in os.walk(SCAN):
    for fn in fns:
        p = os.path.join(dp, fn)
        if os.path.splitext(fn)[1].lower() in SKIP_EXT:
            continue
        try:
            b = open(p, 'rb').read()
        except Exception:
            continue
        if len(b) > 4_000_000:
            continue
        t = b.decode('latin1')
        for rid, mid, nm in PAIRS:
            if rid in t and mid in t:
                hits.setdefault(os.path.relpath(p, ROOT), []).append((rid, mid, nm))

print('=== 同时含 練度ID 与 モデルID 的文件 ===')
if not hits:
    print('   （无）')
for p, v in sorted(hits.items(), key=lambda x: -len(x[1])):
    print('  %-56s 命中 %d 对：%s' % (p, len(v), [x[2] for x in v][:4]))

# 再宽松一轮：只含 モデルID 的文件（看模型号的分布）
print()
print('=== 含任一 モデルID 的文件（前 25）===')
mid_hits = {}
for dp, dns, fns in os.walk(SCAN):
    for fn in fns:
        p = os.path.join(dp, fn)
        if os.path.splitext(fn)[1].lower() in SKIP_EXT:
            continue
        try:
            b = open(p, 'rb').read()
        except Exception:
            continue
        if len(b) > 4_000_000:
            continue
        t = b.decode('latin1')
        c = sum(1 for _, m, _ in PAIRS if m in t)
        if c:
            mid_hits[os.path.relpath(p, ROOT)] = c
for p, c in sorted(mid_hits.items(), key=lambda x: -x[1])[:25]:
    print('  %-56s %d' % (p, c))
