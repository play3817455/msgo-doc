# -*- coding: utf-8 -*-
"""宽度核对（权威口径）：DB 物理列数 / meta.cfg_manifest.raw_csv 实际字段数
   vs 客户端 reader 真正读到的最大列号 -> datatables/_out_sweep_width_db.txt / .json

依据：服务端 cfg.DBStore.ReadFile 直接把 meta.cfg_manifest.raw_csv 原样下发给客户端；
      而 GM 改动后 SyncTableManifest -> ExportTableRawCSV 会用 cfg.{表} 的物理列**重拼** CSV。
      所以「raw_csv 字段数」和「DB 列数」都必须 >= reader 读到的列数。
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES_DIR = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

verdict = json.load(open(os.path.join(HERE, "_out_sweep_verdict.json"), encoding="utf-8"))
emu = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
reader_reads = {t: sorted(x for x in m[3] if x is not None) for t, m in verdict["by_table"].items()}
# 读集由静态反汇编背书的表（仿真结构性失败，但读集确证）⇒ 不能被 emu_err 一票否决出宽度判定
static_ok = {t for t, m in verdict["by_table"].items() if str(m[0]).startswith("STATIC-")}
reader_err = {}
for name, v in emu.items():
    for t in v["tables"]:
        reader_err[t] = v["err"]


def width_of_raw(raw):
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8", "replace")
    best = 0
    n = 0
    for line in raw.split("\n"):
        s = line.rstrip("\r").strip()
        if not s or s.startswith("#"):
            continue
        n += 1
        # 客户端按逗号切字段：带尾逗号时「末位空字段」也算一列
        c = s.count(",") + 1
        best = max(best, c)
    return best, n


with psycopg.connect(DSN) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema='cfg' ORDER BY table_name""")
        dbtables = [r[0] for r in cur.fetchall()]
        colcount = {}
        for t in dbtables:
            cur.execute("""SELECT count(*) FROM information_schema.columns
                           WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'""", (t,))
            colcount[t] = cur.fetchone()[0]
        rowcount = {}
        for t in dbtables:
            cur.execute(f'SELECT count(*) FROM cfg."{t}"')
            rowcount[t] = cur.fetchone()[0]
        cur.execute("""SELECT file, filepath, raw_csv FROM meta.cfg_manifest""")
        man = {}
        for f, p, raw in cur.fetchall():
            w, n = width_of_raw(raw or "")
            man[f] = {"path": p, "fields": w, "rows": n}

rows = []
for fn in sorted(os.listdir(TABLES_DIR)):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(TABLES_DIR, fn), encoding="utf-8"))
    t = d.get("table") or fn[:-5]
    reads = reader_reads.get(t, [])
    rmax = max(reads) + 1 if reads else None
    dbc = colcount.get(t)
    m = man.get(t)
    rows.append({
        "table": t,
        "csv_path": d.get("csv_path"),
        "reader_read_max": rmax,
        "schema_defined": d.get("column_defined"),
        "schema_declared": d.get("column_count"),
        "db_cols": dbc,
        "raw_fields": (m or {}).get("fields"),
        "raw_rows": (m or {}).get("rows"),
        "emu_err": bool(reader_err.get(t)),
        "emu_partial": bool(reader_err.get(t)),
        "disposition": d.get("disposition"),
        "db_rows": rowcount.get(t),
    })

bad, ok, skip = [], [], []
for r in rows:
    if r["raw_fields"] is None:
        skip.append(r)
    elif r["reader_read_max"] is None:
        skip.append(r)
    elif r["emu_err"] and r["table"] not in static_ok:
        skip.append(r)
    elif r["raw_fields"] < r["reader_read_max"] or (r["db_cols"] or 0) < r["reader_read_max"]:
        bad.append(r)
    else:
        ok.append(r)

lines = [f"总表 {len(rows)}｜宽度达标 {len(ok)}｜★偏窄 {len(bad)}｜未能判定 {len(skip)}", ""]
lines.append("== ★ 下发 CSV / DB 列数 < reader 实际读到的列数 ==")
for r in sorted(bad, key=lambda x: (x["raw_fields"] or 0) - (x["reader_read_max"] or 0)):
    lines.append(
        f"  {r['table']:26s} raw_csv={r['raw_fields']:3d} db={r['db_cols']:3d} "
        f"reader读={r['reader_read_max']:3d} schema定义={r['schema_defined']:3d} "
        f"schema声明={r['schema_declared']:3d} ({r['csv_path']})"
    )
lines.append("")
lines.append("== 未判定（仿真不完整 / 无 manifest） ==")
for r in skip:
    lines.append(f"  {r['table']:26s} raw_csv={r['raw_fields']} db={r['db_cols']} emu={r['emu_err']}")
lines.append("")
lines.append("== 其余（宽达标，仅列 reader 读集差异见 _out_sweep_verdict.txt） ==")
lines.append("  " + "  ".join(r["table"] for r in ok))
if static_ok:
    lines.append("")
    lines.append("★ 其中宽度判定未被 emu_err 一票否决（读集由**静态反汇编**背书）: "
                 + "  ".join(sorted(static_ok)))
text = "\n".join(lines)
print(text)
json.dump(rows, open(os.path.join(HERE, "_out_sweep_width_db.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(HERE, "_out_sweep_width_db.txt"), "w", encoding="utf-8").write(text + "\n")
