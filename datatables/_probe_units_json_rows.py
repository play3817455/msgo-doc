# -*- coding: utf-8 -*-
"""把 units.json 里这 2 个 icon_id 的行**完整**打出来（键全列），与一个正常武器对照。只读。"""
import io
import json

P = r"F:\9ymsgo\9you\gow_wiki\data\units.json"
d = json.load(io.open(P, encoding="utf-8"))
T = {"10840101", "10840501", "05840101"}

found = {}
for u in d:
    if u.get("page", "").find("エクシア") < 0:
        continue
    for w in u.get("weapons", []):
        for r in w.get("rows", []):
            if r.get("icon_id") in T:
                found.setdefault(r["icon_id"], []).append((u["page"], r))

for k in sorted(found):
    for page, r in found[k]:
        print("=" * 70)
        print("icon_id=%s  page=%s" % (k, page))
        for kk, vv in r.items():
            print("    %-16s %r" % (kk, vv))
