# -*- coding: utf-8 -*-
"""`-recreate` 真实哑弹半径（只读）-> datatables/_out_recreate_blast.txt

`cfgsync -recreate <表>` = DROP + 按 schema 建表 + **只从种子 CSV 灌**。
所以危险的不是"种子行数少"，而是「**种子宽度外的库列里有真值**」——
那些值在 `-recreate` 后必然变空，而 manifest 又只导库 ⇒ 客户端立刻丢数据。

对每张表算：
  种子宽度 ws（原始字段数）／schema 列数 ／
  csv_index >= ws 的库列里 **有值的格数**（>0 = 哑弹命中）
并给出前几个有值的列名，便于判方向（该回写种子还是该清库）。
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT = os.path.join(HERE, "_out_recreate_blast.txt")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def seed_width(rel):
    p = os.path.join(LOUNGE, rel.replace("/", os.sep))
    if not os.path.exists(p):
        return None, {}
    with open(p, "rb") as f:
        raw = f.read().decode("utf-8", "replace")
    dist = {}
    for ln in raw.replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        n = len(ln.split(","))
        dist[n] = dist.get(n, 0) + 1
    if not dist:
        return 0, dist
    # 取最常见宽度（防个别残行）
    return max(dist, key=lambda k: dist[k]), dist


specs = []
for fn in sorted(os.listdir(SCHEMA)):
    if fn.endswith(".json"):
        specs.append(json.load(io.open(os.path.join(SCHEMA, fn), encoding="utf-8")))

lines = []
lines.append("%-30s %-5s %8s %9s %10s  %s" %
             ("表", "tid", "种子宽", "schema列", "宽外有值格", "有值的前几列（csv_index）"))
lines.append("-" * 118)
hits = []
with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    for s in specs:
        t = s["id"]
        tid = s.get("table_id")
        csvp = s.get("csv_path", "")
        if not csvp or csvp.startswith("本地"):
            continue
        ws, dist = seed_width(csvp)
        if ws is None:
            continue
        nsch = len(s.get("columns") or [])
        # 库物理列序 -> csv_index
        cur.execute(
            "select column_name from information_schema.columns "
            "where table_schema='cfg' and table_name=%s order by ordinal_position", (t,))
        cols = [r[0] for r in cur.fetchall()]
        if not cols:
            continue
        by_csv = {pos - 2: n for pos, n in enumerate(cols)}
        extra = [(i, by_csv[i]) for i in sorted(by_csv) if i >= ws and by_csv[i] != "_row_id"]
        cur.execute('select count(*) from cfg."%s"' % t)
        nrow = cur.fetchone()[0]
        hit_cols = []
        cells = 0
        for i, n in extra:
            cur.execute(
                'select count(*) from cfg."%s" where coalesce(btrim("%s"::text),\'\') <> \'\''
                % (t, n))
            k = cur.fetchone()[0]
            if k:
                hit_cols.append((i, n, k))
                cells += k
        mark = ""
        if cells:
            mark = "★"
            hits.append((t, tid, ws, nsch, cells, hit_cols, csvp))
        lines.append("%-30s %-5s %8d %9d %10d  %s%s" %
                     (t, tid, ws, nsch, cells,
                      "; ".join("%s(+%d)" % (n, i) for i, n, k in hit_cols[:4]),
                      mark if cells else ""))
    lines.append("")
    lines.append("== 种子宽度外仍有值（`-recreate` 会真的丢）%d 张 ==" % len(hits))
    for t, tid, ws, nsch, cells, hit_cols, csvp in hits:
        lines.append("\n### #%s %s  种子 %s" % (tid, t, csvp))
        lines.append("    种子宽 %d ／ schema %d 列 ／ 宽外有值 %d 格，分布：%s"
                     % (ws, nsch, cells,
                        ", ".join("%s(csv%d)=%d行" % (n, i, k) for i, n, k in hit_cols[:20])))
        if len(hit_cols) > 20:
            lines.append("    …另 %d 列" % (len(hit_cols) - 20))

open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
print("wrote", OUT)
