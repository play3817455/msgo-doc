import json
import glob

for f in sorted(glob.glob("*.json")):
    if f.startswith("_"):
        continue
    d = json.load(open(f, encoding="utf-8"))
    for m in d.get("members", []):
        if m["name"] in ("pilot_id", "npc_id") and m.get("role") == "ref":
            print(d["id"], m["name"], m["wire_type"], "->", m.get("fk_target"))
