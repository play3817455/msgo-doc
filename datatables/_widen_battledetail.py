# -*- coding: utf-8 -*-
"""按新 schema 给两张属性长表补列（ADD COLUMN，保行）+ 种子 CSV 补宽（同 `_widen_seed.py` 口径）。"""
import io
import json
import os
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
SEED_ROOT = os.path.join(ROOT, "server", "datafiles", "lounge")
BACKUP = os.path.join(HERE, "_backup_seeds")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

TABLES = ["WEAPON_BATTLE_DETAIL", "MSMA_BATTLE_DETAIL"]
STAMP = "★2026-10-05 补列宽"

specs = {t: json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8")) for t in TABLES}

# ---------------------------------------------------------------- 1) DB 补列
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        want = [c["db_column"] for c in specs[t]["columns"]]
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        have = [r[0] for r in cur.fetchall()]
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        before = cur.fetchone()[0]
        added = []
        for c in want:
            if c not in have:
                cur.execute(f'ALTER TABLE cfg."{t}" ADD COLUMN IF NOT EXISTS "{c}" TEXT')
                added.append(c)
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        now = [r[0] for r in cur.fetchall()]
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        after = cur.fetchone()[0]
        print(f"[{t}] +{len(added)} 列 {added}")
        print(f"    列 {len(have)} → {len(now)}，序==schema {now == want}；行 {before} → {after}")
    conn.commit()

# ---------------------------------------------------------------- 2) 种子补宽
for t in TABLES:
    spec = specs[t]
    cols = sorted(spec["columns"], key=lambda c: c["csv_index"])
    width = max(c["csv_index"] for c in cols) + 1
    reads, skips = [], []
    for c in cols:
        if c.get("status") == "gap":
            skips.append(str(c["csv_index"]))
        else:
            off = c.get("memory_offset")
            reads.append(f"{c['csv_index']}" + (f"→+{off}" if off is not None else "→(不落内存)"))
    note = (
        f"# 表ID {spec.get('table_id','?')}｜CSV {width} 列（csv 0..{width-1}）｜reader "
        f"{spec.get('asm_reader')} + 子表 vtable[0] 按**绝对列号**取值：{'、'.join(reads)}"
        + (f"；csv {'、'.join(skips)} 不读" if skips else "")
        + f"｜{STAMP}：col0=属性名、col1=键、**col2 起是按属性名定宽的值槽**"
          f"（旧种子只到 col2/col3，其余列被越界兜底吃成 0，行为等价但列位不诚实）"
    )
    rel = spec["csv_path"]
    path = os.path.join(SEED_ROOT, *rel.split("/"))
    raw = open(path, "rb").read()
    crlf = raw.count(b"\r\n") > 0
    nl = "\r\n" if crlf else "\n"
    lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
    trailing_empty = lines and lines[-1] == ""

    bdir = os.path.join(BACKUP, *rel.split("/"))
    os.makedirs(os.path.dirname(bdir), exist_ok=True)
    shutil.copyfile(path, bdir)

    out, inserted, grew, over = [], False, 0, []
    for ln in lines:
        body = ln.rstrip("\r")
        stripped = body.strip()
        if stripped.startswith("#"):
            out.append(body)
            continue
        if stripped == "":
            if body != "":
                out.append(body)
            continue
        if not inserted:
            out.append(note)
            inserted = True
        fields = body.strip().split(",")
        while fields and fields[-1] == "":
            fields.pop()
        if len(fields) > width:
            over.append(body)
        if len(fields) < width:
            grew += 1
            fields += [""] * (width - len(fields))
        out.append(",".join(fields) + ",")
    if trailing_empty:
        out.append("")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(nl.join(out))
    print(f"[{t}] {rel}：行宽 → {width} 列（改 {grew} 行；超宽 {len(over)} 行）")
    for b in over[:3]:
        print("    超宽:", b[:120])

print("备份:", os.path.relpath(BACKUP, ROOT))
