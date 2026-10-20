# -*- coding: utf-8 -*-
"""打印某表 schema 的 csv_index / 列名 / 类型 / 内存偏移 / 状态。"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")


def dump(table):
    d = json.load(open(os.path.join(SCHEMA, table + ".json"), encoding="utf-8"))
    print("== %s  reader=%s cols=%d gap=%s" % (table, d.get("asm_reader"), len(d["columns"]), d.get("column_gap")))
    for c in d["columns"]:
        off = c.get("memory_offset")
        print("%4s %-28s %-6s %6s %-10s %s" % (
            c["csv_index"], c["db_column"], c.get("type"), off if off is not None else "-",
            c.get("status"), (c.get("meaning") or "")[:56]))


if __name__ == "__main__":
    for t in sys.argv[1:]:
        dump(t)
