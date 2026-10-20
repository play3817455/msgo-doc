# -*- coding: utf-8 -*-
"""第 5 批落地：`ITEM_PART` 的**库列**（改名 + 补列 + NULL 归一）与**种子行宽**按新 schema 对齐。

改名保留物理位置（`RENAME COLUMN`，数据不动）；补列追加到末尾（= schema 顺序）；
新列在旧行的 `NULL` 归一成 `''`；种子补宽到 50 段。原文件备份 `datatables/_backup_seeds/`。

同时把**快照目录**里的 `ITEM_PART.json` 换成"改前"的 21 列记录（GM schema 里仍是旧的一份），
便于日后回溯（本仓无 git）。
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
STAMP = "★2026-10-05 第 5 批：补列宽到 50 列（16 前导 + 8 组 + 2 尾 + 8 余量）"
T = "ITEM_PART"

RENAME = {                      # 旧名 → 新名（位置不变）
    "effect_scope": "group1_scope",
    "stat_name": "group1_stat",
    "loop_param_value": "group1_value",
    "priority": "group2_scope",
    "stack_rule": "group2_stat",
}

# ---------------------------------------------------------------- 0) 快照里换成"改前 schema"
snaps = sorted(p for p in (os.path.join(HERE, "_rollback", d) for d in os.listdir(os.path.join(HERE, "_rollback")))
               if p.endswith("_item_part"))
if snaps:
    snap = snaps[-1]
    gm = json.load(open(os.path.join(ROOT, "serverv", "static", "cfg_schema.json"), encoding="utf-8"))
    gm = gm["tables"] if "tables" in gm else gm
    old_cols = gm[T]["columns"]
    json.dump({"id": T, "note": "改前（21 列）记录；由 serverv/static/cfg_schema.json 抽出",
               "columns": old_cols}, open(os.path.join(snap, T + ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"快照 {os.path.basename(snap)}：ITEM_PART.json 换成改前 21 列记录（{len(old_cols)} 列）")

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
cols = sorted(spec["columns"], key=lambda c: c["csv_index"])
width = max(c["csv_index"] for c in cols) + 1
reads = [f"{c['csv_index']}" + (f"→+{c['memory_offset']}" if c.get("memory_offset") is not None
                                else "→(不落内存)")
         for c in cols if c.get("status") != "gap"]
note = (f"# 表ID {spec.get('table_id','?')}｜CSV {width} 列（csv 0..{width-1}）｜reader {spec.get('asm_reader')} "
        f"按**光标顺序**取值：16 前导（{'、'.join(reads[:16])}；csv1 不读）+ **8 组×3 列**"
        f"（{'、'.join(reads[16:40])}）+ 尾部 2 列（{'、'.join(reads[40:42])}）+ 余量 8 列"
        f"（csv42..49，仅当某组参数名为 MS_BOOST_GAUGE_RECOV(109) 时该组多占 1 列才会读到）"
        f"｜{STAMP}：旧种子行宽 21，已补空列到 {width} 列")
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
