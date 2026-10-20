# -*- coding: utf-8 -*-
"""仿真失败/零写的诊断输出 -> datatables/_out_emu_triage.txt"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))

print("== err 全文 ==")
for k, v in sorted(d.items()):
    if v["err"]:
        print(f"{k:12s} {','.join(v['tables'])[:40]:40s} err={v['err']!r}")
        print(f"             calls={len(v['calls'])} writes={len(v['stores'])} seq={v['n_seq'][:30]}")
print()
print("== 有读无写 ==")
for k, v in sorted(d.items()):
    if not v["err"] and v["calls"] and not v["stores"]:
        print(f"{k:12s} {','.join(v['tables'])[:40]:40s} calls={len(v['calls'])}")
        print(f"             seq={v['n_seq'][:40]}")
print()
print("== 读列数 vs schema 非gap 数（排名） ==")
rows = []
for k, v in sorted(d.items()):
    obs = sorted({n for n in v["n_seq"] if n is not None})
    rows.append((len(obs) - len(v["non_gap"]), len(obs), len(v["non_gap"]), k, ",".join(v["tables"])))
rows.sort(reverse=True)
for delta, no, nn, k, t in rows[:25]:
    print(f"  Δ={delta:+5d} 仿真={no:4d} schema={nn:4d} {k:12s} {t[:40]}")
print("  ...")
for delta, no, nn, k, t in rows[-10:]:
    print(f"  Δ={delta:+5d} 仿真={no:4d} schema={nn:4d} {k:12s} {t[:40]}")
