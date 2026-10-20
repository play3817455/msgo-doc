# -*- coding: utf-8 -*-
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
for n in sys.argv[1:]:
    d = json.load(open(rf"f:\9ymsgo\9you\db_design\schema\cfg\tables\{n}.json", encoding="utf-8"))
    print(f"== {n} src={d.get('source_md')} csv={d.get('csv_path')} disp={d.get('disposition')} count={d.get('column_count')} defined={d.get('column_defined')} gap={d.get('column_gap')}")
    for c in d["columns"]:
        print("   ", c.get("csv_index"), c.get("db_column"), c.get("type"), c.get("status"),
              c.get("memory_offset"), c.get("asm_va"), (c.get("meaning") or "")[:60])
