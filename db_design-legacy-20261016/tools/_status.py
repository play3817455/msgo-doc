import json
from pathlib import Path

idx = json.loads(Path("db_design/schema/cfg/index.json").read_text(encoding="utf-8"))
partial = [t for t in idx["tables"] if t.get("asm_status") != "complete"]
complete = [t for t in idx["tables"] if t.get("asm_status") == "complete"]
print(f"COMPLETE {len(complete)}")
for t in complete:
    print(f"  {t['id']}")
print(f"PARTIAL {len(partial)}")
for t in sorted(partial, key=lambda x: -x.get("column_pending", 0)):
    print(
        f"  {t['id']:32} pending={t.get('column_pending', 0):4} "
        f"confirmed={t.get('column_confirmed', 0):4} reader={t.get('reader_func', '')}"
    )
