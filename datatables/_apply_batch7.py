# -*- coding: utf-8 -*-
"""第 7 批落地（2026-10-05）：`COMMANDER_NPC` / `MISSION_XWAR_BANPICK` / `AI_PARAM`
按新 schema **物理重排**库列 + 种子补宽。

为什么这批必须重排（不像第 5/6 批可以只 RENAME/ADD）：
  `cfg.ExportTableRawCSV` = 取 `information_schema` 里除 `_row_id` 外的列、**按物理序**拼 CSV
  （见 `serverv/internal/cfg/csv_export.go`），而客户端按 **csv 序号**取列 ⇒ **物理列序必须 == csv 序**。
  这三张表旧 schema 的 csv_index 与真读列错位（甚至把 csv19/22 误判成 gap），
  旧列散落在错误的物理位置，`ADD COLUMN` 只能追加在末尾 ⇒ 只能**重建表重排**。

重排做法（事务内，64 行逐行搬迁，`_row_id` 原值保留）：
  1. `CREATE TABLE cfg."T__b7"`（按新 csv 序列出列，全 TEXT，`_row_id` integer NOT NULL）
  2. `INSERT INTO … SELECT`（旧列按 **旧名→新名映射** 搬；无映射的新列显式写 `''`）
  3. `DROP TABLE cfg."T"` / 建新序列+默认值+PK / `ALTER TABLE … RENAME TO "T"` / `setval`
  4. 断言：列序 == schema 列序、行数不变、0 个 NULL

安全前提（已核）：
  * `pg_depend` 查询：**没有任何视图/物化视图依赖 `cfg.*`**（否则 DROP 会连带删除）。
  * 三张表都没有外键/唯一约束，唯一约束是 `PRIMARY KEY (_row_id)`。
  * 全库 64 行都是"种子占位行"，被丢弃的旧列值**全为空**（脚本内断言）。

种子同步：`server/datafiles/lounge/<csv_path>` 补宽到新列数 + 一行布局注记，原文件备份 `datatables/_backup_seeds/`。
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

# 旧列名 → 新列名（同名的不用列；只在"跨名搬迁"时登记）
RENAME = {
    "COMMANDER_NPC": {
        "support_type_1": "support1_type",
    },
    "MISSION_XWAR_BANPICK": {
        "ban_ms_id": "ban_ms_id_1",
        "pick_count": "ban_ms_count",
    },
    "AI_PARAM": {},          # 前 18 列同名同序；第 18 列起旧名全部作废（旧值全空，已断言）
}

SEED_NOTE = {
    "COMMANDER_NPC": (
        "# 表ID 28｜CSV 50 列（csv 0..49）｜reader sub_572EE0｜布局：csv0 键(commander_id) + csv1..6 + "
        "**4 槽消耗(u16, csv12/13/17/21) + 3 槽冷却(u32, csv14/18/22)**（列步长 5） + "
        "**12 组 ×{原始值 u32(csv25,27,…,47), 类型名(csv26,28,…,48)}** + csv49 尾列；"
        "缝列 csv 7,8,9,10,11 / 15,16 / 19,20 / 23,24 不读。"
        "枚举：csv5 ∈ {NEUTRAL,EFF,ZEON}；csv26..48 ∈ {BOMB,CARPET_BOMB,…,JAMMING}(31 值)。"
        "｜★2026-10-05 第 7 批：旧种子行宽 2，已补空列到 50 列"),
    "MISSION_XWAR_BANPICK": (
        "# 表ID 75｜CSV 43 列（csv 0..42）｜reader sub_5A0300｜布局：csv0 键(rule_id) + csv1 模式 + "
        "csv2 条数(硬上限 40) + csv3..42 = 40 个 Ban 机体 ID 槽；★**真读列数 = 3 + min(csv2,40)**，"
        "43 列是上限。｜★2026-10-05 第 7 批：旧种子行宽 2，已补空列到 43 列"),
    "AI_PARAM": (
        "# 表ID 42｜CSV 127 列（csv 0..126）｜reader sub_56EA00｜布局：固定头 csv0..17 + "
        "**距离带块 ×3**（每块 25 列 = 3 字节 + 22 浮点；NEAR csv23..48、MIDDLE csv52..76、FAR csv79..103，"
        "各带尾随参数）+ 尾段 csv106..126。枚举：csv1 ∈ {NORMAL,…,DEBRIS}(17 值)；"
        "csv2 ∈ {NORMAL,LANDLUBBERLY,…,BROADWAYONLY}(9 值)；csv22 ∈ {NEAR=2,MIDDLE=3,FAR=4}。"
        "｜★2026-10-05 第 7 批：旧种子行宽 2，已补空列到 127 列"),
}


def db_cols(cur, t):
    cur.execute("""SELECT column_name FROM information_schema.columns
                   WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                   ORDER BY ordinal_position""", (t,))
    return [r[0] for r in cur.fetchall()]


def rebuild(cur, t, want):
    old = db_cols(cur, t)
    cur.execute(f'SELECT count(*) FROM cfg."{t}"')
    n0 = cur.fetchone()[0]

    ren = RENAME.get(t, {})
    src_of = {}                     # 新列名 → 旧列名
    for c in want:
        if c in old:
            src_of[c] = c
        else:
            for o, nn in ren.items():
                if nn == c and o in old:
                    src_of[c] = o
    stray = [c for c in old if c not in src_of.values()]
    for c in stray:                 # 被丢弃的旧列：必须全空（否则会丢数据）
        cur.execute(f'SELECT count(*) FROM cfg."{t}" WHERE coalesce("{c}",%s) <> %s', ("", ""))
        bad = cur.fetchone()[0]
        if bad:
            raise SystemExit(f"[{t}] ✗ 旧列 {c} 有 {bad} 行非空值，重建会丢数据 —— 停手")

    cur.execute(f'DROP TABLE IF EXISTS cfg."{t}__b7"')
    ddl = ", ".join([f'"_row_id" integer NOT NULL'] + [f'"{c}" text' for c in want])
    cur.execute(f'CREATE TABLE cfg."{t}__b7" ({ddl})')
    sel = ", ".join(f'coalesce("{src_of[c]}",\'\')' if c in src_of else "''" for c in want)
    collist = ", ".join(f'"{c}"' for c in want)
    cur.execute(f'INSERT INTO cfg."{t}__b7" ("_row_id", {collist}) '
                f'SELECT "_row_id", {sel} FROM cfg."{t}" ORDER BY "_row_id"')
    cur.execute(f'DROP TABLE cfg."{t}"')
    cur.execute(f'CREATE SEQUENCE cfg."{t}__row_id_seq"')
    cur.execute(f'ALTER TABLE cfg."{t}__b7" ALTER COLUMN "_row_id" '
                f'SET DEFAULT nextval(\'cfg."{t}__row_id_seq"\'::regclass)')
    cur.execute(f'ALTER SEQUENCE cfg."{t}__row_id_seq" OWNED BY cfg."{t}__b7"."_row_id"')
    cur.execute(f'ALTER TABLE cfg."{t}__b7" ADD CONSTRAINT "{t}_pkey" PRIMARY KEY ("_row_id")')
    cur.execute(f'ALTER TABLE cfg."{t}__b7" RENAME TO "{t}"')
    cur.execute(f'SELECT setval(\'cfg."{t}__row_id_seq"\', coalesce(max("_row_id"),1)) FROM cfg."{t}"')

    now = db_cols(cur, t)
    cur.execute(f'SELECT count(*) FROM cfg."{t}"')
    n1 = cur.fetchone()[0]
    cur.execute("SELECT count(*) FROM (SELECT " + ", ".join(f'"{c}"' for c in now) +
                f' FROM cfg."{t}") q WHERE ' + " OR ".join(f'"{c}" IS NULL' for c in now))
    nnull = cur.fetchone()[0]
    print(f"[{t}] 旧 {len(old)} 列 → 新 {len(now)} 列；行 {n0} → {n1}；"
          f"列序==schema序 {now == want}；0 NULL {nnull == 0}")
    print(f"   旧列序: {old}")
    print(f"   新列序: {now}")
    print(f"   跨名搬迁: {ren}；丢弃旧列（已断言全空）: {stray}")
    if now != want or n1 != n0 or nnull:
        raise SystemExit(f"[{t}] ✗ 重建后校验不过")


def widen_seed(spec):
    t = spec["id"] if "id" in spec else spec["table"]
    width = max(c["csv_index"] for c in spec["columns"]) + 1
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
            if body != "" and s != SEED_NOTE[t].strip():
                out.append(body)
            continue
        if not inserted:
            out.append(SEED_NOTE[t])
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
    print(f"[{t}] {rel}：行宽 → {width} 段（改 {grew} 行；超宽 {len(over)} 行）")


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in ["COMMANDER_NPC", "MISSION_XWAR_BANPICK", "AI_PARAM"]:
        spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        want = [c["db_column"] for c in spec["columns"]]
        rebuild(cur, t, want)
    conn.commit()

for t in ["COMMANDER_NPC", "MISSION_XWAR_BANPICK", "AI_PARAM"]:
    spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
    widen_seed(spec)
