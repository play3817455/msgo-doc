import json
from pathlib import Path

S = Path(__file__).resolve().parents[1] / "schema"
vas = json.loads((S / "_meta" / "ida_wire_vas_batch2.json").read_text(encoding="utf-8"))
for ent in ["lpcard", "ms", "AI", "recruits", "snapshot"]:
    comp = json.loads((S / "composites" / f"{ent}.json").read_text(encoding="utf-8"))
    segs = vas[ent]["segments"]
    print(f"\n=== {ent} segs={len(segs)} members={len(comp['members'])} total={vas[ent]['total']} len={comp['length']}")
    for m, s in zip(comp["members"], segs):
        ok = m["offset"] == s["offset"] and m["length"] == s["size"]
        mark = "OK" if ok else "MISMATCH"
        print(f"  {m['name']:25} mem {m['offset']:3}+{m['length']:3} seg {s['offset']:3}+{s['size']:3} {mark} {s['va']}")
