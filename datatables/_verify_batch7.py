# -*- coding: utf-8 -*-
"""第 7 批验收（COMMANDER_NPC / MISSION_XWAR_BANPICK / AI_PARAM）：

1) 全库列漂移 0（物理列序 == schema csv_index 序，逐表逐列）
2) 三表：库列数 == schema 宽度 == manifest 段数；reader 上限 <= 宽度-1；行数不变；0 NULL
3) 老列取值按**名字**逐格未变（新列插在中间，位置不再 1:1，故按列名比对；改名走映射表）
   被物理丢弃的旧列，逐格断言基线全空（否则视为数据丢失）
4) manifest 数据格 == 库格（导出链无错位）
5) 邻表行数扫描：除三表外无表行数变化
"""
import csv
import glob
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

SNAP_OF = {
    "COMMANDER_NPC": "20261005-233942_commander_npc",
    "MISSION_XWAR_BANPICK": "20261005-233942_mission_xwar_banpick",
    "AI_PARAM": "20261005-233943_ai_param",
}
RENAME_OF = {
    "COMMANDER_NPC": {"support_type_1": "support1_type"},
    "MISSION_XWAR_BANPICK": {"pick_count": "ban_ms_count", "ban_ms_id": "ban_ms_id_1"},
    "AI_PARAM": {},
}
TABLES = tuple(SNAP_OF)
fails = []


def check(ok, msg):
    print(("  ok  " if ok else "  FAIL") + " " + msg)
    if not ok:
        fails.append(msg)


def db_cols(cur, t):
    cur.execute(
        """SELECT column_name FROM information_schema.columns
           WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
           ORDER BY ordinal_position""",
        (t,),
    )
    return [r[0] for r in cur.fetchall()]


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute(
        """SELECT table_name FROM information_schema.tables
           WHERE table_schema='cfg' ORDER BY table_name"""
    )
    dbt = [r[0] for r in cur.fetchall()]
    got = {t: db_cols(cur, t) for t in dbt}

    print("== 1) 全库列漂移 ==")
    drift = []
    for fn in sorted(os.listdir(SCHEMA)):
        if not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(SCHEMA, fn), encoding="utf-8"))
        t = d.get("table") or fn[:-5]
        if t not in got:
            continue
        want = [c["db_column"] for c in d["columns"]]
        if want != got[t]:
            drift.append(t)
            print(f"  {t}: 缺 {[c for c in want if c not in got[t]]} 多 {[c for c in got[t] if c not in want]}")
    check(not drift, f"列漂移表数 = {len(drift)}（应为 0）")

    print("== 5) 邻表行数扫描（基线 manifest 行数 vs 现库行数）==")
    base_rows = {}
    for fn in glob.glob(os.path.join(HERE, "_rollback", "*", "*.db.csv")):
        t0 = os.path.basename(fn)[: -len(".db.csv")]
        if t0 in base_rows:
            continue
        with open(fn, encoding="utf-8", newline="") as fh:
            base_rows[t0] = max(0, sum(1 for _ in fh) - 1)
    moved = []
    for t in dbt:
        if t not in base_rows or t in TABLES:
            continue
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        n = cur.fetchone()[0]
        if n != base_rows[t]:
            moved.append((t, base_rows[t], n))
    check(not moved, f"邻表行数变化 = {len(moved)} {moved}")

    print("== 2/3/4) 逐表 ==")
    for t in TABLES:
        print(f"-- {t} --")
        d = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        width = len(d["columns"])
        rmax = d["reader_max_csv_index"]
        cols = got[t]
        check(len(cols) == width, f"库列数 {len(cols)} == schema 宽度 {width}")
        check(
            [c["db_column"] for c in d["columns"]] == cols,
            "物理列序 == schema csv_index 序",
        )
        check(rmax + 1 <= width, f"reader 上限 csv#{rmax}（需 {rmax+1} 列）<= {width}")

        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        nrow = cur.fetchone()[0]
        check(nrow == 64, f"行数 {nrow} == 64")

        cur.execute(
            'SELECT count(*) FROM (SELECT ' + ", ".join(f'"{c}"' for c in cols) + f' FROM cfg."{t}") q WHERE '
            + " OR ".join(f'"{c}" IS NULL' for c in cols)
        )
        check(cur.fetchone()[0] == 0, "0 个 NULL 行")

        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        raw = cur.fetchone()[0]
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
        mrows = [l.rstrip("\r") for l in raw.split("\n") if l.strip() and not l.strip().startswith("#")]
        segs = sorted({len(next(csv.reader([r]))) for r in mrows})
        check(segs == [width], f"manifest 段数 {segs} == {width}；行 {len(mrows)}")
        check(len(mrows) == nrow, f"manifest 行数 {len(mrows)} == 库行数 {nrow}")

        # 3) 老列按名比对
        with open(os.path.join(HERE, "_rollback", SNAP_OF[t], t + ".db.csv"), encoding="utf-8", newline="") as fh:
            r = csv.reader(fh)
            ohdr = next(r)[1:]                       # 去掉 _row_id
            old = {row[0]: row for row in r}
        ren = RENAME_OF[t]
        dropped = [c for c in ohdr if (ren.get(c, c) not in cols)]
        cell = bad = 0
        samples = []
        cur.execute(f'SELECT _row_id, ' + ", ".join(f'"{c}"' for c in cols) + f' FROM cfg."{t}" ORDER BY _row_id')
        for row in cur:
            rid = str(row[0])
            o = old.get(rid)
            if o is None:
                bad += 1
                samples.append((rid, "<缺行>"))
                continue
            for c in ohdr:
                nc = ren.get(c, c)
                if nc not in cols:
                    continue
                ov = o[1 + ohdr.index(c)]
                nv = row[1 + cols.index(nc)]
                nv = "" if nv is None else str(nv)
                if ov:
                    cell += 1
                if ov != nv:
                    bad += 1
                    if len(samples) < 6:
                        samples.append((rid, f"{c}->{nc}", ov, nv))
        check(bad == 0, f"老列取值逐格未变（比较 {cell} 非空格，差异 {bad}）{samples}")

        miss = [c for c in ohdr if ren.get(c, c) not in cols]
        ne = 0
        for rid, row in old.items():
            for c in miss:
                if row[1 + ohdr.index(c)] != "":
                    ne += 1
                    if ne <= 4:
                        print(f"     非空丢弃格: row {rid} {c} = {row[1 + ohdr.index(c)]!r}")
        check(ne == 0, f"被丢弃旧列全部为空（列 {len(miss)}，非空格 {ne}）")

        # 4) manifest == db
        mism = 0
        cur.execute(f'SELECT ' + ", ".join(f'"{c}"' for c in cols) + f' FROM cfg."{t}" ORDER BY _row_id')
        mdata = [[("" if v is None else str(v)) for v in r] for r in cur]
        for i, r in enumerate(mdata):
            fr = next(csv.reader([mrows[i]]))
            if len(fr) < width:
                fr = fr + [""] * (width - len(fr))
            if fr[:width] != r:
                mism += 1
                if mism <= 4:
                    print(f"     manifest≠db 行 {i+1}: {fr[:8]} vs {r[:8]}")
        check(mism == 0, f"manifest 数据格 == 库格（差异行 {mism}）")

print()
if fails:
    print(f"结论：FAIL（{len(fails)} 项）")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("结论：PASS —— 漂移 0 / 宽度与列序一致 / 行数 64 / 0 NULL / 老值未变 / manifest 同步 / 邻表未动")
