# -*- coding: utf-8 -*-
"""全库 reader 清单 + 结构卫生检查（不连 IDA）-> datatables/_out_reader_inventory.txt

产物：
  _out_reader_inventory.txt  人读报告
  _out_reader_list.json      {reader: {"tables":[...], "declared":[...], "unknown_index_cols":[...]}}
"""
import glob
import io
import json
import os
import sys
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT_TXT = os.path.join(HERE, "_out_reader_inventory.txt")
OUT_JSON = os.path.join(HERE, "_out_reader_list.json")

log = []


def emit(s=""):
    print(s)
    log.append(s)


def main():
    tables = []
    for p in sorted(glob.glob(os.path.join(TABLES, "*.json"))):
        tables.append(json.load(open(p, encoding="utf-8")))

    readers = defaultdict(list)
    for t in tables:
        readers[t.get("asm_reader") or "(none)"].append(t)

    emit(f"表数 {len(tables)} ｜ 不同 reader {len(readers)}")
    emit()
    emit(f"{'reader':14s} {'表数':>4s}  声明列位（csv_index）")
    emit("-" * 100)

    reader_list = {}
    for r, ts in sorted(readers.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        declared = sorted({c["csv_index"] for t in ts for c in t["columns"]})
        non_gap = sorted({c["csv_index"] for t in ts for c in t["columns"] if c.get("status") != "gap"})
        holes = [i for i in range(max(declared) + 1) if i not in declared] if declared else []
        emit(f"{r:14s} {len(ts):4d}  全={len(declared)} 非gap={len(non_gap)} 洞={holes}")
        emit(f"{'':16s} {', '.join(t['id'] for t in ts)[:150]}")
        reader_list[r] = {
            "tables": [t["id"] for t in ts],
            "declared": declared,
            "non_gap": non_gap,
            "holes": holes,
            "same_declared": len({tuple(declared) for _ in [0]}) == 1,
        }

    # 多表共用同一 reader 但声明列位不一致 -> 必须人工确认（同一段代码不可能对两张表用两套列位）
    emit()
    emit("== 共用 reader 但声明列位不一致（可疑） ==")
    suspicious = []
    for r, ts in readers.items():
        if len(ts) < 2:
            continue
        sigs = {}
        for t in ts:
            sig = tuple(sorted(c["csv_index"] for c in t["columns"] if c.get("status") != "gap"))
            sigs.setdefault(sig, []).append(t["id"])
        if len(sigs) > 1:
            suspicious.append((r, sigs))
    if not suspicious:
        emit("  无")
    for r, sigs in suspicious:
        emit(f"  {r}:")
        for sig, ids in sigs.items():
            emit(f"    {list(sig)} <- {', '.join(ids)}")

    # asm_va 覆盖度
    emit()
    emit("== 每表 asm_va 覆盖度（有 VA 才能做锚点核验） ==")
    emit(f"{'表':30s} {'列':>4s} {'有VA':>5s} {'无VA':>5s}")
    for t in sorted(tables, key=lambda t: t["id"]):
        cols = t["columns"]
        withva = sum(1 for c in cols if c.get("asm_va"))
        emit(f"{t['id']:30s} {len(cols):4d} {withva:5d} {len(cols)-withva:5d}")

    with open(OUT_TXT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(reader_list, fh, ensure_ascii=False, indent=2)
    print(f"\nwrote {OUT_TXT}\nwrote {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
