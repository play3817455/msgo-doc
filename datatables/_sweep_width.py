# -*- coding: utf-8 -*-
"""宽度三方核对：客户端 reader 实际读到的最大列号 vs DB 列数 vs 种子 CSV 字段数
-> datatables/_out_sweep_width.txt / .json

为什么要看这个：服务端 `cfg.SyncTableManifest` 走 `ExportTableRawCSV`，
它按 `cfg.{表}` 的**物理列**重新拼 CSV 下发给客户端。
所以「reader 读到第 N 列」而「DB 只有 M<N 列」= GM 改过之后下发的 CSV 会变窄，
客户端读越界 → 数值错。这是能直接造成线上数值错的一类。
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES_DIR = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")

verdict = json.load(open(os.path.join(HERE, "_out_sweep_verdict.json"), encoding="utf-8"))
emu = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
reader_reads = {t: set(m[3]) for t, m in verdict["by_table"].items()}
reader_err = {}
for name, v in emu.items():
    for t in v["tables"]:
        reader_err[t] = v["err"]


def csv_width(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
            best = 0
            n = 0
            for line in fh:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                n += 1
                # 客户端按逗号切；末列后带不带逗号都算
                c = s.count(",") + (0 if s.endswith(",") else 1)
                best = max(best, c)
            return best, n
    except Exception:
        return None, None


rows = []
for fn in sorted(os.listdir(TABLES_DIR)):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(TABLES_DIR, fn), encoding="utf-8"))
    t = d.get("table") or fn[:-5]
    reads = sorted(x for x in reader_reads.get(t, []) if x is not None)
    read_max = (max(reads) + 1) if reads else None
    db_cols = d.get("column_defined")
    cnt = d.get("column_count")
    csvp = d.get("csv_path") or ""
    w, n = csv_width(os.path.join(LOUNGE, csvp.replace("/", os.sep)))
    err = reader_err.get(t)
    rows.append({
        "table": t, "csv_path": csvp,
        "reader_read_max": read_max, "db_cols": db_cols, "reader_declared_cols": cnt,
        "csv_fields": w, "csv_rows": n, "err": bool(err),
    })

narrow_csv, narrow_db, ok = [], [], []
for r in rows:
    if r["err"] or r["reader_read_max"] is None:
        continue
    if r["csv_fields"] is not None and r["csv_fields"] < r["reader_read_max"]:
        narrow_csv.append(r)
    elif r["db_cols"] is not None and r["db_cols"] < r["reader_read_max"]:
        narrow_db.append(r)
    else:
        ok.append(r)

lines = []
lines.append(f"总表 {len(rows)}｜宽度足够 {len(ok)}｜CSV 偏窄 {len(narrow_csv)}｜DB 偏窄 {len(narrow_db)}")
lines.append("")
lines.append("== CSV 字段数 < reader 读到的列数（客户端读越界） ==")
for r in sorted(narrow_csv, key=lambda x: x["csv_fields"] - x["reader_read_max"]):
    lines.append(f"  {r['table']:26s} csv={r['csv_fields']:3d} db={r['db_cols']:3d} reader读={r['reader_read_max']:3d} ({r['csv_path']})")
lines.append("")
lines.append("== DB 列数 < reader 读到的列数（GM 改动后 CSV 会被截窄） ==")
for r in sorted(narrow_db, key=lambda x: x["db_cols"] - x["reader_read_max"]):
    lines.append(f"  {r['table']:26s} db={r['db_cols']:3d} reader读={r['reader_read_max']:3d} csv={r['csv_fields']} ({r['csv_path']})")
lines.append("")
lines.append("== 表里 reader 读不到 / 仿真不完整（列宽未判） ==")
for r in rows:
    if r["err"] or r["reader_read_max"] is None:
        lines.append(f"  {r['table']:26s} db={r['db_cols']} declared={r['reader_declared_cols']} csv={r['csv_fields']} err={r['err']}")
text = "\n".join(lines)
print(text)
json.dump(rows, open(os.path.join(HERE, "_out_sweep_width.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(HERE, "_out_sweep_width.txt"), "w", encoding="utf-8").write(text + "\n")
