import json
from pathlib import Path

S = Path(__file__).resolve().parents[1] / "schema" / "composites"
batch = ["lpcard", "ms", "snapshot", "funnelss", "unlockw", "adop_list", "recruits", "leaders", "bracket", "AI"]
for e in batch:
    c = json.loads((S / f"{e}.json").read_text(encoding="utf-8"))
    miss = [m["name"] for m in c.get("members", []) if not any(ws.get("evidence_va") for ws in m.get("wire_sources", []))]
    print(f"{e:12} len={c.get('length')} r={c.get('reader','')} members={len(c.get('members',[]))} no_va={len(miss)}")
