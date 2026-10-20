# -*- coding: utf-8 -*-
"""全库列位对账：IDA 实证（真跑 reader）vs cfg_schema.json -> datatables/_out_sweep_report.txt

三类判据：
  J1 读列集合：仿真读到的 CSV 字段号集合 == schema 非 gap 列的 csv_index 集合
  J2 gap 矛盾：仿真读到的字段号里有 schema 标成 status=gap（"不读"）的
  J3 偏移映射：{csv_index -> memory_offset} 必须一致（★这一条抓到过 #50 MODULE 的一格错位）
"""
import glob
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
EMU = os.path.join(HERE, "_out_emu_readers.json")
OUT = os.path.join(HERE, "_out_sweep_report.txt")

log = []


def emit(s=""):
    print(s)
    log.append(s)


def main():
    emu = json.load(open(EMU, encoding="utf-8"))
    schema = {}
    for p in sorted(glob.glob(os.path.join(TABLES, "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        schema[d["id"]] = d

    # reader -> 该函数服务的表集合
    per_table = {}
    for reader, e in emu.items():
        for t in e["tables"]:
            per_table[t] = (reader, e)

    # ---------- 逐表结论 ----------
    rows = []
    for tid, d in sorted(schema.items(), key=lambda kv: kv[1].get("table_id") or "999"):
        if tid not in per_table:
            rows.append({"tid": tid, "table": tid, "reader": d.get("asm_reader"), "verdict": "NO_READER",
                         "note": "AUTOEXEC/无 reader（SkipDB）" if d.get("disposition") == "SCRIPT" else "未仿真"})
            continue
        reader, e = per_table[tid]
        cols = d["columns"]
        non_gap = sorted(c["csv_index"] for c in cols if c.get("status") != "gap")
        gaps = sorted(c["csv_index"] for c in cols if c.get("status") == "gap")
        obs = sorted({n for n in e["n_seq"] if n is not None})
        exp_map = {c["csv_index"]: c.get("memory_offset") for c in cols
                   if c.get("status") != "gap" and c.get("memory_offset") is not None}
        got_map = {}
        for s in e["resolved"]:
            if s["n"] is not None and s["off"] is not None:
                got_map.setdefault(s["n"], []).append(s["off"])

        miss = [i for i in non_gap if i not in obs]           # schema 说有、reader 没读到
        extra = [i for i in obs if i not in non_gap]          # reader 读了、schema 没登记
        gap_hit = [i for i in obs if i in gaps]               # reader 读了 schema 标"不读"的列
        off_bad = []
        for i, off in exp_map.items():
            if i in got_map and off not in got_map[i]:
                off_bad.append((i, off, sorted(set(got_map[i]))))

        if e["err"]:
            verdict = "READER_FAIL"
        elif not e["stores"]:
            verdict = "NO_WRITES"
        elif miss or extra or gap_hit or off_bad:
            verdict = "MISMATCH"
        else:
            verdict = "OK"
        rows.append({
            "tid": d.get("table_id"), "table": tid, "reader": reader, "verdict": verdict,
            "non_gap": non_gap, "gaps": gaps, "obs": obs, "miss": miss, "extra": extra,
            "gap_hit": gap_hit, "off_bad": off_bad,
            "err": e["err"], "seq": e["n_seq"], "exp_map": exp_map,
            "got_map": {k: sorted(set(v)) for k, v in got_map.items()},
        })

    def bucket(v):
        return [r for r in rows if r["verdict"] == v]

    emit(f"表 {len(rows)} ｜ OK {len(bucket('OK'))} ｜ MISMATCH {len(bucket('MISMATCH'))} ｜ "
         f"NO_WRITES {len(bucket('NO_WRITES'))} ｜ READER_FAIL {len(bucket('READER_FAIL'))} ｜ "
         f"NO_READER {len(bucket('NO_READER'))}")
    emit()
    emit("== J1/J2/J3 全部一致的（OK） ==")
    for r in sorted(bucket("OK"), key=lambda r: r["table"]):
        emit(f"  #{r['tid']:>3s} {r['table']:30s} {r['reader']:12s} 读列 {r['obs']}")
    emit()

    for v, title in [("MISMATCH", "★不一致（需人工判定）"), ("NO_WRITES", "读到了但没观测到写内存（需补）"),
                     ("READER_FAIL", "仿真失败（需修仿真/单独看）")]:
        b = sorted(bucket(v), key=lambda r: r["table"])
        emit(f"== {title}：{len(b)} 张 ==")
        for r in b:
            emit(f"  #{r['tid']:>3s} {r['table']:30s} {r['reader']:12s} verdict={r['verdict']}")
            if r["verdict"] == "READER_FAIL":
                emit(f"      err={r['err']}")
                continue
            if r["miss"]:
                emit(f"      schema 非gap 但 reader 未读到: {r['miss']}")
            if r["extra"]:
                emit(f"      reader 读到但 schema 未登记（非gap）: {r['extra']}")
            if r["gap_hit"]:
                emit(f"      ★reader 读到但 schema 标为 gap（声称不读）: {r['gap_hit']}")
            for i, off, got in r["off_bad"]:
                emit(f"      ★偏移不符 csv{i}: schema 写 +{off}，仿真写 +{got}")
            if r["verdict"] == "NO_WRITES":
                emit(f"      读列 seq={r['seq'][:24]}")
        emit()

    emit("== NO_READER ==")
    for r in sorted(bucket("NO_READER"), key=lambda r: r["table"]):
        emit(f"  {r['table']:30s} {r['note']}")

    emit()
    emit("== 全表逐行明细 ==")
    emit(f"{'tid':>4s} {'表':30s} {'读者':12s} {'判':16s} {'仿真读列':34s} schema非gap")
    for r in sorted(rows, key=lambda r: (r.get("tid") or "9", r["table"])):
        if r["verdict"] == "NO_READER":
            emit(f"{'':>4s} {r['table']:30s} {'':12s} {r['verdict']:16s}")
            continue
        emit(f"{r['tid']:>4s} {r['table']:30s} {r['reader']:12s} {r['verdict']:16s} "
             f"{str(r['obs'])[:34]:34s} {str(r.get('non_gap'))[:60]}")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
