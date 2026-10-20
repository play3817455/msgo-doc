# -*- coding: utf-8 -*-
"""目标 5 表补列后的取值盘点 + 客户端读取等价性论证（按 manifest 字节逐列模拟 sub_BBB370）。

模拟口径（与客户端一致）：
  * 一条数据行的字段数 = 逗号数 + 1（客户端 sub_456D90 按列号取；越界 ⇒ 空串）
  * 空串经 atoi/atof ⇒ 0
  * 所以「补空列」与「不补列」在每个列号上的取值**完全相同**（都是 0）
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
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TABLES = ["PLAY_BONUS_REWARD", "PLAYER_NAVI", "BUFF", "MODULE_DEVELOP", "MISSION_EXTRULE"]

log = []


def emit(s=""):
    print(s)
    log.append(s)


def fields(line):
    s = line.rstrip("\r\n")
    out, cur, q = [], "", False
    for ch in s:
        if ch == '"':
            q = not q
        elif ch == "," and not q:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        cols = sorted(spec["columns"], key=lambda c: c["csv_index"])
        width = max(c["csv_index"] for c in cols) + 1
        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        raw = cur.fetchone()[0].decode("utf-8")
        data = [l for l in raw.split("\r\n") if l.strip() and not l.lstrip().startswith("#")]
        widths = {len(fields(l)) for l in data}
        emit(f"### {t}：CSV 宽 {width} 列 | 行 {len(data)}｜每行实际字段数集合 {sorted(widths)}")
        # 每列的「非空值个数」
        nonempty = [0] * width
        for l in data:
            f = fields(l)
            for i in range(min(width, len(f))):
                if f[i].strip() != "":
                    nonempty[i] += 1
        for c in cols:
            i = c["csv_index"]
            tag = "gap" if c.get("status") == "gap" else "读"
            emit(f"    csv{i:2d} {c['db_column']:22s} [{tag}] 非空 {nonempty[i]:3d}/{len(data)}"
                 f"  off={c.get('memory_offset')}")
        emit()

open(os.path.join(HERE, "_out_widen_verify.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
