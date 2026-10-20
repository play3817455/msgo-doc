# -*- coding: utf-8 -*-
"""看「只补整型定长数组宽度」后在**其他**命令上冒出的差异，逐条列细节判真假。"""
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
IDS = {t["id"] for t in BATCH["targets"]}

V.scalar_width = AB.scalar_width2
V.wire_shape = AB.wire_shape2


def arr_fields(cmd):
    out = []
    for f in cmd.get("fields", []):
        t = str(f.get("wire_type") or "")
        if AB.ARR_INT.match(t.strip().strip("`").lower()):
            out.append((f.get("name"), t, f.get("length")))
    return out


for p in sorted(V.RAW_DIR.glob("*.json")):
    cid = p.stem
    if cid in IDS:
        continue
    cp = V.CMD_DIR / (cid + ".json")
    if not cp.is_file():
        continue
    cmd = V.load_json(cp)
    res = V.analyze(V.Slice(V.load_json(p)), cmd)
    if not res["mismatches"]:
        continue
    print("=" * 100)
    print(cid, "| 整型数组字段:", arr_fields(cmd))
    for m in res["mismatches"]:
        print("   %-18s model=%r" % (m.get("check"), str(m.get("model"))[:60]))
        print("   %-18s asm  =%r" % ("", str(m.get("asm"))[:60]))
        print("   %-18s %s" % ("", (m.get("note") or "")[:150]))
        for g in (m.get("gaps") or [])[:6]:
            print("        gap:", json.dumps(g, ensure_ascii=False)[:160])
