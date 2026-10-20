# -*- coding: utf-8 -*-
"""查看某几个 reader 的仿真写点明细 -> datatables/_out_emu_detail.txt"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
TARGETS = sys.argv[1:] or ["sub_570880", "sub_5A2DB0", "sub_571380", "sub_57D070", "sub_56FF30"]
out = []
for k in TARGETS:
    v = d.get(k)
    if not v:
        out.append(f"### {k} 缺失")
        continue
    out.append("=" * 90)
    out.append(f"### {k} {v['tables']} err={v['err']}")
    out.append(f"  n_seq   = {v['n_seq']}")
    out.append(f"  observed= {v['observed']}")
    out.append(f"  non_gap = {v['non_gap']}")
    out.append(f"  declared= {v['declared']}")
    out.append(f"  calls   = {[(c['cid'], c['kind'], c['n']) for c in v['calls']][:20]}")
    out.append(f"  stores({len(v['stores'])}) =")
    for s in v["stores"][:60]:
        out.append(f"     seq={s['seq']:5d} off={s['off']:7d} size={s['size']} val={s['value']:#010x} n={s['n']} kind={s['kind']} via={s['via']}")
text = "\n".join(out)
print(text)
open(os.path.join(HERE, "_out_emu_detail.txt"), "w", encoding="utf-8").write(text + "\n")
