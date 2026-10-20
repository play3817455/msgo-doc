# -*- coding: utf-8 -*-
"""核对 db_design schema 里 WEAPON_SETTING 的 col23..col32 元数据。只读。"""
import io
import json

P = "db_design/schema/cfg/tables/WEAPON_SETTING.json"
d = json.load(io.open(P, encoding="utf-8"))
print("top keys:", list(d.keys()))
cols = d.get("columns") or d.get("cols") or []
print("列数:", len(cols))
print("样例:", json.dumps(cols[0], ensure_ascii=False))
want = {23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
for c in cols:
    try:
        idx = int(c.get("csv_index"))
    except (TypeError, ValueError):
        continue
    if idx in want:
        print(
            "  col%-3s %-24s type=%-6s mem_off=%-6s enum=%s"
            % (idx, c.get("name"), c.get("type"), c.get("memory_offset"), c.get("enum"))
        )
        m = (c.get("meaning") or "").replace("\n", " ")
        print("        meaning:", m[:200])
