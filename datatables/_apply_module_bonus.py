# -*- coding: utf-8 -*-
"""第 6 批落地：`MODULE_BONUS` 的**库列**（改名 + 补列 + NULL 归一）与**种子行宽**按新 schema 对齐。

改名保留物理位置（`RENAME COLUMN`，数据不动）；补列追加到末尾（= schema 顺序）；
新列在旧行的 `NULL` 归一成 `''`；种子补宽到 41 段。原文件备份 `datatables/_backup_seeds/`。
"""
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
STAMP = "★2026-10-05 第 6 批：补列宽到 41 列（键列 csv1 + 8 组 × {A,B,V}，列步长 5）"
T = "MODULE_BONUS"

RENAME = {                      # 旧名 → 新名（位置不变）
    "stat_id_a": "group1_stat_id_a",
    "stat_id_b": "group1_stat_id_b",
    "stat_value": "group1_stat_value",
}

spec = json.load(open(os.path.join(SCHEMA, T + ".json"), encoding="utf-8"))
want = [c["db_column"] for c in spec["columns"]]

# ---------------------------------------------------------------- 1) DB：改名 + 补列 + 归一
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    def have():
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (T,))
        return [r[0] for r in cur.fetchall()]

    cur.execute(f'SELECT count(*) FROM cfg."{T}"')
    before = cur.fetchone()[0]

    for old, new in RENAME.items():
        if old in have() and new not in have():
            cur.execute(f'ALTER TABLE cfg."{T}" RENAME COLUMN "{old}" TO "{new}"')
            print(f"[{T}] RENAME {old} → {new}")

    added = []
    for c in want:
        if c not in have():
            cur.execute(f'ALTER TABLE cfg."{T}" ADD COLUMN IF NOT EXISTS "{c}" TEXT')
            added.append(c)
    fixed = 0
    for c in added:
        cur.execute(f'UPDATE cfg."{T}" SET "{c}" = %s WHERE "{c}" IS NULL', ("",))
        fixed += cur.rowcount
    now = have()
    cur.execute(f'SELECT count(*) FROM cfg."{T}"')
    after = cur.fetchone()[0]
    conn.commit()

print(f"[{T}] +{len(added)} 列；列 {len(now)}；物理序==schema 序 {now == want}；"
      f"行 {before} → {after}；新列 NULL→'' {fixed} 格")
if now != want:
    print("  期望:", want)
    print("  实际:", now)
    sys.exit(1)

# ---------------------------------------------------------------- 2) 种子补宽
width = max(c["csv_index"] for c in spec["columns"]) + 1
note = (f"# 表ID {spec.get('table_id','?')}｜CSV {width} 列（csv 0..{width-1}）｜reader {spec.get('asm_reader')} "
        f"读列：1 键列 csv1 + **8 组 × {{A,B,V}}**（组 k 列号 {{5k-3, 5k-1, 5k}}，列步长 5）"
        f"⇒ 读到 csv40；缝列 csv 0, 3/6, 8/11, 13/16, 18/21, 23/26, 28/31, 33/36, 38 不读。"
        f"★注意：**本表索引键在 csv1**（vtable[5] `sub_5A2A10` 读 csv1），csv0 reader 不读 —— "
        f"本文件沿用「字段 0 = 行号」占位约定，客户端按键 csv1 取行，故这些占位行客户端取到的是空键(=0)。"
        f"｜{STAMP}：旧种子行宽 2，已补空列到 {width} 列")
rel = spec["csv_path"]
path = os.path.join(SEED_ROOT, *rel.split("/"))
raw = open(path, "rb").read()
nl = "\r\n" if raw.count(b"\r\n") else "\n"
lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
trailing_empty = lines and lines[-1] == ""
bdir = os.path.join(BACKUP, *rel.split("/"))
os.makedirs(os.path.dirname(bdir), exist_ok=True)
shutil.copyfile(path, bdir)

out, inserted, grew, over = [], False, 0, []
for ln in lines:
    body = ln.rstrip("\r")
    s = body.strip()
    if s.startswith("#") or s == "":
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
print(f"[{T}] {rel}：行宽 → {width} 段（改 {grew} 行；超宽 {len(over)} 行）")
