# -*- coding: utf-8 -*-
"""第 8 批勘查：把 `_out_sweep_verdict.json` 里 READSET-DIFF 的表逐条摊开，
对照 `_out_sweep_width_db.json` 的宽度，判断哪些是**真结构缺口**（reader 读了我们没声明的列）。"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
v = json.load(open(os.path.join(HERE, "_out_sweep_verdict.json"), encoding="utf-8"))
w = {r["table"]: r for r in json.load(open(os.path.join(HERE, "_out_sweep_width_db.json"), encoding="utf-8"))}
emu = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))

print("== READSET-DIFF / EMU-PARTIAL 逐表 ==")
for t, r in sorted(v["by_table"].items()):
    if r[0] not in ("READSET-DIFF", "EMU-PARTIAL"):
        continue
    wr = w.get(t, {})
    print(f"\n-- {t} [{r[0]}] reader={r[2]}")
    print(f"   宽度: reader_read_max={wr.get('reader_read_max')} schema={wr.get('schema_defined')} "
          f"db={wr.get('db_cols')} raw={wr.get('raw_fields')} rows={wr.get('raw_rows')}")
    print(f"   备注: {r[1]}")

print("\n\n== 仿真读集（真值列号）==")
for t in sorted(emu):
    if t in ("ACTION_MODULE_INFO", "CHARA_MODEL", "CHARA_PARAM", "MSMA_RENTAL",
             "ITEM_PART", "SCORE_CONFIG_CATEGORY"):
        d = emu[t]
        if isinstance(d, dict):
            cols = d.get("cols") or d.get("read_cols") or []
            print(f"\n-- {t}: {sorted(cols) if cols else d}")
        else:
            print(f"\n-- {t}: {d}")
