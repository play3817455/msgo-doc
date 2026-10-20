import json

s = json.load(open(r"serverv/static/cfg_schema.json", encoding="utf-8"))
print("JSON OK, tables:", len(s))
n = s["WEAPON_SETTING"]
for c in [74, 77, 79, 81, 87, 89, 91, 93, 95, 98, 100]:
    e = [v for v in n["columns"].values() if v.get("csv_index") == c][0]
    print(f"col{c:>4}  {e['name']:<20} {e['display_name']}")
