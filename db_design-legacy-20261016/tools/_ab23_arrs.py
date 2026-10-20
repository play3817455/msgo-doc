# -*- coding: utf-8 -*-
"""批次 23 的 15 条：把「整型定长数组」字段列为可判后，逐条报它的对位/缺口状态。

这是在回答「这 15 条里的 u16[N]/u32[N] 字段到底有没有被核过」——原复核器把它们当
`agg`/宽度未知，直接跳过（静默放过）。
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_commands_ida as V  # noqa: E402
import _ab_intarray as AB  # noqa: E402

ROOT = os.path.dirname(HERE)
BATCH = json.load(io.open(os.path.join(ROOT, "schema", "commands", "_meta", "batch_23.json"),
                          encoding="utf-8"))
IDS = [t["id"] for t in BATCH["targets"]]

V.scalar_width = AB.scalar_width2
V.wire_shape = AB.wire_shape2

for cid in IDS:
    cp = V.CMD_DIR / (cid + ".json")
    rp = V.RAW_DIR / (cid + ".json")
    cmd = V.load_json(cp)
    arrs = []
    for f in cmd.get("fields", []):
        t = str(f.get("wire_type") or "").strip().strip("`").lower()
        if AB.ARR_INT.match(t):
            arrs.append(f)
    res = V.analyze(V.Slice(V.load_json(rp)), cmd)
    ws = res["checks"]["primitive_widths"]
    pairs = {p["field"]: p for p in ws["pairs"]}
    gaps = {g["field"] for g in ws["gaps"]}
    print("=" * 96)
    print("%s   差异=%d" % (cid, len(res["mismatches"])))
    if not arrs:
        print("   （无整型定长数组字段）")
    for f in arrs:
        n = f.get("name")
        p = pairs.get(n)
        st = "已对位" if p else ("缺口" if n in gaps else "未列")
        print("   %-22s %-10s 声明=%-6s 宽度=%s  → %s%s"
              % (n, f.get("wire_type"), f.get("length"), V.scalar_width(f.get("wire_type")),
                 st, ("  va=%s" % p["va"]) if p else ""))
