"""列出给定复合体声明的 memory_offset / length 与 IDA 槽表的对照。"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
META = ROOT / "schema" / "_meta"

ida = {}
for p in sorted(META.glob("ida_memory_slots_batch*.json")):
    ida.update(json.loads(p.read_text(encoding="utf-8")))

for cid in sys.argv[1:]:
    comp = json.loads((COMP / f"{cid}.json").read_text(encoding="utf-8"))
    ent = ida.get(cid, {})
    print(f"=== {cid}  reader={comp.get('reader')}  claim={comp.get('memory_claim')} "
          f"wire={comp.get('length')}")
    print(f"    fn={ent.get('function')} slots={ent.get('slots')}")
    for m in comp.get("members", []):
        mo = m.get("memory_offset")
        if mo is None and not m.get("memory_only"):
            continue
        print(f"      {m['name']:24s} mem={str(mo):>6} len={str(m.get('length')):>4} "
              f"wire={str(m.get('offset')):>5} {m.get('type', '')}")
