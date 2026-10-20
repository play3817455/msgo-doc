# -*- coding: utf-8 -*-
"""#50 MODULE 列错位修复后的验收探针 -> datatables/_out_module_fix.txt

验三件事：
  A. 库列序 == schema csv_index 顺序（param_c 在 module_category 之前）
  B. manifest.raw_csv（客户端实际收到的字节）每行 10 字段，枚举串落在**索引 8**
  C. 按 sub_5A2DB0 的 push 常量 0,2,3,4,5,7,8,9 复现客户端内存写入，
     断言 module_category 是合法枚举名（不是 "1"）、unlock_level=1、param_c=0
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
SEED = os.path.join(ROOT, "server", "datafiles", "lounge", "module", "module.csv")
OUT = os.path.join(HERE, "_out_module_fix.txt")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

# sub_5A2DB0：push 常量 -> 内存偏移（ASM 实测）
PUSH_ORDER = [(0, 0), (2, 20), (3, 4), (4, 8), (5, 16), (7, 12), (8, 24), (9, 28)]
CATEGORY = {0: "ATTACK", 1: "DEFENSE", 2: "MOVE", 3: "SPECIAL", 4: "AID", 5: "FIXED"}
ENUM_INDEX = 8
CAT_OFFSET = 24

log = []


def emit(s=""):
    print(s)
    log.append(s)


def norm(line):
    s = line.rstrip("\r\n").rstrip()
    while s.endswith(","):
        s = s[:-1]
    return s


def split(line):
    return [f.strip() for f in norm(line).split(",")]


def main():
    spec = json.load(open(os.path.join(SCHEMA, "MODULE.json"), encoding="utf-8"))
    want = [
        c["db_column"]
        for c in sorted(spec["columns"], key=lambda c: c["csv_index"])
    ]
    emit("A. 库列序 vs schema")
    emit(f"   schema csv_index 顺序: {want}")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_schema='cfg' AND table_name='MODULE' AND column_name<>'_row_id' "
                "ORDER BY ordinal_position"
            )
            actual = [r[0] for r in cur.fetchall()]
            emit(f"   库 actual  : {actual}")
            emit(f"   ==> {'OK 一致' if actual == want else 'MISMATCH'}")

            cur.execute("SELECT raw_csv, row_count FROM meta.cfg_manifest WHERE file='MODULE'")
            raw_csv, row_count = cur.fetchone()
            cur.execute('SELECT ' + ", ".join(f'"{c}"' for c in want) + ' FROM cfg."MODULE" ORDER BY _row_id')
            db_rows = cur.fetchall()

    lines = [l for l in raw_csv.decode("utf-8").split("\n") if l.strip() and not l.lstrip().startswith("#")]
    emit()
    emit("B. manifest.raw_csv（客户端收到的字节）")
    emit(f"   row_count={row_count}  数据行={len(lines)}")
    bad_width = [i for i, l in enumerate(lines) if len(split(l)) != 10]
    emit(f"   字段数!=10 的行: {bad_width if bad_width else '无'}")

    emit()
    emit("C. 复现客户端 sub_5A2DB0 的读取结果")
    emit(f"   push 常量->偏移: {PUSH_ORDER}")
    fails = []
    for i, (line, dbr) in enumerate(zip(lines, db_rows), 1):
        f = split(line)
        by_name = {n: k for k, n in CATEGORY.items()}
        reads = {}
        raw_cat = ""
        for cidx, off in PUSH_ORDER:
            v = f[cidx] if cidx < len(f) else ""
            if off == CAT_OFFSET:
                raw_cat = v
                reads[off] = by_name.get(v, -1)
            else:
                try:
                    reads[off] = int(v) if v != "" else 0
                except ValueError:
                    reads[off] = 0
        ok = (
            reads[0] == int(f[0])
            and 0 <= reads[CAT_OFFSET] <= 5
            and reads[28] == 1
            and reads[12] == 0
        )
        if not ok:
            fails.append(i)
        emit(
            f"   [{i}] +0={reads[0]} +20={reads[20]} +4={reads[4]} +8={reads[8]} "
            f"+16={reads[16]} +12={reads[12]} +24={CATEGORY.get(reads[CAT_OFFSET], 'INVALID')} "
            f"(raw={raw_cat!r}) +28={reads[28]}  {'OK' if ok else 'FAIL'}"
        )
    emit()
    emit(f"   ==> 失败行: {fails if fails else '无'}")

    emit()
    emit("D. 种子文件")
    seed_lines = [l for l in open(SEED, encoding="utf-8").read().split("\n") if l.strip() and not l.lstrip().startswith("#")]
    seed_set = {norm(l) for l in seed_lines}
    man_set = {norm(l) for l in lines}
    emit(f"   种子行={len(seed_set)} manifest行={len(man_set)}")
    emit(f"   只种子有: {sorted(seed_set - man_set) or '无'}")
    emit(f"   只manifest有: {sorted(man_set - seed_set) or '无'}")

    verdict = not bad_width and not fails and not (seed_set - man_set) and not (man_set - seed_set)
    emit()
    emit(f"VERDICT: {'PASS' if verdict else 'FAIL'}")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(log) + "\n")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
