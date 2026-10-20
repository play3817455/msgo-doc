# -*- coding: utf-8 -*-
"""第 4 批落地：两张窄表的**库列**（改名 + 补列 + NULL 归一）与**种子行宽**按新 schema 对齐。

- 改名用 `ALTER TABLE ... RENAME COLUMN`（**位置不变、数据不动**），不用 `-recreate`；
- 补列用 `ADD COLUMN IF NOT EXISTS`（追加到末尾 = schema 顺序）；
- 补出来的新列在旧行是 `NULL` ⇒ 归一成 `''`（cfg 其余列口径）；
- 种子 CSV 补宽到 schema 行宽（只追加空字段），原文件备份到 `datatables/_backup_seeds/`。
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
STAMP = "★2026-10-05 补列宽（第 4 批）"

RENAME = {
    # 旧名 → 新名（旧名是**错的名字**，位置恰好就是真列的位置）
    "BEGINNER_CHALLENGE": {
        "sort_order": "unknown_u32_1",
        "reward_type": "unknown_u32_2",
        "reward_param_id": "unknown_u32_3",
        "reward_quantity": "reward1_type",
        "condition_param": "reward1_param_a",
    },
    "CHALLENGE_HIGHSCORE": {
        "rank_title": "col2",        # reader 根本不读 col2/3/4 ⇒ 归位成占位列
        "rank_description": "col3",
        "reward_title": "col4",
    },
}
TABLES = list(RENAME)

specs = {t: json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8")) for t in TABLES}

# ---------------------------------------------------------------- 1) DB：改名 + 补列 + 归一
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        want = [c["db_column"] for c in specs[t]["columns"]]
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        before = cur.fetchone()[0]

        def have():
            cur.execute("""SELECT column_name FROM information_schema.columns
                           WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                           ORDER BY ordinal_position""", (t,))
            return [r[0] for r in cur.fetchall()]

        for old, new in RENAME[t].items():
            if old in have() and new not in have():
                cur.execute(f'ALTER TABLE cfg."{t}" RENAME COLUMN "{old}" TO "{new}"')
                print(f"[{t}] RENAME {old} → {new}")

        added = []
        for c in want:
            if c not in have():
                cur.execute(f'ALTER TABLE cfg."{t}" ADD COLUMN IF NOT EXISTS "{c}" TEXT')
                added.append(c)
        fixed = 0
        for c in added:
            cur.execute(f'UPDATE cfg."{t}" SET "{c}" = %s WHERE "{c}" IS NULL', ("",))
            fixed += cur.rowcount
        now = have()
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        after = cur.fetchone()[0]
        print(f"[{t}] +{len(added)} 列；列 {len(now)}，物理序==schema 序 {now == want}；"
              f"行 {before} → {after}；新列 NULL→'' {fixed} 格")
        if now != want:
            print(f"    期望 {want}")
            print(f"    实际 {now}")
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
        f"{spec.get('asm_reader')} 按**绝对列号**取值：{'、'.join(reads)}"
        + (f"；csv {'、'.join(skips)} 不读（占位）" if skips else "")
        + f"｜{STAMP}：旧种子行宽不足，已补空列到 {width} 列（补列为占位 0；"
          f"缺列时客户端 sub_456D90 越界返回 \"\" ⇒ atoi 0，行为等价）"
    )
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

print("备份:", os.path.relpath(BACKUP, ROOT))
